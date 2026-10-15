namespace NuHistoryResearch

open System
open System.IO
open System.Numerics
open System.Collections.Generic
open System.Text.Json
open Prime
open Nu
open Nu.Gaia
open Breakout

module Program =
    let fields (pairs : (string * obj) list) = Dictionary<string, obj> (dict pairs)
    let json value = JsonSerializer.Serialize value
    let bits (value : single) = (BitConverter.SingleToInt32Bits value).ToString "X8"
    let vector (value : Vector3) = [| bits value.X; bits value.Y; bits value.Z |]
    let quaternion (value : Quaternion) = [| bits value.X; bits value.Y; bits value.Z; bits value.W |]
    let colorBits (value : Color) = [| bits value.R; bits value.G; bits value.B; bits value.A |]
    let modelData (g : Gameplay) =
        fields
            [ "time", box g.GameplayTime; "state", box (string g.GameplayState)
              "paddlePosition", box (vector g.Paddle.Position); "paddleSize", box (vector g.Paddle.Size)
              "ballPosition", box (vector g.Ball.Position); "ballSize", box (vector g.Ball.Size)
              "ballSpeed", box (bits g.Ball.Speed); "ballDirection", box (vector g.Ball.Direction)
              "bricks", box [| for KeyValue (name, brick) in g.Bricks ->
                                  fields ["name", box name; "position", box (vector brick.Position)
                                          "size", box (vector brick.Size); "color", box (colorBits brick.Color)] |]
              "score", box g.Score; "lives", box g.Lives ]

    let scene = Simulants.GameplayScene
    let projection (world : World) =
        let g = Simulants.Gameplay.GetGameplay world
        let sprite name =
            let entity = scene / name
            if entity.GetExists world then
                fields ["name", box name; "exists", box true
                        "position", box (vector (entity.GetPosition world))
                        "size", box (vector (entity.GetSize world))
                        "color", box (colorBits (entity.GetColor world))]
            else fields ["name", box name; "exists", box false]
        fields
            [ "names", box (World.getEntities scene world |> Seq.map (fun entity -> entity.Name) |> Seq.sort |> Seq.toArray)
              "paddle", box (sprite "Paddle"); "ball", box (sprite "Ball")
              "bricks", box (g.Bricks |> Map.toArray |> Array.map (fun (name, _) -> sprite name))
              "scoreText", box ((scene / "Score").GetText world)
              "messageText", box ((scene / "Message").GetText world)
              "rotation", box (quaternion ((scene / "StaticModel").GetRotation world)) ]

    let projectionErrors (g : Gameplay) (world : World) =
        let failures = ResizeArray<string> ()
        let check label passed = if not passed then failures.Add label
        let checkSprite name position size =
            let entity = scene / name
            check (name + ":exists") (entity.GetExists world)
            if entity.GetExists world then
                check (name + ":position") (vector (entity.GetPosition world) = vector position)
                check (name + ":size") (vector (entity.GetSize world) = vector size)
        checkSprite "Paddle" g.Paddle.Position g.Paddle.Size
        checkSprite "Ball" g.Ball.Position g.Ball.Size
        for KeyValue (name, brick) in g.Bricks do
            checkSprite name brick.Position brick.Size
            if (scene / name).GetExists world then
                check (name + ":color") (colorBits ((scene / name).GetColor world) = colorBits brick.Color)
        check "score" ((scene / "Score").GetText world = "Score: " + string g.Score)
        let expectedMessage = if g.Lives <= 0 then "Game over!" elif g.Bricks.Count = 0 then "You win!" else ""
        check "message" ((scene / "Message").GetText world = expectedMessage)
        let actualLives = World.getEntities scene world |> Seq.map (fun entity -> entity.Name) |> Seq.filter (fun name -> name.StartsWith "Life+") |> Set.ofSeq
        check "life-icons" (actualLives = Set.ofList [for i in 0 .. g.Lives - 1 -> "Life+" + string i])
        let expectedRotation = Quaternion.CreateFromAxisAngle ((v3 1.0f 0.75f 0.5f).Normalized, single (g.GameplayTime % 360L) |> degToRadF)
        check "model-rotation" (quaternion ((scene / "StaticModel").GetRotation world) = quaternion expectedRotation)
        failures.ToArray ()

    [<EntryPoint; STAThread>]
    let main args =
        if args.Length <> 4 || not (List.contains args[0] ["history"; "fresh"]) then
            eprintfn "Usage: Probe <history|fresh> <Breakout DLL> <checkpoint directory> <new receipt directory>"
            2
        else
            let mode, dll, checkpointDir, output = args[0], Path.GetFullPath args[1], Path.GetFullPath args[2], Path.GetFullPath args[3]
            if Directory.Exists output then invalidOp "Receipt directory must be new."
            if mode = "history" && Directory.Exists checkpointDir && not (Directory.EnumerateFileSystemEntries checkpointDir |> Seq.isEmpty) then
                invalidOp "History checkpoint directory must be new or empty."
            Directory.CreateDirectory output |> ignore
            Directory.CreateDirectory checkpointDir |> ignore
            let trace = Path.Combine (output, "trace.jsonl")
            let emit label values =
                let record = fields (("event", box label) :: values)
                File.AppendAllText (trace, json record + Environment.NewLine)
            let mutable updates = 0
            let mutable timeUpdates = 0
            let mutable callbacks = 0
            let mutable leftInputs = 0
            let mutable rightInputs = 0
            let mutable phase = "initialize"
            let mutable targetOpt : Gameplay option = None
            let mutable targetProjection = ""
            let mutable checkpointUpdate = 0
            let mutable undoCounts = (0, 0)
            let mutable passed = false
            let mutable done_ = false
            let observe label world =
                let g = Simulants.Gameplay.GetGameplay world
                emit label ["updates", box updates; "timeUpdates", box timeUpdates; "callbacks", box callbacks
                            "functional", box (not world.Imperative); "accompanied", box world.Accompanied
                            "advancing", box world.Advancing; "model", box (modelData g)
                            "projection", box (projection world); "projectionErrors", box (projectionErrors g world)]
            let finish success detail world =
                passed <- success
                done_ <- true
                emit "result" ["pass", box success; "detail", box detail; "phase", box phase
                               "updates", box updates; "timeUpdates", box timeUpdates
                               "leftInputUpdates", box leftInputs; "rightInputUpdates", box rightInputs]
                World.setAdvancing false world
                World.exit world
            let require message condition = if not condition then invalidOp message
            let equalModel a b = json (modelData a) = json (modelData b)
            let verifyTarget label world =
                let target = Option.get targetOpt
                observe label world
                require (label + ": model mismatch") (equalModel target (Simulants.Gameplay.GetGameplay world))
                require (label + ": projected values mismatch") ((projectionErrors target world).Length = 0)
                require (label + ": projection/entity set mismatch") (json (projection world) = targetProjection)
                require (label + ": world advanced") world.Halted
                require (label + ": wrong screen") (World.getSelectedScreen world = Simulants.Gameplay)
            let callback (world : World) =
                if not done_ then
                    try
                        callbacks <- callbacks + 1
                        require "callback watchdog" (callbacks <= 1200)
                        require "wrong mode" (not world.Imperative && world.Accompanied)
                        require "wrong static clock" (Constants.GameTime.DesiredFrameRate = StaticFrameRate 60L)
                        let g = Simulants.Gameplay.GetGameplay world
                        if callbacks <= 5 || callbacks % 60 = 0 then
                            emit "progress" ["phase", box phase; "callbacks", box callbacks
                                             "updates", box updates; "timeUpdates", box timeUpdates
                                             "advancing", box world.Advancing; "gameplayTime", box g.GameplayTime
                                             "score", box g.Score; "bricks", box g.Bricks.Count; "lives", box g.Lives]
                        match phase with
                        | "initialize" ->
                            require "initial world is advancing" world.Halted
                            require "Gameplay is not selected/idling" (World.getSelectedScreen world = Simulants.Gameplay && World.getSelectedScreenIdling world)
                            require "initial Gameplay contract" (g.Score = 0 && g.Bricks.Count = 30 && g.GameplayState = Playing)
                            World.subscribe (fun _ w ->
                                updates <- updates + 1
                                if World.isKeyboardKeyDown KeyboardKey.Left w then leftInputs <- leftInputs + 1
                                if World.isKeyboardKeyDown KeyboardKey.Right w then rightInputs <- rightInputs + 1
                                Cascade) Simulants.Gameplay.UpdateEvent Game world |> ignore
                            World.subscribe (fun _ _ -> timeUpdates <- timeUpdates + 1; Cascade) Simulants.Gameplay.TimeUpdateEvent Game world |> ignore
                            observe "fresh-initial" world
                            if mode = "history" then
                                phase <- "reach-checkpoint"
                                World.setAdvancing true world
                            else
                                let target = scvalue<Gameplay> (File.ReadAllText (Path.Combine (checkpointDir, "gameplay.symbol")))
                                targetOpt <- Some target
                                targetProjection <- File.ReadAllText (Path.Combine (checkpointDir, "projection.json"))
                                require "fresh initial negative control passed incorrectly" (not (equalModel target g))
                                require "fresh initial projection negative control passed incorrectly" (json (projection world) <> targetProjection)
                                Simulants.Gameplay.SetGameplay { target with Score = g.Score } world
                                phase <- "partial-reconstruction"
                        | "reach-checkpoint" ->
                            if g.Score > 0 && g.Bricks.Count < 30 then
                                observe "eligible-hit-halt-request" world
                                World.setAdvancing false world
                                phase <- "checkpoint-halt-requested"
                            elif updates >= 600 then finish false "No eligible brick-hit checkpoint within 600 actual Updates." world
                        | "checkpoint-halt-requested" when world.Halted ->
                                require "halted checkpoint no longer eligible" (g.Score > 0 && g.Bricks.Count < 30)
                                require "checkpoint projection mismatch" ((projectionErrors g world).Length = 0)
                                Gaia.researchSnapshot world
                                targetOpt <- Some g
                                targetProjection <- json (projection world)
                                checkpointUpdate <- updates
                                let encoded = scstring g
                                require "checkpoint serialization loses values" (equalModel g (scvalue<Gameplay> encoded))
                                File.WriteAllText (Path.Combine (checkpointDir, "gameplay.symbol"), encoded)
                                File.WriteAllText (Path.Combine (checkpointDir, "projection.json"), targetProjection)
                                observe "checkpoint-post-update-pre-timeupdate" world
                                phase <- "drift"
                                World.setAdvancing true world
                        | "drift" when updates >= checkpointUpdate + 10 ->
                            observe "drift-halt-request" world
                            World.setAdvancing false world
                            phase <- "drift-halt-requested"
                        | "drift-halt-requested" when world.Halted ->
                            observe "drift" world
                            require "drift did not distinguish model" (not (equalModel (Option.get targetOpt) g))
                            undoCounts <- updates, timeUpdates
                            require "Gaia undo returned false" (Gaia.researchUndo world)
                            verifyTarget "history-immediate-B0" world
                            require "event during undo" ((updates, timeUpdates) = undoCounts)
                            phase <- "history-halted"
                        | "history-halted" ->
                            require "advancing event after undo" ((updates, timeUpdates) = undoCounts)
                            verifyTarget "history-next-halted-boundary" world
                            finish true "B0 model and projected properties restored; next halted boundary agrees." world
                        | "partial-reconstruction" ->
                            let target = Option.get targetOpt
                            observe "partial-negative-control" world
                            require "incomplete model incorrectly accepted" (not (equalModel target g))
                            require "incomplete projection incorrectly accepted" (json (projection world) <> targetProjection)
                            require "score-specific detector did not reject partial reconstruction" ((projectionErrors target world) |> Array.contains "score")
                            Simulants.Gameplay.SetGameplay target world
                            observe "fresh-full-setter-immediate" world
                            require "setter model mismatch" (equalModel target (Simulants.Gameplay.GetGameplay world))
                            phase <- "fresh-halted"
                        | "fresh-halted" ->
                            require "fresh reconstruction advanced" (updates = 0 && timeUpdates = 0)
                            verifyTarget "fresh-next-halted-boundary" world
                            finish true "Fresh same-state reconstruction and both negative controls passed." world
                        | _ -> ()
                    with ex ->
                        emit "exception" ["type", box (ex.GetType().FullName); "message", box ex.Message; "stack", box ex.StackTrace]
                        finish false ex.Message world
            try
                Directory.SetCurrentDirectory AppContext.BaseDirectory
                let state = { GaiaState.defaultState with ProjectDllPath = dll; ProjectEditModeOpt = Some "Gameplay"; ProjectFreshlyLoaded = true; ProjectImperativeExecution = false }
                let (actualState, targetDir, plugin) = Nu.initPlus (fun () ->
                    File.WriteAllText (Path.Combine (AppContext.BaseDirectory, Constants.Gaia.StateFilePath), scstring state)
                    Gaia.selectNuPlugin (GaiaPlugin ()))
                Constants.GameTime.DesiredFrameRate <- StaticFrameRate 60L
                emit "configuration" ["arm", box mode; "projectDll", box dll; "targetDirectory", box targetDir
                                      "functional", box (not actualState.ProjectImperativeExecution)
                                      "plugin", box (plugin.GetType().FullName); "runtime", box (Environment.Version.ToString())
                                      "nuAssembly", box typeof<World>.Assembly.FullName]
                require "selected plugin is not Breakout" (plugin.GetType().FullName = typeof<BreakoutPlugin>.FullName)
                Gaia.setResearchPostProcess callback
                let exitCode = Gaia.run actualState targetDir plugin
                emit "engine-exit" ["exitCode", box exitCode; "probeFinished", box done_; "probePassed", box passed]
                if passed && done_ && exitCode = 0 then 0 else 1
            with ex ->
                emit "launch-exception" ["type", box (ex.GetType().FullName); "message", box ex.Message; "stack", box ex.StackTrace]
                1
