# Prospective runtime fault gates

These source mutants are fixed before any runtime launch. Each starts from `pause-explicit`, changes one behavior, must build, and must be run as its own retained attempt. A fault is validated only if the real runtime reaches the named gate with the declared prior trigger/count evidence and then fails for the predicted reason.

| Mutant | Single source fault | Required prior evidence | Predicted first failing gate |
| --- | --- | --- | --- |
| `missing-toggle` | Remove the Pause button's `ClickEvent => TogglePause` binding. | Pause entity exists; synthetic Pause ClickEvent observer count becomes 1. | `pause-reached`: model remains `Playing` after the counted event. |
| `hidden-content` | Restore the content gate to `GameplayState = Playing`. | Counted Pause event changes model to `Paused`. | `pause-projection`: scene, Resume control, and Quit control are absent. |
| `advancing-time` | Restore the unconditional TimeUpdate increment. | Paused state/projection accepted and the first positive TimeUpdate/Update pair is observed. The normal arms continue through ten pairs. | `pause-frozen-model` at the first post-content boundary after the first pair: GameplayTime differs, with rotation mismatch also expected. An early fault is retained immediately rather than delayed to pair ten. |
| `reset-resume` | Change only the `Paused` TogglePause transition to `Gameplay.initial`. | First pause and ten-pair interval pass; second counted Pause/Resume event occurs. | `resume-retained`: score, bricks, time, ball, or other B0 values reset. No later one-step recovery can rescue it. |
| `stale-quit` | Change only `FinishQuitting` to return the current gameplay rather than `Gameplay.empty`. | Pause/Quit counts are correct and Title becomes selected/idling. | `quit-reset`: the halted Title model lacks the deterministic vacant invariants: time zero, Quit, initial paddle and ball shape, empty bricks, score zero, and lives zero. The oracle does not reevaluate the randomized `Ball.initial` direction for exact equality. |

The separate `pause-wildcard` reference is the required correct-alternative control. The independent content and time mutants cover the compiled-but-incomplete "enumerate Paused with identity while omitting coordinated work" mechanism without treating the correct identity update as a fault.

If compact trace-data mutations are later used to test parsers, label them observation-data controls. They do not validate these source/runtime faults, engine reachability, event routing, or oracle sensitivity to actual application behavior.

