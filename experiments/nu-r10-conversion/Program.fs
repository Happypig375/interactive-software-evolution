module R10ConversionProbe

open System
open System.IO
open System.Reflection
open System.Security.Cryptography
open System.Text.Json
open Prime

type GameplayStateV0 =
    | Playing
    | Quit

type GameplayStateV1 =
    | Playing
    | Quit

type GameplayStateRenamed =
    | Active
    | Quit

type Paddle =
    { Position : int
      Size : int }

type PaddleReordered =
    { Size : int
      Position : int }

type Ball =
    { Position : int
      Size : int
      Speed : int
      Direction : int }

type Brick =
    { Position : int
      Size : int
      Color : int }

type [<SymbolicExpansion>] GameplayV0 =
    { GameplayTime : int64
      GameplayState : GameplayStateV0
      Paddle : Paddle
      Ball : Ball
      Bricks : Map<string, Brick>
      Score : int
      Lives : int }

// Deliberately reordered to exercise named expanded-record correspondence.
type [<SymbolicExpansion>] GameplayV1A =
    { Score : int
      BrickReward : int
      Bricks : Map<string, Brick>
      GameplayState : GameplayStateV1
      Lives : int
      Ball : Ball
      GameplayTime : int64
      Paddle : Paddle }

// A second edition with another order, used for ordinary and repeat reloads.
type [<SymbolicExpansion>] GameplayV1B =
    { BrickReward : int
      GameplayTime : int64
      Paddle : Paddle
      Lives : int
      GameplayState : GameplayStateV1
      Score : int
      Ball : Ball
      Bricks : Map<string, Brick> }

type [<SymbolicExpansion>] GameplayV1C =
    { Ball : Ball
      Score : int
      GameplayState : GameplayStateV1
      BrickReward : int
      Paddle : Paddle
      Bricks : Map<string, Brick>
      Lives : int
      GameplayTime : int64 }

type [<SymbolicExpansion>] GameplayV1PaddleReordered =
    { GameplayTime : int64
      GameplayState : GameplayStateV1
      Paddle : PaddleReordered
      Ball : Ball
      Bricks : Map<string, Brick>
      Score : int
      Lives : int
      BrickReward : int }

type [<SymbolicExpansion>] GameplayV1Renamed =
    { GameplayTime : int64
      GameplayState : GameplayStateRenamed
      Paddle : Paddle
      Ball : Ball
      Bricks : Map<string, Brick>
      Score : int
      Lives : int
      BrickReward : int }

type LogicalState =
    { GameplayTime : int64
      State : string
      PaddlePosition : int
      PaddleSize : int
      BallPosition : int
      BallSize : int
      BallSpeed : int
      BallDirection : int
      Bricks : (string * int * int * int) array
      Score : int
      Lives : int
      Reward : int option }

type CaseResult =
    { Case : string
      Passed : bool
      Expected : string
      Actual : string }

type InstallationSource =
    | SourceV0 of GameplayV0
    | SourceV1 of GameplayV1A
    | SourceUnknown of string

let private convert<'source, 'dest> (source : 'source) : 'dest =
    source |> valueToSymbol<'source> |> symbolToValue<'dest>

let private bricksSnapshot (bricks : Map<string, Brick>) =
    bricks
    |> Map.toArray
    |> Array.map (fun (key, brick) -> key, brick.Position, brick.Size, brick.Color)

let private snapshotV0 (value : GameplayV0) : LogicalState =
    { GameplayTime = value.GameplayTime
      State = string value.GameplayState
      PaddlePosition = value.Paddle.Position
      PaddleSize = value.Paddle.Size
      BallPosition = value.Ball.Position
      BallSize = value.Ball.Size
      BallSpeed = value.Ball.Speed
      BallDirection = value.Ball.Direction
      Bricks = bricksSnapshot value.Bricks
      Score = value.Score
      Lives = value.Lives
      Reward = None }

let private snapshotV1A (value : GameplayV1A) : LogicalState =
    { GameplayTime = value.GameplayTime
      State = string value.GameplayState
      PaddlePosition = value.Paddle.Position
      PaddleSize = value.Paddle.Size
      BallPosition = value.Ball.Position
      BallSize = value.Ball.Size
      BallSpeed = value.Ball.Speed
      BallDirection = value.Ball.Direction
      Bricks = bricksSnapshot value.Bricks
      Score = value.Score
      Lives = value.Lives
      Reward = Some value.BrickReward }

let private snapshotV1B (value : GameplayV1B) : LogicalState =
    { GameplayTime = value.GameplayTime
      State = string value.GameplayState
      PaddlePosition = value.Paddle.Position
      PaddleSize = value.Paddle.Size
      BallPosition = value.Ball.Position
      BallSize = value.Ball.Size
      BallSpeed = value.Ball.Speed
      BallDirection = value.Ball.Direction
      Bricks = bricksSnapshot value.Bricks
      Score = value.Score
      Lives = value.Lives
      Reward = Some value.BrickReward }

let private snapshotV1C (value : GameplayV1C) : LogicalState =
    { GameplayTime = value.GameplayTime
      State = string value.GameplayState
      PaddlePosition = value.Paddle.Position
      PaddleSize = value.Paddle.Size
      BallPosition = value.Ball.Position
      BallSize = value.Ball.Size
      BallSpeed = value.Ball.Speed
      BallDirection = value.Ball.Direction
      Bricks = bricksSnapshot value.Bricks
      Score = value.Score
      Lives = value.Lives
      Reward = Some value.BrickReward }

let private withoutReward state = { state with Reward = None }

let private witnessV0 : GameplayV0 =
    { GameplayTime = 941L
      GameplayState = GameplayStateV0.Playing
      Paddle = { Position = 110; Size = 64 }
      Ball = { Position = 73; Size = 8; Speed = 3; Direction = -1 }
      Bricks =
        Map.ofList
            [ "brick-A", { Position = 101; Size = 64; Color = 0x112233 }
              "brick-C", { Position = 303; Size = 32; Color = 0x445566 } ]
      Score = 700
      Lives = 3 }

let private freshV1A : GameplayV1A =
    { Score = 0
      BrickReward = 200
      Bricks = Map.ofList [ "fresh-brick", { Position = 1; Size = 64; Color = 0xFFFFFF } ]
      GameplayState = GameplayStateV1.Playing
      Lives = 5
      Ball = { Position = 48; Size = 8; Speed = 3; Direction = 1 }
      GameplayTime = 0L
      Paddle = { Position = 0; Size = 64 } }

let private freshRenamed : GameplayV1Renamed =
    { GameplayTime = 0L
      GameplayState = GameplayStateRenamed.Active
      Paddle = { Position = 0; Size = 64 }
      Ball = { Position = 48; Size = 8; Speed = 3; Direction = 1 }
      Bricks = Map.ofList [ "fresh-brick", { Position = 1; Size = 64; Color = 0xFFFFFF } ]
      Score = 0
      Lives = 5
      BrickReward = 200 }

let private installV0 (source : GameplayV0) =
    match valueToSymbol source with
    | Symbols (fields, origin) ->
        let rewardField =
            Symbols
                ([ Atom ("BrickReward", ValueNone)
                   valueToSymbol 200 ],
                 ValueNone)
        Symbols (rewardField :: fields, origin) |> symbolToValue<GameplayV1A>
    | symbol -> failwith $"Expected expanded V0 symbol, got {symbol}."

let private install source =
    match source with
    | SourceV0 value -> Ok (installV0 value)
    | SourceV1 value -> Ok value
    | SourceUnknown identity -> Error ("unknown source edition: " + identity)

let private convertOrFallback<'source, 'dest> fallback source =
    try
        let converted = convert<'source, 'dest> source
        converted, false, None
    with exn ->
        fallback, true, Some (exn.GetType().FullName + ": " + exn.Message)

let private result name expected passed actual =
    { Case = name; Passed = passed; Expected = expected; Actual = actual }

let private json value = JsonSerializer.Serialize (value, JsonSerializerOptions (WriteIndented = false))

[<EntryPoint>]
let main _ =
    let expectedV0 = snapshotV0 witnessV0

    let rawV1, rawFallbackUsed, rawError =
        convertOrFallback<GameplayV0, GameplayV1A> freshV1A witnessV0
    let rawV1State = snapshotV1A rawV1
    let rawPass =
        withoutReward rawV1State = expectedV0 && rawV1.BrickReward = 0 &&
        not rawFallbackUsed && Option.isNone rawError

    let installedV1 =
        match install (SourceV0 witnessV0) with
        | Ok value -> value
        | Error error -> failwith error
    let installedState = snapshotV1A installedV1
    let installPass = withoutReward installedState = expectedV0 && installedV1.BrickReward = 200

    let reloaded200 = convert<GameplayV1A, GameplayV1B> installedV1
    let repeated200 = convert<GameplayV1B, GameplayV1C> reloaded200
    let repeatPass =
        snapshotV1B reloaded200 = installedState &&
        snapshotV1C repeated200 = installedState

    let configuredZero = { installedV1 with BrickReward = 0 }
    let configured75 = { installedV1 with BrickReward = 75 }
    let reloadedZero = convert<GameplayV1A, GameplayV1B> configuredZero
    let reloaded75 = convert<GameplayV1A, GameplayV1B> configured75
    let repeatedZero = convert<GameplayV1B, GameplayV1C> reloadedZero
    let repeated75 = convert<GameplayV1B, GameplayV1C> reloaded75
    let dispatchedZero = install (SourceV1 configuredZero)
    let configuredPass =
        snapshotV1B reloadedZero = snapshotV1A configuredZero &&
        snapshotV1B reloaded75 = snapshotV1A configured75 &&
        snapshotV1C repeatedZero = snapshotV1A configuredZero &&
        snapshotV1C repeated75 = snapshotV1A configured75 &&
        dispatchedZero = Ok configuredZero &&
        reloadedZero.BrickReward = 0 && reloaded75.BrickReward = 75 &&
        repeatedZero.BrickReward = 0 && repeated75.BrickReward = 75

    let freshState = snapshotV1A freshV1A
    let freshPass =
        freshV1A.BrickReward = 200 && freshV1A.Score = 0 && freshV1A.Lives = 5 &&
        freshState <> installedState

    let positional = convert<GameplayV0, GameplayV1PaddleReordered> witnessV0
    let positionalPass = positional.Paddle.Size = 110 && positional.Paddle.Position = 64

    let fallbackValue, fallbackUsed, fallbackError =
        convertOrFallback<GameplayV0, GameplayV1Renamed> freshRenamed witnessV0
    let fallbackPass =
        fallbackUsed && Option.isSome fallbackError && fallbackValue = freshRenamed &&
        fallbackValue.Score = 0 && fallbackValue.Lives = 5

    let unknownResult = install (SourceUnknown "unregistered")
    let unknownPass = unknownResult = Error "unknown source edition: unregistered"

    let results =
        [| result "raw-v0-to-v1-default" "Retain seven fields; BrickReward=0; no fallback" rawPass
               (json {| State = rawV1State; FallbackUsed = rawFallbackUsed; Error = rawError |})
           result "explicit-v0-installation" "Retain seven fields; BrickReward=200" installPass (json installedState)
           result "repeat-v1-reload" "Two V1 conversions retain state and reward 200" repeatPass (json (snapshotV1C repeated200))
           result "configured-zero-and-75" "Two V1 reloads and edition dispatch retain rewards 0 and 75" configuredPass
               (json [| snapshotV1C repeatedZero; snapshotV1C repeated75 |])
           result "fresh-v1-round" "Fresh state separately defaults reward=200, score=0, lives=5" freshPass (json freshState)
           result "nested-positional-reorder" "Destination Size=110 and Position=64 (semantic swap)" positionalPass (json positional.Paddle)
           result "renamed-active-case-fallback" "Prime throws; wrapper marks fallback and returns fresh state" fallbackPass
               (json
                   {| FallbackUsed = fallbackUsed
                      Error = fallbackError
                      State = string fallbackValue.GameplayState
                      Score = fallbackValue.Score
                      Lives = fallbackValue.Lives
                      Reward = fallbackValue.BrickReward
                      BrickKeys = fallbackValue.Bricks |> Map.toArray |> Array.map fst |})
           result "unknown-edition" "Explicit unresolved error; no conversion/reset" unknownPass
               (json {| Outcome = "Error"; Message = "unknown source edition: unregistered" |}) |]

    let primeAssembly = typeof<Symbol>.Assembly
    let primePath = primeAssembly.Location
    let assemblyRecord =
        {| Name = primeAssembly.GetName().Name
           AssemblyVersion = string (primeAssembly.GetName().Version)
           InformationalVersion = primeAssembly.GetCustomAttribute<AssemblyInformationalVersionAttribute>() |> Option.ofObj |> Option.map _.InformationalVersion
           FileVersion = primeAssembly.GetCustomAttribute<AssemblyFileVersionAttribute>() |> Option.ofObj |> Option.map _.Version
           Location = primePath
           Sha256 = File.ReadAllBytes primePath |> SHA256.HashData |> Convert.ToHexString |}

    printfn "%s" (json {| Kind = "assembly"; Prime = assemblyRecord |})
    for caseResult in results do printfn "%s" (json {| Kind = "case"; Result = caseResult |})

    if Array.forall _.Passed results then 0 else 1
