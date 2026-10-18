"""Independent data checks for the fixed R12 Terra Firma observation pair."""
import argparse
import json
import math
from pathlib import Path
import re

from run import NU_SHA, SCENE_SHA, manifest, read, save, sha

TRANSFORMS = {'Position', 'PositionLocal', 'Rotation', 'RotationLocal', 'Scale', 'ScaleLocal'}
SELECTED = TRANSFORMS | {'Size', 'Offset', 'MountOpt', 'Static', 'Clipped', 'BodyShape', 'StaticModel', 'MaterialProperties'}
HISTORY = 'PropagatedDescriptorOpt'
LINK = 'PropagationSourceOpt'
FAMILY_ROOTS = {'Game/Gameplay/Scene/' + name for name in ('Villa', 'Villa-0002', 'Villa-0003', 'Villa-0004')}


def symbol(text):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|\[|\]|[^\s\[\]"]+', text)
    position = 0

    def parse():
        nonlocal position
        if position >= len(tokens):
            raise ValueError('Unexpected end of symbol.')
        token = tokens[position]
        position += 1
        if token == '[':
            values = []
            while position < len(tokens) and tokens[position] != ']':
                values.append(parse())
            if position >= len(tokens):
                raise ValueError('Unclosed symbol list.')
            position += 1
            return values
        if token == ']':
            raise ValueError('Unexpected closing bracket.')
        return json.loads(token) if token.startswith('"') else token

    result = parse()
    if position != len(tokens):
        raise ValueError('Trailing symbol input.')
    return result


def equivalent(left, right, numeric=False):
    a, b = symbol(left), symbol(right)
    if not numeric:
        return a == b

    def close(x, y):
        if isinstance(x, list) or isinstance(y, list):
            return (isinstance(x, list) and isinstance(y, list) and len(x) == len(y)
                    and all(close(u, v) for u, v in zip(x, y)))
        try:
            u, v = float(x), float(y)
        except (TypeError, ValueError):
            return False
        return math.isfinite(u) and math.isfinite(v) and abs(u - v) <= 0.0001

    return close(a, b)


def property_map(node):
    rows = node['Properties']
    result = {p['Name']: p for p in rows}
    if len(result) != len(rows):
        raise ValueError('Duplicate property observation.')
    return result


def history_value(text):
    value = symbol(text)
    if value == 'None':
        return value
    if not isinstance(value, list) or len(value) != 2 or value[0] != 'Some':
        raise ValueError('Malformed saved-history option.')

    def descriptor(row):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError('Malformed history descriptor.')
        properties = dict(row[1])
        if len(properties) != len(row[1]):
            raise ValueError('Duplicate history property.')
        return {'dispatcher': row[0], 'properties': properties,
                'children': [descriptor(child) for child in row[2]]}

    return descriptor(value[1])


def saved_nodes(path):
    group = symbol(path.read_text(encoding='utf-8'))
    if not isinstance(group, list) or len(group) != 3 or group[0] != 'GroupDispatcher':
        raise ValueError('Wrong saved group descriptor.')
    result = {}

    def walk(parent, descriptors):
        for descriptor in descriptors:
            if len(descriptor) != 3:
                raise ValueError('Wrong saved entity descriptor.')
            props = dict(descriptor[1])
            address = parent + '/' + props['Name']
            if address in result:
                raise ValueError('Duplicate saved address.')
            result[address] = {'dispatcher': descriptor[0], 'properties': props}
            walk(address, descriptor[2])

    walk('Game/Gameplay/Scene', group[2])
    return result


def evaluate(l0, l1=None):
    findings = []
    descriptive = []
    observations = {}
    originals = None

    def flag(kind, phase, name, expected=None, actual=None):
        findings.append({'kind': kind, 'phase': phase, 'name': name, 'expected': expected, 'actual': actual})

    def prop_value(row, name, phase, address, required=False):
        prop = property_map(row).get(name)
        if prop is None or prop.get('Error'):
            flag('invalid', phase, address + ':' + name + ':observation', 'record without conversion error', prop)
            return None
        if not prop['Found']:
            if required:
                flag('adverse', phase, address + ':' + name + ':missing_property', 'present', False)
            return None
        return prop['Value']

    for arm, path in [('L0', l0), ('L1', l1)]:
        if path is None:
            continue
        receipt = read(path / 'receipt.json')
        obs = path / 'observations'
        if not receipt.get('complete_observation_and_save'):
            flag('invalid', arm, 'complete_native_observations', True, receipt.get('complete_observation_and_save'))
            continue
        process = read(path / 'process.json')
        summary = read(obs / 'summary.json')
        authority = path / 'authorities'
        native_acceptance = read(authority / 'native-acceptance.json')
        if (receipt['process'] != process or process['exit_code'] != 0 or process['timed_out']
                or not receipt['protected_application_files_unchanged'] or not receipt['runtime_selection_recorded']
                or receipt['summary'] != summary or not summary['Complete'] or summary['EngineExitCode'] != 0
                or summary['CaptureCount'] != 2 or not summary['ServerGC']):
            flag('invalid', arm, 'underlying_process_and_summary', 'successful complete native observation', receipt)
        if (receipt['build_receipt_sha256'] != sha(authority / 'receipt.json')
                or receipt['native_acceptance_sha256'] != sha(authority / 'native-acceptance.json')
                or native_acceptance['build_receipt_sha256'] != receipt['build_receipt_sha256']
                or native_acceptance['decision'] != 'accepted_for_native_execution'
                or native_acceptance['protocol_sha256'] != sha(path / 'package-inputs/PROTOCOL.md')):
            flag('invalid', arm, 'accepted_build_and_protocol_binding')
        if (sha(path / 'observations-manifest.json') != receipt['observations_manifest_sha256']
                or manifest(obs) != read(path / 'observations-manifest.json')):
            flag('invalid', arm, 'sealed_observation_inputs')
        if arm == 'L1' and receipt['build_receipt_sha256'] != read(l0 / 'receipt.json')['build_receipt_sha256']:
            flag('invalid', arm, 'same_compiled_build_as_L0')
        startup = read(obs / 'startup.json')
        if not startup['ServerGC']:
            flag('invalid', arm, 'effective_server_GC', True, startup['ServerGC'])
        expected_input = SCENE_SHA if arm == 'L0' else sha(l0 / 'observations/saved-Scene.nugroup')
        if receipt['arm'] != arm or startup['Arm'] != arm or startup['InputSceneSha256'] != expected_input:
            flag('invalid', arm, 'assigned_arm_and_input', [arm, expected_input], [receipt['arm'], startup])
        if arm == 'L1':
            predecessor = receipt.get('predecessor') or {}
            if predecessor.get('sha256') != sha(l0 / 'receipt.json'):
                flag('invalid', arm, 'actual_L0_predecessor', sha(l0 / 'receipt.json'), predecessor)
        rows = read(obs / 'original-expectations.json')
        this_original = {row['Address']: row for row in rows}
        if len(rows) != 197 or len(this_original) != 197 or startup['OriginalSceneSha256'] != SCENE_SHA:
            flag('invalid', arm, 'fixed_original_correspondence', 197, len(this_original))
        if originals is None:
            originals = this_original
        elif this_original != originals:
            flag('invalid', arm, 'same_original_expectations', 'L0 original', 'different')
        original_props = {address: {p['Name']: p['Symbol'] for p in row['Properties']}
                          for address, row in this_original.items()}
        source_addresses = {address for address, props in original_props.items() if HISTORY in props}
        link_addresses = {address for address, props in original_props.items() if LINK in props}
        palms = {address for address, props in original_props.items()
                 if 'StaticModel' in props and symbol(props['StaticModel']) == ['Gameplay', 'PalmTree']}
        if (len(source_addresses), len(link_addresses), len(palms)) != (11, 166, 32):
            flag('invalid', arm, 'fixed_family_counts', [11, 166, 32], [len(source_addresses), len(link_addresses), len(palms)])
        selected = palms | FAMILY_ROOTS
        for label in ('A', 'B'):
            phase = arm + label
            data = read(obs / (label + '.json'))
            nodes = {row['Address']: row for row in data['Entities']}
            observations[phase] = nodes
            if len(nodes) != len(data['Entities']):
                flag('invalid', phase, 'unique_observed_addresses')
            mode = [data['Imperative'], data['Accompanied'], data['Advancing'], data['Halted'], data['GameState'], data['GameplaySelected']]
            if mode != [False, True, False, True, 'Gameplay', True]:
                flag('invalid', phase, 'mode_and_selection', [False, True, False, True, 'Gameplay', True], mode)
            if 'SDL_WINDOW_HIDDEN' not in data['WindowFlags']:
                flag('invalid', phase, 'observed_hidden_window', True, data['WindowFlags'])
            if not any(a['Name'] == 'Nu' and a['Sha256'] == NU_SHA for a in data['LoadedAssemblies']):
                flag('invalid', phase, 'loaded_Nu_identity', NU_SHA, data['LoadedAssemblies'])
            if not 1 <= data['Callback'] <= 120 or data['Label'] != label:
                flag('invalid', phase, 'bounded_observation_phase', label, data['Callback'])
            for address, expected in this_original.items():
                actual = nodes.get(address)
                if actual is None:
                    flag('adverse', phase, address + ':exists', True, False)
                    continue
                for field, value in [('Parent', address.rsplit('/', 1)[0]), ('Name', address.rsplit('/', 1)[1]), ('Dispatcher', expected['Dispatcher'])]:
                    if actual[field] != value:
                        flag('adverse', phase, address + ':' + field, value, actual[field])
                props = property_map(actual)
                for name, value in original_props[address].items():
                    prop = props.get(name)
                    if prop is None or not prop['ExpectedPresent'] or symbol(prop['ExpectedSymbol']) != symbol(value):
                        flag('invalid', phase, address + ':' + name + ':original_binding', value, prop)
                for name in (LINK, HISTORY):
                    observed = prop_value(actual, name, phase, address, required=True)
                    if name in original_props[address]:
                        expected_value = original_props[address][name]
                        matches = (history_value(expected_value) == history_value(observed) if name == HISTORY
                                   else equivalent(expected_value, observed)) if observed is not None else False
                        if observed is not None and not matches:
                            flag('adverse', phase, address + ':' + name, expected_value, observed)
                    elif observed is not None and symbol(observed) != 'None':
                        flag('adverse', phase, address + ':' + name + ':unexpected', 'None', observed)
                    if name == LINK and observed is not None:
                        parsed = symbol(observed)
                        if isinstance(parsed, list) and parsed[0] == 'Some' and parsed[1] not in nodes:
                            flag('adverse', phase, address + ':unresolved_source', parsed[1], None)
                if address in selected:
                    if sorted(actual['Children']) != sorted(expected['Children']):
                        flag('adverse', phase, address + ':child_names', expected['Children'], actual['Children'])
                    for name in SELECTED:
                        prop = props.get(name)
                        value = prop_value(actual, name, phase, address, required=name in original_props[address])
                        if arm == 'L0' and prop and prop['ExpectedPresent'] and value is not None:
                            expected_value = original_props[address][name]
                            if not equivalent(expected_value, value, name in TRANSFORMS):
                                flag('adverse', phase, address + ':' + name, expected_value, value)
                for name, prop in props.items():
                    if prop.get('Error'):
                        descriptive.append({'phase': phase, 'address': address, 'property': name, 'conversion_error': prop['Error']})
                    elif prop['ExpectedPresent'] and prop['Found'] and prop['ExpectedCanonical'] != prop['Value']:
                        descriptive.append({'phase': phase, 'address': address, 'property': name,
                                            'original_canonical': prop['ExpectedCanonical'], 'actual': prop['Value']})
        a, b = read(obs / 'A.json'), read(obs / 'B.json')
        if b['Callback'] != a['Callback'] + 1:
            flag('invalid', arm, 'B_immediately_follows_A', a['Callback'] + 1, b['Callback'])
        phase_paths = sorted(obs.glob('phase-*.json'))
        phases = [read(p) for p in phase_paths]
        wanted = list(range(1, b['Callback'] + 1))
        first_true = next((p['Callback'] for p in phases if p['SceneExists']), None)
        if ([p['Callback'] for p in phases] != wanted
                or [p.name for p in phase_paths] != [f'phase-{n:03d}.json' for n in wanted]
                or first_true != a['Callback'] or summary['CallbackCount'] != b['Callback']):
            flag('invalid', arm, 'A_first_scene_exists_and_contiguous_phases',
                 {'callbacks': wanted, 'A': a['Callback']}, {'callbacks': [p['Callback'] for p in phases], 'first_true': first_true})
        saved = saved_nodes(obs / 'saved-Scene.nugroup')
        if set(saved) != set(this_original):
            flag('adverse', arm, 'saved_named_tree', sorted(this_original), sorted(saved))
        if not receipt['summary']['SavedDescriptorMatchesB'] or symbol((obs / 'B.nugroup').read_text(encoding='utf-8')) != symbol((obs / 'saved-Scene.nugroup').read_text(encoding='utf-8')):
            flag('adverse', arm, 'saved_descriptor_matches_B', True, False)
        observations[arm + '_selected'] = selected
        descriptive.append({'phase': arm, 'generated_entities_A': [r for r in a['Entities'] if r['Address'] not in this_original],
                            'generated_entities_B': [r for r in b['Entities'] if r['Address'] not in this_original]})

    if originals is not None and 'L0B' in observations:
        baseline = observations['L0B']
        for phase in ('L0A', 'L1A', 'L1B'):
            if phase not in observations:
                continue
            for address in originals:
                old, new = baseline.get(address), observations[phase].get(address)
                if old is None or new is None:
                    continue  # The original-name check retains each absence above.
                changes = []
                for name in ('Persistent', 'Protection'):
                    if old[name] != new[name]:
                        (changes if phase == 'L0A' else findings).append(
                            {'kind': 'adverse', 'phase': phase, 'name': address + ':' + name, 'expected': old[name], 'actual': new[name]})
                names = {LINK, HISTORY}
                if address in observations['L0_selected']:
                    names |= SELECTED
                for name in names:
                    old_prop, new_prop = property_map(old).get(name), property_map(new).get(name)
                    if old_prop is None or new_prop is None or old_prop.get('Error') or new_prop.get('Error'):
                        continue  # Observation failure is already invalid above.
                    same = old_prop['Found'] == new_prop['Found']
                    if same and old_prop['Found']:
                        same = equivalent(old_prop['Value'], new_prop['Value'], name in TRANSFORMS)
                    if not same:
                        change = {'kind': 'adverse', 'phase': phase, 'name': address + ':' + name + ':versus_L0B',
                                  'expected': old_prop, 'actual': new_prop}
                        (changes if phase == 'L0A' else findings).append(change)
                if changes:
                    descriptive.extend(changes)
    counts = {kind: sum(f['kind'] == kind for f in findings) for kind in ('invalid', 'adverse')}
    disposition = 'invalid_or_incomplete' if counts['invalid'] else 'adverse' if counts['adverse'] else 'passed_declared_checks'
    return {'disposition': disposition, 'scope': 'pair' if l1 is not None else 'L0_only',
            'counts': counts, 'L1_assigned_observed': l1 is not None,
            'findings': findings, 'descriptive': descriptive}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--l0', type=Path, required=True)
    parser.add_argument('--l1', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('Retain each comparison output; destination already exists.')
    input_hashes = {}
    for arm, root in (('L0', args.l0), ('L1', args.l1)):
        if root is not None:
            input_hashes[arm] = {'receipt_sha256': sha(root / 'receipt.json'),
                                 'observations': manifest(root / 'observations')}
    package = Path(__file__).parent
    source_hashes = {name: sha(package / name) for name in ('compare.py', 'run.py', 'PROTOCOL.md')}
    try:
        result = evaluate(args.l0, args.l1)
    except Exception as error:
        result = {'disposition': 'invalid_or_incomplete', 'comparison_error': str(error), 'type': type(error).__name__}
    unchanged = all(sha(root / 'receipt.json') == input_hashes[arm]['receipt_sha256']
                    and manifest(root / 'observations') == input_hashes[arm]['observations']
                    for arm, root in (('L0', args.l0), ('L1', args.l1)) if root is not None)
    unchanged = unchanged and all(sha(package / name) == value for name, value in source_hashes.items())
    if not unchanged:
        result['disposition'] = 'invalid_or_incomplete'
        result['concurrent_input_change'] = True
    result['inputs'] = {'L0': str(args.l0), 'L1': str(args.l1) if args.l1 else None,
                        'source_hashes': source_hashes, 'run_hashes': input_hashes, 'unchanged_during_comparison': unchanged}
    save(args.output, result)
    print(json.dumps({k: v for k, v in result.items() if k not in ('findings', 'descriptive')}, indent=2))
    return 2 if result['disposition'] == 'invalid_or_incomplete' else 0


if __name__ == '__main__':
    raise SystemExit(main())
