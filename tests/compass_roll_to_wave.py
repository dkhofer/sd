"""Run from src: python3 ../tests/compass_roll_to_wave.py."""
import re
import subprocess
from pathlib import Path

BINARY = str(Path('sdtty').resolve())


def run(start, call):
    commands = f'c4\n{start}\ntouch 1/4\n{call}\nquit the program\ny\n'
    result = subprocess.run(
        [BINARY, '-no_console', '-session', '0'], input=commands,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10)
    assert result.returncode == 0, result.stdout
    assert 'no matches' not in result.stdout, result.stdout
    return result.stdout


# Exact final dancer positions and facings. The opposite-facing tandems must
# choose opposite handedness to move their leaders in the same compass direction.
expected = {
    'east': ('heads 1p2p', '2GV 2B^ 3G^ 3BV 1GV 1B^ 4G^ 4BV'),
    'west': ('heads 1p2p', '2B^ 2GV 3BV 3G^ 1B^ 1GV 4BV 4G^'),
    'north': ('sides 1p2p', '4B> 1B> 4G< 1G< 3B< 2B< 3G> 2G>'),
    'south': ('sides 1p2p', '4G< 1G< 4B> 1B> 3G> 2G> 3B< 2B<'),
    'right': ('heads 1p2p', '2B^ 2GV 3G^ 3BV 1B^ 1GV 4G^ 4BV'),
    'left': ('heads 1p2p', '2GV 2B^ 3BV 3G^ 1GV 1B^ 4BV 4G^'),
}
for direction, (start, dancers) in expected.items():
    for call in (f'roll {direction} to a wave', f'{direction} roll to a wave',
                 f'leads roll {direction} to a wave', f'leads {direction} roll to a wave'):
        output = run(start, call)
        assert "Can't do this call" not in output, output
        assert re.findall(r'[1-4][BG][<>^V]', output)[-8:] == dancers.split(), output

# A compass direction along the tandem's facing axis is not a sideways roll.
# EVERYONE exposes the full call menu, including calls invalid in this setup.
for direction in ('north', 'south'):
    output = run('heads 1p2p', f'everyone roll {direction} to a wave')
    assert f'Cannot roll {direction} from this facing direction.' in output, output
for direction in ('east', 'west'):
    output = run('sides 1p2p', f'everyone roll {direction} to a wave')
    assert f'Cannot roll {direction} from this facing direction.' in output, output

print('Compass roll-to-a-wave checks passed (including left/right regressions).')
