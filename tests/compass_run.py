"""Run from src: python3 ../tests/compass_run.py."""
import re
import subprocess
from pathlib import Path

binary = str(Path('sdtty').resolve())
cases = [
    ('sides 1p2p', ('north', 'north 4', 'northerners', 'near 4'),
     '3G> 3B> 2G> 2B> 4B> 4G> 1B> 1G>'),
    ('sides 1p2p', ('south', 'south 4', 'southerners', 'far 4'),
     '3G< 3B< 2G< 2B< 4B< 4G< 1B< 1G<'),
    ('heads 1p2p', ('east', 'east 4', 'easterners'),
     '3B^ 2G^ 3G^ 2B^ 4B^ 1G^ 4G^ 1B^'),
    ('heads 1p2p', ('west', 'west 4', 'westerners'),
     '3BV 2GV 3GV 2BV 4BV 1GV 4GV 1BV'),
]

# From columns, each designated runner has a non-runner beside them.
# Rotate the starting formation so both caller-relative axes are exercised.
for start, designees, expected in cases:
    for designee in designees:
        commands = (f'ms\n{start}\ntouch 1/4\n{designee} run\n'
                    'quit the program\ny\n')
        result = subprocess.run(
            [binary, '-no_console', '-session', '0'], input=commands,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10)
        assert result.returncode == 0, result.stdout
        assert 'no matches' not in result.stdout, result.stdout
        assert "Can't do this call" not in result.stdout, result.stdout
        assert re.findall(r'[1-4][BG][<>^V]', result.stdout)[-8:] == expected.split(), result.stdout

print('Compass run checks passed for all four halves and their aliases.')
