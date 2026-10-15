namespace NuR02StandaloneLifecycle

open System
open System.Collections.Generic
open System.IO
open System.Text.Json
open Prime
open Nu
open Breakout
open NuR02StandaloneLifecycle.Common

module Arm =

#if MMCC
    let name = "mmcc"
    let windowTitle = "Breakout Mmcc"
    let splash = Simulants.Splash
    let title = Simulants.Title
    let gameplay = Simulants.Gameplay
    let titlePlay = Simulants.TitlePlay
    let gameplayScene = Simulants.GameplayScene
    let gameplayQuit = Simulants.GameplayQuit

    let topState world = string (Game.GetBreakout world)

    let scalar world =
        let value = gameplay.GetGameplay world
        Some (string value.GameplayState, value.Score, value.Lives, value.Bricks.Count)

    let ballPosition world = Some (gameplay.GetGameplay world).Ball.Position

    let projection world =
        let value = gameplay.GetGameplay world
        fields
            ["topState", box (topState world)
             "gameplayScreen", box (screenExistsData gameplay world)
             "gameplayTime", box value.GameplayTime
             "gameplayState", box (string value.GameplayState)
             "score", box value.Score
             "lives", box value.Lives
             "brickCount", box value.Bricks.Count
             "paddlePosition", box (vector value.Paddle.Position)
             "ballPosition", box (vector value.Ball.Position)
             "sceneExists", box (gameplayScene.GetExists world)]

    let stableTitleCheck world =
        let value = gameplay.GetGameplay world
        value.GameplayTime = 0L && string value.GameplayState = "Quit" &&
        value.Score = 0 && value.Lives = 0 && value.Bricks.Count = 0 &&
        not (gameplayScene.GetExists world)

    let stableTitleData world = projection world
    let publishPlay world = World.publish () titlePlay.ClickEvent titlePlay world |> ignore
    let publishQuit world = World.publish () gameplayQuit.ClickEvent gameplayQuit world |> ignore
    let quitOwned counters (_ : World) = count "gameplay-quit-request" counters > 0
#else
    let name = "imsim"
    let windowTitle = "Breakout ImSim"
    let splash = Simulants.Splash
    let title = Simulants.Title
    let gameplay = Simulants.Gameplay
    let titleGui : Group = title / "Gui"
    let titlePlay : Entity = titleGui / "Play"
    let gameplayScene : Group = gameplay / "Scene"
    let gameplayQuit : Entity = gameplayScene / "Quit"
    let gameplayPaddle : Entity = gameplayScene / "Paddle"
    let gameplayBall : Entity = gameplayScene / "Ball"

    let topState world = string (Game.GetGameState world)

    let scalar world =
        if gameplay.GetExists world then
            Some (string (gameplay.GetGameplayState world), gameplay.GetScore world, gameplay.GetLives world, (gameplay.GetBricks world).Count)
        else None

    let ballPosition world =
        if gameplayBall.GetExists world then Some (gameplayBall.GetPosition world)
        else None

    let projection world =
        if gameplay.GetExists world then
            let bricks = gameplay.GetBricks world
            fields
                ["topState", box (topState world)
                 "gameplayScreen", box (screenExistsData gameplay world)
                 "gameplayState", box (string (gameplay.GetGameplayState world))
                 "score", box (gameplay.GetScore world)
                 "lives", box (gameplay.GetLives world)
                 "brickCount", box bricks.Count
                 "sceneExists", box (gameplayScene.GetExists world)
                 "paddle", box (entityData gameplayPaddle world)
                 "ball", box (bodyEntityData gameplayBall world)
                 "quit", box (entityData gameplayQuit world)]
        else
            fields
                ["topState", box (topState world)
                 "gameplayScreen", box (screenExistsData gameplay world)]

    let private absent (entity : Entity) world = not (entity.GetExists world)

    let stableTitleCheck world =
        if not (gameplay.GetExists world) || gameplay.GetSelected world || gameplayScene.GetExists world then false
        else
            let bricks = gameplay.GetBricks world
            let lives = gameplay.GetLives world
            absent gameplayPaddle world && absent gameplayBall world && absent gameplayQuit world &&
            (bricks |> Seq.forall (fun (KeyValue (brickName, _)) -> absent (gameplayScene / brickName) world)) &&
            ([0 .. max -1 (lives - 1)] |> List.forall (fun index -> absent (gameplayScene / ("Life+" + string index)) world))

    let stableTitleData world = projection world
    let publishPlay world = World.publish () titlePlay.ClickEvent titlePlay world |> ignore
    let publishQuit world = World.publish () gameplayQuit.ClickEvent gameplayQuit world |> ignore
    let quitOwned _ world =
        match scalar world with
        | Some (state, _, _, _) -> state = "Quit"
        | None -> false
#endif

module Probe =

    type Phase =
        | Startup
        | AwaitFirstGameplay
        | ActiveWitness
        | AwaitTitle
        | TitleHold
        | AwaitSecondGameplay
        | FreshHold
        | Finished

    let phaseName phase =
        match phase with
        | Startup -> "startup"
        | AwaitFirstGameplay -> "await-first-gameplay"
        | ActiveWitness -> "active-witness"
        | AwaitTitle -> "await-title"
        | TitleHold -> "title-hold"
        | AwaitSecondGameplay -> "await-second-gameplay"
        | FreshHold -> "fresh-hold"
        | Finished -> "finished"

    let private subscribeAll (trace : Trace) (counters : Counters) (secondary : Secondary)
                             (preOrdinal : int ref) (postOrdinal : int ref) (world : World) =
        let mutable nextId = 0x5230320000000000UL
        let subscribe name address =
            nextId <- nextId + 1UL
            World.subscribePlus nextId
                (fun _ eventWorld ->
                    let value = count name counters + 1
                    counters.Values[name] <- value
                    let item =
                        fields
                            ["event", box name
                             "count", box value
                             "outerEntry", box preOrdinal.Value
                             "postProcessSeen", box postOrdinal.Value
                             "updateTime", box eventWorld.UpdateTime
                             "gameTime", box (string eventWorld.GameTime)]
                    counters.Order.Add item
                    trace.Emit "observed-event"
                        ["event", box name
                         "count", box value
                         "outerEntry", box preOrdinal.Value
                         "postProcessSeen", box postOrdinal.Value
                         "updateTime", box eventWorld.UpdateTime
                         "gameTime", box (string eventWorld.GameTime)]
                    Cascade)
                address Game world |> ignore
        subscribe "play-click" Arm.titlePlay.ClickEvent
        subscribe "quit-click" Arm.gameplayQuit.ClickEvent
        subscribe "splash-deselecting" Arm.splash.DeselectingEvent
        subscribe "splash-outgoing-finish" Arm.splash.OutgoingFinishEvent
        subscribe "title-select" Arm.title.SelectEvent
        subscribe "title-incoming-finish" Arm.title.IncomingFinishEvent
        subscribe "title-deselecting" Arm.title.DeselectingEvent
        subscribe "title-outgoing-finish" Arm.title.OutgoingFinishEvent
        subscribe "gameplay-select" Arm.gameplay.SelectEvent
        subscribe "gameplay-incoming-finish" Arm.gameplay.IncomingFinishEvent
        subscribe "gameplay-deselecting" Arm.gameplay.DeselectingEvent
        subscribe "gameplay-outgoing-finish" Arm.gameplay.OutgoingFinishEvent
#if MMCC
        subscribe "gameplay-quit-request" Arm.gameplay.QuitEvent
        nextId <- nextId + 1UL
        World.subscribePlus nextId
            (fun event eventWorld ->
                match event.Data with
                | Some screen when screen = Arm.gameplay ->
                    try
                        let generation = count "gameplay-select" counters
                        match Arm.scalar eventWorld with
                        | Some (state, score, lives, bricks) ->
                            let gameplayTime = Arm.gameplay.GetGameplay(eventWorld).GameplayTime
                            let selectedGameplay = selectedIs Arm.gameplay eventWorld
                            let record =
                                fields
                                    ["seam", box "mmcc-post-select"
                                     "generation", box generation
                                     "gameplayTime", box gameplayTime
                                     "state", box state
                                     "score", box score
                                     "lives", box lives
                                     "brickCount", box bricks
                                     "selectedGameplay", box selectedGameplay
                                     "selected", box (selectedData eventWorld)
                                     "outerEntry", box preOrdinal.Value
                                     "postProcessSeen", box postOrdinal.Value
                                     "updateTime", box eventWorld.UpdateTime
                                     "tickTime", box eventWorld.TickTime
                                     "gameTime", box (string eventWorld.GameTime)]
                            secondary.Records.Add record
                            trace.Emit "secondary-initializer" ["record", box record]
                            if generation < 1 || generation > 2 || generation <> secondary.Records.Count then
                                secondaryFailure "MMCC exact callbacks did not bind one-to-one to Select generations" secondary
                            elif not selectedGameplay then
                                secondaryFailure "MMCC exact callback did not observe Gameplay selected" secondary
                            elif state <> "Playing" || score <> 0 || lives <> 5 || bricks <> 30 || gameplayTime <> 0L then
                                secondaryFailure "MMCC exact initializer scalars contradicted Playing/time0/score0/lives5/bricks30" secondary
                        | None -> secondaryMissing "MMCC exact initializer scalar projection unavailable" secondary
                    with error ->
                        secondaryMissing "MMCC exact initializer callback raised during observation" secondary
                        trace.Emit "secondary-initializer-exception"
                            ["type", box (error.GetType().FullName); "message", box error.Message]
                | _ -> ()
                Cascade)
            Game.PostSelectEvent Game world |> ignore
#else
        nextId <- nextId + 1UL
        World.subscribePlus nextId
            (fun _ eventWorld ->
                try
                    let generation = count "gameplay-select" counters
                    match Arm.scalar eventWorld with
                    | Some (state, score, lives, bricks) ->
                        let sceneId = Arm.gameplayScene.GetId eventWorld
                        let sceneExists = Arm.gameplayScene.GetExists eventWorld
                        let gameplaySelected = Arm.gameplay.GetSelected eventWorld
                        let prePlayBound =
                            generation >= 1 && generation <= secondary.PrePlayGenerations.Count &&
                            secondary.PrePlayGenerations[generation - 1] = generation &&
                            secondary.PrePlaySceneAbsent[generation - 1]
                        let record =
                            fields
                                ["seam", box "imsim-scene-register"
                                 "generation", box generation
                                 "sceneId", box sceneId
                                 "sceneExists", box sceneExists
                                 "gameplaySelected", box gameplaySelected
                                 "prePlayAbsenceBound", box prePlayBound
                                 "state", box state
                                 "score", box score
                                 "lives", box lives
                                 "brickCount", box bricks
                                 "selected", box (selectedData eventWorld)
                                 "outerEntry", box preOrdinal.Value
                                 "postProcessSeen", box postOrdinal.Value
                                 "updateTime", box eventWorld.UpdateTime
                                 "tickTime", box eventWorld.TickTime
                                 "gameTime", box (string eventWorld.GameTime)]
                        secondary.Records.Add record
                        secondary.SceneIds.Add sceneId
                        trace.Emit "secondary-initializer" ["record", box record]
                        if generation < 1 || generation > 2 || generation <> secondary.Records.Count then
                            secondaryFailure "ImSim exact callbacks did not bind one-to-one to Select generations" secondary
                        elif not prePlayBound then
                            secondaryFailure "ImSim exact callback lacked its generation-bound pre-Play Scene absence" secondary
                        elif not sceneExists || not gameplaySelected then
                            secondaryFailure "ImSim exact callback did not observe an existing Scene under selected Gameplay" secondary
                        elif state <> "Playing" || score <> 0 || lives <> 5 || bricks <> 30 then
                            secondaryFailure "ImSim exact initializer scalars contradicted Playing/score0/lives5/bricks30" secondary
                    | None -> secondaryMissing "ImSim exact initializer scalar projection unavailable" secondary
                with error ->
                    secondaryMissing "ImSim exact initializer callback raised during observation" secondary
                    trace.Emit "secondary-initializer-exception"
                        ["type", box (error.GetType().FullName); "message", box error.Message]
                Cascade)
            Arm.gameplayScene.RegisterEvent Game world |> ignore
#endif

    [<EntryPoint; STAThread>]
    let main args =
        if args.Length <> 1 then
            eprintfn "usage: StandaloneLifecycleProbe <new-or-empty-output-directory>"
            2
        else
            let output = Path.GetFullPath args[0]
            if Directory.Exists output && Directory.EnumerateFileSystemEntries output |> Seq.isEmpty |> not then
                eprintfn "output directory must be new or empty"
                2
            else
                Directory.CreateDirectory output |> ignore
                use trace = new Trace (Arm.name, output)
                let counters = makeCounters ()
                let secondary = makeSecondary ()
                let preOrdinal = ref 0
                let postOrdinal = ref 0
                let mutable subscriptionsInstalled = false
                let mutable phase = Startup
                let mutable status = "unfinished"
                let mutable message = "engine returned before a probe result"
                let mutable firstPlayAt = -1
                let mutable quitAt = -1
                let mutable secondPlayAt = -1
                let mutable witnessedSelects = 0
                let mutable activeSamples = 0
                let activePositions = ResizeArray<string> ()
                let mutable titleHoldSamples = 0
                let mutable freshHoldSamples = 0
                let mutable firstGameplayRequestAt = -1
                let mutable titleRequestAt = -1
                let mutable secondGameplayRequestAt = -1
                let mutable quitOwnershipAt = -1

                let finalizeSecondary () =
                    if secondary.Status <> "failure" then
                        if secondary.Records.Count <> 2 then
                            secondaryMissing "did not capture exactly two exact initializer callbacks" secondary
#if IMSIM
                        elif secondary.PrePlaySceneAbsent.Count <> 2 then
                            secondaryMissing "did not capture both pre-Play Scene absence observations" secondary
                        elif secondary.PrePlaySceneAbsent |> Seq.exists not then
                            secondaryFailure "Scene existed immediately before a Play action" secondary
                        elif secondary.PrePlayGenerations.ToArray () <> [|1; 2|] then
                            secondaryFailure "pre-Play Scene absence observations did not bind to generations one and two" secondary
                        elif secondary.SceneIds.Count <> 2 then
                            secondaryMissing "did not capture two ImSim Scene IDs" secondary
                        elif secondary.SceneIds[0] = secondary.SceneIds[1] then
                            secondaryFailure "ImSim Scene IDs were not distinct across logical sessions" secondary
#endif
                        elif secondary.Status = "pending" then
                            secondary.Status <- "pass"
                            secondary.Message <- "two exact initializer generations passed"

                let finish result text (world : World) =
                    if phase <> Finished then
                        finalizeSecondary ()
                        status <- result
                        message <- text
                        phase <- Finished
                        trace.Emit "probe-result"
                            ["status", box result
                             "message", box text
                             "outerEntry", box preOrdinal.Value
                             "postProcess", box postOrdinal.Value
                             "secondaryInitializerDiagnostic", box (secondaryData secondary)
                             "counters", box (counterData counters)
                             "eventOrder", box (counters.Order.ToArray ())]
                        World.exit world

                let fail text world = finish "failure" text world
                let missing text world = finish "missing" text world

                let fullObservation (world : World) =
                    fields
                        ["phase", box (phaseName phase)
                         "outerEntry", box preOrdinal.Value
                         "postProcess", box postOrdinal.Value
                         "updateTime", box world.UpdateTime
                         "tickTime", box world.TickTime
                         "gameTime", box (string world.GameTime)
                         "imperative", box world.Imperative
                         "accompanied", box world.Accompanied
                         "advancing", box world.Advancing
                         "selected", box (selectedData world)
                         "input", box (inputData world)
                         "counters", box (counterData counters)
                         "application", box (Arm.projection world)]

                let emitObservation kind (world : World) =
                    trace.Emit kind ["observation", box (fullObservation world)]

                let captureApplicationRequests observationPoint (world : World) =
                    if phase <> Finished && firstGameplayRequestAt < 0 && firstPlayAt >= 0 && Arm.topState world = "Gameplay" then
                        firstGameplayRequestAt <- postOrdinal.Value
                        trace.Emit "application-request"
                            ["destination", box "Gameplay"; "postProcess", box postOrdinal.Value; "action", box "first-play"; "observationPoint", box observationPoint]
                    if phase <> Finished && quitOwnershipAt < 0 && quitAt >= 0 && Arm.quitOwned counters world then
                        quitOwnershipAt <- postOrdinal.Value
                        trace.Emit "application-request"
                            ["destination", box "Quit"; "postProcess", box postOrdinal.Value; "action", box "quit"; "observationPoint", box observationPoint]
                    if phase <> Finished && titleRequestAt < 0 && quitAt >= 0 && Arm.topState world = "Title" then
                        titleRequestAt <- postOrdinal.Value
                        trace.Emit "application-request"
                            ["destination", box "Title"; "postProcess", box postOrdinal.Value; "action", box "quit"; "observationPoint", box observationPoint]
                    if phase <> Finished && secondGameplayRequestAt < 0 && secondPlayAt >= 0 && Arm.topState world = "Gameplay" then
                        secondGameplayRequestAt <- postOrdinal.Value
                        trace.Emit "application-request"
                            ["destination", box "Gameplay"; "postProcess", box postOrdinal.Value; "action", box "second-play"; "observationPoint", box observationPoint]

                let publishAction label publish counterName (world : World) =
                    let before = count counterName counters
                    emitObservation (label + "-before") world
                    publish world
                    emitObservation (label + "-after") world
                    captureApplicationRequests "after-publication" world
                    let after = count counterName counters
                    let delta = after - before
                    trace.Emit "action-counter"
                        ["action", box label; "before", box before; "after", box after; "delta", box delta]
                    if delta = 0 then
                        missing (label + " publication counter did not observe the published event") world
                        false
                    elif delta <> 1 then
                        fail (label + " publication counter changed by a contradictory delta of " + string delta) world
                        false
                    else true

                let checkPostSelectWitness (world : World) =
                    let observed = count "gameplay-select" counters
                    if observed > 2 then
                        fail "more than two Gameplay Select events" world
                    elif observed > witnessedSelects then
                        if observed <> witnessedSelects + 1 then
                            fail "Gameplay Select generation jumped" world
                        else
                            match Arm.scalar world with
                            | None -> missing "Gameplay scalar witness unavailable after Select" world
                            | Some (state, score, lives, bricks) ->
                                trace.Emit "post-select-witness"
                                    ["generation", box observed
                                     "state", box state
                                     "score", box score
                                     "lives", box lives
                                     "brickCount", box bricks
                                     "application", box (Arm.projection world)]
                                if state <> "Playing" || score <> 0 || lives <> 5 || bricks <> 30 then
                                    fail "complete post-Select scalar witness contradicts Playing/0/5/30" world
                                else witnessedSelects <- observed

                let lifecycleCountsFinal () =
                    count "play-click" counters = 2 &&
                    count "quit-click" counters = 1 &&
                    count "splash-deselecting" counters = 1 &&
                    count "splash-outgoing-finish" counters = 1 &&
                    count "title-select" counters = 2 &&
                    count "title-incoming-finish" counters = 2 &&
                    count "title-deselecting" counters = 2 &&
                    count "title-outgoing-finish" counters = 2 &&
                    count "gameplay-select" counters = 2 &&
                    count "gameplay-incoming-finish" counters = 2 &&
                    count "gameplay-deselecting" counters = 1 &&
                    count "gameplay-outgoing-finish" counters = 1

                let effectiveTransitionConfiguration (world : World) =
                    let splashIncoming = (Arm.splash.GetIncoming world).TransitionLifeTime
                    let splashOutgoing = (Arm.splash.GetOutgoing world).TransitionLifeTime
                    let titleIncoming = (Arm.title.GetIncoming world).TransitionLifeTime
                    let titleOutgoing = (Arm.title.GetOutgoing world).TransitionLifeTime
                    let gameplayIncoming = (Arm.gameplay.GetIncoming world).TransitionLifeTime
                    let gameplayOutgoing = (Arm.gameplay.GetOutgoing world).TransitionLifeTime
                    let splashSlide = Arm.splash.GetSlideOpt world
                    let matches expected value =
                        match value with
                        | UpdateTime actual -> actual = expected
                        | TickTime _ -> false
                    let slideMatches =
                        match splashSlide with
                        | Some slide -> matches 60L slide.IdlingTime
                        | None -> false
                    let data =
                        fields
                            ["splashIncoming", box (string splashIncoming)
                             "splashOutgoing", box (string splashOutgoing)
                             "splashSlide", box (match splashSlide with Some slide -> string slide.IdlingTime | None -> "None")
                             "titleIncoming", box (string titleIncoming)
                             "titleOutgoing", box (string titleOutgoing)
                             "gameplayIncoming", box (string gameplayIncoming)
                             "gameplayOutgoing", box (string gameplayOutgoing)]
                    let valid =
                        matches 30L splashIncoming && matches 60L splashOutgoing && slideMatches &&
                        matches 30L titleIncoming && matches 60L titleOutgoing &&
                        matches 30L gameplayIncoming && matches 60L gameplayOutgoing
                    data, valid

                let preProcess (world : World) =
                    preOrdinal.Value <- preOrdinal.Value + 1
                    if not subscriptionsInstalled then
                        subscribeAll trace counters secondary preOrdinal postOrdinal world
                        subscriptionsInstalled <- true
                    trace.Emit "pre-heartbeat"
                        (["outerEntry", box preOrdinal.Value] @ timeFields "" world)

                let postProcess (world : World) =
                    postOrdinal.Value <- postOrdinal.Value + 1
                    try
                        emitObservation "post-observation" world
                        if phase <> Finished then
                            if postOrdinal.Value = 1 then
                                let static60 =
                                    match Constants.GameTime.DesiredFrameRate with
                                    | StaticFrameRate 60L -> true
                                    | _ -> false
                                let transitionConfiguration, transitionConfigurationValid = effectiveTransitionConfiguration world
                                trace.Emit "effective-configuration"
                                    ["desiredFrameRate", box (string Constants.GameTime.DesiredFrameRate)
                                     "tickDeltaAveraging", box Constants.Engine.TickDeltaAveraging
                                     "subscriptionsInstalled", box subscriptionsInstalled
                                     "imperative", box world.Imperative
                                     "accompanied", box world.Accompanied
                                     "advancing", box world.Advancing
                                     "transitionConfiguration", box transitionConfiguration]
                                if not subscriptionsInstalled then missing "subscriptions were not installed in first preProcess" world
                                elif not static60 || Constants.Engine.TickDeltaAveraging then fail "effective clock differs" world
                                elif not transitionConfigurationValid then fail "effective transition or Splash idling configuration differs" world
                                elif not world.Imperative || world.Accompanied || not world.Advancing then fail "effective standalone mode differs" world

                            if phase <> Finished then checkPostSelectWitness world

                            if phase <> Finished then captureApplicationRequests "postProcess-entry" world

                            match phase with
                            | Startup ->
                                if selectedIdlingIs Arm.title world then
                                    if count "title-select" counters = 0 || count "title-incoming-finish" counters = 0 then
                                        missing "stable startup Title lacked installed lifecycle evidence" world
                                    elif count "title-select" counters <> 1 || count "title-incoming-finish" counters <> 1 then
                                        fail "startup Title lifecycle counts differ" world
                                    else
#if IMSIM
                                        let sceneAbsent = not (Arm.gameplayScene.GetExists world)
                                        secondary.PrePlaySceneAbsent.Add sceneAbsent
                                        secondary.PrePlayGenerations.Add 1
                                        trace.Emit "secondary-pre-play"
                                            ["generation", box 1; "sceneAbsent", box sceneAbsent; "postProcess", box postOrdinal.Value]
                                        if not sceneAbsent then secondaryFailure "Scene existed immediately before first Play" secondary
#endif
                                        firstPlayAt <- postOrdinal.Value
                                        if publishAction "first-play" Arm.publishPlay "play-click" world then phase <- AwaitFirstGameplay
                                elif postOrdinal.Value >= 200 then
                                    fail "natural startup did not reach idling Title by callback 200" world

                            | AwaitFirstGameplay ->
                                if selectedIdlingIs Arm.gameplay world && Arm.topState world = "Gameplay" then
                                    if count "gameplay-select" counters = 0 || count "gameplay-incoming-finish" counters = 0 then
                                        missing "first stable Gameplay lacked installed lifecycle evidence" world
                                    elif count "gameplay-select" counters <> 1 || count "gameplay-incoming-finish" counters <> 1 || witnessedSelects <> 1 then
                                        fail "first Gameplay lifecycle generation differs" world
                                    else
                                        phase <- ActiveWitness
                                        trace.Emit "phase-boundary" ["phase", box "active-witness"; "postProcess", box postOrdinal.Value]
                                elif postOrdinal.Value - firstPlayAt >= 100 then
                                    fail "first Play did not reach idling Gameplay within 100 increments" world

                            | ActiveWitness ->
                                if not (selectedIdlingIs Arm.gameplay world) || Arm.topState world <> "Gameplay" then
                                    fail "Gameplay changed during active witness" world
                                else
                                    match Arm.scalar world, Arm.ballPosition world with
                                    | Some (state, _, _, _), Some position ->
                                        if state <> "Playing" then fail "Gameplay was not Playing during active witness" world
                                        elif not (sampledKeysUp world) then fail "sampled Left/Right/P was held during active witness" world
                                        else
                                            activeSamples <- activeSamples + 1
                                            activePositions.Add (JsonSerializer.Serialize (vector position))
                                            trace.Emit "active-sample"
                                                ["sample", box activeSamples
                                                 "ballPosition", box (vector position)
                                                 "input", box (inputData world)]
                                            if activeSamples = 3 then
                                                if activePositions |> Seq.distinct |> Seq.length < 2 then
                                                    fail "ball position did not change across three active samples" world
                                                else
                                                    quitAt <- postOrdinal.Value
                                                    if publishAction "quit" Arm.publishQuit "quit-click" world then phase <- AwaitTitle
                                    | _ -> missing "active Gameplay projection unavailable" world

                            | AwaitTitle ->
                                if selectedIdlingIs Arm.title world && Arm.topState world = "Title" then
                                    trace.Emit "stable-title" ["application", box (Arm.stableTitleData world)]
                                    if count "title-select" counters = 0 || count "gameplay-deselecting" counters = 0 then
                                        missing "stable return Title lacked installed lifecycle evidence" world
                                    elif count "title-select" counters <> 2 || count "title-incoming-finish" counters <> 2 ||
                                         count "gameplay-deselecting" counters <> 1 || count "gameplay-outgoing-finish" counters <> 1 then
                                        fail "return-to-Title lifecycle counts differ" world
                                    elif not (Arm.stableTitleCheck world) then
                                        fail "stable Title application lifetime projection differs" world
                                    else
                                        phase <- TitleHold
                                        trace.Emit "phase-boundary" ["phase", box "title-hold"; "postProcess", box postOrdinal.Value]
                                elif postOrdinal.Value - quitAt >= 100 then
                                    fail "Quit did not reach idling Title within 100 increments" world

                            | TitleHold ->
                                if not (selectedIdlingIs Arm.title world) || Arm.topState world <> "Title" then
                                    fail "Title changed during three-callback hold" world
                                elif count "play-click" counters <> 1 || count "quit-click" counters <> 1 || count "gameplay-select" counters <> 1 then
                                    fail "unexpected action or Gameplay Select during Title hold" world
                                else
                                    titleHoldSamples <- titleHoldSamples + 1
                                    trace.Emit "title-hold-sample" ["sample", box titleHoldSamples]
                                    if titleHoldSamples = 3 then
#if IMSIM
                                        let sceneAbsent = not (Arm.gameplayScene.GetExists world)
                                        secondary.PrePlaySceneAbsent.Add sceneAbsent
                                        secondary.PrePlayGenerations.Add 2
                                        trace.Emit "secondary-pre-play"
                                            ["generation", box 2; "sceneAbsent", box sceneAbsent; "postProcess", box postOrdinal.Value]
                                        if not sceneAbsent then secondaryFailure "Scene existed immediately before second Play" secondary
#endif
                                        secondPlayAt <- postOrdinal.Value
                                        if publishAction "second-play" Arm.publishPlay "play-click" world then phase <- AwaitSecondGameplay

                            | AwaitSecondGameplay ->
                                if selectedIdlingIs Arm.gameplay world && Arm.topState world = "Gameplay" then
                                    if count "gameplay-select" counters = 0 || count "gameplay-incoming-finish" counters = 0 then
                                        missing "second stable Gameplay lacked installed lifecycle evidence" world
                                    elif count "gameplay-select" counters <> 2 || count "gameplay-incoming-finish" counters <> 2 || witnessedSelects <> 2 then
                                        fail "second Gameplay lifecycle generation differs" world
                                    else
                                        phase <- FreshHold
                                        trace.Emit "phase-boundary" ["phase", box "fresh-hold"; "postProcess", box postOrdinal.Value]
                                elif postOrdinal.Value - secondPlayAt >= 100 then
                                    fail "second Play did not reach idling Gameplay within 100 increments" world

                            | FreshHold ->
                                if not (selectedIdlingIs Arm.gameplay world) || Arm.topState world <> "Gameplay" then
                                    fail "unsolicited Title transition during fresh-session hold" world
                                else
                                    match Arm.scalar world with
                                    | None -> missing "fresh-session Gameplay scalar unavailable" world
                                    | Some (state, _, _, _) when state <> "Playing" -> fail "fresh-session Gameplay retained Quit" world
                                    | Some _ ->
                                        if count "play-click" counters <> 2 || count "quit-click" counters <> 1 || count "gameplay-select" counters <> 2 then
                                            fail "unexpected action or Gameplay Select during fresh-session hold" world
                                        else
                                            freshHoldSamples <- freshHoldSamples + 1
                                            trace.Emit "fresh-hold-sample" ["sample", box freshHoldSamples]
                                            if freshHoldSamples = 5 then
                                                if firstGameplayRequestAt < 0 || quitOwnershipAt < 0 || titleRequestAt < 0 || secondGameplayRequestAt < 0 then
                                                    fail "one or more application-owned request boundaries were not observed" world
                                                elif not (lifecycleCountsFinal ()) then
                                                    fail "final lifecycle counts differ" world
                                                else
                                                    finish "pass" "unchanged standalone Play / Gameplay / Quit / Title / fresh-Play lifecycle passed" world

                            | Finished -> ()

                            if phase <> Finished && postOrdinal.Value >= callbackCap then
                                fail "live phase exhausted 600 postProcess callbacks" world
                    with error ->
                        try emitObservation "exception-observation" world with _ -> ()
                        trace.Emit "probe-exception"
                            ["type", box (error.GetType().FullName)
                             "message", box error.Message
                             "stack", box error.StackTrace]
                        missing "required observation or probe operation raised an exception" world

                let mutable engineExitCode = -1
                let mutable engineTermination = "not-started"
                try
                    Directory.SetCurrentDirectory AppContext.BaseDirectory
                    Nu.init ()
                    Constants.GameTime.DesiredFrameRate <- StaticFrameRate 60L
                    Constants.Engine.TickDeltaAveraging <- false
                    let sdlWindowConfig = {SdlWindowConfig.defaultConfig with WindowTitle = Arm.windowTitle}
                    let sdlConfig = {SdlConfig.defaultConfig with WindowConfig = sdlWindowConfig}
                    let worldConfig = {WorldConfig.defaultConfig with SdlConfig = sdlConfig}
                    let windowSize = Constants.Render.DisplayVirtualResolution * Globals.Render.DisplayScalar
                    let windowViewport = Viewport.makeWindow1 windowSize
                    let geometryViewport = Viewport.makeGeometry windowViewport.Bounds.Size
                    trace.Emit "launch"
                        ["pin", box pin
                         "runtime", box (Environment.Version.ToString ())
                         "nuAssembly", box typeof<World>.Assembly.FullName
                         "plugin", box typeof<BreakoutPlugin>.FullName
                         "callbackCap", box callbackCap
                         "windowTitle", box Arm.windowTitle
                         "displayVirtualResolution", box (vector2i Constants.Render.DisplayVirtualResolution)
                         "displayScalar", box Globals.Render.DisplayScalar
                         "computedWindowSize", box (vector2i windowSize)
                         "windowViewport", box (viewportData windowViewport)
                         "geometryViewport", box (viewportData geometryViewport)]
                    engineExitCode <-
                        World.runPlus (constant None) tautology preProcess ignore postProcess ignore ignore
                            worldConfig windowViewport.Outer.Size geometryViewport windowViewport (BreakoutPlugin ())
                    engineTermination <- if engineExitCode = 0 then "returned-zero" else "returned-nonzero"
                    trace.Emit "engine-exit"
                        ["exitCode", box engineExitCode
                         "status", box status
                         "outerEntry", box preOrdinal.Value
                         "postProcess", box postOrdinal.Value]
                with error ->
                    let enteredLoop = preOrdinal.Value > 0
                    engineTermination <- if phase = Finished then "exception-after-primary-result" elif enteredLoop then "loop-exception" else "launch-exception"
                    trace.Emit "engine-exception"
                        ["type", box (error.GetType().FullName)
                         "message", box error.Message
                         "stack", box error.StackTrace
                         "enteredLoop", box enteredLoop
                         "phase", box (phaseName phase)
                         "primaryStatus", box status]
                    if status = "unfinished" then
                        finalizeSecondary ()
                        status <- "missing"
                        message <- if enteredLoop then "engine loop raised before a probe result" else "standalone launch raised before the first loop entry"
                        trace.Emit "probe-result"
                            ["status", box status
                             "message", box message
                             "outerEntry", box preOrdinal.Value
                             "postProcess", box postOrdinal.Value
                             "secondaryInitializerDiagnostic", box (secondaryData secondary)
                             "counters", box (counterData counters)
                             "eventOrder", box (counters.Order.ToArray ())]
                if status = "unfinished" then
                    finalizeSecondary ()
                    status <- "missing"
                    message <- "engine returned before a probe result"
                    trace.Emit "probe-result"
                        ["status", box status
                         "message", box message
                         "outerEntry", box preOrdinal.Value
                         "postProcess", box postOrdinal.Value
                         "secondaryInitializerDiagnostic", box (secondaryData secondary)
                         "counters", box (counterData counters)
                         "eventOrder", box (counters.Order.ToArray ())]
                trace.Close ()
                writeResult output Arm.name status message engineExitCode engineTermination preOrdinal.Value postOrdinal.Value trace.Path (secondaryData secondary)
                if status = "pass" && engineExitCode = 0 then 0 else 1
