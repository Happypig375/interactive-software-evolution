"""Synthetic checker fault controls; never launch Nu or claim runtime evidence."""
import argparse
import copy
import json
from pathlib import Path
import shutil

from compare import SELECTED, TRANSFORMS, HISTORY, LINK, evaluate, symbol
from run import NU_SHA, SCENE_SHA, manifest, read, save, sha


def render(value):
    if isinstance(value, list):
        return '[' + ' '.join(render(x) for x in value) + ']'
    return json.dumps(value) if not value or any(c.isspace() or c in '[]"' for c in value) else value


def fixture(scene, output):
    group = symbol(scene.read_text(encoding='utf-8'))
    originals, nodes = [], []

    def walk(parent, descriptors):
        for descriptor in descriptors:
            props = dict(descriptor[1])
            address = parent + '/' + props['Name']
            children = [dict(child[1])['Name'] for child in descriptor[2]]
            originals.append({'Address': address, 'Dispatcher': descriptor[0], 'Children': children,
                              'Properties': [{'Name': name, 'Symbol': render(value)} for name, value in props.items()]})
            observations = []
            for name in sorted(set(props) | SELECTED | {LINK, HISTORY}):
                default = ('[0 0 0 1]' if name.startswith('Rotation') else
                           '[1 1 1]' if name.startswith('Scale') or name == 'Size' else '[0 0 0]') if name in TRANSFORMS else (
                               'None' if name in (LINK, HISTORY) else 'synthetic-default')
                value = render(props[name]) if name in props else default
                observations.append({'Name': name, 'Found': True, 'TypeName': 'synthetic', 'Value': value,
                                     'ExpectedPresent': name in props, 'ExpectedSymbol': render(props[name]) if name in props else '',
                                     'ExpectedCanonical': render(props[name]) if name in props else '', 'Error': ''})
            nodes.append({'Address': address, 'Parent': parent, 'Name': props['Name'], 'Dispatcher': descriptor[0],
                          'Id': 'synthetic', 'Persistent': True, 'Protection': 'Unprotected', 'Children': children,
                          'Original': True, 'Properties': observations})
            walk(address, descriptor[2])

    walk('Game/Gameplay/Scene', group[2])
    for arm in ('L0', 'L1'):
        root = output / arm
        obs = root / 'observations'
        obs.mkdir(parents=True)
        authority = root / 'authorities'
        authority.mkdir()
        (root / 'package-inputs').mkdir()
        shutil.copy2(Path(__file__).parent / 'PROTOCOL.md', root / 'package-inputs/PROTOCOL.md')
        save(authority / 'receipt.json', {'Synthetic': True, 'stage': 'synthetic_build'})
        save(authority / 'source-binary-seal.json', {'Synthetic': True})
        save(authority / 'native-acceptance.json', {'Synthetic': True, 'decision': 'accepted_for_native_execution',
             'build_receipt_sha256': sha(authority / 'receipt.json'),
             'source_binary_seal_sha256': sha(authority / 'source-binary-seal.json'),
             'protocol_sha256': sha(root / 'package-inputs/PROTOCOL.md')})
        for name in ('B.nugroup', 'saved-Scene.nugroup', 'saved-canonical.nugroup'):
            shutil.copy2(scene, obs / name)
        save(obs / 'original-expectations.json', originals)
        save(obs / 'startup.json', {'Arm': arm, 'OriginalSceneSha256': SCENE_SHA, 'InputSceneSha256': SCENE_SHA,
                                   'Synthetic': True, 'ServerGC': True})
        for i, label in enumerate(('A', 'B'), start=2):
            save(obs / (label + '.json'), {'Label': label, 'Callback': i, 'Imperative': False, 'Accompanied': True,
                                         'Advancing': False, 'Halted': True, 'GameState': 'Gameplay', 'GameplaySelected': True,
                                         'WindowFlags': 'SDL_WINDOW_HIDDEN', 'LoadedAssemblies': [{'Name': 'Nu', 'Sha256': NU_SHA}],
                                         'Entities': nodes, 'Synthetic': True})
        for callback in range(1, 4):
            save(obs / f'phase-{callback:03d}.json', {'Callback': callback, 'SceneExists': callback >= 2, 'Synthetic': True})
        summary = {'Complete': True, 'EngineExitCode': 0, 'CaptureCount': 2, 'CallbackCount': 3,
                   'ServerGC': True, 'SavedDescriptorMatchesB': True, 'Synthetic': True}
        save(obs / 'summary.json', summary)
        process = {'exit_code': 0, 'timed_out': False, 'Synthetic': True}
        save(root / 'process.json', process)
        save(root / 'observations-manifest.json', manifest(obs))
        save(root / 'receipt.json', {'arm': arm, 'complete_observation_and_save': True, 'Synthetic': True,
                                    'predecessor': {'sha256': sha(output / 'L0/receipt.json')} if arm == 'L1' else None,
                                    'summary': summary, 'process': process,
                                    'protected_application_files_unchanged': True, 'runtime_selection_recorded': True,
                                    'build_receipt_sha256': sha(authority / 'receipt.json'),
                                    'native_acceptance_sha256': sha(authority / 'native-acceptance.json'),
                                    'observations_manifest_sha256': sha(root / 'observations-manifest.json')})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if sha(args.scene) != SCENE_SHA:
        raise ValueError('Controls require the fixed original scene.')
    args.output.mkdir(parents=True, exist_ok=False)
    package = Path(__file__).parent
    inputs = args.output / 'inputs'
    inputs.mkdir()
    for name in ('compare.py', 'check_controls.py', 'run.py'):
        shutil.copy2(package / name, inputs / name)
    template = args.output / 'synthetic-template'
    fixture(args.scene, template)
    palm = 'Game/Gameplay/Scene/Villa/Palm'
    cases = [
        ('unchanged_pair', 'passed_declared_checks'),
        ('missing_original_entity', 'adverse'),
        ('changed_source_history', 'adverse'),
        ('wrong_world_mode', 'invalid_or_incomplete'),
        ('missing_selected_observation', 'invalid_or_incomplete'),
        ('wrong_predecessor', 'invalid_or_incomplete'),
        ('delayed_B', 'invalid_or_incomplete'),
        ('save_content_mismatch', 'adverse'),
        ('transform_outside_tolerance', 'adverse'),
        ('transform_within_tolerance', 'passed_declared_checks'),
        ('nonfinite_transform', 'adverse'),
        ('small_size_change', 'adverse'),
        ('small_offset_change', 'adverse'),
        ('earlier_scene_exists', 'invalid_or_incomplete'),
        ('nonzero_process_marked_complete', 'invalid_or_incomplete'),
        ('wrong_effective_GC', 'invalid_or_incomplete'),
        ('postseal_observation_change', 'invalid_or_incomplete')]
    results = []
    for name, expected in cases:
        case = args.output / name
        shutil.copytree(template, case)
        # Rebind each synthetic predecessor after copying, preserving actual bytes.
        receipt = read(case / 'L1/receipt.json')
        receipt['predecessor']['sha256'] = sha(case / 'L0/receipt.json')
        save(case / 'L1/receipt.json', receipt)
        path = case / 'L1/observations/A.json'
        observation = read(path)
        node = next(n for n in observation['Entities'] if n['Address'] == palm)
        if name == 'missing_original_entity':
            observation['Entities'] = [n for n in observation['Entities'] if n['Address'] != palm]
        elif name == 'changed_source_history':
            prop = next(p for p in node['Properties'] if p['Name'] == HISTORY)
            value = symbol(prop['Value'])
            next(p for p in value[1][1] if p[0] == 'Name')[1] = 'ChangedSavedName'
            prop['Value'] = render(value)
        elif name == 'wrong_world_mode':
            observation['Imperative'] = True
        elif name == 'missing_selected_observation':
            node['Properties'] = [p for p in node['Properties'] if p['Name'] != 'Position']
        elif name == 'wrong_predecessor':
            receipt['predecessor']['sha256'] = '0' * 64
            save(case / 'L1/receipt.json', receipt)
        elif name == 'delayed_B':
            bpath = case / 'L1/observations/B.json'
            b = read(bpath)
            b['Callback'] += 1
            save(bpath, b)
        elif name == 'earlier_scene_exists':
            ppath = case / 'L1/observations/phase-001.json'
            phase = read(ppath)
            phase['SceneExists'] = True
            save(ppath, phase)
        elif name == 'nonzero_process_marked_complete':
            process = read(case / 'L1/process.json')
            process['exit_code'] = 2
            receipt['process'] = process
            save(case / 'L1/process.json', process)
        elif name == 'wrong_effective_GC':
            startup = read(case / 'L1/observations/startup.json')
            startup['ServerGC'] = False
            save(case / 'L1/observations/startup.json', startup)
        elif name == 'save_content_mismatch':
            saved = case / 'L1/observations/saved-Scene.nugroup'
            saved.chmod(saved.stat().st_mode | 0o200)
            saved.write_text(saved.read_text(encoding='utf-8').replace('True', 'False', 1), encoding='utf-8')
        elif name in ('transform_outside_tolerance', 'transform_within_tolerance', 'nonfinite_transform'):
            prop = next(p for p in node['Properties'] if p['Name'] == 'Position')
            value = symbol(prop['Value'])
            value[0] = 'NaN' if name == 'nonfinite_transform' else str(float(value[0]) + (0.00005 if name == 'transform_within_tolerance' else 0.0002))
            prop['Value'] = render(value)
        elif name in ('small_size_change', 'small_offset_change'):
            prop = next(p for p in node['Properties'] if p['Name'] == ('Size' if name == 'small_size_change' else 'Offset'))
            value = symbol(prop['Value'])
            value[0] = str(float(value[0]) + 0.00005)
            prop['Value'] = render(value)
        save(path, observation)
        save(case / 'L1/observations-manifest.json', manifest(case / 'L1/observations'))
        receipt['observations_manifest_sha256'] = sha(case / 'L1/observations-manifest.json')
        save(case / 'L1/receipt.json', receipt)
        if name == 'postseal_observation_change':
            observation['SyntheticExtraAfterSeal'] = True
            save(path, observation)
        result = evaluate(case / 'L0', case / 'L1')
        save(case / 'result.json', result)
        results.append({'case': name, 'expected': expected, 'actual': result['disposition'],
                        'counts': result['counts'], 'passed': expected == result['disposition']})
    receipt = {'synthetic_only': True, 'source_scene_sha256': SCENE_SHA, 'controls': results,
               'passed': all(row['passed'] for row in results)}
    save(args.output / 'receipt.json', receipt)
    print(json.dumps(receipt, indent=2))
    return 0 if receipt['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
