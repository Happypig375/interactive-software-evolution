namespace NuR04PauseRuntime

open System
open System.Collections.Generic
open System.Numerics
open System.Text.Json
open Prime
open Nu
open Breakout

module Common =

    let fields (pairs : (string * obj) list) = Dictionary<string, obj> (dict pairs)
    let json value = JsonSerializer.Serialize value
    let bits (value : single) = (BitConverter.SingleToInt32Bits value).ToString "X8"
    let vector (value : Vector3) = [| bits value.X; bits value.Y; bits value.Z |]
    let quaternion (value : Quaternion) = [| bits value.X; bits value.Y; bits value.Z; bits value.W |]
    let colorBits (value : Color) = [| bits value.R; bits value.G; bits value.B; bits value.A |]
    let require message condition = if not condition then invalidOp message

    let modelData (gameplay : Gameplay) =
        fields
            ["time", box gameplay.GameplayTime
             "state", box (string gameplay.GameplayState)
             "paddlePosition", box (vector gameplay.Paddle.Position)
             "paddleSize", box (vector gameplay.Paddle.Size)
             "ballPosition", box (vector gameplay.Ball.Position)
             "ballSize", box (vector gameplay.Ball.Size)
             "ballSpeed", box (bits gameplay.Ball.Speed)
             "ballDirection", box (vector gameplay.Ball.Direction)
             "bricks", box [|for KeyValue (name, brick) in gameplay.Bricks ->
                                  fields ["name", box name
                                          "position", box (vector brick.Position)
                                          "size", box (vector brick.Size)
                                          "color", box (colorBits brick.Color)]|]
             "score", box gameplay.Score
             "lives", box gameplay.Lives]

    let equalModel left right = json (modelData left) = json (modelData right)
    let equalVector left right = vector left = vector right

    let initialBallCoreShape (ball : Ball) =
        let direction = ball.Direction
        equalVector ball.Size (v3 8.0f 8.0f 0.0f) &&
        bits ball.Speed = bits 3.0f &&
        Single.IsFinite direction.X && Single.IsFinite direction.Y && Single.IsFinite direction.Z &&
        abs (direction.Length () - 1.0f) <= 0.00001f &&
        bits direction.Z = bits 0.0f &&
        abs direction.X <= 0.447224f && direction.Y <= -0.894417f

    let initialBallShape (ball : Ball) =
        equalVector ball.Position (v3 0.0f 48.0f 0.0f) && initialBallCoreShape ball

    let initialFixedShape (gameplay : Gameplay) =
        gameplay.GameplayTime = 0L &&
        equalVector gameplay.Paddle.Position (v3 0.0f -160.0f 0.0f) &&
        equalVector gameplay.Paddle.Size (v3 64.0f 16.0f 0.0f) &&
        initialBallShape gameplay.Ball && gameplay.Score = 0

    let vacantShape (gameplay : Gameplay) =
        initialFixedShape gameplay && gameplay.GameplayState = Quit &&
        gameplay.Bricks.IsEmpty && gameplay.Lives = 0

    let freshBricksShape (gameplay : Gameplay) =
        let positionKey (value : Vector3) = bits value.X, bits value.Y, bits value.Z
        let expectedPositions =
            Set.ofList
                [for i in 0 .. 4 do
                    for j in 0 .. 5 do
                        positionKey (v3 (single i * 64.0f - 128.0f) (single j * 16.0f + 64.0f) 0.0f)]
        let actualPositions = gameplay.Bricks |> Seq.map (fun (KeyValue (_, brick)) -> positionKey brick.Position) |> Set.ofSeq
        gameplay.Bricks.Count = 30 && actualPositions = expectedPositions &&
        (gameplay.Bricks |> Seq.forall (fun (KeyValue (_, brick)) ->
            equalVector brick.Size (v3 64.0f 16.0f 0.0f) &&
            Single.IsFinite brick.Color.R && brick.Color.R >= 0.5f && brick.Color.R <= 1.0f &&
            Single.IsFinite brick.Color.G && brick.Color.G >= 0.5f && brick.Color.G <= 1.0f &&
            Single.IsFinite brick.Color.B && brick.Color.B >= 0.5f && brick.Color.B <= 1.0f &&
            bits brick.Color.A = bits 1.0f))

    let freshAfterOneShape (gameplay : Gameplay) =
        let initialPosition = v3 0.0f 48.0f 0.0f
        gameplay.GameplayTime = 1L && gameplay.GameplayState = Playing &&
        equalVector gameplay.Paddle.Position (v3 0.0f -160.0f 0.0f) &&
        equalVector gameplay.Paddle.Size (v3 64.0f 16.0f 0.0f) &&
        initialBallCoreShape gameplay.Ball &&
        equalVector gameplay.Ball.Position (initialPosition + gameplay.Ball.Velocity) &&
        freshBricksShape gameplay && gameplay.Score = 0 && gameplay.Lives = 5

    let scene = Simulants.GameplayScene

    let controlData (entity : Entity) world =
        if entity.GetExists world then
            fields
                ["exists", box true
                 "position", box (vector (entity.GetPosition world))
                 "size", box (vector (entity.GetSize world))
                 "visible", box (entity.GetVisible world)
                 "enabled", box (entity.GetEnabled world)
                 "text", box (entity.GetText world)]
        else fields ["exists", box false]

    let projection includePause (world : World) =
        let gameplay = Simulants.Gameplay.GetGameplay world
        if not (scene.GetExists world) then
            fields ["sceneExists", box false]
        else
            let sprite name =
                let entity = scene / name
                if entity.GetExists world then
                    fields
                        ["name", box name
                         "exists", box true
                         "position", box (vector (entity.GetPosition world))
                         "size", box (vector (entity.GetSize world))
                         "color", box (colorBits (entity.GetColor world))]
                else fields ["name", box name; "exists", box false]
            fields
                ["sceneExists", box true
                 "names", box (World.getEntities scene world |> Seq.map (fun entity -> entity.Name) |> Seq.sort |> Seq.toArray)
                 "paddle", box (sprite "Paddle")
                 "ball", box (sprite "Ball")
                 "bricks", box (gameplay.Bricks |> Map.toArray |> Array.map (fun (name, _) -> sprite name))
                 "scoreText", box ((scene / "Score").GetText world)
                 "messageText", box ((scene / "Message").GetText world)
                 "rotation", box (quaternion ((scene / "StaticModel").GetRotation world))
                 "quit", box (controlData Simulants.GameplayQuit world)
                 if includePause then "pause", box (controlData (scene / "Pause") world)]

    let projectionErrors includePause (gameplay : Gameplay) (world : World) =
        let failures = ResizeArray<string> ()
        let check label passed = if not passed then failures.Add label
        let shouldExist = string gameplay.GameplayState <> "Quit"
        check "scene-existence" (scene.GetExists world = shouldExist)
        if shouldExist && scene.GetExists world then
            let fixedNames =
                ["SkyBox"; "Light3d"; "StaticModel"; "LeftWall"; "RightWall"; "TopWall";
                 "Paddle"; "Ball"; "Score"; "Lives"; "Message"; "Quit"]
            let expectedNames =
                fixedNames @
                (gameplay.Bricks |> Map.toList |> List.map fst) @
                [for i in 0 .. gameplay.Lives - 1 -> "Life+" + string i] @
                (if includePause then ["Pause"] else [])
                |> Set.ofList
            let actualNames =
                World.getEntities scene world
                |> Seq.map (fun entity -> entity.Name)
                |> Set.ofSeq
            check "entity-names" (actualNames = expectedNames)
            let checkSprite name position size =
                let entity = scene / name
                check (name + ":exists") (entity.GetExists world)
                if entity.GetExists world then
                    check (name + ":position") (vector (entity.GetPosition world) = vector position)
                    check (name + ":size") (vector (entity.GetSize world) = vector size)
            checkSprite "Paddle" gameplay.Paddle.Position gameplay.Paddle.Size
            checkSprite "Ball" gameplay.Ball.Position gameplay.Ball.Size
            for KeyValue (name, brick) in gameplay.Bricks do
                checkSprite name brick.Position brick.Size
                if (scene / name).GetExists world then
                    check (name + ":color") (colorBits ((scene / name).GetColor world) = colorBits brick.Color)
            check "score" ((scene / "Score").GetText world = "Score: " + string gameplay.Score)
            let expectedMessage = if gameplay.Lives <= 0 then "Game over!" elif gameplay.Bricks.Count = 0 then "You win!" else ""
            check "message" ((scene / "Message").GetText world = expectedMessage)
            let actualLives =
                World.getEntities scene world
                |> Seq.map (fun entity -> entity.Name)
                |> Seq.filter (fun name -> name.StartsWith "Life+")
                |> Set.ofSeq
            check "life-icons" (actualLives = Set.ofList [for i in 0 .. gameplay.Lives - 1 -> "Life+" + string i])
            let expectedRotation = Quaternion.CreateFromAxisAngle ((v3 1.0f 0.75f 0.5f).Normalized, single (gameplay.GameplayTime % 360L) |> degToRadF)
            check "model-rotation" (quaternion ((scene / "StaticModel").GetRotation world) = quaternion expectedRotation)
            let checkControl label expectedPosition expectedText (entity : Entity) =
                check (label + ":exists") (entity.GetExists world)
                if entity.GetExists world then
                    check (label + ":position") (vector (entity.GetPosition world) = vector expectedPosition)
                    check (label + ":size") (vector (entity.GetSize world) = vector (v3 128.0f 32.0f 0.0f))
                    check (label + ":visible") (entity.GetVisible world)
                    check (label + ":enabled") (entity.GetEnabled world)
                    check (label + ":text") (entity.GetText world = expectedText)
            checkControl "quit" (v3 232.0f -144.0f 0.0f) "Quit" Simulants.GameplayQuit
            if includePause then
                let pause = scene / "Pause"
                let text = if string gameplay.GameplayState = "Paused" then "Resume" else "Pause"
                checkControl "pause" (v3 232.0f -112.0f 0.0f) text pause
        failures.ToArray ()

    let expectedActiveOne (target : Gameplay) =
        {target with
            GameplayTime = target.GameplayTime + 1L
            Ball = {target.Ball with Position = target.Ball.Position + target.Ball.Velocity}}

    let audioKind message =
        match message with
        | LoadAudioPackageMessage _ -> "LoadAudioPackage"
        | UnloadAudioPackageMessage _ -> "UnloadAudioPackage"
        | PlaySoundMessage _ -> "PlaySound"
        | PlaySongMessage _ -> "PlaySong"
        | SetSongVolumeMessage _ -> "SetSongVolume"
        | FadeOutSongMessage _ -> "FadeOutSong"
        | StopSongMessage -> "StopSong"
        | ReloadAudioAssetsMessage -> "ReloadAudioAssets"

    let screenData (world : World) =
        fields
            ["selected", box (string (World.getSelectedScreen world))
             "selectedIdling", box (World.getSelectedScreenIdling world)
             "desired", box (string (Game.GetDesiredScreen world))]
