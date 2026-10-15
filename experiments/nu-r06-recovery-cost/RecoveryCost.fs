namespace NuRecoveryCostResearch

open System
open System.Diagnostics
open System.IO
open System.Numerics
open System.Text
open System.Collections.Generic
open Prime
open Nu
open Nu.Gaia
open Breakout

module B0 = NuHistoryResearch.Program

module Program =
    let require message condition = if not condition then invalidOp message

    let expectedAt (target : Gameplay) step =
        // The same bounded source prediction accepted for R03 B1.
        let mutable x = target.Ball.Position.X
        let mutable y = target.Ball.Position.Y
        for index in 1 .. step do
            let directionX = if index <= 5 then target.Ball.Direction.X else -target.Ball.Direction.X
            x <- x + target.Ball.Speed * directionX
            y <- y + target.Ball.Speed * target.Ball.Direction.Y
        let direction =
            if step >= 5 then Vector3 (-target.Ball.Direction.X, target.Ball.Direction.Y, target.Ball.Direction.Z)
            else target.Ball.Direction
        { target with
            GameplayTime = target.GameplayTime + int64 step
            Ball = { target.Ball with Position = Vector3 (x, y, target.Ball.Position.Z); Direction = direction } }

    let projectionForModel names paddleColor ballColor (g : Gameplay) =
        let sprite name position size color =
            B0.fields
                [ "name", box name; "exists", box true
                  "position", box (B0.vector position); "size", box (B0.vector size)
                  "color", box (B0.colorBits color) ]
        let rotation =
            Quaternion.CreateFromAxisAngle
                ((v3 1.0f 0.75f 0.5f).Normalized,
                 single (g.GameplayTime % 360L) |> degToRadF)
        B0.fields
            [ "names", box names
              "paddle", box (sprite "Paddle" g.Paddle.Position g.Paddle.Size paddleColor)
              "ball", box (sprite "Ball" g.Ball.Position g.Ball.Size ballColor)
              "bricks", box [| for KeyValue (name, brick) in g.Bricks ->
                                   sprite name brick.Position brick.Size brick.Color |]
              "scoreText", box ("Score: " + string g.Score)
              "messageText", box (if g.Lives <= 0 then "Game over!" elif g.Bricks.Count = 0 then "You win!" else "")
              "rotation", box (B0.quaternion rotation) ]

    [<EntryPoint; STAThread>]
    let main args =
        if args.Length <> 6 || not (List.contains args[0] ["H"; "R"]) ||
           not (List.contains args[1] ["feasibility"; "measured"]) then
            eprintfn "Usage: RecoveryCost <H|R> <feasibility|measured> <attempt-id> <Breakout DLL> <checkpoint directory> <new receipt directory>"
            2
        else
            let route, attemptKind, attemptId = args[0], args[1], args[2]
            let dll, checkpoint, output = Path.GetFullPath args[3], Path.GetFullPath args[4], Path.GetFullPath args[5]
            require "Receipt directory must be new" (not (Directory.Exists output))
            Directory.CreateDirectory output |> ignore
            let tracePath = Path.Combine (output, "trace.jsonl")
            let process = Process.GetCurrentProcess ()
            let frequency = Stopwatch.Frequency
            let probeStartTick = Stopwatch.GetTimestamp ()
            let mutable traceWorkTicks = 0L
            let emit label values =
                let start = Stopwatch.GetTimestamp ()
                let record = B0.fields (("event", box label) :: values)
                File.AppendAllText (tracePath, B0.json record + Environment.NewLine)
                traceWorkTicks <- traceWorkTicks + Stopwatch.GetTimestamp () - start
            let sample label =
                process.Refresh ()
                B0.fields
                    [ "label", box label; "timestamp", box (Stopwatch.GetTimestamp ())
                      "allocatedBytesApproximate", box (GC.GetTotalAllocatedBytes false)
                      "gen0Collections", box (GC.CollectionCount 0)
                      "gen1Collections", box (GC.CollectionCount 1)
                      "gen2Collections", box (GC.CollectionCount 2)
                      "managedHeapBytesSecondary", box (GC.GetTotalMemory false)
                      "workingSetBytesSecondary", box process.WorkingSet64
                      "privateBytesSecondary", box process.PrivateMemorySize64 ]
            let samples = ResizeArray<Dictionary<string, obj>> ()
            let storeSample label = samples.Add (sample label)
            let mutable updates, timeUpdates, callbacks = 0, 0, 0
            let mutable leftInputs, rightInputs = 0, 0
            let mutable phase = "initialize"
            let mutable driftStartUpdates, driftStartTimeUpdates = 0, 0
            let mutable recoveryCounts = (0, 0)
            let order = ResizeArray<string> ()
            let updateDeltas = ResizeArray<int64> ()
            let timeUpdateDeltas = ResizeArray<int64> ()
            let mutable targetModelOracle = ""
            let mutable targetProjectionOracle = ""
            let mutable driftModelOracle = ""
            let mutable driftProjectionOracle = ""
            let mutable clearedModelOracle = ""
            let mutable clearRequestCallback = 0
            let mutable recoveryPayloadOpt : string option = None
            let mutable acquisitionStart, acquisitionStop = 0L, 0L
            let mutable recoveryStart, recoveryDirectStop, readinessStop = 0L, 0L, 0L
            let mutable oracleWorkStart, oracleWorkStop = 0L, 0L
            let mutable clockPair1Start, clockPair1Stop, clockPair2Start, clockPair2Stop = 0L, 0L, 0L, 0L
            let mutable passed, done_ = false, false
            let safeCapture name (capture : unit -> obj) =
                try [name, capture ()]
                with error ->
                    [ name + "CaptureErrorType", box (error.GetType().FullName)
                      name + "CaptureErrorMessage", box error.Message ]
            let observe label (world : World) =
                let g = Simulants.Gameplay.GetGameplay world
                emit label
                    [ "phase", box phase; "updates", box updates; "timeUpdates", box timeUpdates
                      "callbacks", box callbacks; "functional", box (not world.Imperative)
                      "accompanied", box world.Accompanied; "advancing", box world.Advancing
                      "selectedGameplay", box (World.getSelectedScreen world = Simulants.Gameplay)
                      "selectedIdling", box (World.getSelectedScreenIdling world)
                      "model", box (B0.modelData g); "projection", box (B0.projection world)
                      "projectionErrors", box (B0.projectionErrors g world) ]
            let observeFailure (world : World) =
                let captures =
                    safeCapture "functional" (fun () -> box (not world.Imperative)) @
                    safeCapture "accompanied" (fun () -> box world.Accompanied) @
                    safeCapture "advancing" (fun () -> box world.Advancing) @
                    safeCapture "halted" (fun () -> box world.Halted) @
                    safeCapture "selectedGameplay" (fun () -> box (World.getSelectedScreen world = Simulants.Gameplay)) @
                    safeCapture "selectedIdling" (fun () -> box (World.getSelectedScreenIdling world)) @
                    safeCapture "model" (fun () -> box (B0.modelData (Simulants.Gameplay.GetGameplay world))) @
                    safeCapture "projection" (fun () -> box (B0.projection world)) @
                    safeCapture "projectionErrors" (fun () ->
                        let g = Simulants.Gameplay.GetGameplay world
                        box (B0.projectionErrors g world))
                emit "failure-state"
                    ([ "phase", box phase; "updates", box updates; "timeUpdates", box timeUpdates
                       "callbacks", box callbacks; "leftInputUpdates", box leftInputs
                       "rightInputUpdates", box rightInputs ] @ captures)
            let finish success detail (world : World) =
                passed <- success
                done_ <- true
                emit "result"
                    [ "pass", box success; "detail", box detail; "phase", box phase
                      "route", box route; "attemptKind", box attemptKind; "attemptId", box attemptId
                      "updates", box updates; "timeUpdates", box timeUpdates; "callbacks", box callbacks
                      "leftInputUpdates", box leftInputs; "rightInputUpdates", box rightInputs
                      "stopwatchFrequency", box frequency
                      "acquisitionStart", box acquisitionStart; "acquisitionStop", box acquisitionStop
                      "acquisitionTicks", box (if acquisitionStop > 0L then acquisitionStop - acquisitionStart else -1L)
                      "recoveryStart", box recoveryStart; "recoveryDirectStop", box recoveryDirectStop
                      "recoveryDirectTicks", box (if recoveryDirectStop > 0L then recoveryDirectStop - recoveryStart else -1L)
                      "readinessStop", box readinessStop
                      "requestToReadyTicks", box (if readinessStop > 0L then readinessStop - recoveryStart else -1L)
                      "oracleWorkStart", box oracleWorkStart; "oracleWorkStop", box oracleWorkStop
                      "oracleWorkTicks", box (if oracleWorkStop > 0L then oracleWorkStop - oracleWorkStart else -1L)
                      "traceWorkTicksBeforeResult", box traceWorkTicks
                      "clockPairs", box [|
                          B0.fields ["start", box clockPair1Start; "stop", box clockPair1Stop; "ticks", box (clockPair1Stop - clockPair1Start)]
                          B0.fields ["start", box clockPair2Start; "stop", box clockPair2Stop; "ticks", box (clockPair2Stop - clockPair2Start)] |]
                      "gcAndMemorySamples", box (samples.ToArray ()) ]
                World.setAdvancing false world
                World.exit world
            let beginDrift (world : World) =
                driftStartUpdates <- updates
                driftStartTimeUpdates <- timeUpdates
                order.Clear ()
                updateDeltas.Clear ()
                timeUpdateDeltas.Clear ()
                phase <- "drift"
                World.setAdvancing true world
            let callback (world : World) =
                let callbackEntry = Stopwatch.GetTimestamp ()
                // The unconditional timestamp capture above is deliberately the first callback operation.
                if phase = "await-ready" && readinessStop = 0L then
                    readinessStop <- callbackEntry
                if not done_ then
                    try
                        callbacks <- callbacks + 1
                        require "callback watchdog" (callbacks <= 1200)
                        require "wrong execution mode" (not world.Imperative && world.Accompanied)
                        require "wrong static clock" (Constants.GameTime.DesiredFrameRate = StaticFrameRate 60L)
                        require "screen selection changed"
                            (World.getSelectedScreen world = Simulants.Gameplay && World.getSelectedScreenIdling world)
                        let g = Simulants.Gameplay.GetGameplay world
                        match phase with
                        | "initialize" ->
                            require "initial world not halted" world.Halted
                            require "initial gameplay contract"
                                (g.GameplayState = Playing && g.Score = 0 && g.Bricks.Count = 30)
                            World.subscribe (fun _ w ->
                                updates <- updates + 1
                                if World.isKeyboardKeyDown KeyboardKey.Left w then leftInputs <- leftInputs + 1
                                if World.isKeyboardKeyDown KeyboardKey.Right w then rightInputs <- rightInputs + 1
                                if phase = "drift" then
                                    order.Add "Update"
                                    updateDeltas.Add w.GameDelta.Updates
                                    if updates - driftStartUpdates = 10 then World.setAdvancing false w
                                Cascade) Simulants.Gameplay.UpdateEvent Game world |> ignore
                            World.subscribe (fun _ w ->
                                timeUpdates <- timeUpdates + 1
                                if phase = "drift" then
                                    order.Add "TimeUpdate"
                                    timeUpdateDeltas.Add w.GameDelta.Updates
                                Cascade) Simulants.Gameplay.TimeUpdateEvent Game world |> ignore
                            observe "fresh-initial" world
                            let target = scvalue<Gameplay> (File.ReadAllText (Path.Combine (checkpoint, "gameplay.symbol")))
                            require "fixed target summary differs"
                                (target.GameplayTime = 149L && target.Score = 100 && target.Bricks.Count = 29 && target.Lives = 5)
                            targetModelOracle <- B0.json (B0.modelData target)
                            targetProjectionOracle <- File.ReadAllText (Path.Combine (checkpoint, "projection.json"))
                            require "initial negative control failed" (B0.json (B0.modelData g) <> targetModelOracle)
                            let cleared = { g with GameplayState = Quit }
                            clearedModelOracle <- B0.json (B0.modelData cleared)
                            clearRequestCallback <- callbacks
                            phase <- "await-content-clear"
                            Simulants.Gameplay.SetGameplay cleared world
                        | "await-content-clear" ->
                            require "content clear callback boundary differs" (callbacks = clearRequestCallback + 1)
                            require "content clear advanced" (updates = 0 && timeUpdates = 0 && world.Halted)
                            require "content clear changed screen"
                                (World.getSelectedScreen world = Simulants.Gameplay && World.getSelectedScreenIdling world)
                            require "Gameplay scene survived content clear" (not (B0.scene.GetExists world))
                            require "content clear model mismatch" (B0.json (B0.modelData g) = clearedModelOracle)
                            emit "content-cleared"
                                [ "phase", box phase; "updates", box updates; "timeUpdates", box timeUpdates
                                  "callbacks", box callbacks; "clearRequestCallback", box clearRequestCallback
                                  "selectedGameplay", box (World.getSelectedScreen world = Simulants.Gameplay)
                                  "selectedIdling", box (World.getSelectedScreenIdling world)
                                  "sceneExists", box (B0.scene.GetExists world); "model", box (B0.modelData g) ]
                            let target = scvalue<Gameplay> (File.ReadAllText (Path.Combine (checkpoint, "gameplay.symbol")))
                            require "reloaded fixed target summary differs"
                                (target.GameplayTime = 149L && target.Score = 100 && target.Bricks.Count = 29 && target.Lives = 5)
                            require "reloaded fixed target differs" (B0.json (B0.modelData target) = targetModelOracle)
                            Simulants.Gameplay.SetGameplay target world
                            phase <- "seed-ready"
                        | "seed-ready" ->
                            require "seed callback boundary differs" (callbacks = clearRequestCallback + 2)
                            require "seed reconstruction advanced" (updates = 0 && timeUpdates = 0 && world.Halted)
                            require "seed model mismatch" (B0.json (B0.modelData g) = targetModelOracle)
                            require "seed projection mismatch" (B0.json (B0.projection world) = targetProjectionOracle)
                            require "seed projection values mismatch" ((B0.projectionErrors g world).Length = 0)
                            let names =
                                World.getEntities B0.scene world
                                |> Seq.map (fun entity -> entity.Name)
                                |> Seq.sort
                                |> Seq.toArray
                            let paddleColor = (B0.scene / "Paddle").GetColor world
                            let ballColor = (B0.scene / "Ball").GetColor world
                            let driftExpected = expectedAt g 10
                            driftModelOracle <- B0.json (B0.modelData driftExpected)
                            driftProjectionOracle <- B0.json (projectionForModel names paddleColor ballColor driftExpected)
                            observe "seeded-B0" world
                            clockPair1Start <- Stopwatch.GetTimestamp ()
                            clockPair1Stop <- Stopwatch.GetTimestamp ()
                            clockPair2Start <- Stopwatch.GetTimestamp ()
                            clockPair2Stop <- Stopwatch.GetTimestamp ()
                            storeSample "pre-acquisition"
                            acquisitionStart <- Stopwatch.GetTimestamp ()
                            if route = "H" then Gaia.researchSnapshot world
                            else recoveryPayloadOpt <- Some (scstring (Simulants.Gameplay.GetGameplay world))
                            acquisitionStop <- Stopwatch.GetTimestamp ()
                            storeSample "post-acquisition"
                            emit "acquisition"
                                [ "route", box route; "start", box acquisitionStart; "stop", box acquisitionStop
                                  "ticks", box (acquisitionStop - acquisitionStart)
                                  "payloadUtf8Bytes", box (match recoveryPayloadOpt with Some payload -> Encoding.UTF8.GetByteCount payload | None -> 0) ]
                            beginDrift world
                        | "drift" when updates - driftStartUpdates >= 10 && world.Halted ->
                            require "drift Update count differs" (updates - driftStartUpdates = 10)
                            require "drift TimeUpdate count differs" (timeUpdates - driftStartTimeUpdates = 10)
                            let expectedOrder = [| for _ in 1 .. 10 do yield "TimeUpdate"; yield "Update" |]
                            require "drift event order differs" (order.ToArray () = expectedOrder)
                            require "Update GameDelta.Updates differs" (updateDeltas.Count = 10 && updateDeltas |> Seq.forall ((=) 1L))
                            require "TimeUpdate GameDelta.Updates differs" (timeUpdateDeltas.Count = 10 && timeUpdateDeltas |> Seq.forall ((=) 1L))
                            require "host input observed" (leftInputs = 0 && rightInputs = 0)
                            require "complete drift model differs" (B0.json (B0.modelData g) = driftModelOracle)
                            require "complete drift projection differs" (B0.json (B0.projection world) = driftProjectionOracle)
                            require "drift projected values mismatch" ((B0.projectionErrors g world).Length = 0)
                            observe "drift-ready" world
                            emit "drift-schedule"
                                [ "order", box (order.ToArray ()); "updateDeltas", box (updateDeltas.ToArray ())
                                  "timeUpdateDeltas", box (timeUpdateDeltas.ToArray ()) ]
                            storeSample "pre-recovery"
                            recoveryCounts <- updates, timeUpdates
                            recoveryStart <- Stopwatch.GetTimestamp ()
                            try
                                if route = "H" then
                                    require "Gaia undo returned false" (Gaia.researchUndo world)
                                else
                                    let payload = Option.get recoveryPayloadOpt
                                    let target = scvalue<Gameplay> payload
                                    Simulants.Gameplay.SetGameplay target world
                                recoveryDirectStop <- Stopwatch.GetTimestamp ()
                                phase <- "await-ready"
                            with error ->
                                recoveryDirectStop <- Stopwatch.GetTimestamp ()
                                raise error
                        | "await-ready" ->
                            storeSample "ready-entry"
                            require "missing readiness timestamp" (readinessStop > 0L)
                            require "event during recovery/readiness" ((updates, timeUpdates) = recoveryCounts)
                            require "ready world not halted" world.Halted
                            oracleWorkStart <- Stopwatch.GetTimestamp ()
                            let actualModel = B0.json (B0.modelData g)
                            let actualProjection = B0.json (B0.projection world)
                            let projectionErrors = B0.projectionErrors g world
                            let modelMatches = actualModel = targetModelOracle
                            let projectionMatches = actualProjection = targetProjectionOracle
                            let projectedValuesMatch = projectionErrors.Length = 0
                            oracleWorkStop <- Stopwatch.GetTimestamp ()
                            observe "ready-B0" world
                            emit "readiness-timing"
                                [ "start", box recoveryStart; "directStop", box recoveryDirectStop
                                  "readyStop", box readinessStop; "directTicks", box (recoveryDirectStop - recoveryStart)
                                  "requestToReadyTicks", box (readinessStop - recoveryStart)
                                  "oracleWorkTicks", box (oracleWorkStop - oracleWorkStart) ]
                            require "ready model mismatch" modelMatches
                            require "ready projection mismatch" projectionMatches
                            require "ready projected values mismatch" projectedValuesMatch
                            phase <- "complete"
                            finish true "Declared B0 output reached at the next halted callback." world
                        | _ -> ()
                    with error ->
                        if recoveryStart > 0L && recoveryDirectStop = 0L then recoveryDirectStop <- Stopwatch.GetTimestamp ()
                        try observeFailure world with _ -> ()
                        finish false (error.GetType().FullName + ": " + error.Message) world
            try
                Directory.SetCurrentDirectory AppContext.BaseDirectory
                let state =
                    { GaiaState.defaultState with
                        ProjectDllPath = dll
                        ProjectEditModeOpt = Some "Gameplay"
                        ProjectFreshlyLoaded = true
                        ProjectImperativeExecution = false }
                let (actualState, targetDir, plugin) = Nu.initPlus (fun () ->
                    File.WriteAllText (Path.Combine (AppContext.BaseDirectory, Constants.Gaia.StateFilePath), scstring state)
                    Gaia.selectNuPlugin (GaiaPlugin ()))
                Constants.GameTime.DesiredFrameRate <- StaticFrameRate 60L
                emit "configuration"
                    [ "route", box route; "attemptKind", box attemptKind; "attemptId", box attemptId
                      "projectDll", box dll; "checkpoint", box checkpoint; "targetDirectory", box targetDir
                      "functional", box (not actualState.ProjectImperativeExecution)
                      "plugin", box (plugin.GetType().FullName); "runtime", box (Environment.Version.ToString ())
                      "nuAssembly", box typeof<World>.Assembly.FullName; "stopwatchFrequency", box frequency
                      "probeStartTick", box probeStartTick ]
                require "wrong plugin" (plugin.GetType().FullName = typeof<BreakoutPlugin>.FullName)
                Gaia.setResearchPostProcess callback
                let exitCode = Gaia.run actualState targetDir plugin
                emit "engine-exit"
                    [ "exitCode", box exitCode; "probeFinished", box done_; "probePassed", box passed
                      "probeEndTick", box (Stopwatch.GetTimestamp ()); "traceWorkTicksBeforeExit", box traceWorkTicks ]
                let compact =
                    B0.fields
                        [ "attemptId", box attemptId; "attemptKind", box attemptKind; "route", box route
                          "pass", box passed; "exitCode", box exitCode; "stopwatchFrequency", box frequency
                          "acquisitionTicks", box (if acquisitionStop > 0L then acquisitionStop - acquisitionStart else -1L)
                          "recoveryDirectTicks", box (if recoveryDirectStop > 0L then recoveryDirectStop - recoveryStart else -1L)
                          "requestToReadyTicks", box (if readinessStop > 0L then readinessStop - recoveryStart else -1L)
                          "oracleWorkTicks", box (if oracleWorkStop > 0L then oracleWorkStop - oracleWorkStart else -1L)
                          "updates", box updates; "timeUpdates", box timeUpdates; "callbacks", box callbacks ]
                File.WriteAllText (Path.Combine (output, "result.json"), B0.json compact + Environment.NewLine)
                if passed && done_ && exitCode = 0 then 0 else 1
            with error ->
                emit "launch-exception"
                    [ "type", box (error.GetType().FullName); "message", box error.Message; "stack", box error.StackTrace ]
                let compact = B0.fields ["attemptId", box attemptId; "attemptKind", box attemptKind; "route", box route; "pass", box false; "error", box error.Message]
                File.WriteAllText (Path.Combine (output, "result.json"), B0.json compact + Environment.NewLine)
                1
