module R04DiagnosticProbe.SuccessorDistinctExplicit

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
    | Playing | Quit -> gameplay

[<EntryPoint>]
let main _ =
    let ready =
        { GameplayState = ReadyToServe
          Lives = 3
          BrickCount = 10
          PaddleX = 12
          Score = 300 }
    try
        let result = update ready
        eprintfn "OBSERVATION case=successor-distinct-explicit behavior=unexpected-return result=%A" result
        1
    with ex ->
        eprintfn "OBSERVATION case=successor-distinct-explicit behavior=runtime-exception exception=%s" (ex.GetType().FullName)
        2
