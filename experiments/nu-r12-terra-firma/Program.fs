namespace TerraFirma

open System
open System.IO
open System.Reflection
open System.Runtime
open System.Runtime.InteropServices
open System.Security.Cryptography
open System.Text.Json
open SDL
open Prime
open Nu

module SceneLoadProbe =

    let expectedNuSha = "e96cd61d188c689f7e39e2670b4d8582e26b9ea2dc95e1a15056891b7c99cd68"
    let expectedSceneSha = "1dff90c5679233f6b282e03bcb2f2fd7524a6e6e93a7df814a72f5260d3a421a"
    let selectedProperties =
        ["Position"; "PositionLocal"; "Rotation"; "RotationLocal"; "Scale"; "ScaleLocal";
         "Size"; "Offset"; "MountOpt"; "Static"; "Clipped"; "BodyShape"; "StaticModel";
         "MaterialProperties"; "PropagationSourceOpt"; "PropagatedDescriptorOpt"]

    type PropertyObservation =
        { Name : string; Found : bool; TypeName : string; Value : string
          ExpectedPresent : bool; ExpectedSymbol : string; ExpectedCanonical : string; Error : string }

    type EntityObservation =
        { Address : string; Parent : string; Name : string; Dispatcher : string
          Id : string; Persistent : bool; Protection : string; Children : string array
          Original : bool; Properties : PropertyObservation array }

    let shaFile path =
        use stream = File.OpenRead path
        use hash = SHA256.Create ()
        hash.ComputeHash stream |> Convert.ToHexString |> fun text -> text.ToLowerInvariant ()

    let saveJson path (value : obj) =
        let options = JsonSerializerOptions (WriteIndented = true)
        File.WriteAllText (path, JsonSerializer.Serialize (value, value.GetType (), options))

    let identities () =
        AppDomain.CurrentDomain.GetAssemblies ()
        |> Array.filter (fun assembly -> not assembly.IsDynamic && not (String.IsNullOrWhiteSpace assembly.Location))
        |> Array.map (fun assembly ->
            {| Name = assembly.GetName().Name; Version = string (assembly.GetName().Version)
               Path = assembly.Location; Sha256 = shaFile assembly.Location |})
        |> Array.sortBy (fun item -> item.Name)

    let rec originals parent (descriptors : EntityDescriptor list) =
        seq {
            for descriptor in descriptors do
                let name = EntityDescriptor.getNameOpt descriptor |> Option.defaultWith (fun () -> failwith "Unnamed original node.")
                let address = parent + "/" + name
                yield address, descriptor
                yield! originals address descriptor.EntityDescriptors }

    let observeProperty (expected : Map<string, Symbol>) (entity : Entity) world name =
        let original = Map.tryFind name expected
        let initial =
            { Name = name; Found = false; TypeName = ""; Value = ""
              ExpectedPresent = Option.isSome original
              ExpectedSymbol = original |> Option.map Symbol.toString |> Option.defaultValue ""
              ExpectedCanonical = ""; Error = "" }
        try
            match entity.TryGetProperty name world with
            | None -> initial
            | Some property ->
                let converter = SymbolicConverter (false, None, property.PropertyType)
                let stringify value = Symbol.toString (converter.ConvertTo (value, typeof<Symbol>) :?> Symbol)
                let actual = stringify property.PropertyValue
                let canonical = original |> Option.map (fun symbol -> stringify (converter.ConvertFrom symbol)) |> Option.defaultValue ""
                { initial with Found = true; TypeName = property.PropertyType.FullName; Value = actual; ExpectedCanonical = canonical }
        with error -> { initial with Error = error.ToString () }

    let rec observeEntities parent (expected : Map<string, EntityDescriptor>) (entities : Entity seq) world =
        seq {
            for entity in entities |> Seq.sortBy (fun entity -> entity.Name) do
                let address = parent + "/" + entity.Name
                let original = Map.tryFind address expected
                let properties = original |> Option.map (fun node -> node.EntityProperties) |> Option.defaultValue Map.empty
                let names = Set.union (properties |> Map.keys |> Set.ofSeq) (Set.ofList selectedProperties)
                let children = entity.GetChildren world |> Seq.sortBy (fun child -> child.Name) |> Seq.toArray
                yield
                    { Address = address; Parent = parent; Name = entity.Name
                      Dispatcher = (entity.GetDispatcher world).GetType().Name
                      Id = string (entity.GetId world); Persistent = entity.GetPersistent world
                      Protection = string (entity.GetProtection world)
                      Children = children |> Array.map (fun child -> child.Name)
                      Original = Option.isSome original
                      Properties = names |> Seq.map (observeProperty properties entity world) |> Seq.toArray }
                yield! observeEntities address expected children world }

    let [<EntryPoint; STAThread>] main args =
        let mutable output = ""
        let mutable callbacks = 0
        let mutable captures = 0
        let mutable doneRunning = false
        let mutable savedMatches = false
        let mutable engineExit : int option = None
        try
            if args.Length <> 2 || not (List.contains args[0] ["L0"; "L1"]) then failwith "Expected arm and output directory."
            output <- Path.GetFullPath args[1]
            if not (Directory.Exists output) then failwith "Observation directory must already exist."
            Directory.SetCurrentDirectory AppContext.BaseDirectory
            if shaFile (Path.Combine (AppContext.BaseDirectory, "original-Scene.nugroup")) <> expectedSceneSha then
                failwith "Wrong fixed original scene."
            if shaFile typeof<World>.Assembly.Location <> expectedNuSha then failwith "Wrong loaded Nu.dll."
            Nu.init ()
            let original : GroupDescriptor = scvalue (File.ReadAllText "original-Scene.nugroup")
            let expected = originals "Game/Gameplay/Scene" original.EntityDescriptors |> Map.ofSeq
            if expected.Count <> 197 || original.EntityDescriptors.Length <> 19 then failwith "Wrong original descriptor structure."
            let originalRows =
                expected |> Map.toArray |> Array.map (fun (address, node) ->
                    {| Address = address; Dispatcher = node.EntityDispatcherName
                       Children = node.EntityDescriptors |> List.map (EntityDescriptor.getNameOpt >> Option.get) |> List.toArray
                       Properties = node.EntityProperties |> Map.toArray |> Array.map (fun (name, value) -> {| Name = name; Symbol = Symbol.toString value |}) |})
            saveJson (Path.Combine (output, "original-expectations.json")) originalRows
            let windowConfig =
                { SdlWindowConfig.defaultConfig with
                    WindowTitle = "R12 Terra Firma observation"
                    WindowFlags = SdlWindowConfig.defaultConfig.WindowFlags ||| SDL_WindowFlags.SDL_WINDOW_HIDDEN }
            let config =
                { WorldConfig.defaultConfig with
                    Imperative = false; Accompanied = true; Advancing = false
                    SdlConfig = { SdlConfig.defaultConfig with WindowConfig = windowConfig } }
            let windowSize = Nu.Constants.Render.DisplayVirtualResolution * Globals.Render.DisplayScalar
            let windowViewport = Viewport.makeWindow1 windowSize
            let geometryViewport = Viewport.makeGeometry windowViewport.Bounds.Size
            saveJson (Path.Combine (output, "startup.json"))
                {| Arm = args[0]; Runtime = RuntimeInformation.FrameworkDescription
                   OS = RuntimeInformation.OSDescription; ServerGC = GCSettings.IsServerGC
                   RequestedImperative = false; RequestedAccompanied = true; RequestedAdvancing = false
                   RequestedWindowFlags = string windowConfig.WindowFlags
                   DisplayScalar = Globals.Render.DisplayScalar
                   InputSceneSha256 = shaFile "Assets/Gameplay/Scene.nugroup"
                   OriginalSceneSha256 = expectedSceneSha; LoadedAssemblies = identities () |}
            let pre world =
                callbacks <- callbacks + 1
                if callbacks = 1 then Game.SetGameState Gameplay world
            let capture label (world : World) =
                let entities = observeEntities "Game/Gameplay/Scene" expected (World.getEntitiesSovereign Simulants.GameplayScene world) world |> Seq.toArray
                let descriptor = World.writeGroup GroupDescriptor.empty Simulants.GameplayScene world
                File.WriteAllText (Path.Combine (output, label + ".nugroup"), scstring descriptor)
                saveJson (Path.Combine (output, label + ".json"))
                    {| Label = label; Callback = callbacks; Imperative = world.Imperative
                       Accompanied = world.Accompanied; Advancing = world.Advancing; Halted = world.Halted
                       UpdateTime = string world.UpdateTime; GameState = string (Game.GetGameState world)
                       GameplaySelected = Simulants.Gameplay.GetSelected world
                       WindowFlags = string (World.tryGetWindowFlags world)
                       WindowSize = string (World.getWindowSize world)
                       WindowViewport = string (World.getWindowViewport world)
                       GeometryViewport = string (World.getGeometryViewport world)
                       Entities = entities; LoadedAssemblies = identities () |}
                descriptor
            let post (world : World) =
                saveJson (Path.Combine (output, sprintf "phase-%03i.json" callbacks))
                    {| Callback = callbacks; SceneExists = Simulants.GameplayScene.GetExists world
                       GameplayExists = Simulants.Gameplay.GetExists world
                       GameState = string (Game.GetGameState world) |}
                if captures = 0 && Simulants.GameplayScene.GetExists world then
                    capture "A" world |> ignore
                    captures <- 1
                elif captures = 1 then
                    let descriptor = capture "B" world
                    captures <- 2
                    let savedPath = Path.Combine (output, "saved-Scene.nugroup")
                    World.writeGroupToFile savedPath Simulants.GameplayScene world
                    let parsed : GroupDescriptor = scvalue (File.ReadAllText savedPath)
                    File.WriteAllText (Path.Combine (output, "saved-canonical.nugroup"), scstring parsed)
                    savedMatches <- scstring descriptor = scstring parsed
                    doneRunning <- true
                    World.exit world
            let exitCode =
                World.runPlus (fun () -> None) (fun _ -> callbacks < 120 && not doneRunning)
                    pre ignore post ignore ignore config windowViewport.Outer.Size geometryViewport windowViewport (TerraFirmaPlugin ())
            engineExit <- Some exitCode
            let complete = exitCode = 0 && captures = 2 && doneRunning
            saveJson (Path.Combine (output, "summary.json"))
                {| Arm = args[0]; Complete = complete; CallbackCount = callbacks; CaptureCount = captures
                   EngineExitCode = exitCode; SavedDescriptorMatchesB = savedMatches
                   LoadedAssemblies = identities (); ServerGC = GCSettings.IsServerGC |}
            if complete then 0 else 2
        with error ->
            if output <> "" && Directory.Exists output then
                saveJson (Path.Combine (output, "exception.json"))
                    {| Error = error.ToString (); CallbackCount = callbacks; CaptureCount = captures
                       EngineExit = string engineExit |}
            Console.Error.WriteLine (error.ToString ())
            2
