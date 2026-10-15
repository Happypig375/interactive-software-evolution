namespace NuHistoryContinuationResearch

open System
open System.IO
open System.Numerics
open Prime
open Nu
open Nu.Gaia
open Breakout

module B0 = NuHistoryResearch.Program

module Program =
    let expectedAt (target : Gameplay) step =
        // A bounded reference trajectory, not a second implementation of collision detection.
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

    let equalModel left right = B0.json (B0.modelData left) = B0.json (B0.modelData right)
    let require message condition = if not condition then invalidOp message

    [<EntryPoint; STAThread>]
    let main args =
        if args.Length <> 4 || not (List.contains args[0] ["history"; "fresh"]) then
            eprintfn "Usage: B1 <history|fresh> <Breakout DLL> <fixed checkpoint directory> <new receipt directory>"
            2
        else
            let mode, dll, checkpoint, output = args[0], Path.GetFullPath args[1], Path.GetFullPath args[2], Path.GetFullPath args[3]
            require "Receipt directory must be new" (not (Directory.Exists output))
            Directory.CreateDirectory output |> ignore
            let trace = Path.Combine (output, "trace.jsonl")
            let emit label values =
                File.AppendAllText (trace, B0.json (B0.fields (("event", box label) :: values)) + Environment.NewLine)
            let mutable updates, timeUpdates, callbacks = 0, 0, 0
            let mutable leftInputs, rightInputs = 0, 0
            let mutable phase = "initialize"
            let mutable targetOpt : Gameplay option = None
            let mutable targetProjection = ""
            let mutable targetNames : string array = [||]
            let mutable startUpdates, startTimeUpdates = 0, 0
            let mutable lastObserved = 0
            let mutable stableCounts = (0, 0)
            let mutable finalProjection = ""
            let order = ResizeArray<string> ()
            let mutable done_, passed = false, false
            let observe label step (world : World) =
                let g = Simulants.Gameplay.GetGameplay world
                emit label ["phase", box phase; "step", box step; "updates", box updates; "timeUpdates", box timeUpdates
                            "callbacks", box callbacks; "functional", box (not world.Imperative); "accompanied", box world.Accompanied
                            "advancing", box world.Advancing; "model", box (B0.modelData g)
                            "projection", box (B0.projection world); "projectionErrors", box (B0.projectionErrors g world)]
            let finish success detail world =
                done_ <- true
                passed <- success
                emit "result" ["pass", box success; "detail", box detail; "phase", box phase
                               "updates", box updates; "timeUpdates", box timeUpdates
                               "leftInputUpdates", box leftInputs; "rightInputUpdates", box rightInputs]
                World.setAdvancing false world
                World.exit world
            let verifyTarget label world =
                let target = Option.get targetOpt
                observe label 0 world
                require (label + ": model mismatch") (equalModel target (Simulants.Gameplay.GetGameplay world))
                require (label + ": projection mismatch") (B0.json (B0.projection world) = targetProjection)
                require (label + ": projected values mismatch") ((B0.projectionErrors target world).Length = 0)
                require (label + ": not halted") world.Halted
            let beginPhase name world =
                phase <- name
                startUpdates <- updates
                startTimeUpdates <- timeUpdates
                lastObserved <- 0
                order.Clear ()
                emit "resume-request" ["phase", box phase; "updates", box updates; "timeUpdates", box timeUpdates]
                World.setAdvancing true world
            let verifySchedule count =
                let expected = [| for _ in 1 .. count do yield "TimeUpdate"; yield "Update" |]
                emit "event-schedule" ["phase", box phase; "updates", box (updates - startUpdates);
                                      "timeUpdates", box (timeUpdates - startTimeUpdates); "order", box (order.ToArray ())]
                require "Update count differs" (updates - startUpdates = count)
                require "TimeUpdate count differs" (timeUpdates - startTimeUpdates = count)
                require "event sequence differs" (order.ToArray () = expected)
            let callback (world : World) =
                if not done_ then
                    try
                        callbacks <- callbacks + 1
                        require "callback watchdog" (callbacks <= 200)
                        require "wrong execution mode" (not world.Imperative && world.Accompanied)
                        require "wrong clock" (Constants.GameTime.DesiredFrameRate = StaticFrameRate 60L)
                        require "screen selection changed" (World.getSelectedScreen world = Simulants.Gameplay && World.getSelectedScreenIdling world)
                        require "host input observed; outside no-input contract" (leftInputs = 0 && rightInputs = 0)
                        let g = Simulants.Gameplay.GetGameplay world
                        match phase with
                        | "initialize" ->
                            require "initial world not halted" world.Halted
                            require "initial gameplay contract" (g.GameplayState = Playing && g.Score = 0 && g.Bricks.Count = 30)
                            World.subscribe (fun _ w ->
                                updates <- updates + 1
                                if World.isKeyboardKeyDown KeyboardKey.Left w then leftInputs <- leftInputs + 1
                                if World.isKeyboardKeyDown KeyboardKey.Right w then rightInputs <- rightInputs + 1
                                if phase = "drift" || phase = "continuation" then
                                    order.Add "Update"
                                    let limit = if phase = "drift" then 10 else 20
                                    if updates - startUpdates = limit then
                                        emit "halt-request-in-update" ["phase", box phase; "step", box limit]
                                        World.setAdvancing false w
                                Cascade) Simulants.Gameplay.UpdateEvent Game world |> ignore
                            World.subscribe (fun _ _ ->
                                timeUpdates <- timeUpdates + 1
                                if phase = "drift" || phase = "continuation" then order.Add "TimeUpdate"
                                Cascade) Simulants.Gameplay.TimeUpdateEvent Game world |> ignore
                            let target = scvalue<Gameplay> (File.ReadAllText (Path.Combine (checkpoint, "gameplay.symbol")))
                            require "fixed target summary differs" (target.GameplayTime = 149L && target.Score = 100 && target.Bricks.Count = 29 && target.Lives = 5)
                            targetOpt <- Some target
                            targetProjection <- File.ReadAllText (Path.Combine (checkpoint, "projection.json"))
                            observe "fresh-initial" 0 world
                            require "initial negative control failed" (not (equalModel target g))
                            Simulants.Gameplay.SetGameplay target world
                            phase <- "seed-halted"
                        | "seed-halted" ->
                            require "reconstruction advanced" (updates = 0 && timeUpdates = 0)
                            verifyTarget "seeded-B0" world
                            targetNames <- World.getEntities B0.scene world |> Seq.map (fun e -> e.Name) |> Seq.sort |> Seq.toArray
                            if mode = "history" then
                                Gaia.researchSnapshot world
                                beginPhase "drift" world
                            else beginPhase "continuation" world
                        | "drift" when updates - startUpdates >= 10 ->
                            observe "drift-end" 10 world
                            require "drift halt not effective" world.Halted
                            verifySchedule 10
                            require "drift did not distinguish the model" (not (equalModel (Option.get targetOpt) g))
                            stableCounts <- updates, timeUpdates
                            require "Gaia undo returned false" (Gaia.researchUndo world)
                            verifyTarget "history-immediate-B0" world
                            require "event during undo" ((updates, timeUpdates) = stableCounts)
                            phase <- "post-undo-halted"
                        | "post-undo-halted" ->
                            verifyTarget "history-next-halted-B0" world
                            require "event at next halted boundary" ((updates, timeUpdates) = stableCounts)
                            beginPhase "continuation" world
                        | "continuation" ->
                            let step = updates - startUpdates
                            if step > lastObserved then
                                observe "continuation-step" step world
                                require "missing or excess observation" (step = lastObserved + 1 && step <= 20)
                                let expected = expectedAt (Option.get targetOpt) step
                                require "source-bounded trajectory/model mismatch" (equalModel expected g)
                                require "projected model mismatch" ((B0.projectionErrors expected world).Length = 0)
                                let names = World.getEntities B0.scene world |> Seq.map (fun e -> e.Name) |> Seq.sort |> Seq.toArray
                                require "scene entity set changed" (names = targetNames)
                                lastObserved <- step
                            if step = 20 then
                                require "continuation halt not effective" world.Halted
                                verifySchedule 20
                                stableCounts <- updates, timeUpdates
                                finalProjection <- B0.json (B0.projection world)
                                phase <- "final-halted"
                        | "final-halted" ->
                            observe "continuation-next-halted" 20 world
                            require "event after final halt" ((updates, timeUpdates) = stableCounts && world.Halted)
                            require "model changed after final halt" (equalModel (expectedAt (Option.get targetOpt) 20) g)
                            require "projection changed after final halt" (B0.json (B0.projection world) = finalProjection)
                            finish true "Twenty bounded continuation states and final halted observation agree with the declared reference." world
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
                                      "plugin", box (plugin.GetType().FullName); "runtime", box (Environment.Version.ToString ())
                                      "nuAssembly", box typeof<World>.Assembly.FullName]
                require "wrong plugin" (plugin.GetType().FullName = typeof<BreakoutPlugin>.FullName)
                Gaia.setResearchPostProcess callback
                let exitCode = Gaia.run actualState targetDir plugin
                emit "engine-exit" ["exitCode", box exitCode; "probeFinished", box done_; "probePassed", box passed]
                if passed && done_ && exitCode = 0 then 0 else 1
            with ex ->
                emit "launch-exception" ["type", box (ex.GetType().FullName); "message", box ex.Message; "stack", box ex.StackTrace]
                1
