namespace NuR10SchemaReload

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

    let fieldNames (raw : obj) =
        FSharpType.GetRecordFields (raw.GetType ()) |> Array.map (fun field -> field.Name)

    let tryRecordField name (value : obj) =
        let infos = FSharpType.GetRecordFields (value.GetType ())
        let values = FSharpValue.GetRecordFields value
        match Array.tryFindIndex (fun (info : PropertyInfo) -> info.Name = name) infos with
        | Some index -> Some values[index]
        | None -> None

    // Complete seven-field comparison surface. Brick geometry and colors are retained bitwise.
    let sevenFieldSummary (raw : obj) =
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

    let typedSummary (g : Gameplay) = sevenFieldSummary (box g)
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

    // Frozen before reload from typed checkpoint data plus the declared single removal.
    let predictedPostProjection (gameplay : Gameplay) (world : World) =
        let raw = box gameplay
        let brickNames = recordField "Bricks" raw |> mapEntries |> Array.map fst
        let spriteFrom name value =
            let entity = scene / name
            fields ["name", box name; "exists", box true
                    "position", box (recordField "Position" value :?> Vector3 |> vector)
                    "size", box (recordField "Size" value :?> Vector3 |> vector)
                    "color", box (entity.GetColor world |> colorBits)]
        let paddle, ball = recordField "Paddle" raw, recordField "Ball" raw
        let time = recordField "GameplayTime" raw :?> int64
        let lives = recordField "Lives" raw :?> int
        let score = recordField "Score" raw :?> int
        let bricks = recordField "Bricks" raw |> mapEntries
        let expectedMessage = if lives <= 0 then "Game over!" elif bricks.Length = 0 then "You win!" else ""
        fields
            ["names", box (World.getEntities scene world |> Seq.map (fun entity -> entity.Name) |> Seq.filter ((<>) "@455") |> Seq.sort |> Seq.toArray)
             "paddle", box (spriteFrom "Paddle" paddle)
             "ball", box (spriteFrom "Ball" ball)
             "bricks", box [|for name, brick in bricks do yield spriteFrom name brick|]
             "scoreText", box ("Score: " + string score)
             "messageText", box expectedMessage
             "rotation", box (Quaternion.CreateFromAxisAngle ((v3 1.0f 0.75f 0.5f).Normalized, single (time % 360L) |> degToRadF) |> quaternion)]

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

    let rewardOfRaw (raw : obj) = recordField "BrickReward" raw :?> int

    let setRecordIntField name value (raw : obj) =
        let ty = raw.GetType ()
        let fields = FSharpType.GetRecordFields ty
        let values = FSharpValue.GetRecordFields raw
        match Array.tryFindIndex (fun (field : PropertyInfo) -> field.Name = name) fields with
        | Some index ->
            values[index] <- box value
            FSharpValue.MakeRecord (ty, values)
        | None -> invalidOp ("Missing record field " + name + " on " + ty.FullName)

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

    let oldSchema = [|"GameplayTime"; "GameplayState"; "Paddle"; "Ball"; "Bricks"; "Score"; "Lives"|]
    let newSchema = Array.append oldSchema [|"BrickReward"|]
    let isGameplayRecord (ty : Type) =
        try ty.Name = "Gameplay" && FSharpType.IsRecord ty && (FSharpType.GetRecordFields ty |> Array.map (fun p -> p.Name) = newSchema)
        with _ -> false

    let atomicWrite (path : string) (text : string) =
        let tmp = path + ".tmp"
        File.WriteAllText (tmp, text)
        File.Move (tmp, path)

    [<EntryPoint; STAThread>]
    let main args =
        if args.Length <> 5 || not (List.contains args[0] ["live"; "fresh"]) then
            eprintfn "Usage: SchemaReload <live|fresh> <Breakout DLL> <B0 seed symbol> <checkpoint dir> <new output dir>"
            2
        else
            let mode = args[0]
            let dll = Path.GetFullPath args[1]
            let seedPath = Path.GetFullPath args[2]
            let checkpoint = Path.GetFullPath args[3]
            let output = Path.GetFullPath args[4]
            if Directory.Exists output then invalidOp "Output directory must be new."
            if mode = "live" && Directory.Exists checkpoint && not (Directory.EnumerateFileSystemEntries checkpoint |> Seq.isEmpty) then
                invalidOp "Live checkpoint directory must be new or empty."
            Directory.CreateDirectory output |> ignore
            Directory.CreateDirectory checkpoint |> ignore
            let trace = Path.Combine (output, "trace.jsonl")
            let emit label values =
                File.AppendAllText (trace, json (fields (("event", box label) :: values)) + Environment.NewLine)
            let mutable updates, timeUpdates, callbacks = 0, 0, 0
            let mutable leftInputs, rightInputs, codeReloadEvents = 0, 0, 0
            let mutable phase = "initialize"
            let mutable checkpointSymbol = ""
            let mutable checkpointSevenJson = ""
            let mutable checkpointProjection = ""
            let expectedModels = Dictionary<int, string> ()
            let expectedProjections = Dictionary<int, string> ()
            let mutable startCounts, stableCounts = (0, 0), (0, 0)
            let order, deltas = ResizeArray<string> (), ResizeArray<int64> ()
            let mutable targetOpt : Gameplay option = None
            let mutable done_, processPassed = false, false
            let mutable requiredRewardInstalled = false
            let mutable mappingRequirementPass = false
            let mutable preservationPass = false
            let mutable continuationAttempted = false
            let mutable continuationPass = false
            let mutable freshInitializationPass = false
            let mutable freshInitialReward = -1
            let mutable observedReward = -1
            let mutable rewardInRange = false
            let raw world = Simulants.Gameplay.GetModelGeneric<obj> world
            let rewardValue raw =
                match tryRecordField "BrickReward" raw with
                | Some value -> Some (value :?> int)
                | None -> None
            let observe label (world : World) =
                let value = raw world
                let reward = rewardValue value
                emit label
                    ["phase", box phase; "updates", box updates; "timeUpdates", box timeUpdates; "callbacks", box callbacks
                     "leftInputs", box leftInputs; "rightInputs", box rightInputs; "codeReloadEvents", box codeReloadEvents
                     "functional", box (not world.Imperative); "accompanied", box world.Accompanied; "advancing", box world.Advancing
                     "rawType", box (value.GetType().FullName); "rawAssembly", box (assemblyInfo (value.GetType().Assembly))
                     "fieldNames", box (fieldNames value); "rewardFieldPresent", box reward.IsSome
                     "reward", (match reward with Some scalar -> box scalar | None -> null)
                     "symbol", box (rawSymbol value); "model", box (sevenFieldSummary value)
                     "projection", box (projectionRaw value world); "projectionErrors", box (projectionErrorsRaw value world)]
            let matchedRequirementPass () =
                if mode = "live" then mappingRequirementPass && preservationPass && continuationPass
                else freshInitializationPass && preservationPass && continuationPass && observedReward = 200
            let finish success detail world =
                done_ <- true
                processPassed <- success
                emit "result"
                    ["processPass", box success; "detail", box detail; "phase", box phase
                     "mode", box mode; "mappingRequirementPass", box mappingRequirementPass
                     "requiredRewardInstalled", box requiredRewardInstalled
                     "preservationPass", box preservationPass; "continuationAttempted", box continuationAttempted
                     "continuationPass", box continuationPass; "freshInitializationApplicable", box (mode = "fresh")
                     "freshInitializationPass", box freshInitializationPass; "freshInitialReward", box freshInitialReward
                     "observedReward", box observedReward; "rewardInRange", box rewardInRange
                     "matchedRequirementPass", box (matchedRequirementPass ()); "updates", box updates
                     "timeUpdates", box timeUpdates; "leftInputs", box leftInputs; "rightInputs", box rightInputs]
                World.setAdvancing false world
                World.exit world
            let resume world =
                startCounts <- updates, timeUpdates
                order.Clear ()
                deltas.Clear ()
                continuationAttempted <- true
                phase <- "continuation"
                emit "resume-request" ["updates", box updates; "timeUpdates", box timeUpdates; "observedReward", box observedReward]
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
                            require "initial world is not halted" world.Halted
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
                                if phase = "continuation" then
                                    order.Add "TimeUpdate"
                                    deltas.Add w.GameDelta.Updates
                                Cascade) Simulants.Gameplay.TimeUpdateEvent Game world |> ignore
                            World.subscribe (fun _ _ ->
                                codeReloadEvents <- codeReloadEvents + 1
                                Cascade) Nu.Game.Handle.CodeReloadEvent Nu.Game.Handle world |> ignore
                            if mode = "fresh" then
                                let initialRaw = raw world
                                require "fresh initial schema differs" (fieldNames initialRaw = newSchema)
                                freshInitialReward <- rewardOfRaw initialRaw
                                freshInitializationPass <- freshInitialReward = 200
                                observe "fresh-initial-model" world
                            let sourceSymbol =
                                if mode = "live" then File.ReadAllText seedPath
                                else File.ReadAllText (Path.Combine (checkpoint, "gameplay.symbol"))
                            let seed = scvalue<Gameplay> sourceSymbol
                            require "seed summary changed" (seed.GameplayTime = 149L && seed.Score = 100 && seed.Lives = 5 && seed.Bricks.Count = 29 && seed.Bricks.ContainsKey "@455")
                            let positioned =
                                if mode = "live" then
                                    {seed with Ball = {seed.Ball with Position = v3 -64.0f 53.0f 0.0f; Size = v3 8.0f 8.0f 0.0f; Speed = 3.0f; Direction = v3 0.0f 1.0f 0.0f}}
                                else seed
                            let target =
                                if mode = "fresh" then setRecordIntField "BrickReward" 200 (box positioned) :?> Gameplay
                                else positioned
                            targetOpt <- Some target
                            Simulants.Gameplay.SetGameplay target world
                            phase <- "seed-halted"
                        | "seed-halted" ->
                            require "seed reconstruction advanced" (updates = 0 && timeUpdates = 0 && world.Halted)
                            let target = Option.get targetOpt
                            let value = raw world
                            let actualFields = fieldNames value
                            if mode = "live" then
                                require "V0 schema differs" (actualFields = oldSchema)
                                require "V0 unexpectedly exposes BrickReward" ((rewardValue value).IsNone)
                            else
                                require "fresh reconstructed schema differs" (actualFields = newSchema)
                                observedReward <- rewardOfRaw value
                                requiredRewardInstalled <- observedReward = 200
                                require "fresh reconstruction reward differs" (observedReward = 200)
                            checkpointSymbol <- rawSymbol value
                            checkpointSevenJson <- json (sevenFieldSummary value)
                            checkpointProjection <- json (projectionRaw value world)
                            require "checkpoint projection errors" ((projectionErrorsRaw value world).Length = 0)
                            let postBase =
                                {target with GameplayTime = 150L; Score = 100
                                             Ball = {target.Ball with Position = v3 -64.0f 56.0f 0.0f; Direction = v3 0.0f -1.0f 0.0f}
                                             Bricks = Map.remove "@455" target.Bricks}
                            for reward in 0 .. 1000 do
                                let expected = {postBase with Score = 100 + reward}
                                expectedModels.Add (reward, json (typedSummary expected))
                                expectedProjections.Add (reward, json (predictedPostProjection expected world))
                            let requiredExpected = {postBase with Score = 300}
                            let resetControl = json (typedSummary {target with GameplayTime = 0L; Score = 0})
                            let alteredOldField = json (typedSummary {target with Lives = 4})
                            let wrongBrick = json (typedSummary {requiredExpected with Bricks = Map.remove "@456" target.Bricks})
                            let wrongScore = json (typedSummary {requiredExpected with Score = 299})
                            require "reset control accepted" (resetControl <> expectedModels[200])
                            require "altered-old-field control accepted" (alteredOldField <> checkpointSevenJson)
                            require "wrong-brick control accepted" (wrongBrick <> expectedModels[200])
                            require "wrong-score control accepted" (wrongScore <> expectedModels[200])
                            require "zero-versus-200 control accepted" (expectedModels[0] <> expectedModels[200] && expectedProjections[0] <> expectedProjections[200])
                            emit "oracle-data-controls"
                                ["resetRejected", box true; "alteredOldFieldRejected", box true
                                 "wrongBrickRejected", box true; "wrongScoreRejected", box true
                                 "zeroVersus200Rejected", box true; "rewardCasesPrecomputed", box expectedModels.Count]
                            emit "precomputed-oracle"
                                ["checkpointModelJson", box checkpointSevenJson
                                 "checkpointProjectionJson", box checkpointProjection
                                 "expectedModelZeroJson", box expectedModels[0]
                                 "expectedModel200Json", box expectedModels[200]
                                 "expectedProjectionZeroJson", box expectedProjections[0]
                                 "expectedProjection200Json", box expectedProjections[200]
                                 "rewardCasesPrecomputed", box expectedModels.Count]
                            if mode = "live" then
                                File.WriteAllText (Path.Combine (checkpoint, "gameplay.symbol"), checkpointSymbol)
                                File.WriteAllText (Path.Combine (checkpoint, "model-seven.json"), checkpointSevenJson)
                                File.WriteAllText (Path.Combine (checkpoint, "projection.json"), checkpointProjection)
                            else
                                preservationPass <-
                                    checkpointSevenJson = File.ReadAllText (Path.Combine (checkpoint, "model-seven.json")) &&
                                    checkpointProjection = File.ReadAllText (Path.Combine (checkpoint, "projection.json"))
                            observe "checkpoint-halted" world
                            if mode = "live" then
                                let dispatcher = Simulants.Gameplay.GetDispatcher world
                                let ready =
                                    json (fields
                                        ["symbolSha256", box (checkpointSymbol |> Text.Encoding.UTF8.GetBytes |> shaBytes)
                                         "modelSevenSha256", box (checkpointSevenJson |> Text.Encoding.UTF8.GetBytes |> shaBytes)
                                         "projectionSha256", box (checkpointProjection |> Text.Encoding.UTF8.GetBytes |> shaBytes)
                                         "oldRawType", box (value.GetType().FullName); "oldAssembly", box (assemblyInfo (value.GetType().Assembly))
                                         "oldDispatcherType", box (dispatcher.GetType().FullName); "oldDispatcherAssembly", box (assemblyInfo (dispatcher.GetType().Assembly))
                                         "fieldNames", box actualFields; "brickRewardPresent", box false])
                                atomicWrite (Path.Combine (output, "ready.json")) ready
                                phase <- "wait-edit"
                            elif not freshInitializationPass then
                                finish true "Fresh initial BrickReward was not 200; continuation withheld." world
                            elif not preservationPass then
                                finish true "Fresh seven-field reconstruction or projection differed; continuation withheld." world
                            else
                                rewardInRange <- true
                                resume world
                        | "wait-edit" when File.Exists (Path.Combine (output, "go.signal")) ->
                            require "world advanced while waiting" (updates = 0 && timeUpdates = 0 && world.Halted)
                            let before = raw world
                            require "pre-reload schema differs" (fieldNames before = oldSchema && (rewardValue before).IsNone)
                            require "pre-reload checkpoint drift" (json (sevenFieldSummary before) = checkpointSevenJson && json (projectionRaw before world) = checkpointProjection)
                            let oldDispatcher = Simulants.Gameplay.GetDispatcher world
                            emit "reload-start"
                                ["oldRawType", box (before.GetType().FullName); "oldRawAssembly", box (assemblyInfo (before.GetType().Assembly))
                                 "oldDispatcherType", box (oldDispatcher.GetType().FullName); "oldDispatcherAssembly", box (assemblyInfo (oldDispatcher.GetType().Assembly))
                                 "fieldNames", box (fieldNames before); "brickRewardPresent", box false]
                            let script, assemblies = Gaia.researchReloadCode world
                            File.WriteAllText (Path.Combine (output, "generated-reload.fsx"), script)
                            emit "fsi-assemblies" ["scriptSha256", box (script |> Text.Encoding.UTF8.GetBytes |> shaBytes); "assemblies", box (assemblies |> Array.map assemblyInfo)]
                            require "reload advanced gameplay" (updates = 0 && timeUpdates = 0 && world.Halted)
                            require "generated script missing" (not (String.IsNullOrWhiteSpace script))
                            require "CodeReloadEvent count differs" (codeReloadEvents = 1)
                            let candidates = assemblies |> Array.collect (fun assembly -> assembly.GetTypes ()) |> Array.filter isGameplayRecord
                            require "FSI Gameplay candidate count differs" (candidates.Length = 1)
                            let actualType = candidates[0]
                            let after = raw world
                            let dispatcher = Simulants.Gameplay.GetDispatcher world
                            let modelType = dispatcherModelType (dispatcher.GetType ())
                            require "raw model is not actual returned FSI type" (Object.ReferenceEquals (after.GetType (), actualType))
                            require "dispatcher generic model differs" (modelType = Some actualType)
                            require "raw model assembly not returned" (assemblies |> Array.exists (fun assembly -> Object.ReferenceEquals (assembly, after.GetType().Assembly)))
                            require "dispatcher assembly not returned" (assemblies |> Array.exists (fun assembly -> Object.ReferenceEquals (assembly, dispatcher.GetType().Assembly)))
                            observedReward <- rewardOfRaw after
                            requiredRewardInstalled <- observedReward = 200
                            rewardInRange <- observedReward >= 0 && observedReward <= 1000
                            preservationPass <-
                                json (sevenFieldSummary after) = checkpointSevenJson &&
                                json (projectionRaw after world) = checkpointProjection &&
                                (projectionErrorsRaw after world).Length = 0 &&
                                updates = 0 && timeUpdates = 0 && leftInputs = 0 && rightInputs = 0
                            mappingRequirementPass <- requiredRewardInstalled && preservationPass
                            emit "reload-installed"
                                ["actualType", box actualType.FullName; "actualAssembly", box (assemblyInfo actualType.Assembly)
                                 "dispatcherType", box (dispatcher.GetType().FullName); "dispatcherAssembly", box (assemblyInfo (dispatcher.GetType().Assembly))
                                 "dispatcherModelType", box ((Option.get modelType).FullName); "fieldNames", box (fieldNames after)
                                 "observedReward", box observedReward; "requiredRewardInstalled", box requiredRewardInstalled
                                 "mappingRequirementPass", box mappingRequirementPass
                                 "preservationPass", box preservationPass; "rewardInRange", box rewardInRange]
                            observe "post-reload-pre-advance" world
                            if not preservationPass then
                                finish true "Live conversion was observed but seven-field state or projection preservation failed; continuation withheld." world
                            elif not rewardInRange then
                                finish true "Live conversion reward was outside 0 through 1000; continuation withheld." world
                            else resume world
                        | "continuation" ->
                            let deltaUpdates = updates - fst startCounts
                            let deltaTimeUpdates = timeUpdates - snd startCounts
                            require "more than one update" (deltaUpdates <= 1 && deltaTimeUpdates <= 1)
                            if deltaUpdates = 1 && deltaTimeUpdates = 1 && world.Halted then
                                emit "event-schedule"
                                    ["updates", box deltaUpdates; "timeUpdates", box deltaTimeUpdates
                                     "order", box (order.ToArray ()); "gameDeltaUpdates", box (deltas.ToArray ())
                                     "leftInputs", box leftInputs; "rightInputs", box rightInputs]
                                require "event word differs" (order.ToArray () = [|"TimeUpdate"; "Update"|])
                                require "GameDelta.Updates differs" (deltas.ToArray () = [|1L|])
                                require "sampled held input occurred" (leftInputs = 0 && rightInputs = 0)
                                let value = raw world
                                require "reward changed during continuation" (rewardOfRaw value = observedReward)
                                require "complete post-update model differs from frozen oracle" (json (sevenFieldSummary value) = expectedModels[observedReward])
                                require "complete post-update projection differs from frozen oracle" (json (projectionRaw value world) = expectedProjections[observedReward])
                                require "post-update projection errors" ((projectionErrorsRaw value world).Length = 0)
                                continuationPass <- true
                                observe "post-update-halted" world
                                stableCounts <- updates, timeUpdates
                                checkpointSymbol <- rawSymbol value
                                checkpointSevenJson <- json (sevenFieldSummary value)
                                checkpointProjection <- json (projectionRaw value world)
                                phase <- "next-halted"
                        | "next-halted" ->
                            require "event after final halt" ((updates, timeUpdates) = stableCounts && world.Halted)
                            let value = raw world
                            require "model drift at next halt" (rawSymbol value = checkpointSymbol && json (sevenFieldSummary value) = checkpointSevenJson)
                            require "projection drift at next halt" (json (projectionRaw value world) = checkpointProjection)
                            require "reward drift at next halt" (rewardOfRaw value = observedReward)
                            observe "next-halted-stable" world
                            finish true (if matchedRequirementPass () then "Required initializer mapping and continuation passed." else "Observation completed with a failed application requirement.") world
                        | _ -> ()
                    with ex ->
                        emit "exception" ["type", box (ex.GetType().FullName); "message", box ex.Message; "stack", box ex.StackTrace]
                        finish false ex.Message world
            try
                Directory.SetCurrentDirectory AppContext.BaseDirectory
                let state =
                    {GaiaState.defaultState with ProjectDllPath = dll; ProjectEditModeOpt = Some "Gameplay"
                                                 ProjectFreshlyLoaded = true; ProjectImperativeExecution = false}
                let actualState, targetDir, plugin =
                    Nu.initPlus (fun () ->
                        File.WriteAllText (Path.Combine (AppContext.BaseDirectory, Constants.Gaia.StateFilePath), scstring state)
                        Gaia.selectNuPlugin (GaiaPlugin ()))
                Constants.GameTime.DesiredFrameRate <- StaticFrameRate 60L
                let identities =
                    [|typeof<World>.Assembly; typeof<GaiaState>.Assembly; typeof<Gameplay>.Assembly
                      typeof<Prime.Symbol>.Assembly; typeof<FSharp.Compiler.Interactive.Shell.FsiEvaluationSession>.Assembly|]
                    |> Array.distinct
                    |> Array.map assemblyInfo
                emit "configuration"
                    ["mode", box mode; "projectDll", box dll; "targetDir", box targetDir
                     "currentDirectory", box (Directory.GetCurrentDirectory ()); "runtime", box RuntimeInformation.FrameworkDescription
                     "os", box RuntimeInformation.OSDescription; "architecture", box (string RuntimeInformation.ProcessArchitecture)
                     "plugin", box (plugin.GetType().FullName); "assemblies", box identities]
                require "wrong initial plugin" (plugin.GetType().Name = "BreakoutPlugin")
                Gaia.setResearchPostProcess callback
                let exitCode = Gaia.run actualState targetDir plugin
                emit "engine-exit" ["exitCode", box exitCode; "done", box done_; "processPassed", box processPassed]
                if exitCode = 0 && done_ && processPassed then 0 else 1
            with ex ->
                emit "launch-exception" ["type", box (ex.GetType().FullName); "message", box ex.Message; "stack", box ex.StackTrace]
                1
