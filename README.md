# Introduction

Sd is a square dance caller's helper.  The program assists you in
writing sequences
for Western square dancing by doing the checker pushing.  You tell the
program what call you want to call next, and it computes the resulting
setup and shows it to you.

## Compass selectors

Use `north` for the near four dancers, `south` for the far four, `east`
for the four on the caller's left, and `west` for the four on the caller's
right. `northerners`, `southerners`, `easterners`, and `westerners` are
synonyms for those respective halves. These directions stay fixed relative
to the caller.

Qualified names include `north 4`, `south box`, `east line`, and `west
column`. North/south also support the existing near/far numbered and
triangle designations. For example, `north u turn back` applies the call
to the near four dancers. East/west halves require eight dancers with an
unambiguous left/right split.

These designations also work with `run`: `northerners run`, `southerners
run`, `easterners run`, and `westerners run`. The shorter forms, such as
`north run` and `east 4 run`, work too. Each runner must have a suitable
non-runner to run around, as with other designations for `run`.

Check these calls with `make -f makefile.macos test-compass-run` from `src`
(requires Python 3).

Use `north facers trade`, `south facers trade`, `east facers trade`, or
`west facers trade` to select dancers by facing direction. North facers
face toward the caller; south facers face away; east facers face the
caller's left; west facers face the caller's right. These selectors work
with other calls that accept designees as well. Use the command without
a comma between the designee and the call.

Check these calls with `make -f makefile.macos test-compass-trade` from
`src` (requires Python 3).

Run the compass selector checks from `src` with:

```sh
make -f makefile.macos test-compass
```

## Compass roll to a wave

`roll north to a wave`, `roll south to a wave`, `roll east to a wave`, and
`roll west to a wave` use the direction of the leaders' sideways movement,
relative to the caller. North is toward the caller, south is away, east is
to the caller's left, and west is to the caller's right. Each tandem chooses
left or right independently, so the result may be asymmetric. A direction
along the dancers' facing axis is rejected because it is not a sideways roll.

The spellings `north roll to a wave` and `leads roll north to a wave`
(and their equivalents in the other directions) are also supported.
Existing left/right calls retain their behavior.

Rebuild both the program and calls database with `make -f makefile.macos`
from `src`. Run the integration checks with
`make -f makefile.macos test-compass-roll` (requires Python 3).

## Compass quarter turns

`quarter north`, `quarter south`, `quarter east`, and `quarter west` turn
every dancer exactly 90 degrees to face the requested caller-relative
direction. The `1/4 north` spelling and its equivalents work too.

North/south require every dancer to start facing east or west. East/west
require every dancer to start facing north or south. If any dancer cannot
make the requested 90-degree turn, the entire call is rejected; dancers
already facing the target direction do not stand still or turn around.

Rebuild with `make -f makefile.macos` from `src` to regenerate the calls
database. Run `make -f makefile.macos test-compass-quarter` to check these
calls (requires Python 3).

## Compass presses

`press north`, `press south`, `press east`, and `press west` require every
dancer to already face the requested caller-relative direction. They then
perform `press ahead`, preserving their facings. If even one dancer faces
another direction, the whole call is rejected without changing the formation.
North is toward the caller, south is away, east is to the caller's left,
and west is to the caller's right.

Half presses such as `1/2 press north` use the same facing requirement.
The existing relative press calls retain their behavior.

Rebuild the program and calls database with `make -f makefile.macos` from
`src`. Run `make -f makefile.macos test-compass-press` to check these calls
(requires Python 3).

## Compass Spin the Windmill

`spin the windmill, outsides north` also accepts `south`, `east`, and
`west`. Each outside dancer must turn exactly 90 degrees to face the named
caller-relative direction. If any outside already faces that direction or
its opposite, the entire call is rejected. North is toward the caller,
south is away, east is to the caller's left, and west is to the caller's right.

The centers perform their normal action, and the outsides then Circulate
as usual. Asymmetric results are allowed. The `and go N positions` and
`and go N-1/2 positions` variants accept cardinal directions too.

For the usual two Circulates, the outsides follow their original track
through both steps without adjusting their positions for an intermediate
collision. They finish diagonally opposite their starting spots, facing
the opposite direction. For example, after `heads fan the top`,
`spin the windmill, outsides south` ends in a 2-by-4 with the outsides
facing north.

Rebuild the program and calls database with `make -f makefile.macos` from
`src`. Run `make -f makefile.macos test-compass-windmill` to check these
calls (requires Python 3).
