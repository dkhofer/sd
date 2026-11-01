"""Run from src: python3 ../tests/compass_trade.py."""
import re
import subprocess
from pathlib import Path

binary = str(Path('sdtty').resolve())
cases = [
    ('sides 1p2p', 'north facers', 'those facing the caller',
     '4B^ 3B^ 4G^ 3G^ 1B^ 2B^ 1G^ 2G^'),
    ('sides 1p2p', 'south facers', 'those facing away from the caller',
     '4GV 3GV 4BV 3BV 1GV 2GV 1BV 2BV'),
    ('heads 1p2p', 'east facers', "those facing the caller's left",
     '3B> 2B> 3G> 2G> 4B> 1B> 4G> 1G>'),
    ('heads 1p2p', 'west facers', "those facing the caller's right",
     '3G< 2G< 3B< 2B< 4G< 1G< 4B< 1B<'),
]

# Touch forms waves at Mainstream level. Both axes and both directions are
# exercised, with the facers spread throughout the formation.
for start, designee, original, expected in cases:
    for name in (designee, original):
        commands = f'ms\n{start}\ntouch\n{name} trade\nquit the program\ny\n'
        result = subprocess.run(
            [binary, '-no_console', '-session', '0'], input=commands,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10)
        assert result.returncode == 0, result.stdout
        assert 'no matches' not in result.stdout, result.stdout
        assert "Can't do this call" not in result.stdout, result.stdout
        assert re.findall(r'[1-4][BG][<>^V]', result.stdout)[-8:] == expected.split(), result.stdout

print('Compass-facing trade checks passed for all four directions.')
