# Selected pinned source provenance

Source identity: Nu `064f7ae92a8506689cd91aff5e6804a375d6ef3d`, `Projects/Breakout Mmcc/Gameplay.fs`, expected SHA-256 `571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423`.

Exact source lines 8-11:

```fsharp
// this represents the state of gameplay simulation.
type GameplayState =
    | Playing
    | Quit
```

Exact source lines 85-90 and 164-168; the intervening Nu-dependent active branch is omitted:

```fsharp
    // this updates the gameplay model every frame
    static member update gameplay world =

        // update only while gameplay is active.
        match gameplay.GameplayState with
        | Playing when gameplay.Lives > 0 && gameplay.Bricks.Count > 0 ->
```

```fsharp
            // fin
            gameplay

        // no update while gameplay is inactive
        | Playing | Quit -> gameplay
```

The probe preserves the case names, guard shape and terminal patterns. It replaces Nu-dependent records and the active branch with a deterministic five-field pure record and `activeUpdate`. This is an adaptation for a compiler diagnostic check, not an extracted Nu implementation or a whole-program equivalence witness.
