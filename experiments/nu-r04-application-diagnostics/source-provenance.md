# Source provenance and transformations

The input is the verified Git archive of Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, archive SHA-256 `EB0AA77197DE1971D79AA0657C2AF5CF33B99BA8302A24BA44F3306CCA4BF92B`. Its pre-existing integrity manifest reported 3,240 files checked and no mismatch. The runner independently verifies the archive and the selected file after a fresh extraction.

Selected source: `Projects/Breakout Mmcc/Gameplay.fs`, original SHA-256 `571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423`.

Pinned lines 9-11 define:

```fsharp
type GameplayState =
    | Playing
    | Quit
```

Pinned lines 167-168 end `Gameplay.update` with:

```fsharp
// no update while gameplay is inactive
| Playing | Quit -> gameplay
```

The tracked [`variant-transformations.patch`](variant-transformations.patch) gives the complete source deltas. The experiment applies those transformations to the full actual source file, compiles it in the real Breakout project graph, and saves each exact transformed file privately with its build receipt. No Nu source body, dependency, asset, cache, object, or binary is committed here.
