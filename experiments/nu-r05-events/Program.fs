module R05EventProbe

open System
open System.Collections.Generic
open System.Reflection
open Prime
open Nu

type ProbePlugin () =
    inherit NuPlugin ()

let join (trace : ResizeArray<string>) =
    String.Join (",", trace)

let assertTrace name expected (trace : ResizeArray<string>) =
    let actual = join trace
    let passed = actual = expected
    printfn "RESULT %s expected=[%s] actual=[%s] pass=%b" name expected actual passed
    passed

let printAssembly label (assembly : Assembly) =
    let informational =
        match assembly.GetCustomAttribute<AssemblyInformationalVersionAttribute> () with
        | null -> "<none>"
        | attribute -> attribute.InformationalVersion
    printfn "ASSEMBLY %s name=%s version=%O informational=%s path=%s"
        label (assembly.GetName().Name) (assembly.GetName().Version) informational assembly.Location

[<EntryPoint>]
let main _ =
    printfn "RUNTIME framework=%s runtime=%s" System.Runtime.InteropServices.RuntimeInformation.FrameworkDescription (Environment.Version.ToString ())
    printAssembly "Nu" typeof<World>.Assembly
    printAssembly "Prime" typeof<Symbol>.Assembly
    Nu.init ()
    let config = { WorldConfig.defaultConfig with Accompanied = true }
    let world = World.makeStub (fun _ -> None) config (ProbePlugin ())
    let game = Nu.Game.Handle
    let screen = game / "ProbeScreen"
    let group = screen / "ProbeGroup"
    let ghostPublisher = game / "GhostPublisher"

    let cascadeAddress = rtoa<int> [|"R05"; "Cascade"; "Event"; "GhostPublisher"|]
    let cascadeTrace = ResizeArray<string> ()
    let cascadeUnsubGroup =
        World.subscribePlus<int, Group> 1001UL
            (fun _ _ -> cascadeTrace.Add "group"; Cascade)
            cascadeAddress group world
    let cascadeUnsubScreen =
        World.subscribePlus<int, Screen> 1002UL
            (fun _ _ -> cascadeTrace.Add "screen"; Cascade)
            cascadeAddress screen world
    let cascadeUnsubGame =
        World.subscribePlus<int, Game> 1003UL
            (fun _ _ -> cascadeTrace.Add "game"; Cascade)
            cascadeAddress game world
    World.publishPlus 11 cascadeAddress EventTrace.empty ghostPublisher true false world
    let cascadePassed = assertTrace "cascade-priority" "game,screen,group" cascadeTrace
    cascadeUnsubGroup world
    cascadeUnsubScreen world
    cascadeUnsubGame world

    let resolveAddress = rtoa<int> [|"R05"; "Resolve"; "Event"; "GhostPublisher"|]
    let resolveTrace = ResizeArray<string> ()
    let resolveUnsubGroup =
        World.subscribePlus<int, Group> 2001UL
            (fun _ _ -> resolveTrace.Add "group"; Cascade)
            resolveAddress group world
    let resolveUnsubScreen =
        World.subscribePlus<int, Screen> 2002UL
            (fun _ _ -> resolveTrace.Add "screen"; Resolve)
            resolveAddress screen world
    let resolveUnsubGame =
        World.subscribePlus<int, Game> 2003UL
            (fun _ _ -> resolveTrace.Add "game"; Cascade)
            resolveAddress game world
    World.publishPlus 22 resolveAddress EventTrace.empty ghostPublisher true false world
    let resolvePassed = assertTrace "resolve-stop" "game,screen" resolveTrace
    resolveUnsubGroup world
    resolveUnsubScreen world
    resolveUnsubGame world

    let lifetimeAddress = rtoa<string> [|"R05"; "Lifetime"; "Event"; "NeverCreatedPublisher"|]
    let neverCreatedPublisher = game / "NeverCreatedPublisher"
    let lifetimeTrace = ResizeArray<string> ()
    let unsubscribe =
        World.subscribePlus<string, Game> 3001UL
            (fun evt _ -> lifetimeTrace.Add ("plain:" + evt.Data); Cascade)
            lifetimeAddress game world
    World.publishPlus "before" lifetimeAddress EventTrace.empty neverCreatedPublisher true false world
    unsubscribe world
    World.publishPlus "after" lifetimeAddress EventTrace.empty neverCreatedPublisher true false world
    let lifetimePassed = assertTrace "publisher-neutral-explicit-unsubscribe" "plain:before" lifetimeTrace

    World.cleanUp world
    let allPassed = cascadePassed && resolvePassed && lifetimePassed
    printfn "SUMMARY pass=%b stubWorld=true fullGameLoop=false hostInput=false nativeBehavior=false" allPassed
    if allPassed then 0 else 1
