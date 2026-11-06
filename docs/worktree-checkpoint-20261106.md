# Valurap source preservation checkpoint — 2026-11-06

The user requested clean worktrees, documented results and GitHub branches
for PX4-VIO and related PX4, NuttX and Valurap work, excluding Aircon.
This checkpoint preserves the pre-existing dirty legacy Valurap checkout on
`sevikkk/codex/worktree-checkpoint-20261106` from base
`d785f44d2a3f789d8c018e1724d5cc858951ab66`.

## Source and result status

The commit retains the existing FreeCAD extraction/generation changes, CAD
originals and reference meshes, host notebooks and motion-planning changes,
optozero/TFT source and STM32 thermocontrol firmware edits. Original authors
and producing sessions are not established for all legacy files. They are
historical, untested WIP. In particular the motion-planning assertion edit is
preserved without endorsing its behavior. No source was executed, built,
tested, simulated, flashed, deployed or printed for this maintenance.

`freecad/README.md` retains the existing detailed CAD handoff. The
`freecad/start_bolts.FCMacro` symlink is preserved as a symlink, including its
existing external target; its target was not followed or made portable.
Notebook outputs and historical logs are not current measurement evidence.

## Retained artifacts and exclusions

Large CAD originals `freecad/frame.FCStd` and `freecad/pi_mount.FCStd`, plus
`freecad.backup.tgz`, were copied to
`/Volumes/Data3/px4-vio/archives/worktree-checkpoints-20261106/valurap/` under
their original relative paths. Transfer completion and basic file availability
were checked. The originals remain in this checkout. These archived payloads
are not stored in GitHub; the JSON inventory records their exact locations.

Generated logs, notebook calibration/backup pickle files, generated Cython
and build outputs, toolpath/layer outputs and the snapshot remain in place.
The separate `host_soft/valurap/tft/libdrm/` vendor checkout is retained and
excluded from this parent repository; it is not adopted as a submodule.
No file or checkout was removed or reset. Exact root-anchored local patterns
in `.git/info/exclude` cover only the reviewed paths listed in the inventory.
No broad source glob was added. Existing ignore rules remain in effect.

`worktree-checkpoint-20261106.json` lists every initially dirty or untracked
path, its purpose, its source-versus-artifact disposition and its local
exclusion where applicable. Git metadata and ordinary remote branch identity
checks validate this publication boundary; they do not qualify the CAD,
firmware or printer behavior. The branch is published by an ordinary non-force
push to the existing `sevikkk/valurap` GitHub origin. Final publication and clean
status are recorded by the coordinating PX4-VIO maintenance report.
