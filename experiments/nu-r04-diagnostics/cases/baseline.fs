module R04DiagnosticProbe.Baseline

type GameplayState =
    | Playing
    | Quit

type Gameplay =
    { GameplayState : GameplayState
      Lives : int
      BrickCount : int
      PaddleX : int
      Score : int }

let activeUpdate gameplay =
    { gameplay with
        PaddleX = gameplay.PaddleX + 4
        Score = gameplay.Score + 100 }

let updateExplicit gameplay =
    match gameplay.GameplayState with
    | Playing when gameplay.Lives > 0 && gameplay.BrickCount > 0 -> activeUpdate gameplay
    | Playing | Quit -> gameplay

let updateCatchAll gameplay =
    match gameplay.GameplayState with
    | Playing when gameplay.Lives > 0 && gameplay.BrickCount > 0 -> activeUpdate gameplay
    | _ -> gameplay

[<EntryPoint>]
let main _ =
    let samples =
        [ for state in [Playing; Quit] do
              for lives in [0; 1] do
                  for brickCount in [0; 1] do
                      { GameplayState = state
                        Lives = lives
                        BrickCount = brickCount
                        PaddleX = 12
                        Score = 300 } ]
    let mismatches =
        samples
        |> List.choose (fun gameplay ->
            let explicitResult = updateExplicit gameplay
            let catchAllResult = updateCatchAll gameplay
            if explicitResult = catchAllResult then None
            else Some (gameplay, explicitResult, catchAllResult))
    printfn "OBSERVATION case=baseline samples=%d mismatches=%d" samples.Length mismatches.Length
    if List.isEmpty mismatches then 0 else 1
