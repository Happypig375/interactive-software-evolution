[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $NuSourceRoot,

    [Parameter(Mandatory = $true)]
    [string] $OutputRoot,

    [string] $NuIntegrityManifest
)

$ErrorActionPreference = 'Stop'
$expectedPin = '064f7ae92a8506689cd91aff5e6804a375d6ef3d'
$packageRoot = $PSScriptRoot
$invocationRoot = (Get-Location).Path
$project = Join-Path $packageRoot 'R05EventProbe.fsproj'
$startedUtc = [DateTime]::UtcNow.ToString('o')

function Resolve-TaskPath {
    param([string] $Path, [string] $BasePath)
    if ([IO.Path]::IsPathRooted($Path)) { return [IO.Path]::GetFullPath($Path) }
    return [IO.Path]::GetFullPath((Join-Path $BasePath $Path))
}

function Test-IsWithin {
    param([string] $Candidate, [string] $Container)
    $candidatePath = [IO.Path]::GetFullPath($Candidate).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    $containerPath = [IO.Path]::GetFullPath($Container).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    return $candidatePath.Equals($containerPath, [StringComparison]::OrdinalIgnoreCase) -or
        $candidatePath.StartsWith($containerPath + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)
}

$nuRoot = Resolve-TaskPath $NuSourceRoot $invocationRoot
$output = Resolve-TaskPath $OutputRoot $invocationRoot
if (-not (Test-Path -LiteralPath $nuRoot -PathType Container)) { throw "Nu source root does not exist: $nuRoot" }
if (Test-IsWithin $output $nuRoot) { throw 'OutputRoot must be outside the Nu source root.' }
if (Test-IsWithin $output $packageRoot) { throw 'OutputRoot must be outside the tracked experiment package.' }
if (Test-Path -LiteralPath $output) {
    if ($null -ne (Get-ChildItem -LiteralPath $output -Force | Select-Object -First 1)) {
        throw "OutputRoot is not empty; use a fresh directory to preserve attempts: $output"
    }
}
$null = New-Item -ItemType Directory -Force -Path $output
$logs = Join-Path $output 'logs'
$null = New-Item -ItemType Directory -Force -Path $logs

$sourceExpectations = [ordered]@{
    'Nu/Nu/EventGraph/EventGraph.fs' = 'EDEBEF57E3BABBB8C184322948759052868EFD872DEF5A8BE0DA4F3FFE309F5E'
    'Nu/Nu/World/WorldTypes.fs' = '4854DB6065823E3782A4930075391AFD52A04DB5666C694210D527AFAB8DC738'
    'Nu/Nu/World/WorldModule.fs' = '289F9BD6C9D011027993B9B35F472696B48557E8078807D5FF0CFDC1DFE7F299'
    'Nu/Nu/World/World.fs' = '79E0B12F8AD98B7B2E3CD029296CFF705E85B68DD2F432F8B2D05AD4396A5F22'
    'Nu/Nu/Nu.fsproj' = '0F5706DB6F58ED0BE02DF01D2BA4D570DB518B54D8244760AE1F447DD78315E2'
}
$sourceHashes = [ordered]@{}
foreach ($entry in $sourceExpectations.GetEnumerator()) {
    $path = Join-Path $nuRoot $entry.Key
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Required Nu source is missing: $path" }
    $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
    if ($hash -ne $entry.Value) { throw "Nu source hash mismatch for $($entry.Key): $hash" }
    $sourceHashes[$entry.Key] = $hash
}

$identityEvidence = [Collections.Generic.List[string]]::new()
if (Test-Path -LiteralPath (Join-Path $nuRoot '.git')) {
    $head = (& git -C $nuRoot rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0 -or $head -ne $expectedPin) { throw "Nu Git HEAD is not the expected pin: $head" }
    $identityEvidence.Add("git:$head")
}
if ([string]::IsNullOrWhiteSpace($NuIntegrityManifest)) {
    $manifestPath = Join-Path (Split-Path $nuRoot -Parent) 'source-integrity.json'
}
else { $manifestPath = Resolve-TaskPath $NuIntegrityManifest $invocationRoot }
if (Test-Path -LiteralPath $manifestPath -PathType Leaf) {
    $manifest = [IO.File]::ReadAllText($manifestPath) | ConvertFrom-Json
    if ($manifest.pin -ne $expectedPin -or @($manifest.mismatches).Count -ne 0) { throw 'Nu integrity manifest does not verify the expected pin.' }
    $identityEvidence.Add("manifest:$($manifest.pin);files_checked=$($manifest.files_checked);mismatches=0")
}
if ($identityEvidence.Count -eq 0) { throw 'Supply an exact Git checkout or a matching Nu integrity manifest.' }

$nuDll = Join-Path $nuRoot 'Nu/Nu/bin/Release/net10.0/Nu.dll'
if (-not (Test-Path -LiteralPath $nuDll -PathType Leaf)) { throw "Built Release Nu.dll is missing: $nuDll" }
$nuInfo = [Diagnostics.FileVersionInfo]::GetVersionInfo($nuDll)
if ($nuInfo.ProductVersion -ne "1.0.0+$expectedPin") { throw "Nu.dll ProductVersion does not identify the expected pin: $($nuInfo.ProductVersion)" }
$nuHashBefore = (Get-FileHash -LiteralPath $nuDll -Algorithm SHA256).Hash

$env:DOTNET_CLI_HOME = Join-Path $output '.dotnet-home'
$env:NUGET_PACKAGES = Join-Path $output '.nuget-packages'
$env:DOTNET_NOLOGO = '1'
$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
$commands = [Collections.Generic.List[string]]::new()

function Format-CommandArgument {
    param([string] $Value)
    if ($Value -match '[\s"]') { return '"' + $Value.Replace('"', '\"') + '"' }
    return $Value
}

function ConvertTo-NativeArgument {
    param([string] $Value)
    if ($Value.Length -eq 0) { return '""' }
    if ($Value -notmatch '[\s"]') { return $Value }
    $builder = [Text.StringBuilder]::new()
    $null = $builder.Append('"')
    $backslashes = 0
    foreach ($character in $Value.ToCharArray()) {
        if ($character -eq '\') { $backslashes++ }
        elseif ($character -eq '"') {
            $null = $builder.Append(('\' * ($backslashes * 2 + 1)))
            $null = $builder.Append('"')
            $backslashes = 0
        }
        else {
            if ($backslashes -gt 0) { $null = $builder.Append(('\' * $backslashes)); $backslashes = 0 }
            $null = $builder.Append($character)
        }
    }
    if ($backslashes -gt 0) { $null = $builder.Append(('\' * ($backslashes * 2))) }
    $null = $builder.Append('"')
    return $builder.ToString()
}

function Invoke-DotNetLogged {
    param([string[]] $Arguments, [string] $LogName, [string] $WorkingDirectory = $packageRoot)
    $commands.Add('dotnet ' + (($Arguments | ForEach-Object { Format-CommandArgument $_ }) -join ' '))
    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = 'dotnet'
    $startInfo.WorkingDirectory = $WorkingDirectory
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.Arguments = (($Arguments | ForEach-Object { ConvertTo-NativeArgument $_ }) -join ' ')
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    if (-not $process.Start()) { throw 'Failed to start dotnet.' }
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()
    $combined = $stdout + $stderr
    [IO.File]::WriteAllText((Join-Path $logs $LogName), $combined, [Text.UTF8Encoding]::new($false))
    if ($stdout.Length -gt 0) { [Console]::Out.Write($stdout) }
    if ($stderr.Length -gt 0) { [Console]::Error.Write($stderr) }
    return [pscustomobject]@{ ExitCode = $process.ExitCode; Output = $combined }
}

$version = Invoke-DotNetLogged @('--version') 'dotnet-version.log'
if ($version.ExitCode -ne 0 -or $version.Output.Trim() -ne '10.0.302') { throw "Expected .NET SDK 10.0.302; observed $($version.Output.Trim())" }
$objRoot = Join-Path $output 'obj/'
$binRoot = Join-Path $output 'bin/'
$commonProperties = @("-p:NuSourceRoot=$nuRoot", "-p:BaseIntermediateOutputPath=$objRoot", "-p:BaseOutputPath=$binRoot")
$restore = Invoke-DotNetLogged (@('restore', $project, '--nologo') + $commonProperties) 'restore.log'
if ($restore.ExitCode -ne 0) { throw 'Probe restore failed.' }
$build = Invoke-DotNetLogged (@('build', $project, '--configuration', 'Release', '--no-restore', '--nologo') + $commonProperties) 'build.log'
if ($build.ExitCode -ne 0) { throw 'Probe build failed.' }
$assembly = Join-Path $binRoot 'Release/net10.0/R05EventProbe.dll'
$run = Invoke-DotNetLogged @($assembly) 'run.log' $output
if ($run.ExitCode -ne 0) { throw "Probe run failed with exit $($run.ExitCode)." }

$required = @(
    'RESULT cascade-priority expected=[game,screen,group] actual=[game,screen,group] pass=true',
    'RESULT resolve-stop expected=[game,screen] actual=[game,screen] pass=true',
    'RESULT publisher-neutral-explicit-unsubscribe expected=[plain:before] actual=[plain:before] pass=true',
    'SUMMARY pass=true stubWorld=true fullGameLoop=false hostInput=false nativeBehavior=false'
)
$missing = @($required | Where-Object { $run.Output -notmatch [regex]::Escape($_) })
if ($missing.Count -ne 0) { throw "Expected observations missing: $($missing -join '; ')" }

$nuHashAfter = (Get-FileHash -LiteralPath $nuDll -Algorithm SHA256).Hash
if ($nuHashAfter -ne $nuHashBefore) { throw 'Supplied Nu.dll changed during the run.' }
$loadedNu = Join-Path $binRoot 'Release/net10.0/Nu.dll'
$metadata = [ordered]@{
    schema_version = 1
    started_utc = $startedUtc
    completed_utc = [DateTime]::UtcNow.ToString('o')
    nu_source_root = $nuRoot
    output_root = $output
    expected_pin = $expectedPin
    identity_evidence = @($identityEvidence)
    source_sha256 = $sourceHashes
    nu_dll_product_version = $nuInfo.ProductVersion
    nu_dll_sha256_before = $nuHashBefore
    nu_dll_sha256_after = $nuHashAfter
    loaded_nu_dll_sha256 = (Get-FileHash -LiteralPath $loadedNu -Algorithm SHA256).Hash
    restore_exit_code = $restore.ExitCode
    build_exit_code = $build.ExitCode
    run_exit_code = $run.ExitCode
    required_observations = $required
}
[IO.File]::WriteAllText((Join-Path $output 'run-metadata.json'), ($metadata | ConvertTo-Json -Depth 8), [Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllLines((Join-Path $output 'commands.log'), $commands, [Text.UTF8Encoding]::new($false))
Write-Output "Output retained at: $output"
