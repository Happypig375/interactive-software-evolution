"""Build or execute only the frozen R12 stub-world probe; no Nu rebuild."""
import argparse
import hashlib
import json
import shutil
import subprocess
import time
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
NU_SHA = 'e96cd61d188c689f7e39e2670b4d8582e26b9ea2dc95e1a15056891b7c99cd68'
INPUTS = ('Program.fs', 'R12PropagationProbe.fsproj', 'PROTOCOL.md', 'global.json')


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def manifest(root):
    return {p.relative_to(root).as_posix(): {'sha256': sha(p), 'bytes': p.stat().st_size}
            for p in sorted(root.rglob('*')) if p.is_file()}


def save(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def execute(command, cwd, output, timeout):
    start = time.monotonic()
    result = {'command': command, 'cwd': str(cwd), 'deadline_seconds': timeout,
              'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    save(output / 'command.json', result)
    with (output / 'stdout.log').open('wb') as stdout, (output / 'stderr.log').open('wb') as stderr:
        try:
            completed = subprocess.run(command, cwd=cwd, stdout=stdout, stderr=stderr,
                                       timeout=timeout, check=False)
            result.update(exit_code=completed.returncode, timed_out=False)
        except subprocess.TimeoutExpired:
            result.update(exit_code=None, timed_out=True)
        except OSError as error:
            result.update(exit_code=None, timed_out=False, launch_error=str(error))
    result['elapsed_seconds'] = time.monotonic() - start
    result['stdout_sha256'] = sha(output / 'stdout.log')
    result['stderr_sha256'] = sha(output / 'stderr.log')
    save(output / 'process.json', result)
    return result


def build(args, output):
    host = args.host.resolve(strict=True)
    if output.is_relative_to(host) or host.is_relative_to(output):
        raise ValueError('The new build directory and existing host must be disjoint.')
    if sha(host / 'Nu.dll') != NU_SHA:
        raise ValueError('Nu.dll does not match the accepted R03/R05 assembly.')
    for name in ('R05EventProbe.deps.json', 'R05EventProbe.runtimeconfig.json'):
        if not (host / name).is_file():
            raise ValueError('The accepted R05 dependency/runtime files are required.')
    before = manifest(host)
    save(output / 'host-before.json', before)
    inputs = output / 'inputs'
    inputs.mkdir()
    for name in INPUTS:
        shutil.copy2(PACKAGE / name, inputs / name)
    shutil.copy2(Path(__file__), inputs / 'run_probe.py')
    command = ['dotnet', 'build', str(PACKAGE / 'R12PropagationProbe.fsproj'),
               '-c', 'Release', '--nologo', f'-p:NuHostRoot={host}',
               f'-p:BaseIntermediateOutputPath={output / "obj"}/',
               f'-p:BaseOutputPath={output / "bin"}/']
    result = execute(command, PACKAGE, output, 300)
    host_after = manifest(host)
    save(output / 'host-after.json', host_after)
    binary_dir = output / 'bin/Release/net10.0'
    built = manifest(binary_dir) if binary_dir.is_dir() else {}
    save(output / 'output-manifest.json', built)
    unchanged = all(sha(PACKAGE / name) == sha(inputs / name) for name in INPUTS)
    copied = all(built.get(name) == entry for name, entry in before.items())
    receipt = {'stage': 'build', 'source_host': str(host), 'binary_dir': str(binary_dir),
               'process': result, 'source_inputs': manifest(inputs),
               'source_unchanged': unchanged, 'source_host_unchanged': before == host_after,
               'all_host_files_copied_exactly': copied,
               'output_manifest_sha256': sha(output / 'output-manifest.json'),
               'accepted_nu_sha256': NU_SHA}
    receipt['ready_for_parent_review'] = (result['exit_code'] == 0 and unchanged and
                                          before == host_after and copied and
                                          'R12PropagationProbe.dll' in built)
    save(output / 'receipt.json', receipt)
    print(json.dumps(receipt, indent=2))
    return 0 if receipt['ready_for_parent_review'] else 2


def run(args, output):
    build_dir = args.build.resolve(strict=True)
    receipt = json.loads((build_dir / 'receipt.json').read_text(encoding='utf-8'))
    if not receipt.get('ready_for_parent_review'):
        raise ValueError('A successful sealed build is required; parent review precedes execution.')
    binary_dir = Path(receipt['binary_dir']).resolve(strict=True)
    if sha(build_dir / 'output-manifest.json') != receipt['output_manifest_sha256']:
        raise ValueError('Build manifest hash changed.')
    expected = json.loads((build_dir / 'output-manifest.json').read_text(encoding='utf-8'))
    if manifest(binary_dir) != expected or sha(binary_dir / 'Nu.dll') != NU_SHA:
        raise ValueError('The sealed compiled output has changed.')
    command = ['dotnet', 'exec', '--depsfile', str(binary_dir / 'R05EventProbe.deps.json'),
               '--runtimeconfig', str(binary_dir / 'R05EventProbe.runtimeconfig.json'),
               str(binary_dir / 'R12PropagationProbe.dll')]
    result = execute(command, output, output, 120)
    after = manifest(binary_dir)
    save(output / 'output-after.json', after)
    events = []
    for line in (output / 'stdout.log').read_text(encoding='utf-8', errors='replace').splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue  # Preserve Nu's non-JSON log lines in the unmodified stdout log.
        if isinstance(event, dict) and 'event' in event:
            events.append(event)
    summaries = [e for e in events if e['event'] == 'summary']
    unchanged = all(after.get(name) == entry for name, entry in expected.items())
    summary = summaries[0] if len(summaries) == 1 else None
    complete = (summary is not None and result['exit_code'] == summary['exitCode'] and
                not result['timed_out'] and unchanged)
    record = {'stage': 'run', 'build_receipt': str(build_dir / 'receipt.json'),
              'build_receipt_sha256': sha(build_dir / 'receipt.json'), 'process': result,
              'sealed_files_unchanged': unchanged,
              'new_output_files': sorted(set(after) - set(expected)),
              'summary': summary, 'event_names': [e['event'] for e in events],
              'disposition': summary['disposition'] if complete else 'invalid_or_incomplete'}
    save(output / 'receipt.json', record)
    print(json.dumps(record, indent=2))
    return result['exit_code'] if complete and result['exit_code'] is not None else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='stage', required=True)
    builder = commands.add_parser('build')
    builder.add_argument('--host', type=Path, required=True)
    runner = commands.add_parser('run')
    runner.add_argument('--build', type=Path, required=True)
    for command in (builder, runner):
        command.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output == PACKAGE or output.is_relative_to(PACKAGE):
        raise ValueError('Retain attempt output outside the tracked probe package.')
    output.mkdir(parents=True, exist_ok=False)
    return build(args, output) if args.stage == 'build' else run(args, output)


if __name__ == '__main__':
    raise SystemExit(main())
