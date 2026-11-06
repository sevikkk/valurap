# FreeCAD Folder Handover

This folder is close to a standalone project.

It does not depend on sibling repos like `../host_soft` or `../stm_soft`.
All geometry and scripts used by the current assembly live inside this folder.

## What Is Local

- `frame.py` builds the printer assembly from:
  - local `vitamins/vitamins.FCStd`
  - local printed-part `.brep` files
- generated part scripts such as `left_y_motor_plate.py` and `left_z_rod_plate.py` open local `frame.FCStd` and export local `.brep` files
- source CAD files for several parts exist as local `.FCStd`

## Real External Requirements

The only real outside dependency is FreeCAD itself.

On this machine, the working console entrypoint was:

```sh
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd
```

The part/build scripts use these FreeCAD modules/workbenches:

- `FreeCAD`
- `Part`
- `Sketcher`
- `Mesh` for `print_fixture.py`

## Current Build State

`frame.py` only inserts printed parts if `<part>.brep` exists.

Current status:

- `left_y_motor_plate`: `.py`, `.FCStd`, `.brep` present
- `left_y_carriage_plate`: `.py`, `.FCStd`, `.brep` present
- `left_z_rod_support`: `.py`, `.FCStd`, `.brep` present
- `left_y_idler_plate`: `.py`, `.FCStd` present, `.brep` missing
- `left_z_rod_plate`: `.py`, `.FCStd` present, `.brep` missing
- `x_carriage_plate`: `.FCStd` present, `.py` and `.brep` missing
- `titan_mount_plate`: `.FCStd` present, `.py` and `.brep` missing

So this folder is self-contained as source, but not yet fully self-contained as a clean rebuild of all printed parts.

## Important File Relationships

- `frame.py` assembles the machine and expects local `.brep` files.
- `left_y_motor_plate.py`, `left_y_idler_plate.py`, `left_y_carriage_plate.py`, `left_z_rod_support.py`, and `left_z_rod_plate.py` open local `frame.FCStd` and export a local `.brep`.
- `rebuild_vitamins.py` rebuilds `vitamins/vitamins.FCStd` from local `vitamins/breps`.
- `unbuild_part.py` reverse-engineers a part `.FCStd` into a generated Python script.
- `unbuild_vitamins.py` looks stale: it references `vitamins/vitamins2.FCStd`, which is not present.

## FreeCAD Invocation Notes

Two details mattered here:

1. `python3` did not have the `FreeCAD` module available.
2. `freecadcmd script.py` on this machine tried to open the script as a project file instead of executing it.

The reliable pattern was:

```sh
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd -c 'import pathlib, sys; sys.argv=["unbuild_part.py","left_z_rod_plate.FCStd","left_z_rod_plate.py"]; exec(pathlib.Path("unbuild_part.py").read_text(), {"__name__":"__main__"})'
```

## Notes On `unbuild_part.py`

`unbuild_part.py` was updated during this session to make reverse-engineering less brittle:

- accepts input and output paths from `sys.argv`
- names the generated body/export from the requested output filename
- handles FreeCAD 1.0 sketch API differences:
  - `AttachmentSupport` vs `Support`
  - `Sketch.getConstruction(i)` vs `geom.Construction`
- emits `TraceSupport = False` to match the style of existing generated part scripts

This is what was used to create `left_z_rod_plate.py`.

## Known Gotchas

- Running a generated part script writes `<part>.FCStd` via `saveAs(...)` at the end. That can overwrite the checked-in source `.FCStd`.
- FreeCAD emitted warnings about cache/config files and lost shape-binder links while opening standalone `.FCStd` files. Those warnings did not block reverse-engineering in this folder.
- `print_fixture.py` currently hardcodes `x_carriage_plate.brep`, so it will not work until that `.brep` exists.

## If Rebuilding In A Fresh Copy

Suggested order:

1. Verify FreeCAD works.
2. Verify `vitamins/vitamins.FCStd` exists.
3. Generate any missing `.py` files from local `.FCStd` using `unbuild_part.py`.
4. Run generated part scripts to create missing `.brep` files.
5. Run `frame.py`.

Likely next missing tasks if starting from a fresh folder:

- generate `x_carriage_plate.py` from `x_carriage_plate.FCStd`
- generate `titan_mount_plate.py` from `titan_mount_plate.FCStd`
- export missing `.brep` files for `left_y_idler_plate`, `left_z_rod_plate`, `x_carriage_plate`, and `titan_mount_plate`

## Minimal Conclusion

This folder is standalone in source terms.
It is not yet standalone as a full reproducible build until all printed-part `.brep` outputs are regenerated or committed.
