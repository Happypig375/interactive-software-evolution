"""Reproduce only the prospective R12 unchanged Terra Firma load/save pair."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tarfile
import time

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]
ARCHIVE_SHA = 'eb0aa77197de1971d79aa0657c2af5cf33b99ba8302a24ba44f3306cca4bf92b'
SCENE_SHA = '1dff90c5679233f6b282e03bcb2f2fd7524a6e6e93a7df814a72f5260d3a421a'
NU_SHA = 'e96cd61d188c689f7e39e2670b4d8582e26b9ea2dc95e1a15056891b7c99cd68'
PIPE_SHA = '9b1ec304f9c0df4ad04391ee42d81f2f38082a390b318fd6a2052a08dd01c27d'
PIPE_NU_SHA = '5bcf797de1ae15dc79f9a0f49b30d96247816f928b158a519f64cb563f8b8e3c'
SOURCES = tuple(name + '.fs' for name in ('Assets', 'Constants', 'Simulants', 'Events',
                                        'Character', 'Gameplay', 'TerraFirma', 'TerraFirmaPlugin'))
SCENE = 'Assets/Gameplay/Scene.nugroup'
GRAPH_SHA = '71fa5ba5790149ba5aceb4268fbc69079e65bb070509ddd2e9b3c80e6d866c05'
OVERLAYER_SHA = '1b7a6afb58ce9d1ab0dd41e566d637dbc98647399002c198af5943c6f362a794'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def manifest(root):
    return {p.relative_to(root).as_posix(): {'bytes': p.stat().st_size, 'sha256': sha(p)}
            for p in sorted(root.rglob('*')) if p.is_file()}


def attributes(root):
    return {p.relative_to(root).as_posix(): {'mode': p.stat().st_mode,
            'windows_attributes': getattr(p.stat(), 'st_file_attributes', None)}
            for p in sorted(root.rglob('*')) if p.is_file()}


def asset_closure(source):
    """Only the hash-bound Terra Firma graph: two refinements and seven glob groups."""
    require(sha(source / 'AssetGraph.nuag') == GRAPH_SHA, 'The closure oracle requires the fixed graph.')
    compressed = set('jpg jpeg tga tif tiff dds ktx'.split())
    allowed = compressed | set('bmp png psd ttf skel json cbm fbx gltf glb dae obj mtl raw wav ogg mp3 cur nueffect nuscript csv nuentity nugroup tsx tmx atlas nav nbrd glsl bin'.split())
    outputs, excluded = {}, []
    for path in sorted((source / 'Assets').rglob('*')):
        if not path.is_file():
            continue
        relative = path.relative_to(source)
        extension = path.suffix.lower().lstrip('.')
        if extension not in allowed:
            excluded.append(relative.as_posix())
            continue
        target = relative.with_suffix('.dds') if extension in compressed else relative.with_suffix('.png') if extension == 'psd' else relative
        require(target.as_posix() not in outputs, 'Ambiguous asset output collision: ' + target.as_posix())
        outputs[target.as_posix()] = {'source': relative.as_posix(), 'source_sha256': sha(path),
                                      'transformed': extension in compressed or extension == 'psd',
                                      'expected_container': 'dds' if extension in compressed else 'png' if extension == 'psd' else None}
    return {'expected': outputs, 'excluded_input_files': excluded}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def snapshot(output):
    inputs = output / 'package-inputs'
    inputs.mkdir()
    for source in PACKAGE.iterdir():
        if source.is_file():
            shutil.copy2(source, inputs / source.name)
    save(output / 'package-inputs.json', manifest(inputs))


def process(command, cwd, output, deadline, environment=None):
    receipt = {'command': [str(a) for a in command], 'cwd': str(cwd),
               'deadline_seconds': deadline, 'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    save(output / 'command.json', receipt)
    start = time.monotonic()
    with (output / 'stdout.log').open('wb') as stdout, (output / 'stderr.log').open('wb') as stderr:
        try:
            child = subprocess.Popen(command, cwd=cwd, stdout=stdout, stderr=stderr, env=environment,
                                     creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            receipt['pid'] = child.pid
            save(output / 'command.json', receipt)
            try:
                receipt.update(exit_code=child.wait(timeout=deadline), timed_out=False)
            except subprocess.TimeoutExpired:
                receipt['timed_out'] = True
                if os.name == 'nt':
                    killed = subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'],
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            creationflags=subprocess.CREATE_NO_WINDOW, timeout=30)
                    (output / 'deadline-termination.log').write_bytes(killed.stdout)
                else:
                    child.kill()
                receipt['exit_code'] = child.wait(timeout=30)
        except OSError as error:
            receipt.update(exit_code=None, timed_out=False, launch_error=str(error))
    receipt['elapsed_seconds'] = time.monotonic() - start
    receipt['stdout_sha256'] = sha(output / 'stdout.log')
    receipt['stderr_sha256'] = sha(output / 'stderr.log')
    save(output / 'process.json', receipt)
    return receipt


def assets(args, output):
    archive_path = args.archive.resolve(strict=True)
    pipeline = args.pipeline.resolve(strict=True)
    require(sha(archive_path) == ARCHIVE_SHA, 'Wrong source archive.')
    require(sha(pipeline / 'Nu.Pipe.dll') == PIPE_SHA and sha(pipeline / 'Nu.dll') == PIPE_NU_SHA,
            'Wrong pipeline host.')
    authorities = {
        'terra-firma-pipeline-host-manifest.json': 'fd945db483fe9e8e713f9fc5a515753ea17af52ddb88ee87c23eef460ba62be5',
        'terra-firma-pipeline-pdb-verification.json': '074588749db8048e4afa32bef64b1fe00b6ff8294768ee3823471ed52b52113f'}
    authority_dir = output / 'authorities'
    authority_dir.mkdir()
    for name, expected_sha in authorities.items():
        authority = ROOT / '.artifacts/r12-propagation-20261018' / name
        require(sha(authority) == expected_sha, 'Changed provenance authority: ' + name)
        shutil.copy2(authority, authority_dir / name)
    proof = read(authority_dir / 'terra-firma-pipeline-pdb-verification.json')
    require(len(proof) == 2 and all(p['pe_pdb_identity_matches'] and not p['archive_mismatches'] for p in proof)
            and sum(p['archive_matching'] for p in proof) == 109
            and sum(p['generated_count'] for p in proof) == 4
            and [d for p in proof for d in p['checksumless_documents']] == ['Nu/Nu/unknown']
            and all(d['matches_current_generated'] for p in proof for d in p['documents'] if d.get('generated')),
            'Pipeline PDB proof does not satisfy its retained provenance limits.')
    before = manifest(pipeline)
    host_attrs = attributes(pipeline)
    expected_host = read(authority_dir / 'terra-firma-pipeline-host-manifest.json')
    require(before == {f['path']: {'bytes': f['bytes'], 'sha256': f['sha256']}
                       for f in expected_host['files']}, 'Pipeline dependency manifest changed.')
    save(output / 'pipeline-before.json', before)
    save(output / 'pipeline-attributes-before.json', host_attrs)
    shutil.copytree(pipeline, output / 'pipeline')
    copied_attrs = attributes(output / 'pipeline')
    save(output / 'copied-pipeline-attributes-before.json', copied_attrs)
    source = output / 'source'
    source.mkdir()
    prefix = 'Projects/Terra Firma/'
    with tarfile.open(archive_path) as archive:
        for member in archive.getmembers():
            if not member.isfile() or not member.name.startswith(prefix):
                continue
            relative = member.name[len(prefix):]
            if not (relative.startswith('Assets/') or relative in (*SOURCES, 'App.config', 'AssetGraph.nuag', 'Overlayer.nuol')):
                continue
            target = (source / relative).resolve()
            require(target.is_relative_to(source), 'Archive path escaped private source root.')
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.extractfile(member) as original, target.open('wb') as dest:
                shutil.copyfileobj(original, dest)
    require(len(manifest(source / 'Assets')) == 248, 'Unexpected original asset count.')
    require(sha(source / SCENE) == SCENE_SHA, 'Wrong original scene.')
    for name in (*SOURCES, 'App.config', 'AssetGraph.nuag', 'Overlayer.nuol'):
        require((source / name).is_file(), 'Missing original ' + name)
    source_before = manifest(source)
    save(output / 'source-manifest.json', source_before)
    source_attrs = attributes(source)
    save(output / 'source-attributes-before.json', source_attrs)
    require(sha(source / 'Overlayer.nuol') == OVERLAYER_SHA, 'Wrong original overlayer.')
    closure = asset_closure(source)
    save(output / 'expected-assets.json', closure)
    published = output / 'published'
    refinement = output / 'refinement'
    published.mkdir()
    refinement.mkdir()
    for name in ('AssetGraph.nuag', 'Overlayer.nuol'):
        shutil.copy2(source / name, published / name)
    dotnet = Path(shutil.which('dotnet')).resolve(strict=True)
    environment = os.environ.copy()
    environment['COREHOST_TRACE'] = '1'
    environment['COREHOST_TRACEFILE'] = str(output / 'runtime-host-trace.log')
    environment['DOTNET_HOST_TRACE'] = '1'
    environment['DOTNET_HOST_TRACEFILE'] = str(output / 'runtime-host-trace.log')
    save(output / 'runtime-launch.json', {'dotnet': str(dotnet), 'sha256': sha(dotnet),
         'runtimeconfig': read(output / 'pipeline/Nu.Pipe.runtimeconfig.json'),
         'note': 'Application framework selection is retained in host tracing, independent of SDK global.json.'})
    result = process([str(dotnet), str(output / 'pipeline/Nu.Pipe.dll'), str(source), str(published),
                      str(refinement), 'BcCompression', 'False'], source, output, 900, environment)
    published_manifest = manifest(published)
    save(output / 'published-manifest.json', published_manifest)
    save(output / 'refinement-manifest.json', manifest(refinement))
    published_attrs = attributes(published)
    save(output / 'published-attributes.json', published_attrs)
    save(output / 'source-attributes-after.json', attributes(source))
    save(output / 'pipeline-attributes-after.json', attributes(pipeline))
    save(output / 'copied-pipeline-attributes-after.json', attributes(output / 'pipeline'))
    failures = []
    for relative, entry in closure['expected'].items():
        path = published / relative
        if relative not in published_manifest:
            failures.append({'path': relative, 'failure': 'missing_output'})
            continue
        if not entry['transformed'] and sha(path) != entry['source_sha256']:
            failures.append({'path': relative, 'failure': 'copy_hash_mismatch'})
        if entry['transformed']:
            with path.open('rb') as stream:
                header = stream.read(8)
            if (entry['expected_container'] == 'dds' and header[:4] != b'DDS ') or (entry['expected_container'] == 'png' and header != b'\x89PNG\r\n\x1a\n'):
                failures.append({'path': relative, 'failure': 'wrong_transformed_container_header'})
        if not (published_attrs[relative]['windows_attributes'] or 0) & stat.FILE_ATTRIBUTE_READONLY:
            failures.append({'path': relative, 'failure': 'not_read_only'})
    for name, expected_sha in [('AssetGraph.nuag', GRAPH_SHA), ('Overlayer.nuol', OVERLAYER_SHA)]:
        if published_manifest.get(name, {}).get('sha256') != expected_sha:
            failures.append({'path': name, 'failure': 'copied_configuration_hash_mismatch'})
    closure_result = {'failures': failures, 'expected_count': len(closure['expected']),
                      'unexpected_outputs': sorted(set(published_manifest) - set(closure['expected']) - {'AssetGraph.nuag', 'Overlayer.nuol'}),
                      'limit': 'Presence, container signatures and exact untransformed bytes; not decoded texture/model appearance.'}
    save(output / 'asset-closure.json', closure_result)
    trace = output / 'runtime-host-trace.log'
    runtime_paths = []
    if trace.is_file():
        trace_text = trace.read_text(encoding='utf-8', errors='replace')
        runtime_paths = re.findall(r'CoreCLR path\s*=\s*[^\r\n]+', trace_text)
    save(output / 'runtime-selection.json', {'trace_sha256': sha(trace) if trace.exists() else None,
                                            'coreclr_path_lines': runtime_paths})
    source_unchanged = source_before == manifest(source) and source_attrs == attributes(source)
    host_unchanged = (before == manifest(pipeline) == manifest(output / 'pipeline')
                      and host_attrs == attributes(pipeline) and copied_attrs == attributes(output / 'pipeline'))
    ready = (result['exit_code'] == 0 and not result['timed_out'] and source_unchanged
             and host_unchanged and not failures and bool(runtime_paths)
             and published_manifest.get(SCENE, {}).get('sha256') == SCENE_SHA)
    receipt = {'stage': 'assets', 'archive': str(archive_path), 'archive_sha256': ARCHIVE_SHA,
               'source': str(source), 'published': str(published), 'process': result,
               'source_unchanged': source_unchanged, 'pipeline_host_unchanged': host_unchanged,
               'asset_closure': closure_result, 'runtime_selection_recorded': bool(runtime_paths),
               'published_manifest_sha256': sha(output / 'published-manifest.json'),
               'source_manifest_sha256': sha(output / 'source-manifest.json'),
               'ready_for_parent_review': ready}
    save(output / 'receipt.json', receipt)
    return receipt


def build(args, output):
    prep = args.assets.resolve(strict=True)
    prep_receipt = read(prep / 'receipt.json')
    require(prep_receipt['ready_for_parent_review'], 'Asset preparation is incomplete.')
    source = Path(prep_receipt['source'])
    require(sha(prep / 'source-manifest.json') == prep_receipt['source_manifest_sha256'], 'Source manifest changed.')
    require(manifest(source) == read(prep / 'source-manifest.json'), 'Private original sources changed.')
    host = args.host.resolve(strict=True)
    require(sha(host / 'Nu.dll') == NU_SHA, 'Wrong application Nu.dll.')
    before = manifest(host)
    authority = ROOT / '.artifacts/r12-propagation-20261018/build-01/host-before.json'
    require(sha(authority) == '29529d5f3c7ac48da6fda38f77e05c34ef345081a75e16d204a71dd2108488da',
            'Application host authority changed.')
    shutil.copy2(authority, output / 'accepted-host-authority.json')
    expected = read(output / 'accepted-host-authority.json')
    require(before == expected, 'The application host differs from the accepted R12/R05 host.')
    host_attrs = attributes(host)
    save(output / 'host-attributes-before.json', host_attrs)
    save(output / 'host-before.json', before)
    command = ['dotnet', 'build', str(PACKAGE / 'R12TerraFirmaProbe.fsproj'), '-c', 'Release', '--nologo',
               f'-p:NuHostRoot={host}', f'-p:TerraSourceRoot={source}',
               f'-p:BaseIntermediateOutputPath={output / "obj"}/', f'-p:BaseOutputPath={output / "bin"}/']
    result = process(command, PACKAGE, output, 300)
    binary = output / 'bin/Release/net10.0'
    outputs = manifest(binary) if binary.exists() else {}
    save(output / 'output-manifest.json', outputs)
    save(output / 'output-attributes.json', attributes(binary) if binary.exists() else {})
    save(output / 'host-attributes-after.json', attributes(host))
    copied = all(outputs.get(name) == entry for name, entry in before.items())
    inputs = read(output / 'package-inputs.json')
    unchanged = all((PACKAGE / name).is_file() and sha(PACKAGE / name) == entry['sha256']
                    for name, entry in inputs.items())
    ready = (result['exit_code'] == 0 and unchanged and copied and before == manifest(host)
             and host_attrs == attributes(host)
             and manifest(source) == read(prep / 'source-manifest.json')
             and 'R12TerraFirmaProbe.dll' in outputs and 'R12TerraFirmaProbe.runtimeconfig.json' in outputs)
    receipt = {'stage': 'build', 'process': result, 'assets': str(prep), 'binary': str(binary),
               'source_host': str(host), 'source_host_unchanged': before == manifest(host),
               'source_unchanged': unchanged, 'host_copied_exactly': copied,
               'output_manifest_sha256': sha(output / 'output-manifest.json'),
               'ready_for_parent_review': ready}
    save(output / 'receipt.json', receipt)
    return receipt


def run(args, output):
    built = args.build.resolve(strict=True)
    receipt = read(built / 'receipt.json')
    require(receipt['ready_for_parent_review'], 'Build is incomplete.')
    binary = Path(receipt['binary'])
    require(sha(built / 'output-manifest.json') == receipt['output_manifest_sha256'], 'Output manifest changed.')
    require(manifest(binary) == read(built / 'output-manifest.json'), 'Compiled output changed.')
    seal = read(built / 'source-binary-seal.json')
    acceptance = read(built / 'native-acceptance.json')
    require(acceptance['decision'] == 'accepted_for_native_execution'
            and acceptance['build_receipt_sha256'] == sha(built / 'receipt.json')
            and acceptance['source_binary_seal_sha256'] == sha(built / 'source-binary-seal.json')
            and acceptance['protocol_sha256'] == sha(built / 'package-inputs/PROTOCOL.md'),
            'Missing or mismatched parent compile/harness acceptance.')
    require(seal['pe_pdb_identity_matches'] and seal['verified_original_units'] == 8
            and seal['verified_observer_units'] == 1
            and seal['dll_sha256'] == sha(binary / 'R12TerraFirmaProbe.dll')
            and seal['pdb_sha256'] == sha(binary / 'R12TerraFirmaProbe.pdb'), 'Compiled source seal mismatch.')
    package_inputs = read(built / 'package-inputs.json')
    require(all(sha(PACKAGE / name) == entry['sha256'] for name, entry in package_inputs.items()),
            'Package inputs changed since the accepted build.')
    authorities = output / 'authorities'
    authorities.mkdir()
    for name in ('receipt.json', 'source-binary-seal.json', 'native-acceptance.json', 'package-inputs.json'):
        shutil.copy2(built / name, authorities / name)
    prep = Path(receipt['assets'])
    asset_receipt = read(prep / 'receipt.json')
    published = Path(asset_receipt['published'])
    require(sha(prep / 'published-manifest.json') == asset_receipt['published_manifest_sha256'], 'Asset manifest changed.')
    require(manifest(published) == read(prep / 'published-manifest.json'), 'Published assets changed.')
    app = output / 'application'
    shutil.copytree(binary, app)
    shutil.copytree(published, app, dirs_exist_ok=True)
    shutil.copy2(published / SCENE, app / 'original-Scene.nugroup')
    predecessor = None
    if args.predecessor:
        previous = args.predecessor.resolve(strict=True)
        prev_receipt = read(previous / 'receipt.json')
        require(prev_receipt.get('complete_observation_and_save'), 'Incomplete L0 predecessor.')
        require(prev_receipt['arm'] == 'L0', 'The predecessor must be L0.')
        require(prev_receipt['build_receipt_sha256'] == sha(built / 'receipt.json'), 'Different predecessor build.')
        saved = previous / 'observations/saved-Scene.nugroup'
        require(sha(saved) == prev_receipt['saved_scene_sha256'], 'L0 save changed.')
        save(output / 'scene-before-replacement.json', {'sha256': sha(app / SCENE),
             'mode': (app / SCENE).stat().st_mode, 'windows_attributes': (app / SCENE).stat().st_file_attributes})
        # Nu.Pipe marks published assets read-only. Only this new private copy
        # is made writable; the sealed publication and L0 save remain intact.
        (app / SCENE).chmod((app / SCENE).stat().st_mode | stat.S_IWRITE)
        shutil.copy2(saved, app / SCENE)
        save(output / 'scene-after-replacement.json', {'sha256': sha(app / SCENE),
             'mode': (app / SCENE).stat().st_mode, 'windows_attributes': (app / SCENE).stat().st_file_attributes})
        predecessor = {'receipt': str(previous / 'receipt.json'), 'sha256': sha(previous / 'receipt.json')}
    application_before = manifest(app)
    save(output / 'application-before.json', application_before)
    application_attrs = attributes(app)
    save(output / 'application-attributes-before.json', application_attrs)
    runtimeconfig = read(app / 'R12TerraFirmaProbe.runtimeconfig.json')
    runtime_properties = runtimeconfig['runtimeOptions']['configProperties']
    require(runtime_properties.get('System.GC.Server') is True and runtime_properties.get('System.Runtime.TieredPGO') is True,
            'The generated application GC/TieredPGO configuration differs from the protocol.')
    dotnet = Path(shutil.which('dotnet')).resolve(strict=True)
    save(output / 'runtime-launch.json', {'dotnet': str(dotnet), 'sha256': sha(dotnet), 'runtimeconfig': runtimeconfig})
    environment = os.environ.copy()
    for prefix in ('COREHOST', 'DOTNET_HOST'):
        environment[prefix + '_TRACE'] = '1'
        environment[prefix + '_TRACEFILE'] = str(output / 'runtime-host-trace.log')
    observations = output / 'observations'
    observations.mkdir()
    arm = 'L1' if predecessor else 'L0'
    command = [str(dotnet), 'exec', '--depsfile', str(app / 'R05EventProbe.deps.json'),
               '--runtimeconfig', str(app / 'R12TerraFirmaProbe.runtimeconfig.json'),
               str(app / 'R12TerraFirmaProbe.dll'), arm, str(observations)]
    result = process(command, app, output, 180, environment)
    after = manifest(app)
    save(output / 'application-after.json', after)
    after_attrs = attributes(app)
    save(output / 'application-attributes-after.json', after_attrs)
    save(output / 'observations-manifest.json', manifest(observations))
    trace = output / 'runtime-host-trace.log'
    runtime_paths = re.findall(r'CoreCLR path\s*=\s*[^\r\n]+', trace.read_text(encoding='utf-8', errors='replace')) if trace.exists() else []
    save(output / 'runtime-selection.json', {'coreclr_path_lines': runtime_paths,
                                            'trace_sha256': sha(trace) if trace.exists() else None})
    summary_path = observations / 'summary.json'
    summary = read(summary_path) if summary_path.exists() else None
    save_path = observations / 'saved-Scene.nugroup'
    unchanged = (all(after.get(name) == entry for name, entry in application_before.items())
                 and all(after_attrs.get(name) == entry for name, entry in application_attrs.items()))
    complete = (summary is not None and summary.get('Complete') is True and result['exit_code'] == 0
                and not result['timed_out'] and unchanged and save_path.is_file() and bool(runtime_paths))
    record = {'stage': 'run', 'arm': arm, 'predecessor': predecessor, 'process': result,
              'build_receipt_sha256': sha(built / 'receipt.json'), 'summary': summary,
              'observations_manifest_sha256': sha(output / 'observations-manifest.json'),
              'runtime_selection_recorded': bool(runtime_paths),
              'native_acceptance_sha256': sha(built / 'native-acceptance.json'),
              'protected_application_files_unchanged': unchanged,
              'changed_or_removed_application_files': [n for n, e in application_before.items() if after.get(n) != e],
              'new_application_files': sorted(set(after) - set(application_before)),
              'complete_observation_and_save': complete,
              'saved_scene_sha256': sha(save_path) if save_path.exists() else None}
    save(output / 'receipt.json', record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    stages = parser.add_subparsers(dest='stage', required=True)
    asset_parser = stages.add_parser('assets')
    asset_parser.add_argument('--archive', type=Path, required=True)
    asset_parser.add_argument('--pipeline', type=Path, required=True)
    build_parser = stages.add_parser('build')
    build_parser.add_argument('--assets', type=Path, required=True)
    build_parser.add_argument('--host', type=Path, required=True)
    run_parser = stages.add_parser('run')
    run_parser.add_argument('--build', type=Path, required=True)
    run_parser.add_argument('--predecessor', type=Path)
    for stage in (asset_parser, build_parser, run_parser):
        stage.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    private = (ROOT / '.artifacts/r12-propagation-20261018').resolve()
    require(output.is_relative_to(private) and output != private, 'Use a new private R12 attempt directory.')
    output.mkdir(parents=True, exist_ok=False)
    snapshot(output)
    try:
        result = {'assets': assets, 'build': build, 'run': run}[args.stage](args, output)
    except Exception as error:
        save(output / 'preparation-error.json', {'type': type(error).__name__, 'error': str(error)})
        raise
    print(json.dumps(result, indent=2))
    return 0 if result.get('ready_for_parent_review', result.get('complete_observation_and_save', False)) else 2


if __name__ == '__main__':
    raise SystemExit(main())
