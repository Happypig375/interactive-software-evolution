module R04DiagnosticProbe.SuccessorFallbackCatchAll

type GameplayState =
    | Playing
    | Quit
    | Paused

type Gameplay =
    { GameplayState : GameplayState
      Lives : int
      BrickCount : int
      PaddleX : int
      Score : int }

let activeUpdate gameplay =
    { gameplay with PaddleX = gameplay.PaddleX + 4; Score = gameplay.Score + 100 }

let update gameplay =
    match gameplay.GameplayState with
    | Playing when gameplay.Lives > 0 && gameplay.BrickCount > 0 -> activeUpdate gameplay
    | _ -> gameplay

[<EntryPoint>]
let main _ =
    let paused =
        { GameplayState = Paused
          Lives = 3
          BrickCount = 10
          PaddleX = 12
          Score = 300 }
    let result = update paused
    let passed = result = paused
    printfn "OBSERVATION case=successor-fallback-catchall oracle=paused-identity passed=%b" passed
    if passed then 0 else 1
