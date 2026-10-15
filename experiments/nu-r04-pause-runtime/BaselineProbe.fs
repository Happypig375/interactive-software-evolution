namespace NuR04PauseRuntime

open System
open System.IO
open Prime
open Nu
open Nu.Gaia
open Breakout
open Common

module BaselineProbe =

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
            let mutable advancingEvents = 0
            let order = ResizeArray<string> ()
            let deltas = ResizeArray<string * int64> ()
            let audio = ResizeArray<string * string> ()
            let mutable done_, passed = false, false
            let fixtures = ResizeArray<string * Gameplay * Gameplay> ()
            let mutable fixtureIndex = -1
            let mutable expectedCurrent : Gameplay option = None
            let mutable clearedOpt : Gameplay option = None
            let finish success detail (world : World) =
                done_ <- true
                passed <- success
                emit "result" ["pass", box success; "detail", box detail; "phase", box phase;
                               "updates", box updates; "timeUpdates", box timeUpdates; "callbacks", box callbacks]
                World.setAudioMessageObserver None
                World.setAdvancing false world
                World.exit world
            let audioCount kind phaseName = audio |> Seq.filter (fun (p, k) -> p = phaseName && k = kind) |> Seq.length
            let verifyControls world =
                require "projected values differ" ((projectionErrors false (Simulants.Gameplay.GetGameplay world) world).Length = 0)
            let beginFixture world =
                fixtureIndex <- fixtureIndex + 1
                if fixtureIndex = fixtures.Count then finish true "Four baseline fixtures satisfied the declared one-pair observations." world
                else
                    let (name, initial, expected) = fixtures[fixtureIndex]
                    expectedCurrent <- Some expected
                    Simulants.Gameplay.SetGameplay initial world
                    phase <- "fixture-settle:" + name
            let callback (world : World) =
                if not done_ then
                    try
                        callbacks <- callbacks + 1
                        require "callback watchdog" (callbacks <= 200)
                        require "wrong execution mode" (not world.Imperative && world.Accompanied)
                        require "wrong static clock" (Constants.GameTime.DesiredFrameRate = StaticFrameRate 60L)
                        match phase with
                        | "initialize" ->
                            require "initial world not halted" world.Halted
                            require "Gameplay not selected/idling" (World.getSelectedScreen world = Simulants.Gameplay && World.getSelectedScreenIdling world)
                            World.subscribe (fun _ w ->
                                updates <- updates + 1
                                if phase.StartsWith "fixture-run:" then
                                    order.Add "Update"
                                    deltas.Add ("Update", w.GameDelta.Updates)
                                    if w.Advancing then advancingEvents <- advancingEvents + 1
                                    if updates - startUpdates = 1 then World.setAdvancing false w
                                Cascade) Simulants.Gameplay.UpdateEvent Game world |> ignore
                            World.subscribe (fun _ w ->
                                timeUpdates <- timeUpdates + 1
                                if phase.StartsWith "fixture-run:" then
                                    order.Add "TimeUpdate"
                                    deltas.Add ("TimeUpdate", w.GameDelta.Updates)
                                    if w.Advancing then advancingEvents <- advancingEvents + 1
                                Cascade) Simulants.Gameplay.TimeUpdateEvent Game world |> ignore
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
                            fixtures.Add ("active", target, expectedActiveOne target)
                            let lives0 = {target with Lives = 0}
                            fixtures.Add ("lives0", lives0, {lives0 with GameplayTime = lives0.GameplayTime + 1L})
                            let emptyBricks = {target with Bricks = Map.empty}
                            fixtures.Add ("empty-bricks", emptyBricks, {emptyBricks with GameplayTime = emptyBricks.GameplayTime + 1L})
                            let quit = {target with GameplayState = Quit}
                            fixtures.Add ("quit", quit, {quit with GameplayTime = quit.GameplayTime + 1L})
                            let initial = Simulants.Gameplay.GetGameplay world
                            let cleared = {initial with GameplayState = Quit}
                            clearedOpt <- Some cleared
                            startUpdates <- updates
                            startTimeUpdates <- timeUpdates
                            order.Clear ()
                            deltas.Clear ()
                            Simulants.Gameplay.SetGameplay cleared world
                            phase <- "preseed-clear-settle"
                        | "preseed-clear-settle" ->
                            let cleared = Option.get clearedOpt
                            let actual = Simulants.Gameplay.GetGameplay world
                            emit "preseed-cleared-observation"
                                ["phase", box phase; "callbacks", box callbacks; "updates", box updates; "timeUpdates", box timeUpdates;
                                 "intervalUpdates", box (updates - startUpdates); "intervalTimeUpdates", box (timeUpdates - startTimeUpdates);
                                 "order", box (order.ToArray ()); "deltas", box (deltas.ToArray ());
                                 "worldAdvancing", box world.Advancing; "worldHalted", box world.Halted;
                                 "model", box (modelData actual); "projection", box (projection false world); "projectionErrors", box (projectionErrors false actual world);
                                 "screen", box (screenData world)]
                            require "preseed clear not halted" world.Halted
                            require "preseed clear event counts differ" (updates - startUpdates = 0 && timeUpdates - startTimeUpdates = 0)
                            require "preseed clear screen differs" (World.getSelectedScreen world = Simulants.Gameplay && World.getSelectedScreenIdling world)
                            require "preseed clear model differs" (equalModel cleared actual)
                            require "preseed clear scene survived" (not (scene.GetExists world))
                            beginFixture world
                        | value when value.StartsWith "fixture-settle:" ->
                            let (_, initial, _) = fixtures[fixtureIndex]
                            require "fixture setter mismatch" (equalModel initial (Simulants.Gameplay.GetGameplay world))
                            verifyControls world
                            emit "fixture-before" ["fixture", box value; "model", box (modelData initial); "projection", box (projection false world); "screen", box (screenData world)]
                            startUpdates <- updates
                            startTimeUpdates <- timeUpdates
                            advancingEvents <- 0
                            order.Clear ()
                            deltas.Clear ()
                            phase <- value.Replace ("fixture-settle:", "fixture-run:")
                            World.setAdvancing true world
                        | value when value.StartsWith "fixture-run:" && updates - startUpdates >= 1 ->
                            let expected = Option.get expectedCurrent
                            require "fixture did not halt" world.Halted
                            require "fixture event counts differ" (updates - startUpdates = 1 && timeUpdates - startTimeUpdates = 1)
                            require "fixture event order differs" (order.ToArray () = [|"TimeUpdate"; "Update"|])
                            require "fixture GameDelta.Updates differs" (deltas.ToArray () = [|"TimeUpdate", 1L; "Update", 1L|])
                            require "events did not observe engine advancement" (advancingEvents = 2)
                            require "fixture model differs" (equalModel expected (Simulants.Gameplay.GetGameplay world))
                            verifyControls world
                            require "unexpected gameplay sound request" (audioCount "PlaySound" value = 0)
                            emit "fixture-after" ["fixture", box value; "model", box (modelData expected); "projection", box (projection false world);
                                                   "order", box (order.ToArray ()); "deltas", box (deltas.ToArray ()); "screen", box (screenData world)]
                            beginFixture world
                        | _ -> ()
                    with error ->
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
