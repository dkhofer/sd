"""Run from src: python3 ../tests/compass_quarter.py."""
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


# Each starting formation contains dancers facing in both opposite directions.
# Every dancer must turn one quarter, without changing position.
cases = [('north', 'heads 1p2p', 'V'), ('south', 'heads 1p2p', '^'),
         ('east', 'sides 1p2p', '<'), ('west', 'sides 1p2p', '>')]
for direction, start, facing in cases:
    for spelling in ('quarter', '1/4'):
        call = f'{spelling} {direction}'
        output = run(start, [call])
        assert "Can't do this call" not in output, output
        snapshots = re.findall(r'[1-4][BG][<>^V]', output)
        assert dancers(output) == [p[:2] + facing for p in snapshots[:8]], output

        # Repeating the call would require zero-degree turns. Its opposite
        # would require 180 degrees. Neither is a quarter turn.
        opposite = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}[direction]
        for invalid in (call, f'{spelling} {opposite}'):
            rejected = run(start, [call, invalid])
            assert "Can't do this call" in rejected, rejected
            assert 'requires every dancer to turn exactly 90' in rejected, rejected
            assert dancers(rejected) == dancers(output), rejected

        # From a squared set, only half the dancers can quarter toward the
        # requested direction. The whole call must fail, leaving everyone
        # in place. A subsequent ordinary quarter right must match baseline.
        rejected = run('just as they are', [call, 'quarter right'])
        baseline = run('just as they are', ['quarter right'])
        assert "Can't do this call" in rejected, rejected
        assert 'requires every dancer to turn exactly 90' in rejected, rejected
        assert dancers(rejected) == dancers(baseline), rejected

print('Compass quarter-turn checks passed, including whole-formation rejection.')
