module R12PropagationProbe

open System
open System.IO
open System.Reflection
open System.Runtime.InteropServices
open System.Security.Cryptography
open System.Text.Json
open Prime
open Nu

let expectedNuSha256 = "e96cd61d188c689f7e39e2670b4d8582e26b9ea2dc95e1a15056891b7c99cd68"

type ProbePlugin () =
    inherit NuPlugin ()

type RelevantNode =
    { Name : string
      Dispatcher : string
      Text : string
      Children : RelevantNode array }

type ActualNode =
    { Exists : bool
      Name : string
      Dispatcher : string
      Text : string
      Persistent : bool
      Protection : string
      Id : string
      Children : ActualNode array }

type AssemblyIdentity =
    { Name : string
      Version : string
      InformationalVersion : string
      Location : string
      Sha256 : string }

type Check =
    { Name : string
      Passed : bool }

let jsonOptions = JsonSerializerOptions (WriteIndented = false)

let emit (value : obj) =
    Console.Out.WriteLine (JsonSerializer.Serialize (value, value.GetType (), jsonOptions))
    Console.Out.Flush ()

let sha256File path =
    use stream = File.OpenRead path
    use sha256 = SHA256.Create ()
    sha256.ComputeHash stream
    |> Array.map (fun value -> value.ToString "x2")
    |> String.concat ""

let assemblyIdentity (assembly : Assembly) =
    let informational = assembly.GetCustomAttribute<AssemblyInformationalVersionAttribute> ()
    let location = assembly.Location
    { Name = assembly.GetName().Name
      Version = string (assembly.GetName().Version)
      InformationalVersion = if isNull informational then "" else informational.InformationalVersion
      Location = location
      Sha256 = if String.IsNullOrWhiteSpace location || not (File.Exists location) then "" else sha256File location }

let loadedAssemblyIdentities () =
    AppDomain.CurrentDomain.GetAssemblies ()
    |> Array.filter (fun assembly -> not assembly.IsDynamic && not (String.IsNullOrWhiteSpace assembly.Location))
    |> Array.map assemblyIdentity
    |> Array.sortBy (fun identity -> identity.Name, identity.Location)

let rec actualNode (entity : Entity) world : ActualNode =
    if not (entity.GetExists world) then
        { Exists = false
          Name = entity.Name
          Dispatcher = ""
          Text = ""
          Persistent = false
          Protection = ""
          Id = ""
          Children = [||] }
    else
        let children =
            entity.GetChildren world
            |> Seq.sortBy (fun child -> child.Name)
            |> Seq.map (fun child -> actualNode child world)
            |> Seq.toArray
        { Exists = true
          Name = entity.Name
          Dispatcher = (entity.GetDispatcher world).GetType().Name
          Text = entity.GetText world
          Persistent = entity.GetPersistent world
          Protection = string (entity.GetProtection world)
          Id = string (entity.GetId world)
          Children = children }

let rec relevantActual (node : ActualNode) : RelevantNode =
    { Name = node.Name
      Dispatcher = node.Dispatcher
      Text = node.Text
      Children = Array.map relevantActual node.Children }

let descriptorText (descriptor : EntityDescriptor) =
    match Map.tryFind "Text" descriptor.EntityProperties with
    | Some symbol -> symbolToValue<string> symbol
    | None -> ""

let rec relevantDescriptor (descriptor : EntityDescriptor) : RelevantNode =
    { Name = EntityDescriptor.getNameOpt descriptor |> Option.defaultValue ""
      Dispatcher = descriptor.EntityDispatcherName
      Text = descriptorText descriptor
      Children =
        descriptor.EntityDescriptors
        |> List.map relevantDescriptor
        |> List.sortBy (fun node -> node.Name)
        |> List.toArray }

let allPersistentUnprotected (root : ActualNode) =
    let rec loop node =
        node.Exists && node.Persistent && node.Protection = string Unprotected && Array.forall loop node.Children
    loop root

let childNames (root : ActualNode) = root.Children |> Array.map (fun child -> child.Name)

let check name passed : Check = { Name = name; Passed = passed }

let expectedNode name dispatcher text children : RelevantNode =
    { Name = name; Dispatcher = dispatcher; Text = text; Children = children }

let expectedSourceV0 =
    expectedNode "Source" "ButtonDispatcher" "Family v0"
        [| expectedNode "EqualValue" "TextDispatcher" "Equal v0" [||]
           expectedNode "LocalDeleted" "TextDispatcher" "Local v0" [||]
           expectedNode "Shared" "TextDispatcher" "Shared v0" [||]
           expectedNode "SourceDeleted" "TextDispatcher" "Deleted v0" [||] |]

let expectedTargetV0 = { expectedSourceV0 with Name = "Target" }

let expectedSourcePreAndPost =
    expectedNode "Source" "ButtonDispatcher" "Family v1"
        [| expectedNode "Added" "TextDispatcher" "Added v1" [||]
           expectedNode "EqualValue" "TextDispatcher" "Equal v1" [||]
           expectedNode "LocalDeleted" "TextDispatcher" "Local v0" [||]
           expectedNode "Shared" "TextDispatcher" "Shared v1" [||] |]

let expectedTargetPre =
    expectedNode "Target" "ButtonDispatcher" "Target override"
        [| expectedNode "EqualValue" "TextDispatcher" "Equal v0" [||]
           expectedNode "Shared" "TextDispatcher" "Shared v0" [||]
           expectedNode "SourceDeleted" "TextDispatcher" "Local edited deletion" [||]
           expectedNode "TargetOnly" "TextDispatcher" "Target only" [||] |]

let expectedTargetPost =
    expectedNode "Target" "ButtonDispatcher" "Target override"
        [| expectedNode "Added" "TextDispatcher" "Added v1" [||]
           expectedNode "EqualValue" "TextDispatcher" "Equal v1" [||]
           expectedNode "Shared" "TextDispatcher" "Shared v1" [||]
           expectedNode "TargetOnly" "TextDispatcher" "Target only" [||] |]

let sameLink expected (actual : Entity option) = actual = Some expected

let propagationSourceOpt (entity : Entity) world =
    if entity.GetExists world then entity.GetPropagationSourceOpt world else None

let hasPropagationTargets (entity : Entity) world =
    entity.GetExists world && entity.HasPropagationTargets world

let propagatedDescriptorOpt (entity : Entity) world =
    if entity.GetExists world then entity.GetPropagatedDescriptorOpt world else None

let descriptorComplete (entity : Entity) world =
    if entity.GetExists world
    then scstring (World.writeEntity true true EntityDescriptor.empty entity world)
    else ""

let createTextChild parentName childName text group world =
    let child =
        World.createEntity<TextDispatcher>
            (Some Address.parent) DefaultOverlay (Some [|parentName; childName|]) group world
    child.SetPersistent true world
    child.SetProtection Unprotected world
    child.SetText text world
    child

[<EntryPoint>]
let main _ =
    let mutable phase = "assembly_precondition"
    let mutable disposition = "invalid_or_incomplete"
    let mutable exitCode = 2
    let mutable worldOpt : World option = None
    let mutable wrapperCalls = 0
    let mutable wrapperCompleted = false
    let mutable cleanupAttempted = false
    let mutable cleanupPassed = false
    let mutable cleanupError = ""

    try
        try
            let nuIdentity = assemblyIdentity typeof<World>.Assembly
            emit
                {| event = "runtime"
                   phase = phase
                   framework = RuntimeInformation.FrameworkDescription
                   runtimeVersion = string Environment.Version
                   processArchitecture = string RuntimeInformation.ProcessArchitecture
                   os = RuntimeInformation.OSDescription
                   baseDirectory = Path.GetFullPath AppContext.BaseDirectory
                   expectedNuSha256 = expectedNuSha256
                   loadedNu = nuIdentity |}

            if not (String.Equals (nuIdentity.Sha256, expectedNuSha256, StringComparison.OrdinalIgnoreCase)) then
                emit {| event = "invalid_precondition"; phase = phase; reason = "loaded_nu_hash_mismatch"; loadedNu = nuIdentity |}
            else
                phase <- "world_initialization"
                Nu.init ()
                let config =
                    { WorldConfig.defaultConfig with
                        Imperative = false
                        Accompanied = true
                        Advancing = false }
                let world = World.makeStub (fun _ -> None) config (ProbePlugin ())
                worldOpt <- Some world
                let screen = World.createScreen<ScreenDispatcher> (Some "R12") world
                let group = World.createGroup<GroupDispatcher> (Some "Scene") screen world
                let effectiveFunctional = world.Functional
                let effectiveAccompanied = world.Accompanied
                let effectiveHalted = world.Halted

                phase <- "fixture_bootstrap"
                let source =
                    World.createEntity<ButtonDispatcher>
                        (Some Address.parent) DefaultOverlay (Some [|"Source"|]) group world
                source.SetPersistent true world
                source.SetProtection Unprotected world
                source.SetText "Family v0" world
                let _ = createTextChild "Source" "Shared" "Shared v0" group world
                let _ = createTextChild "Source" "EqualValue" "Equal v0" group world
                let _ = createTextChild "Source" "LocalDeleted" "Local v0" group world
                let _ = createTextChild "Source" "SourceDeleted" "Deleted v0" group world

                let sourceBaselineDescriptor = World.writeEntity false false EntityDescriptor.empty source world
                let target = World.readEntity false false sourceBaselineDescriptor (Some "Target") (group :> Simulant) world
                target.SetPropagationSourceOpt (Some source) world

                let sourceBootstrap = actualNode source world
                let targetBootstrap = actualNode target world
                let savedBootstrapOpt = propagatedDescriptorOpt source world
                let savedBootstrapRelevant = Option.map relevantDescriptor savedBootstrapOpt
                let bootstrapChecks =
                    [| check "effective_functional" effectiveFunctional
                       check "effective_accompanied" effectiveAccompanied
                       check "effective_halted" effectiveHalted
                       check "source_exists" sourceBootstrap.Exists
                       check "target_exists" targetBootstrap.Exists
                       check "source_tree_v0" (relevantActual sourceBootstrap = expectedSourceV0)
                       check "target_tree_v0" (relevantActual targetBootstrap = expectedTargetV0)
                       check "source_persistent_unprotected" (allPersistentUnprotected sourceBootstrap)
                       check "target_persistent_unprotected" (allPersistentUnprotected targetBootstrap)
                       check "target_linked" (sameLink source (propagationSourceOpt target world))
                       check "source_has_target" (hasPropagationTargets source world)
                       check "saved_descriptor_present" (Option.isSome savedBootstrapOpt)
                       check "saved_descriptor_v0" (savedBootstrapRelevant = Some expectedSourceV0) |]
                emit
                    {| event = "bootstrap"
                       phase = phase
                       checks = bootstrapChecks
                       source = sourceBootstrap
                       target = targetBootstrap
                       effectiveWorld = {| functional = effectiveFunctional; accompanied = effectiveAccompanied; halted = effectiveHalted |}
                       targetRootIdDescriptive = targetBootstrap.Id
                       sourceDescriptorComplete = scstring sourceBaselineDescriptor
                       targetDescriptorComplete = descriptorComplete target world
                       savedSourceDescriptorComplete = savedBootstrapOpt |> Option.map scstring |> Option.defaultValue "" |}

                phase <- "declared_revision"
                target.SetText "Target override" world
                let targetEqualValue : Entity = target / "EqualValue"
                targetEqualValue.SetText "Temporary" world
                let equalTemporaryObserved = targetEqualValue.GetText world = "Temporary"
                targetEqualValue.SetText "Equal v0" world
                let equalReturnedObserved = targetEqualValue.GetText world = "Equal v0"
                let targetSourceDeleted : Entity = target / "SourceDeleted"
                targetSourceDeleted.SetText "Local edited deletion" world
                let localEditObservedBeforeSourceDeletion = targetSourceDeleted.GetText world = "Local edited deletion"
                World.destroyEntityImmediate (target / "LocalDeleted") world
                let _ = createTextChild "Target" "TargetOnly" "Target only" group world

                source.SetText "Family v1" world
                (source / "Shared").SetText "Shared v1" world
                (source / "EqualValue").SetText "Equal v1" world
                World.destroyEntityImmediate (source / "SourceDeleted") world
                let _ = createTextChild "Source" "Added" "Added v1" group world

                phase <- "pre_wrapper_validation"
                let sourcePre = actualNode source world
                let targetPre = actualNode target world
                let savedPreOpt = propagatedDescriptorOpt source world
                let savedPreRelevant = Option.map relevantDescriptor savedPreOpt
                let preChecks =
                    Array.concat
                        [ bootstrapChecks
                          [| check "equal_temporary_observed" equalTemporaryObserved
                             check "equal_returned_to_v0" equalReturnedObserved
                             check "local_edit_observed_before_source_deletion" localEditObservedBeforeSourceDeletion
                             check "effective_functional_pre" world.Functional
                             check "effective_accompanied_pre" world.Accompanied
                             check "effective_halted_pre" world.Halted
                             check "source_tree_declared_revision" (relevantActual sourcePre = expectedSourcePreAndPost)
                             check "target_tree_declared_revision" (relevantActual targetPre = expectedTargetPre)
                             check "source_persistent_unprotected_pre" (allPersistentUnprotected sourcePre)
                             check "target_persistent_unprotected_pre" (allPersistentUnprotected targetPre)
                             check "target_linked_pre" (sameLink source (propagationSourceOpt target world))
                             check "source_has_target_pre" (hasPropagationTargets source world)
                             check "saved_previous_source_still_v0" (savedPreRelevant = Some expectedSourceV0) |] ]
                let preconditionsValid = Array.forall (fun check -> check.Passed) preChecks
                emit
                    {| event = "pre_wrapper"
                       phase = phase
                       valid = preconditionsValid
                       checks = preChecks
                       wrapperCalls = wrapperCalls
                       source = sourcePre
                       target = targetPre
                       effectiveWorld = {| functional = world.Functional; accompanied = world.Accompanied; halted = world.Halted |}
                       targetRootIdDescriptive = targetPre.Id
                       sourceDescriptorComplete = descriptorComplete source world
                       targetDescriptorComplete = descriptorComplete target world
                       savedPreviousSourceDescriptorComplete = savedPreOpt |> Option.map scstring |> Option.defaultValue ""
                       loadedAssemblies = loadedAssemblyIdentities () |}

                if not preconditionsValid then
                    emit {| event = "invalid_precondition"; phase = phase; reason = "fixture_or_saved_descriptor_mismatch"; checks = preChecks |}
                else
                    phase <- "public_wrapper"
                    wrapperCalls <- wrapperCalls + 1
                    World.propagateEntityStructure source world
                    wrapperCompleted <- true

                    phase <- "post_wrapper_observation"
                    let sourcePost = actualNode source world
                    let targetPost = actualNode target world
                    let sourceDescriptorPostComplete = descriptorComplete source world
                    let targetDescriptorPostComplete = descriptorComplete target world
                    let savedPostOpt = propagatedDescriptorOpt source world
                    let savedPostRelevant = Option.map relevantDescriptor savedPostOpt
                    let postChecks =
                        [| check "wrapper_called_exactly_once" (wrapperCalls = 1)
                           check "wrapper_completed" wrapperCompleted
                           check "source_exists_post" sourcePost.Exists
                           check "target_exists_post" targetPost.Exists
                           check "source_tree_v1" (relevantActual sourcePost = expectedSourcePreAndPost)
                           check "target_tree_required" (relevantActual targetPost = expectedTargetPost)
                           check "source_exact_children" (childNames sourcePost = [|"Added"; "EqualValue"; "LocalDeleted"; "Shared"|])
                           check "target_exact_children" (childNames targetPost = [|"Added"; "EqualValue"; "Shared"; "TargetOnly"|])
                           check "source_persistent_unprotected_post" (allPersistentUnprotected sourcePost)
                           check "target_persistent_unprotected_post" (allPersistentUnprotected targetPost)
                           check "target_linked_post" (sameLink source (propagationSourceOpt target world))
                           check "source_has_target_post" (hasPropagationTargets source world)
                           check "saved_descriptor_present_post" (Option.isSome savedPostOpt)
                           check "saved_descriptor_advanced_to_v1" (savedPostRelevant = Some expectedSourcePreAndPost) |]
                    let passed = Array.forall (fun check -> check.Passed) postChecks
                    disposition <- if passed then "completed_pass" else "completed_adverse"
                    exitCode <- if passed then 0 else 1
                    emit
                        {| event = "post_wrapper"
                           phase = phase
                           disposition = disposition
                           passed = passed
                           checks = postChecks
                           wrapperCalls = wrapperCalls
                           source = sourcePost
                           target = targetPost
                           targetRootIdBeforeDescriptive = targetPre.Id
                           targetRootIdAfterDescriptive = targetPost.Id
                           sourceDescriptorComplete = sourceDescriptorPostComplete
                           targetDescriptorComplete = targetDescriptorPostComplete
                           savedCurrentSourceDescriptorComplete = savedPostOpt |> Option.map scstring |> Option.defaultValue "" |}
        with ex ->
            disposition <- "invalid_or_incomplete"
            exitCode <- 2
            emit
                {| event = "failure"
                   phase = phase
                   disposition = disposition
                   wrapperCalls = wrapperCalls
                   wrapperCompleted = wrapperCompleted
                   exceptionType = ex.GetType().FullName
                   message = ex.Message
                   stackTrace = if isNull ex.StackTrace then "" else ex.StackTrace |}
    finally
        match worldOpt with
        | Some world ->
            cleanupAttempted <- true
            try
                World.cleanUp world
                cleanupPassed <- true
            with ex ->
                cleanupError <- ex.GetType().FullName + ": " + ex.Message
                disposition <- "invalid_or_incomplete"
                exitCode <- 2
                emit {| event = "cleanup_failure"; phase = "cleanup"; exceptionType = ex.GetType().FullName; message = ex.Message |}
        | None -> ()

    emit
        {| event = "summary"
           disposition = disposition
           exitCode = exitCode
           finalPhase = phase
           wrapperCalls = wrapperCalls
           wrapperCompleted = wrapperCompleted
           cleanupAttempted = cleanupAttempted
           cleanupPassed = cleanupPassed
           cleanupError = cleanupError
           mechanismScope = "one public stub-world entity-propagation call"
           fullApplication = false
           nativeInput = false
           gaia = false
           benefitClaim = false |}
    exitCode
