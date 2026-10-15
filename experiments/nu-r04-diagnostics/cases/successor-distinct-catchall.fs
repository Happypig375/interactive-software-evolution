module R04DiagnosticProbe.SuccessorDistinctCatchAll

type GameplayState =
    | Playing
    | Quit
    | ReadyToServe

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
    let ready =
        { GameplayState = ReadyToServe
          Lives = 3
          BrickCount = 10
          PaddleX = 12
          Score = 300 }
    let actual = update ready
    let expected = { ready with PaddleX = ready.PaddleX + 4 }
    let passed = actual = expected
    printfn "OBSERVATION case=successor-distinct-catchall oracle=ready-moves-paddle passed=%b actual=%A expected=%A" passed actual expected
    if passed then 0 else 1
