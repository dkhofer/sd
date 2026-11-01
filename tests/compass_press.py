"""Run from src: python3 ../tests/compass_press.py."""
import re
import subprocess
from pathlib import Path

binary = str(Path('sdtty').resolve())


def run(start, calls):
    commands = 'ms\n' + start + '\n' + '\n'.join(calls) + '\nquit the program\ny\n'
    result = subprocess.run(
        [binary, '-no_console', '-session', '0'], input=commands,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10)
    assert result.returncode == 0, result.stdout
    assert 'no matches' not in result.stdout, result.stdout
    return result.stdout


def dancers(output):
    return re.findall(r'[1-4][BG][<>^V]', output)[-8:]


for direction, start in [('north', 'heads 1p2p'), ('south', 'heads 1p2p'),
                         ('east', 'sides 1p2p'), ('west', 'sides 1p2p')]:
    preparation = [f'quarter {direction}']
    for call, reference in [(f'press {direction}', 'press ahead'),
                            (f'1/2 press {direction}', '1/2 press ahead')]:
        output = run(start, preparation + [call])
        baseline = run(start, preparation + [reference])
        assert "Can't do this call" not in output, output
        assert "Can't do this call" not in baseline, baseline
        assert dancers(output) == dancers(baseline), output

        # Every other uniform facing must be rejected, not turned or moved.
        for turns in (1, 2, 3):
            setup = preparation + ['quarter right'] * turns
            rejected = run(start, setup + [call, 'quarter right'])
            baseline = run(start, setup + ['quarter right'])
            assert f'Press {direction} requires every dancer to already face' in rejected, rejected
            assert dancers(rejected) == dancers(baseline), rejected

        # A single wrong-facing dancer invalidates the whole press.
        setup = preparation + ['#1 boy u turn back']
        rejected = run(start, setup + [call, 'quarter right'])
        baseline = run(start, setup + ['quarter right'])
        assert f'Press {direction} requires every dancer to already face' in rejected, rejected
        assert dancers(rejected) == dancers(baseline), rejected

    # The squared-set formation mixes both axes and cannot pass the check.
    rejected = run('just as they are', [f'press {direction}', 'quarter right'])
    baseline = run('just as they are', ['quarter right'])
    assert f'Press {direction} requires every dancer to already face' in rejected, rejected
    assert dancers(rejected) == dancers(baseline), rejected

print('Compass press checks passed, including all-dancer facing requirements.')
