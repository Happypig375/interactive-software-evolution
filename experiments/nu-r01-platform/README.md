# Nu R01 ordinary-platform dependency probe

This is the reviewable reproduction package for the bounded feasibility result
reported in
[`docs/nu-platform-feasibility-2026-10-15.md`](../../docs/nu-platform-feasibility-2026-10-15.md).
It runs Box2D.NET 3.1.1.557 directly with the Nu-like mappings and frozen inputs
in [`PROTOCOL.md`](PROTOCOL.md). It does not run a Nu world or compare Godot.

Requirements:

- .NET 8 SDK;
- access to the locked Box2D.NET NuGet package; and
- a writable output directory.

From the repository root, restore, build, and run with commands that work in
PowerShell, Bash, and ordinary command prompts:

```text
dotnet restore experiments/nu-r01-platform/nu-r01-platform.csproj --locked-mode
dotnet build experiments/nu-r01-platform/nu-r01-platform.csproj --no-restore --configuration Release
dotnet run --project experiments/nu-r01-platform/nu-r01-platform.csproj --no-restore --configuration Release -- --output-dir .artifacts/nu-r01-platform-output
```

The supplied output directory receives `summary.json`,
`trace-stationary.csv`, and `trace-moving.csv`. Generated outputs, package
caches, and `bin/` and `obj/` products are intentionally absent from this
package. The small checked-in [`result-receipt.json`](result-receipt.json)
records the completed reproduction without publishing the raw traces.

The output directory must be absent or empty. The runner checks this before
creating a physics world and rejects a nonempty directory, so a repeat cannot
overwrite a completed or partial attempt. Give every attempt a new directory.

An exit code of zero means the fixture completed. The scientific outcome is the
`dependencyCarryPositive` field in `summary.json`; the frozen moving condition
is expected to remain false for the recorded package and settings.
