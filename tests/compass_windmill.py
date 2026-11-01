"""Run from src: python3 ../tests/compass_windmill.py."""
import re
import subprocess
from pathlib import Path

binary = str(Path('sdtty').resolve())


def run(start, calls, preparation="pass thru\nwheel and deal\n"):
    commands = ('a2\n' + start + '\n' + preparation +
                '\n'.join(calls) + '\nquit the program\ny\n')
    result = subprocess.run(
        [binary, '-no_console', '-session', '0'], input=commands,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10)
    assert result.returncode == 0, result.stdout
    assert 'no matches' not in result.stdout, result.stdout
    return result.stdout


def diagram(output):
    # Keep phantom slots and row spacing as well as identities and facings.
    tail = re.split(r'^\s+\d+: {2,}[^\n]+$', output, flags=re.MULTILINE)[-1]
    return [line.rstrip() for line in tail.splitlines()
            if re.fullmatch(r'[ .1-4BG<>^V]+', line) and
            (re.search(r'[1-4][BG][<>^V]', line) or '.' in line)]


cases = [('heads 1p2p', 'north'), ('heads 1p2p', 'south'),
         ('sides 1p2p', 'east'), ('sides 1p2p', 'west')]
for start, direction in cases:
    # Calls ending at an intermediate position retain the existing collision
    # handling at their endpoint, after the cardinal quarter turn.
    for prefix in ('', 'left '):
        for suffix, reference in [
                (' and go 1 positions', 'go 1 positions as you are'),
                (' and go 3 positions', 'go 3 positions as you are'),
                (' and go 1-1/2 positions', 'go 1-1/2 positions as you are')]:
            output = run(start, [f'{prefix}spin the windmill, outsides {direction}{suffix}'])
            baseline = run(start, [f'outsides quarter {direction}',
                                  f'{prefix}spin the windmill, outsides {reference}'])
            assert "Can't do this call" not in output, output
            assert "Can't do this call" not in baseline, baseline
            assert diagram(output) and diagram(output) == diagram(baseline), output

    # Already-facing and opposite-facing outsides cannot make a quarter turn.
    opposite = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}[direction]
    for invalid in (direction, opposite):
        setup = [f'outsides quarter {direction}']
        output = run(start, setup + [f'spin the windmill, outsides {invalid}', 'quarter right'])
        baseline = run(start, setup + ['quarter right'])
        assert f'Quarter {invalid} requires every dancer to turn exactly 90' in output, output
        assert diagram(output) == diagram(baseline), output

    # One outside facing the wrong axis must invalidate the whole call.
    setup = ['#1 boy quarter right']
    output = run(start, setup + [f'spin the windmill, outsides {direction}', 'quarter right'])
    baseline = run(start, setup + ['quarter right'])
    assert "Can't do this call" in output, output
    assert diagram(output) == diagram(baseline), output

# Full-track endpoint oracles: each pair of Circulates exchanges diagonally
# opposite outsiders and reverses their facings. Four returns them to start.
# Center action is fixed independently for the normal and left calls.
fixtures = [
    ('heads 1p2p', 'north', '', ['3B^ 4G^ 4BV 1G^', '3G^ 2B^ 2GV 1B^']),
    ('heads 1p2p', 'south', '', ['3BV 4G^ 4BV 1GV', '3GV 2B^ 2GV 1BV']),
    ('sides 1p2p', 'east', '', ['2G> 2B>', '1B> 3G>', '1G< 3B<', '4B> 4G>']),
    ('sides 1p2p', 'west', '', ['2G< 2B<', '1B> 3G>', '1G< 3B<', '4B< 4G<']),
    ('heads 1p2p', 'north', 'left ', ['3B^ 2GV 2B^ 1G^', '3G^ 4BV 4G^ 1B^']),
    ('heads 1p2p', 'south', 'left ', ['3BV 2GV 2B^ 1GV', '3GV 4BV 4G^ 1BV']),
    ('sides 1p2p', 'east', 'left ', ['2G> 2B>', '3B< 1G<', '3G> 1B>', '4B> 4G>']),
    ('sides 1p2p', 'west', 'left ', ['2G< 2B<', '3B< 1G<', '3G> 1B>', '4B< 4G<']),
]


def grid(output):
    return [row.split() for row in diagram(output)]


def four_circulates(two):
    result = [row[:] for row in two]
    corners = [(0, 0), (0, len(two[0])-1),
               (len(two)-1, len(two[0])-1), (len(two)-1, 0)]
    reverse = str.maketrans('^V<>', 'V^><')
    for i, (r, c) in enumerate(corners):
        source_r, source_c = corners[(i+2) % 4]
        result[r][c] = two[source_r][source_c].translate(reverse)
    return result


for start, direction, prefix, rows in fixtures:
    expected = [row.split() for row in rows]
    for n in range(2, 15, 2):
        output = run(start, [f'{prefix}spin the windmill, outsides {direction} and go {n} positions'])
        assert "Can't do this call" not in output, output
        assert 'Take right hands' not in output, output
        assert grid(output) == (expected if n % 4 else four_circulates(expected)), output
    default = run(start, [f'{prefix}spin the windmill, outsides {direction}'])
    assert grid(default) == expected, default

# The reported quarter-tag regression, plus the other cardinal directions.
for start, direction, rows in [
    ('heads start', 'south', ['2BV 3G^ 3BV 4GV', '2GV 1B^ 1GV 4BV']),
    ('heads start', 'north', ['2B^ 3G^ 3BV 4G^', '2G^ 1B^ 1GV 4B^']),
    ('sides start', 'east', ['1G> 1B>', '4B> 2G>', '4G< 2B<', '3B> 3G>']),
    ('sides start', 'west', ['1G< 1B<', '4B> 2G>', '4G< 2B<', '3B< 3G<']),
]:
    preparation = start.split()[0] + ' fan the top\n'
    for suffix in ('', ' and go 2 positions'):
        output = run(start, [f'spin the windmill, outsides {direction}{suffix}'], preparation)
        assert "Can't do this call" not in output, output
        assert 'Take right hands' not in output, output
        assert grid(output) == [row.split() for row in rows], output

# Preserve the existing relative-direction calls.
for start in ('heads 1p2p', 'sides 1p2p'):
    for direction in ('right', 'left'):
        output = run(start, [f'spin the windmill, outsides {direction}'])
        baseline = run(start, [f'outsides quarter {direction}',
                              'spin the windmill, outsides go as you are'])
        assert "Can't do this call" not in output, output
        assert diagram(output) == diagram(baseline), output

print('Compass Windmill checks passed, including variants and invalid outside facings.')
