#!/usr/bin/env python3
"""Prepare isolated demo copies, run checks and preserve rehearsal evidence."""
import argparse
import hashlib
import html
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / '.workshop'
CANDIDATE = WORK / 'workspace'
STATE = WORK / 'state.json'
COPY_PATHS = ('app', 'tests', 'data', 'legacy', 'catalog', 'mcp', 'docs/business-rules.md',
              'dependencies.json', '.github/agents', '.github/prompts',
              '.github/copilot-instructions.md', '.vscode', '.gitignore')


def catalog():
    return json.loads((ROOT / 'scenarios/manifest.json').read_text(encoding='utf-8'))


def snapshot(path):
    result = {}
    for file in sorted(path.rglob('*')):
        relative = file.relative_to(path)
        if any(part in ('.git', '__pycache__', 'runtime') for part in relative.parts):
            continue
        if file.is_symlink():
            raise ValueError(f'Symlink is not allowed in a demo workspace: {relative}')
        if file.is_file():
            result[relative.as_posix()] = hashlib.sha256(file.read_bytes()).hexdigest()
    return result


def state():
    if not STATE.exists() or not CANDIDATE.is_dir():
        raise ValueError('Primero ejecuta: python3 lab.py prepare retry')
    return json.loads(STATE.read_text(encoding='utf-8'))


def git(*args):
    return subprocess.run(['git', '-C', str(CANDIDATE), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def prepare(name, profile='controlled', archive=False):
    scenario = catalog()[name]
    if CANDIDATE.exists():
        if not archive:
            raise ValueError('Ya existe un ensayo. Usa reset para archivarlo o reset --scenario NOMBRE.')
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        destination = WORK / 'archives' / stamp
        destination.mkdir(parents=True)
        shutil.move(str(CANDIDATE), str(destination / 'workspace'))
        if STATE.exists():
            shutil.copy2(STATE, destination / 'state.json')
        if (WORK / 'results').exists():
            shutil.move(str(WORK / 'results'), str(destination / 'results'))
        print(f'Ensayo anterior conservado en {destination.relative_to(ROOT)}')
    CANDIDATE.mkdir(parents=True)
    for name_ in COPY_PATHS:
        source, target = ROOT / name_, CANDIDATE / name_
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target, ignore=shutil.ignore_patterns('__pycache__'))
        else:
            shutil.copy2(source, target)
    overlay = ROOT / 'scenarios' / name / 'overrides'
    if overlay.exists():
        shutil.copytree(overlay, CANDIDATE, dirs_exist_ok=True)
    shutil.copy2(ROOT / 'scenarios' / name / 'ticket.md', CANDIDATE / 'TICKET.md')
    shutil.copy2(ROOT / 'profiles' / f'{profile}.md', CANDIDATE / 'PROFILE.md')
    # Both profiles retain the same red lines. No auto-approval is enabled here.
    with (CANDIDATE / '.github/copilot-instructions.md').open('a', encoding='utf-8') as f:
        f.write('\nConsulta también PROFILE.md y TICKET.md para este ensayo.\n')
    (CANDIDATE / 'README.md').write_text(
        '# Faro — copia de ensayo\n\nLee TICKET.md y docs/business-rules.md.\n'
        'Este directorio contiene fallos educativos intencionales.\n'
        'Pruebas heredadas: `python3 -m unittest discover -s tests -v`.\n'
        'Carga: `python3 -m app.cli`. No despliegues esta copia.\n', encoding='utf-8')
    git('init', '-b', 'main')
    git('add', '.')
    git('-c', 'user.name=Workshop Fixture', '-c',
        'user.email=workshop@example.invalid', 'commit', '-m', f'Fixture educativa: {name}')
    data = dict(scenario=name, profile=profile, baseline=snapshot(CANDIDATE),
                started_at=datetime.now(timezone.utc).isoformat(),
                base_commit=git('rev-parse', 'HEAD'))
    STATE.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(f'Preparado: {name} / {profile}\nAbre SOLO .workshop/workspace en VS Code.')
    print('Pruebas: python3 lab.py unit\nNegocio: python3 lab.py check\nPanel: python3 lab.py report')


def guards(data):
    current = snapshot(CANDIDATE)
    baseline = data['baseline']
    changed = sorted(path for path in set(current) | set(baseline)
                     if current.get(path) != baseline.get(path))
    spec = catalog()[data['scenario']]
    outside = [path for path in changed if path not in spec['allowed_files']]
    deleted = [path for path in baseline if path not in current]
    return dict(changed_files=changed, outside_scope=outside, deleted_files=deleted,
                max_files=spec['max_files'],
                passed=not outside and not deleted and len(changed) <= spec['max_files'])


def verify(use_docker=False):
    data = state()
    control = guards(data)
    if use_docker:
        command = ['docker', 'run', '--rm', '--network=none', '--read-only',
                   '--cap-drop=ALL', '--security-opt=no-new-privileges',
                   '--pids-limit=64', '--memory=256m', '--cpus=1',
                   '--tmpfs', '/tmp:rw,noexec,nosuid,size=32m', '--mount',
                   f'type=bind,src={CANDIDATE},dst=/candidate,readonly',
                   'copilot-control-room-evaluator', '--scenario', data['scenario']]
    else:
        command = [sys.executable, '-I', '-B', str(ROOT / 'evaluation/verify.py'),
                   '--candidate', str(CANDIDATE), '--scenario', data['scenario']]
    try:
        run = subprocess.run(command, capture_output=True, text=True, timeout=40)
        result = json.loads(run.stdout)
        if run.returncode not in (0, 1):
            raise ValueError(f'Runner exited {run.returncode}')
    except (subprocess.TimeoutExpired, OSError, ValueError) as exc:
        result = dict(passed=False, checks=[dict(name='runner', passed=False, detail=str(exc))])
        if 'run' in locals():
            result['runner_stderr'] = run.stderr[-2000:]
    result.update(scenario=data['scenario'], profile=data['profile'], scope=control,
                  checked_at=datetime.now(timezone.utc).isoformat(),
                  runner='docker' if use_docker else 'local (not sandboxed)')
    result['passed'] = result['passed'] and control['passed']
    output = WORK / 'results'
    output.mkdir(exist_ok=True)
    (output / 'latest.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    for item in result['checks']:
        print(f"{'PASS' if item['passed'] else 'FAIL'} {item['name']}: {item['detail']}")
    print(f"{'PASS' if control['passed'] else 'FAIL'} scope: {control['changed_files']}")
    if control['outside_scope']:
        print(f"Fuera de alcance: {control['outside_scope']}")
    print('RESULTADO: ' + ('PASS' if result['passed'] else 'FAIL'))
    render_report(result)
    return 0 if result['passed'] else 1


def render_report(result):
    esc = lambda value: html.escape(str(value))
    rows = ''.join('<tr><td>' + esc(item['name']) + '</td><td class="' +
                   ('pass' if item['passed'] else 'fail') + '">' +
                   ('PASS' if item['passed'] else 'FAIL') + '</td><td>' + esc(item['detail']) +
                   '</td></tr>' for item in result['checks'])
    status = 'PASS' if result['passed'] else 'FAIL'
    document = '''<!doctype html><html lang="es"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Copilot Control Room — evidencia</title><style>
body{background:#0c1525;color:#e5edf9;font:17px/1.5 system-ui;margin:0;padding:4vw}
main{max-width:1100px;margin:auto}h1{font-size:clamp(28px,5vw,54px);margin:.2em 0}
.eyebrow{color:#5ae1c3;text-transform:uppercase;letter-spacing:.2em}.card{background:#17253a;padding:24px;border-radius:12px;margin:24px 0}
table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:12px;border-bottom:1px solid #324157}
.pass{color:#6ee7b7}.fail{color:#fda4af}code{overflow-wrap:anywhere}footer{color:#b4c3d7}
</style><main><div class="eyebrow">Copilot Control Room / Faro</div>
<h1>¿Lo aprobarías?</h1><p>La carga termina. Ahora comprobamos el negocio.</p>'''
    document += f'<div class="card"><h2>{status} · {esc(result["scenario"])}</h2>'
    document += f'<p>Perfil: {esc(result["profile"])} · Runner: {esc(result["runner"])}</p>'
    document += f'<p>Verificado: {esc(result["checked_at"])}</p></div>'
    document += '<table><thead><tr><th>Regla</th><th>Estado</th><th>Evidencia</th></tr></thead><tbody>' + rows + '</tbody></table>'
    document += '<div class="card"><h2>Alcance del cambio</h2><pre>' + esc(json.dumps(result['scope'], indent=2)) + '</pre></div>'
    document += '<footer>Datos sintéticos. Resultado de esta ejecución; no certifica seguridad ni corrección general.</footer></main></html>'
    (WORK / 'results/report.html').write_text(document, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('list')
    sub.add_parser('doctor')
    prep = sub.add_parser('prepare')
    prep.add_argument('scenario', choices=catalog())
    prep.add_argument('--profile', choices=['controlled', 'exploratory'], default='controlled')
    reset = sub.add_parser('reset')
    reset.add_argument('--scenario', choices=catalog())
    reset.add_argument('--profile', choices=['controlled', 'exploratory'])
    sub.add_parser('unit')
    sub.add_parser('demo')
    check = sub.add_parser('check')
    check.add_argument('--docker', action='store_true')
    sub.add_parser('report')
    recover = sub.add_parser('recover')
    recover.add_argument('--reference', action='store_true', required=True)
    args = parser.parse_args()
    try:
        if args.action == 'list':
            for key, value in catalog().items():
                print(f'{key:12} {value["title"]}')
        elif args.action == 'doctor':
            print(f'Python: {sys.version.split()[0]} (requires 3.11+)')
            print(f'Git: {shutil.which("git") or "MISSING"}')
            print(f'Docker (optional): {shutil.which("docker") or "not installed"}')
            print('Copilot/license/model/MCP: verify manually in VS Code; no model call made.')
            return 0 if sys.version_info >= (3, 11) and shutil.which('git') else 1
        elif args.action == 'prepare':
            prepare(args.scenario, args.profile)
        elif args.action == 'reset':
            previous = state()
            prepare(args.scenario or previous['scenario'],
                    args.profile or previous['profile'], archive=True)
        elif args.action in ('unit', 'demo'):
            state()
            command = ['-m', 'unittest', 'discover', '-s', 'tests', '-v'] if args.action == 'unit' else ['-m', 'app.cli']
            return subprocess.run([sys.executable, *command], cwd=CANDIDATE, timeout=40).returncode
        elif args.action == 'check':
            return verify(args.docker)
        elif args.action == 'report':
            target = WORK / 'results/report.html'
            if not target.exists():
                raise ValueError('Ejecuta check primero, aunque su resultado sea FAIL.')
            print(target.as_uri())
        elif args.action == 'recover':
            data = state()
            source = ROOT / 'facilitator/solutions' / data['scenario']
            if not source.is_dir():
                raise ValueError('No reference solution available')
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            backup = WORK / 'archives' / f'pre-reference-{stamp}'
            shutil.copytree(CANDIDATE, backup, ignore=shutil.ignore_patterns('__pycache__'))
            shutil.copytree(source, CANDIDATE, dirs_exist_ok=True)
            print('RECUPERACIÓN: parche de referencia preparado, NO generado por Copilot en esta ejecución.')
            print(f'Copia anterior: {backup.relative_to(ROOT)}. Ejecuta check.')
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
