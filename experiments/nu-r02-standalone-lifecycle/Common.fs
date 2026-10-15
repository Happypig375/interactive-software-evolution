namespace NuR02StandaloneLifecycle

open System
open System.Collections.Generic
open System.Diagnostics
open System.IO
open System.Numerics
open System.Security.Cryptography
open System.Text.Json
open Nu

module Common =

    let pin = "064f7ae92a8506689cd91aff5e6804a375d6ef3d"
    let callbackCap = 600

    let fields (pairs : (string * obj) list) = Dictionary<string, obj> (dict pairs)
    let bits (value : single) = (BitConverter.SingleToInt32Bits value).ToString "X8"
    let vector (value : Vector3) =
        fields
            ["values", box [|value.X; value.Y; value.Z|]
             "bits", box [|bits value.X; bits value.Y; bits value.Z|]]

    let vector2i (value : Vector2i) = [|value.X; value.Y|]

    let viewportData (value : Viewport) =
        fields
            ["distanceNearBits", box (bits value.DistanceNear)
             "distanceFarBits", box (bits value.DistanceFar)
             "innerMin", box (vector2i value.Inner.Min)
             "innerSize", box (vector2i value.Inner.Size)
             "boundsMin", box (vector2i value.Bounds.Min)
             "boundsSize", box (vector2i value.Bounds.Size)
             "outerMin", box (vector2i value.Outer.Min)
             "outerSize", box (vector2i value.Outer.Size)
             "displayScalar", box value.DisplayScalar
             "ssaoResolutionDivisor", box value.SsaoResolutionDivisor]

    let timeFields prefix (world : World) =
        [prefix + "UpdateTime", box world.UpdateTime
         prefix + "TickTime", box world.TickTime
         prefix + "GameTime", box (string world.GameTime)]

    let digest path =
        use stream = File.OpenRead path
        SHA256.HashData stream |> Convert.ToHexString |> fun value -> value.ToLowerInvariant ()

    type Trace (arm : string, output : string) =
        let tracePath = Path.Combine (output, "trace.jsonl")
        let writer = new StreamWriter (tracePath, false, Text.UTF8Encoding false)
        let timer = Stopwatch.StartNew ()
        let mutable sequence = 0L
        do writer.AutoFlush <- true

        member _.Path = tracePath
        member _.Sequence = sequence
        member _.Emit kind pairs =
            sequence <- sequence + 1L
            let record =
                fields
                    (["sequence", box sequence
                      "kind", box kind
                      "arm", box arm
                      "elapsedMilliseconds", box timer.ElapsedMilliseconds] @ pairs)
            writer.WriteLine (JsonSerializer.Serialize record)

        member _.Close () = writer.Dispose ()

        interface IDisposable with
            member _.Dispose () = writer.Dispose ()

    type Counters =
        { Values : Dictionary<string, int>
          Order : ResizeArray<obj> }

    let makeCounters () =
        { Values = Dictionary<string, int> (StringComparer.Ordinal)
          Order = ResizeArray<obj> () }

    type Secondary =
        { Records : ResizeArray<obj>
          SceneIds : ResizeArray<uint64>
          PrePlaySceneAbsent : ResizeArray<bool>
          PrePlayGenerations : ResizeArray<int>
          mutable Status : string
          mutable Message : string }

    let makeSecondary () =
        { Records = ResizeArray<obj> ()
          SceneIds = ResizeArray<uint64> ()
          PrePlaySceneAbsent = ResizeArray<bool> ()
          PrePlayGenerations = ResizeArray<int> ()
          Status = "pending"
          Message = "awaiting two exact initializer callbacks" }

    let secondaryData (secondary : Secondary) =
        fields
            ["status", box secondary.Status
             "message", box secondary.Message
             "records", box (secondary.Records.ToArray ())
             "sceneIds", box (secondary.SceneIds.ToArray ())
             "prePlaySceneAbsent", box (secondary.PrePlaySceneAbsent.ToArray ())
             "prePlayGenerations", box (secondary.PrePlayGenerations.ToArray ())]

    let secondaryFailure message (secondary : Secondary) =
        secondary.Status <- "failure"
        secondary.Message <- message

    let secondaryMissing message (secondary : Secondary) =
        if secondary.Status <> "failure" then
            secondary.Status <- "missing"
            secondary.Message <- message

    let count name (counters : Counters) =
        match counters.Values.TryGetValue name with
        | true, value -> value
        | false, _ -> 0

    let counterData (counters : Counters) =
        counters.Values
        |> Seq.map (fun pair -> pair.Key, pair.Value)
        |> Seq.sortBy fst
        |> Seq.map (fun (name, value) -> fields ["name", box name; "value", box value])
        |> Seq.toArray

    let selectedData (world : World) =
        match World.getSelectedScreenOpt world with
        | None -> fields ["exists", box false]
        | Some screen ->
            fields
                ["exists", box true
                 "name", box screen.Name
                 "idling", box (screen.GetIdling world)
                 "transition", box (string (screen.GetTransitionState world))]

    let selectedIs (screen : Screen) (world : World) =
        match World.getSelectedScreenOpt world with
        | Some selected -> selected = screen
        | None -> false

    let selectedIdlingIs screen world =
        selectedIs screen world && World.getSelectedScreenIdling world

    let inputData (world : World) =
        fields
            ["left", box (World.isKeyboardKeyDown KeyboardKey.Left world)
             "right", box (World.isKeyboardKeyDown KeyboardKey.Right world)
             "p", box (World.isKeyboardKeyDown KeyboardKey.P world)]

    let sampledKeysUp world =
        not (World.isKeyboardKeyDown KeyboardKey.Left world) &&
        not (World.isKeyboardKeyDown KeyboardKey.Right world) &&
        not (World.isKeyboardKeyDown KeyboardKey.P world)

    let screenExistsData (screen : Screen) (world : World) =
        fields ["exists", box (screen.GetExists world); "selected", box (screen.GetExists world && screen.GetSelected world)]

    let entityData (entity : Entity) (world : World) =
        if entity.GetExists world then
            fields
                ["exists", box true
                 "position", box (vector (entity.GetPosition world))]
        else fields ["exists", box false]

    let bodyEntityData (entity : Entity) (world : World) =
        if entity.GetExists world then
            fields
                ["exists", box true
                 "position", box (vector (entity.GetPosition world))
                 "linearVelocity", box (vector (entity.GetLinearVelocity world))]
        else fields ["exists", box false]

    let writeResult output arm status message engineExitCode engineTermination preCount postCount tracePath secondary =
        let result =
            fields
                ["pin", box pin
                 "arm", box arm
                 "status", box status
                 "message", box message
                 "engineExitCode", box engineExitCode
                 "engineTermination", box engineTermination
                 "preProcessCount", box preCount
                 "postProcessCount", box postCount
                 "callbackCap", box callbackCap
                 "secondaryInitializerDiagnostic", box secondary
                 "trace", box (fields ["path", box "trace.jsonl"; "bytes", box (FileInfo tracePath).Length; "sha256", box (digest tracePath)])]
        File.WriteAllText (Path.Combine (output, "result.json"), JsonSerializer.Serialize (result, JsonSerializerOptions (WriteIndented = true)) + Environment.NewLine)
