namespace NuR04PauseRuntime

open System
open System.IO
open Prime
open Nu
open Nu.Gaia
open Breakout
open Common

module PauseProbe =

    [<EntryPoint; STAThread>]
    let main args =
        if args.Length <> 3 then
            eprintfn "Usage: Probe <Breakout DLL> <B0 gameplay symbol> <new receipt directory>"
            2
        else
            let dll, symbolPath, output = Path.GetFullPath args[0], Path.GetFullPath args[1], Path.GetFullPath args[2]
            require "Receipt directory must be new" (not (Directory.Exists output))
            Directory.CreateDirectory output |> ignore
            let trace = Path.Combine (output, "trace.jsonl")
            let emit label values = File.AppendAllText (trace, json (fields (("event", box label) :: values)) + Environment.NewLine)
            let mutable phase = "initialize"
            let mutable callbacks, updates, timeUpdates = 0, 0, 0
            let mutable startUpdates, startTimeUpdates = 0, 0
            let mutable advancingEvents, leftInputs, rightInputs = 0, 0, 0
            let mutable pauseClicks, quitClicks, playClicks = 0, 0, 0
            let order = ResizeArray<string> ()
            let deltas = ResizeArray<string * int64> ()
            let audio = ResizeArray<string * string> ()
            let mutable targetOpt : Gameplay option = None
            let mutable clearedOpt : Gameplay option = None
            let mutable pausedOpt : Gameplay option = None
            let mutable pausedProjection = ""
            let mutable done_, passed = false, false
            let safeCapture producer =
                try fields ["available", box true; "value", box (producer ())]
                with error -> fields ["available", box false; "errorType", box (error.GetType().FullName); "error", box error.Message]
            let observeScored label includePause (gameplay : Gameplay) (world : World) =
                let projectionCapture () =
                    fields
                        ["data", box (projection includePause world);
                         "errors", box (projectionErrors includePause gameplay world)]
                emit label
                    ["phase", box phase; "callbacks", box callbacks; "updates", box updates; "timeUpdates", box timeUpdates;
                     "intervalUpdates", box (updates - startUpdates); "intervalTimeUpdates", box (timeUpdates - startTimeUpdates);
                     "order", box (order.ToArray ()); "deltas", box (deltas.ToArray ()); "advancingEvents", box advancingEvents;
                     "worldAdvancing", box world.Advancing; "worldHalted", box world.Halted;
                     "model", box (modelData gameplay);
                     "projection", box (safeCapture projectionCapture);
                     "screen", box (safeCapture (fun () -> screenData world))]
            let finish success detail (world : World) =
                done_ <- true
                passed <- success
                emit "result" ["pass", box success; "detail", box detail; "phase", box phase;
                               "updates", box updates; "timeUpdates", box timeUpdates; "callbacks", box callbacks;
                               "pauseClicks", box pauseClicks; "quitClicks", box quitClicks; "playClicks", box playClicks]
                World.setAudioMessageObserver None
                World.setAdvancing false world
                World.exit world
            let audioCount kind phaseName = audio |> Seq.filter (fun (p, k) -> p = phaseName && k = kind) |> Seq.length
            let publishPause world = World.publish () Simulants.GameplayPause.ClickEvent Simulants.GameplayPause world |> ignore
            let publishQuit world = World.publish () Simulants.GameplayQuit.ClickEvent Simulants.GameplayQuit world |> ignore
            let publishPlay world = World.publish () Simulants.TitlePlay.ClickEvent Simulants.TitlePlay world |> ignore
            let beginRun name world =
                startUpdates <- updates
                startTimeUpdates <- timeUpdates
                advancingEvents <- 0
                order.Clear ()
                deltas.Clear ()
                phase <- name
                World.setAdvancing true world
            let callback (world : World) =
                if not done_ then
                    let mutable failureGameplayOpt : Gameplay option = None
                    try
                        callbacks <- callbacks + 1
                        require "callback watchdog" (callbacks <= 600)
                        require "wrong execution mode" (not world.Imperative && world.Accompanied)
                        require "wrong static clock" (Constants.GameTime.DesiredFrameRate = StaticFrameRate 60L)
                        let gameplay = Simulants.Gameplay.GetGameplay world
                        failureGameplayOpt <- Some gameplay
                        match phase with
                        | "initialize" ->
                            require "initial world not halted" world.Halted
                            require "Gameplay not selected/idling" (World.getSelectedScreen world = Simulants.Gameplay && World.getSelectedScreenIdling world)
                            World.subscribe (fun _ w ->
                                updates <- updates + 1
                                if phase = "paused-run" || phase = "resumed-run" || phase = "fresh-run" then
                                    order.Add "Update"
                                    deltas.Add ("Update", w.GameDelta.Updates)
                                    if w.Advancing then advancingEvents <- advancingEvents + 1
                                    if World.isKeyboardKeyDown KeyboardKey.Left w then leftInputs <- leftInputs + 1
                                    if World.isKeyboardKeyDown KeyboardKey.Right w then rightInputs <- rightInputs + 1
                                    let limit = if phase = "paused-run" then 10 else 1
                                    if updates - startUpdates = limit then World.setAdvancing false w
                                Cascade) Simulants.Gameplay.UpdateEvent Game world |> ignore
                            World.subscribe (fun _ w ->
                                timeUpdates <- timeUpdates + 1
                                if phase = "paused-run" || phase = "resumed-run" || phase = "fresh-run" then
                                    order.Add "TimeUpdate"
                                    deltas.Add ("TimeUpdate", w.GameDelta.Updates)
                                    if w.Advancing then advancingEvents <- advancingEvents + 1
                                Cascade) Simulants.Gameplay.TimeUpdateEvent Game world |> ignore
                            World.subscribe (fun _ _ -> pauseClicks <- pauseClicks + 1; Cascade) Simulants.GameplayPause.ClickEvent Game world |> ignore
                            World.subscribe (fun _ _ -> quitClicks <- quitClicks + 1; Cascade) Simulants.GameplayQuit.ClickEvent Game world |> ignore
                            World.subscribe (fun _ _ -> playClicks <- playClicks + 1; Cascade) Simulants.TitlePlay.ClickEvent Game world |> ignore
                            World.setAudioMessageObserver (Some (fun message ->
                                let kind = audioKind message
                                audio.Add (phase, kind)
                                emit "audio-request" ["phase", box phase; "kind", box kind]))
                            phase <- "audio-single-control"
                            let singleBefore = audio.Count
                            World.playSound 0.0f 0.0f 0.0f Assets.Default.Sound world
                            require "single audio observer control failed" (audio.Count = singleBefore + 1 && audio[audio.Count - 1] = (phase, "PlaySound"))
                            phase <- "audio-plural-control"
                            let mutable enumerations = 0
                            let plural = seq { enumerations <- enumerations + 1; yield SetSongVolumeMessage 0.25f; yield StopSongMessage }
                            let pluralBefore = audio.Count
                            World.enqueueAudioMessages plural world
                            require "plural sequence enumerated more than once" (enumerations = 1)
                            require "plural audio observer control failed" (audio.Count = pluralBefore + 2 && snd audio[pluralBefore] = "SetSongVolume" && snd audio[pluralBefore + 1] = "StopSong")
                            let target = scvalue<Gameplay> (File.ReadAllText symbolPath)
                            require "fixed B0 summary differs" (target.GameplayTime = 149L && target.Score = 100 && target.Bricks.Count = 29 && target.Lives = 5 && target.GameplayState = Playing)
                            targetOpt <- Some target
                            let cleared = {gameplay with GameplayState = Quit}
                            clearedOpt <- Some cleared
                            startUpdates <- updates
                            startTimeUpdates <- timeUpdates
                            advancingEvents <- 0
                            order.Clear ()
                            deltas.Clear ()
                            Simulants.Gameplay.SetGameplay cleared world
                            phase <- "preseed-clear-settle"
                        | "preseed-clear-settle" ->
                            let cleared = Option.get clearedOpt
                            observeScored "preseed-cleared-observation" true gameplay world
                            require "preseed clear not halted" world.Halted
                            require "preseed clear event counts differ" (updates - startUpdates = 0 && timeUpdates - startTimeUpdates = 0)
                            require "preseed clear screen differs" (World.getSelectedScreen world = Simulants.Gameplay && World.getSelectedScreenIdling world)
                            require "preseed clear model differs" (equalModel cleared gameplay)
                            require "preseed clear scene survived" (not (scene.GetExists world))
                            Simulants.Gameplay.SetGameplay (Option.get targetOpt) world
                            phase <- "seed-settle"
                        | "seed-settle" ->
                            let target = Option.get targetOpt
                            observeScored "seed-observation" true gameplay world
                            require "B0 setter mismatch" (equalModel target gameplay)
                            require "B0 projection mismatch" ((projectionErrors true target world).Length = 0)
                            emit "seeded-B0" ["model", box (modelData target); "projection", box (projection true world); "screen", box (screenData world)]
                            phase <- "pause-trigger"
                            publishPause world
                            require "Pause event count differs" (pauseClicks = 1)
                            phase <- "pause-settle"
                        | "pause-settle" ->
                            let target = Option.get targetOpt
                            let expected = {target with GameplayState = Paused}
                            observeScored "scored-observation" true gameplay world
                            require "pause-reached" (gameplay.GameplayState = Paused)
                            require "pause retained model differs" (equalModel expected gameplay)
                            require "pause-projection" ((projectionErrors true expected world).Length = 0)
                            pausedOpt <- Some expected
                            pausedProjection <- json (projection true world)
                            emit "paused-before" ["model", box (modelData expected); "projection", box (projection true world); "screen", box (screenData world)]
                            beginRun "paused-run" world
                        | "paused-run" ->
                            let expected = Option.get pausedOpt
                            observeScored "scored-observation" true gameplay world
                            require "pause-frozen-model" (equalModel expected gameplay)
                            require "paused projection values differ" ((projectionErrors true expected world).Length = 0)
                            require "paused projection changed" (json (projection true world) = pausedProjection)
                            require "paused PlaySound request observed" (audioCount "PlaySound" "paused-run" = 0)
                            if updates - startUpdates >= 10 then
                                require "paused interval did not halt" world.Halted
                                require "paused pair counts differ" (updates - startUpdates = 10 && timeUpdates - startTimeUpdates = 10)
                                require "paused order differs" (order.ToArray () = [|for _ in 1 .. 10 do yield "TimeUpdate"; yield "Update"|])
                                require "paused GameDelta.Updates differs" (deltas.Count = 20 && (deltas |> Seq.forall (fun (_, delta) -> delta = 1L)))
                                require "paused events did not observe engine advancement" (advancingEvents = 20)
                                emit "paused-after-ten" ["model", box (modelData gameplay); "projection", box (projection true world);
                                                           "order", box (order.ToArray ()); "screen", box (screenData world)]
                                phase <- "resume-trigger"
                                publishPause world
                                require "Resume event count differs" (pauseClicks = 2)
                                phase <- "resume-settle"
                        | "resume-settle" ->
                            let target = Option.get targetOpt
                            observeScored "scored-observation" true gameplay world
                            require "resume-reached" (gameplay.GameplayState = Playing)
                            require "resume-retained" (equalModel target gameplay)
                            require "resume projection mismatch" ((projectionErrors true target world).Length = 0)
                            emit "resumed-before" ["model", box (modelData gameplay); "projection", box (projection true world)]
                            leftInputs <- 0
                            rightInputs <- 0
                            beginRun "resumed-run" world
                        | "resumed-run" when updates - startUpdates >= 1 ->
                            let expected = expectedActiveOne (Option.get targetOpt)
                            require "resumed pair did not halt" world.Halted
                            require "resumed pair counts differ" (updates - startUpdates = 1 && timeUpdates - startTimeUpdates = 1)
                            require "resumed order differs" (order.ToArray () = [|"TimeUpdate"; "Update"|])
                            require "resumed GameDelta.Updates differs" (deltas.ToArray () = [|"TimeUpdate", 1L; "Update", 1L|])
                            require "resumed events did not observe engine advancement" (advancingEvents = 2)
                            require "host direction input observed" (leftInputs = 0 && rightInputs = 0)
                            require "resumed one-step model differs" (equalModel expected gameplay)
                            require "resumed projection differs" ((projectionErrors true expected world).Length = 0)
                            emit "resumed-after-one" ["model", box (modelData gameplay); "projection", box (projection true world); "order", box (order.ToArray ())]
                            phase <- "second-pause-trigger"
                            publishPause world
                            require "second Pause event count differs" (pauseClicks = 3)
                            require "second pause did not reach Paused" ((Simulants.Gameplay.GetGameplay world).GameplayState = Paused)
                            phase <- "quit-trigger"
                            publishQuit world
                            require "Quit event count differs" (quitClicks = 1)
                            phase <- "await-title"
                            World.setAdvancing true world
                        | "await-title" when World.getSelectedScreen world = Simulants.Title && World.getSelectedScreenIdling world ->
                            World.setAdvancing false world
                            phase <- "title-halted"
                        | "title-halted" ->
                            observeScored "scored-observation" true gameplay world
                            require "Title halt not effective" world.Halted
                            require "quit-reset" (vacantShape gameplay)
                            require "scene survived Quit" (not (scene.GetExists world))
                            emit "title-after-quit" ["model", box (modelData gameplay); "screen", box (screenData world)]
                            startUpdates <- updates
                            startTimeUpdates <- timeUpdates
                            advancingEvents <- 0
                            leftInputs <- 0
                            rightInputs <- 0
                            order.Clear ()
                            deltas.Clear ()
                            phase <- "fresh-run"
                            publishPlay world
                            require "TitlePlay event count differs" (playClicks = 1)
                            World.setAdvancing true world
                        | "fresh-run" when updates - startUpdates >= 1 && World.getSelectedScreen world = Simulants.Gameplay && World.getSelectedScreenIdling world ->
                            observeScored "scored-observation" true gameplay world
                            require "fresh Gameplay halt not effective" world.Halted
                            require "fresh Gameplay pair counts differ" (updates - startUpdates = 1 && timeUpdates - startTimeUpdates = 1)
                            require "fresh Gameplay order differs" (order.ToArray () = [|"TimeUpdate"; "Update"|])
                            require "fresh Gameplay GameDelta.Updates differs" (deltas.ToArray () = [|"TimeUpdate", 1L; "Update", 1L|])
                            require "fresh Gameplay events did not observe engine advancement" (advancingEvents = 2)
                            require "fresh Gameplay host direction input observed" (leftInputs = 0 && rightInputs = 0)
                            require "fresh Gameplay invariant differs" (freshAfterOneShape gameplay)
                            require "fresh Gameplay projection differs" ((projectionErrors true gameplay world).Length = 0)
                            require "final click counts differ" (pauseClicks = 3 && quitClicks = 1 && playClicks = 1)
                            emit "fresh-gameplay" ["model", box (modelData gameplay); "projection", box (projection true world); "screen", box (screenData world)]
                            finish true "Pause, ten frozen pairs, retained resume, one no-input pair, Quit reset, and fresh play passed." world
                        | _ -> ()
                    with error ->
                        match failureGameplayOpt with
                        | Some gameplay ->
                            try observeScored "failure-observation" true gameplay world
                            with observationError ->
                                emit "failure-observation-error"
                                    ["type", box (observationError.GetType().FullName)
                                     "message", box observationError.Message]
                        | None ->
                            emit "failure-observation-unavailable" ["phase", box phase]
                        emit "exception" ["type", box (error.GetType().FullName); "message", box error.Message; "stack", box error.StackTrace]
                        finish false error.Message world
            try
                Directory.SetCurrentDirectory AppContext.BaseDirectory
                let state = {GaiaState.defaultState with ProjectDllPath = dll; ProjectEditModeOpt = Some "Gameplay"; ProjectFreshlyLoaded = true; ProjectImperativeExecution = false}
                let (actualState, targetDir, plugin) = Nu.initPlus (fun () ->
                    File.WriteAllText (Path.Combine (AppContext.BaseDirectory, Constants.Gaia.StateFilePath), scstring state)
                    Gaia.selectNuPlugin (GaiaPlugin ()))
                Constants.GameTime.DesiredFrameRate <- StaticFrameRate 60L
                emit "configuration" ["projectDll", box dll; "targetDirectory", box targetDir; "functional", box (not actualState.ProjectImperativeExecution);
                                      "plugin", box (plugin.GetType().FullName); "runtime", box (Environment.Version.ToString ()); "nuAssembly", box typeof<World>.Assembly.FullName]
                require "wrong plugin" (plugin.GetType().FullName = typeof<BreakoutPlugin>.FullName)
                Gaia.setResearchPostProcess callback
                let exitCode = Gaia.run actualState targetDir plugin
                emit "engine-exit" ["exitCode", box exitCode; "probeFinished", box done_; "probePassed", box passed]
                if passed && done_ && exitCode = 0 then 0 else 1
            with error ->
                emit "launch-exception" ["type", box (error.GetType().FullName); "message", box error.Message; "stack", box error.StackTrace]
                1
