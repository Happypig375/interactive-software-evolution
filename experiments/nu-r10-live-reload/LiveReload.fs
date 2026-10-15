namespace NuR10LiveReload

open System
open System.IO
open System.Numerics
open System.Reflection
open System.Runtime.InteropServices
open System.Security.Cryptography
open System.Collections
open System.Collections.Generic
open System.Text.Json
open Microsoft.FSharp.Reflection
open Prime
open Nu
open Nu.Gaia
open Breakout

module Program =
    let fields pairs = Dictionary<string, obj> (dict pairs)
    let json value = JsonSerializer.Serialize value
    let require message condition = if not condition then invalidOp message
    let bits (value : single) = (BitConverter.SingleToInt32Bits value).ToString "X8"
    let vector (value : Vector3) = [|bits value.X; bits value.Y; bits value.Z|]
    let quaternion (value : Quaternion) = [|bits value.X; bits value.Y; bits value.Z; bits value.W|]
    let colorBits (value : Color) = [|bits value.R; bits value.G; bits value.B; bits value.A|]
    let shaBytes (bytes : byte array) = (Convert.ToHexString (SHA256.HashData bytes)).ToLowerInvariant ()
    let shaFile path = File.ReadAllBytes path |> shaBytes

    let recordField name (value : obj) =
        let infos = FSharpType.GetRecordFields (value.GetType ())
        let values = FSharpValue.GetRecordFields value
        match Array.tryFindIndex (fun (info : PropertyInfo) -> info.Name = name) infos with
        | Some index -> values[index]
        | None -> invalidOp ("Missing record field " + name + " on " + value.GetType().FullName)

    let mapEntries (value : obj) =
        [|for entry in value :?> IEnumerable do
            let ty = entry.GetType ()
            let key = ty.GetProperty("Key").GetValue(entry) :?> string
            yield key, ty.GetProperty("Value").GetValue(entry)|]

    let rawSummary (raw : obj) =
        let paddle = recordField "Paddle" raw
        let ball = recordField "Ball" raw
        let bricks = recordField "Bricks" raw |> mapEntries
        fields
            ["time", recordField "GameplayTime" raw
             "state", box (string (recordField "GameplayState" raw))
             "paddlePosition", box (recordField "Position" paddle :?> Vector3 |> vector)
             "paddleSize", box (recordField "Size" paddle :?> Vector3 |> vector)
             "ballPosition", box (recordField "Position" ball :?> Vector3 |> vector)
             "ballSize", box (recordField "Size" ball :?> Vector3 |> vector)
             "ballSpeed", box (recordField "Speed" ball :?> single |> bits)
             "ballDirection", box (recordField "Direction" ball :?> Vector3 |> vector)
             "bricks", box [|for name, brick in bricks do
                                  yield fields ["name", box name
                                                "position", box (recordField "Position" brick :?> Vector3 |> vector)
                                                "size", box (recordField "Size" brick :?> Vector3 |> vector)
                                                "color", box (recordField "Color" brick :?> Color |> colorBits)]|]
             "score", recordField "Score" raw
             "lives", recordField "Lives" raw]

    let typedSummary (g : Gameplay) = rawSummary (box g)
    let rawSymbol (raw : obj) = scstring raw
    let scene = Simulants.GameplayScene

    let projectionRaw (raw : obj) (world : World) =
        let brickNames = recordField "Bricks" raw |> mapEntries |> Array.map fst
        let sprite name =
            let entity = scene / name
            if entity.GetExists world then
                fields ["name", box name; "exists", box true
                        "position", box (entity.GetPosition world |> vector)
                        "size", box (entity.GetSize world |> vector)
                        "color", box (entity.GetColor world |> colorBits)]
            else fields ["name", box name; "exists", box false]
        fields
            ["names", box (World.getEntities scene world |> Seq.map (fun e -> e.Name) |> Seq.sort |> Seq.toArray)
             "paddle", box (sprite "Paddle"); "ball", box (sprite "Ball")
             "bricks", box (brickNames |> Array.map sprite)
             "scoreText", box ((scene / "Score").GetText world)
             "messageText", box ((scene / "Message").GetText world)
             "rotation", box ((scene / "StaticModel").GetRotation world |> quaternion)]

    let projectionErrorsRaw (raw : obj) (world : World) =
        let failures = ResizeArray<string> ()
        let check label ok = if not ok then failures.Add label
        let checkSprite name position size =
            let entity = scene / name
            check (name + ":exists") (entity.GetExists world)
            if entity.GetExists world then
                check (name + ":position") (vector (entity.GetPosition world) = vector position)
                check (name + ":size") (vector (entity.GetSize world) = vector size)
        let paddle, ball = recordField "Paddle" raw, recordField "Ball" raw
        checkSprite "Paddle" (recordField "Position" paddle :?> Vector3) (recordField "Size" paddle :?> Vector3)
        checkSprite "Ball" (recordField "Position" ball :?> Vector3) (recordField "Size" ball :?> Vector3)
        for name, brick in recordField "Bricks" raw |> mapEntries do
            checkSprite name (recordField "Position" brick :?> Vector3) (recordField "Size" brick :?> Vector3)
            if (scene / name).GetExists world then
                check (name + ":color") (colorBits ((scene / name).GetColor world) = colorBits (recordField "Color" brick :?> Color))
        let score, lives = recordField "Score" raw :?> int, recordField "Lives" raw :?> int
        check "score" ((scene / "Score").GetText world = "Score: " + string score)
        let brickCount = recordField "Bricks" raw |> mapEntries |> Array.length
        let expectedMessage = if lives <= 0 then "Game over!" elif brickCount = 0 then "You win!" else ""
        check "message" ((scene / "Message").GetText world = expectedMessage)
        let actualLives = World.getEntities scene world |> Seq.map (fun e -> e.Name) |> Seq.filter (fun n -> n.StartsWith "Life+") |> Set.ofSeq
        check "life-icons" (actualLives = Set.ofList [for i in 0 .. lives - 1 -> "Life+" + string i])
        let time = recordField "GameplayTime" raw :?> int64
        let expectedRotation = Quaternion.CreateFromAxisAngle ((v3 1.0f 0.75f 0.5f).Normalized, single (time % 360L) |> degToRadF)
        check "model-rotation" (quaternion ((scene / "StaticModel").GetRotation world) = quaternion expectedRotation)
        failures.ToArray ()

    let rewardOf (ty : Type) =
        let property = ty.GetProperty ("BrickReward", BindingFlags.Public ||| BindingFlags.Static)
        require ("Missing public static BrickReward on " + string ty.FullName) (not (isNull property))
        property.GetValue null :?> int

    let assemblyInfo (assembly : Assembly) =
        let location = try assembly.Location with _ -> ""
        fields ["fullName", box assembly.FullName; "mvid", box (assembly.ManifestModule.ModuleVersionId.ToString "D")
                "dynamic", box assembly.IsDynamic; "location", box location
                "sha256", box (if String.IsNullOrWhiteSpace location || not (File.Exists location) then "" else shaFile location)]

    let rec dispatcherModelType (ty : Type) =
        if isNull ty then None
        elif ty.IsGenericType && ty.GetGenericTypeDefinition().Name.StartsWith("ScreenDispatcher`", StringComparison.Ordinal) then
            Some (ty.GetGenericArguments()[0])
        else dispatcherModelType ty.BaseType

    let schema = [|"GameplayTime"; "GameplayState"; "Paddle"; "Ball"; "Bricks"; "Score"; "Lives"|]
    let isGameplayRecord (ty : Type) =
        try ty.Name = "Gameplay" && FSharpType.IsRecord ty && (FSharpType.GetRecordFields ty |> Array.map (fun p -> p.Name) = schema) && rewardOf ty = 200
        with _ -> false

    let atomicWrite (path : string) (text : string) =
        let tmp = path + ".tmp"
        File.WriteAllText (tmp, text)
        File.Move (tmp, path)

    [<EntryPoint; STAThread>]
    let main args =
        if args.Length <> 5 || not (List.contains args[0] ["live"; "fresh"]) then
            eprintfn "Usage: LiveReload <live|fresh> <Breakout DLL> <B0 seed symbol> <checkpoint dir> <new output dir>"
            2
        else
            let mode, dll, seedPath, checkpoint, output = args[0], Path.GetFullPath args[1], Path.GetFullPath args[2], Path.GetFullPath args[3], Path.GetFullPath args[4]
            if Directory.Exists output then invalidOp "Output directory must be new."
            if mode = "live" && Directory.Exists checkpoint && not (Directory.EnumerateFileSystemEntries checkpoint |> Seq.isEmpty) then invalidOp "Live checkpoint directory must be new or empty."
            Directory.CreateDirectory output |> ignore
            Directory.CreateDirectory checkpoint |> ignore
            let trace = Path.Combine (output, "trace.jsonl")
            let emit label values = File.AppendAllText (trace, json (fields (("event", box label) :: values)) + Environment.NewLine)
            let mutable updates, timeUpdates, callbacks = 0, 0, 0
            let mutable leftInputs, rightInputs, codeReloadEvents = 0, 0, 0
            let mutable phase = "initialize"
            let mutable checkpointSymbol, checkpointProjection, expectedPostJson = "", "", ""
            let mutable startCounts, stableCounts = (0, 0), (0, 0)
            let order, deltas = ResizeArray<string> (), ResizeArray<int64> ()
            let mutable done_, passed = false, false
            let raw world = Simulants.Gameplay.GetModelGeneric<obj> world
            let observe label (world : World) =
                let value = raw world
                emit label ["phase", box phase; "updates", box updates; "timeUpdates", box timeUpdates; "callbacks", box callbacks
                            "leftInputs", box leftInputs; "rightInputs", box rightInputs; "codeReloadEvents", box codeReloadEvents
                            "functional", box (not world.Imperative); "accompanied", box world.Accompanied; "advancing", box world.Advancing
                            "rawType", box (value.GetType().FullName); "rawAssembly", box (assemblyInfo (value.GetType().Assembly))
                            "symbol", box (rawSymbol value); "model", box (rawSummary value)
                            "projection", box (projectionRaw value world); "projectionErrors", box (projectionErrorsRaw value world)]
            let finish success detail world =
                done_ <- true; passed <- success
                emit "result" ["pass", box success; "detail", box detail; "phase", box phase; "updates", box updates
                               "timeUpdates", box timeUpdates; "leftInputs", box leftInputs; "rightInputs", box rightInputs]
                World.setAdvancing false world
                World.exit world
            let resume world =
                startCounts <- updates, timeUpdates
                order.Clear (); deltas.Clear ()
                phase <- "continuation"
                emit "resume-request" ["updates", box updates; "timeUpdates", box timeUpdates]
                World.setAdvancing true world
            let callback (world : World) =
                if not done_ then
                    try
                        callbacks <- callbacks + 1
                        require "monotonic callback watchdog" (callbacks <= 3600)
                        require "wrong execution mode" (not world.Imperative && world.Accompanied)
                        require "wrong static clock" (Constants.GameTime.DesiredFrameRate = StaticFrameRate 60L)
                        require "selected screen changed" (World.getSelectedScreen world = Simulants.Gameplay && World.getSelectedScreenIdling world)
                        require "input occurred" (leftInputs = 0 && rightInputs = 0)
                        match phase with
                        | "initialize" ->
                            require "initial world is advancing" world.Halted
                            World.subscribe (fun _ w ->
                                updates <- updates + 1
                                if World.isKeyboardKeyDown KeyboardKey.Left w then leftInputs <- leftInputs + 1
                                if World.isKeyboardKeyDown KeyboardKey.Right w then rightInputs <- rightInputs + 1
                                if phase = "continuation" then
                                    order.Add "Update"
                                    if updates - fst startCounts = 1 then World.setAdvancing false w
                                Cascade) Simulants.Gameplay.UpdateEvent Game world |> ignore
                            World.subscribe (fun _ w ->
                                timeUpdates <- timeUpdates + 1
                                if phase = "continuation" then order.Add "TimeUpdate"; deltas.Add w.GameDelta.Updates
                                Cascade) Simulants.Gameplay.TimeUpdateEvent Game world |> ignore
                            World.subscribe (fun _ _ -> codeReloadEvents <- codeReloadEvents + 1; Cascade) Nu.Game.Handle.CodeReloadEvent Nu.Game.Handle world |> ignore
                            let target =
                                if mode = "live" then
                                    let seed = scvalue<Gameplay> (File.ReadAllText seedPath)
                                    require "seed summary changed" (seed.GameplayTime = 149L && seed.Score = 100 && seed.Lives = 5 && seed.Bricks.Count = 29 && seed.Bricks.ContainsKey "@455")
                                    {seed with Ball = {seed.Ball with Position = v3 -64.0f 53.0f 0.0f; Size = v3 8.0f 8.0f 0.0f; Speed = 3.0f; Direction = v3 0.0f 1.0f 0.0f}}
                                else scvalue<Gameplay> (File.ReadAllText (Path.Combine (checkpoint, "gameplay.symbol")))
                            let expected =
                                {target with GameplayTime = 150L; Score = 300
                                             Ball = {target.Ball with Position = v3 -64.0f 56.0f 0.0f; Direction = v3 0.0f -1.0f 0.0f}
                                             Bricks = Map.remove "@455" target.Bricks}
                            expectedPostJson <- json (typedSummary expected)
                            let oldScore = json (typedSummary {expected with Score = 200})
                            let resetLike = json (typedSummary {target with GameplayTime = 0L; Score = 0})
                            let wrongBrick = json (typedSummary {expected with Bricks = target.Bricks |> Map.remove "@456"})
                            require "score-100 negative control accepted" (oldScore <> expectedPostJson)
                            require "reset negative control accepted" (resetLike <> expectedPostJson)
                            require "wrong-brick negative control accepted" (wrongBrick <> expectedPostJson)
                            emit "oracle-data-controls" ["score100Rejected", box true; "resetRejected", box true; "wrongBrickRejected", box true]
                            Simulants.Gameplay.SetGameplay target world
                            phase <- "seed-halted"
                        | "seed-halted" ->
                            require "seed reconstruction advanced" (updates = 0 && timeUpdates = 0 && world.Halted)
                            let value = raw world
                            require "checkpoint reward differs" (rewardOf (value.GetType()) = (if mode = "live" then 100 else 200))
                            checkpointSymbol <- rawSymbol value
                            checkpointProjection <- json (projectionRaw value world)
                            require "checkpoint projection errors" ((projectionErrorsRaw value world).Length = 0)
                            if mode = "live" then
                                File.WriteAllText (Path.Combine (checkpoint, "gameplay.symbol"), checkpointSymbol)
                                File.WriteAllText (Path.Combine (checkpoint, "projection.json"), checkpointProjection)
                                File.WriteAllText (Path.Combine (checkpoint, "expected-post.json"), expectedPostJson)
                            else
                                require "fresh checkpoint symbol mismatch" (checkpointSymbol = File.ReadAllText (Path.Combine (checkpoint, "gameplay.symbol")))
                                require "fresh checkpoint projection mismatch" (checkpointProjection = File.ReadAllText (Path.Combine (checkpoint, "projection.json")))
                                require "fresh expected oracle mismatch" (expectedPostJson = File.ReadAllText (Path.Combine (checkpoint, "expected-post.json")))
                            observe "checkpoint-halted" world
                            if mode = "live" then
                                let ready = json (fields ["symbolSha256", box (checkpointSymbol |> Text.Encoding.UTF8.GetBytes |> shaBytes)
                                                          "projectionSha256", box (checkpointProjection |> Text.Encoding.UTF8.GetBytes |> shaBytes)
                                                          "oldRawType", box (value.GetType().FullName); "oldAssembly", box (assemblyInfo (value.GetType().Assembly))
                                                          "oldDispatcher", box ((Simulants.Gameplay.GetDispatcher world).GetType().FullName)
                                                          "oldReward", box (rewardOf (value.GetType()))])
                                atomicWrite (Path.Combine (output, "ready.json")) ready
                                phase <- "wait-edit"
                            else resume world
                        | "wait-edit" when File.Exists (Path.Combine (output, "go.signal")) ->
                            require "world advanced while waiting" (updates = 0 && timeUpdates = 0 && world.Halted)
                            let before = raw world
                            require "pre-reload checkpoint drift" (rawSymbol before = checkpointSymbol && json (projectionRaw before world) = checkpointProjection)
                            let oldDispatcher = Simulants.Gameplay.GetDispatcher world
                            emit "reload-start" ["oldRawType", box (before.GetType().FullName); "oldRawAssembly", box (assemblyInfo (before.GetType().Assembly))
                                                 "oldDispatcherType", box (oldDispatcher.GetType().FullName); "oldDispatcherAssembly", box (assemblyInfo (oldDispatcher.GetType().Assembly))
                                                 "oldReward", box (rewardOf (before.GetType()))]
                            let script, assemblies = Gaia.researchReloadCode world
                            File.WriteAllText (Path.Combine (output, "generated-reload.fsx"), script)
                            emit "fsi-assemblies" ["scriptSha256", box (script |> Text.Encoding.UTF8.GetBytes |> shaBytes)
                                                   "assemblies", box (assemblies |> Array.map assemblyInfo)]
                            require "reload advanced gameplay" (updates = 0 && timeUpdates = 0 && world.Halted)
                            require "generated script missing" (not (String.IsNullOrWhiteSpace script))
                            let candidates = assemblies |> Array.collect (fun a -> a.GetTypes ()) |> Array.filter isGameplayRecord
                            require "FSI Gameplay candidate count differs" (candidates.Length = 1)
                            let actualType = candidates[0]
                            let after = raw world
                            let dispatcher = Simulants.Gameplay.GetDispatcher world
                            let modelType = dispatcherModelType (dispatcher.GetType ())
                            require "raw model is not actual returned FSI type" (Object.ReferenceEquals (after.GetType (), actualType))
                            require "dispatcher generic model differs" (modelType = Some actualType)
                            require "raw model assembly not returned" (assemblies |> Array.exists (fun a -> Object.ReferenceEquals (a, after.GetType().Assembly)))
                            require "dispatcher assembly not returned" (assemblies |> Array.exists (fun a -> Object.ReferenceEquals (a, dispatcher.GetType().Assembly)))
                            require "new reward differs" (rewardOf actualType = 200)
                            require "model changed during reload" (rawSymbol after = checkpointSymbol)
                            require "projection changed during reload" (json (projectionRaw after world) = checkpointProjection)
                            require "post-reload projection errors" ((projectionErrorsRaw after world).Length = 0)
                            emit "reload-installed" ["actualType", box actualType.FullName; "actualAssembly", box (assemblyInfo actualType.Assembly)
                                                     "dispatcherType", box (dispatcher.GetType().FullName); "dispatcherAssembly", box (assemblyInfo (dispatcher.GetType().Assembly))
                                                     "dispatcherModelType", box ((Option.get modelType).FullName); "reward", box (rewardOf actualType)]
                            observe "post-reload-pre-advance" world
                            resume world
                        | "continuation" ->
                            let du, dt = updates - fst startCounts, timeUpdates - snd startCounts
                            require "more than one update" (du <= 1 && dt <= 1)
                            if du = 1 && dt = 1 && world.Halted then
                                emit "event-schedule" ["updates", box du; "timeUpdates", box dt
                                                       "order", box (order.ToArray ()); "gameDeltaUpdates", box (deltas.ToArray ())]
                                require "event word differs" (order.ToArray () = [|"TimeUpdate"; "Update"|])
                                require "GameDelta.Updates differs" (deltas.ToArray () = [|1L|])
                                let value = raw world
                                require "post-update model differs" (json (rawSummary value) = expectedPostJson)
                                require "post-update projection errors" ((projectionErrorsRaw value world).Length = 0)
                                observe "post-update-halted" world
                                stableCounts <- updates, timeUpdates
                                checkpointSymbol <- rawSymbol value
                                checkpointProjection <- json (projectionRaw value world)
                                phase <- "next-halted"
                        | "next-halted" ->
                            require "event after final halt" ((updates, timeUpdates) = stableCounts && world.Halted)
                            let value = raw world
                            require "model drift at next halt" (rawSymbol value = checkpointSymbol)
                            require "projection drift at next halt" (json (projectionRaw value world) = checkpointProjection)
                            observe "next-halted-stable" world
                            finish true (if mode = "live" then "Live reload retained state and installed reward 200 for the declared hit." else "Fresh reward-200 reconstruction matched the declared hit.") world
                        | _ -> ()
                    with ex ->
                        emit "exception" ["type", box (ex.GetType().FullName); "message", box ex.Message; "stack", box ex.StackTrace]
                        finish false ex.Message world
            try
                Directory.SetCurrentDirectory AppContext.BaseDirectory
                let state = {GaiaState.defaultState with ProjectDllPath = dll; ProjectEditModeOpt = Some "Gameplay"; ProjectFreshlyLoaded = true; ProjectImperativeExecution = false}
                let actualState, targetDir, plugin = Nu.initPlus (fun () ->
                    File.WriteAllText (Path.Combine (AppContext.BaseDirectory, Constants.Gaia.StateFilePath), scstring state)
                    Gaia.selectNuPlugin (GaiaPlugin ()))
                Constants.GameTime.DesiredFrameRate <- StaticFrameRate 60L
                let identities = [|typeof<World>.Assembly; typeof<GaiaState>.Assembly; typeof<Gameplay>.Assembly; typeof<Prime.Symbol>.Assembly; typeof<FSharp.Compiler.Interactive.Shell.FsiEvaluationSession>.Assembly|] |> Array.distinct |> Array.map assemblyInfo
                emit "configuration" ["mode", box mode; "projectDll", box dll; "targetDir", box targetDir
                                      "currentDirectory", box (Directory.GetCurrentDirectory ()); "runtime", box RuntimeInformation.FrameworkDescription
                                      "os", box RuntimeInformation.OSDescription; "architecture", box (string RuntimeInformation.ProcessArchitecture)
                                      "plugin", box (plugin.GetType().FullName); "assemblies", box identities]
                require "wrong initial plugin" (plugin.GetType().Name = "BreakoutPlugin")
                Gaia.setResearchPostProcess callback
                let exitCode = Gaia.run actualState targetDir plugin
                emit "engine-exit" ["exitCode", box exitCode; "done", box done_; "passed", box passed]
                if exitCode = 0 && done_ && passed then 0 else 1
            with ex ->
                emit "launch-exception" ["type", box (ex.GetType().FullName); "message", box ex.Message; "stack", box ex.StackTrace]
                1
