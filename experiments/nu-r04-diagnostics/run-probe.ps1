[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $NuSourceRoot,

    [string] $OutputRoot,

    [string] $NuIntegrityManifest
)

$ErrorActionPreference = 'Stop'
$startedUtc = [DateTime]::UtcNow.ToString('o')
$packageRoot = $PSScriptRoot
$invocationRoot = (Get-Location).Path
$expectedNuPin = '064f7ae92a8506689cd91aff5e6804a375d6ef3d'
$expectedGameplaySha256 = '571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423'
$project = Join-Path $packageRoot 'R04DiagnosticProbe.fsproj'

function Resolve-TaskPath {
    param([string] $Path, [string] $BasePath)
    if ([IO.Path]::IsPathRooted($Path)) {
        return [IO.Path]::GetFullPath($Path)
    }
    return [IO.Path]::GetFullPath((Join-Path $BasePath $Path))
}

function Test-IsWithin {
    param([string] $Candidate, [string] $Container)
    $candidatePath = [IO.Path]::GetFullPath($Candidate).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    $containerPath = [IO.Path]::GetFullPath($Container).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    return $candidatePath.StartsWith($containerPath + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase) -or
        $candidatePath.Equals($containerPath, [StringComparison]::OrdinalIgnoreCase)
}

$nuRoot = Resolve-TaskPath -Path $NuSourceRoot -BasePath $invocationRoot
if (-not (Test-Path -LiteralPath $nuRoot -PathType Container)) {
    throw "Nu source root does not exist: $nuRoot"
}

if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
    $repoRoot = [IO.Path]::GetFullPath((Join-Path $packageRoot '../..'))
    $output = Join-Path $repoRoot ".artifacts/nu-r04-diagnostics/$stamp"
}
else {
    $output = Resolve-TaskPath -Path $OutputRoot -BasePath $invocationRoot
}

if (Test-IsWithin -Candidate $output -Container $nuRoot) {
    throw 'OutputRoot must not be the Nu source root or a descendant of it.'
}
if (Test-IsWithin -Candidate $output -Container $packageRoot) {
    throw 'OutputRoot must not be the tracked experiment package or a descendant of it.'
}
if (Test-Path -LiteralPath $output) {
    $existing = Get-ChildItem -LiteralPath $output -Force | Select-Object -First 1
    if ($null -ne $existing) {
        throw "OutputRoot is not empty; use a fresh directory to preserve attempts: $output"
    }
}

$null = New-Item -ItemType Directory -Force -Path $output
$logs = Join-Path $output 'logs'
$null = New-Item -ItemType Directory -Force -Path $logs
$commands = [Collections.Generic.List[string]]::new()

function Format-CommandArgument {
    param([string] $Value)
    if ($Value -match '[\s"]') {
        return '"' + $Value.Replace('"', '\"') + '"'
    }
    return $Value
}

function ConvertTo-NativeArgument {
    param([string] $Value)
    if ($Value.Length -eq 0) {
        return '""'
    }
    if ($Value -notmatch '[\s"]') {
        return $Value
    }
    $builder = [Text.StringBuilder]::new()
    $null = $builder.Append('"')
    $backslashes = 0
    foreach ($character in $Value.ToCharArray()) {
        if ($character -eq '\') {
            $backslashes++
        }
        elseif ($character -eq '"') {
            $null = $builder.Append(('\' * ($backslashes * 2 + 1)))
            $null = $builder.Append('"')
            $backslashes = 0
        }
        else {
            if ($backslashes -gt 0) {
                $null = $builder.Append(('\' * $backslashes))
                $backslashes = 0
            }
            $null = $builder.Append($character)
        }
    }
    if ($backslashes -gt 0) {
        $null = $builder.Append(('\' * ($backslashes * 2)))
    }
    $null = $builder.Append('"')
    return $builder.ToString()
}

function Invoke-NativeLogged {
    param(
        [string] $FileName,
        [string[]] $Arguments,
        [string] $LogPath,
        [string] $WorkingDirectory
    )
    $rendered = @($FileName) + @($Arguments | ForEach-Object { Format-CommandArgument $_ })
    $commands.Add(($rendered -join ' '))

    $startInfo = [Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = $FileName
    $startInfo.WorkingDirectory = $WorkingDirectory
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.Arguments = (@($Arguments | ForEach-Object { ConvertTo-NativeArgument $_ }) -join ' ')

    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    if (-not $process.Start()) {
        throw "Failed to start $FileName"
    }
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()
    $combined = $stdout + $stderr
    [IO.File]::WriteAllText($LogPath, $combined, [Text.UTF8Encoding]::new($false))
    if ($stdout.Length -gt 0) { [Console]::Out.Write($stdout) }
    if ($stderr.Length -gt 0) { [Console]::Error.Write($stderr) }
    return [pscustomobject]@{
        ExitCode = $process.ExitCode
        Output = $combined
    }
}

$gameplayPath = Join-Path $nuRoot 'Projects/Breakout Mmcc/Gameplay.fs'
if (-not (Test-Path -LiteralPath $gameplayPath -PathType Leaf)) {
    throw "Selected source file is missing: $gameplayPath"
}
$sourceHashBefore = (Get-FileHash -Algorithm SHA256 -LiteralPath $gameplayPath).Hash
if ($sourceHashBefore -ne $expectedGameplaySha256) {
    throw "Selected source hash mismatch. Expected $expectedGameplaySha256; observed $sourceHashBefore"
}

$identityEvidence = [Collections.Generic.List[string]]::new()
$gitMarker = Join-Path $nuRoot '.git'
if (Test-Path -LiteralPath $gitMarker) {
    $gitResult = Invoke-NativeLogged -FileName 'git' -Arguments @('-C', $nuRoot, 'rev-parse', 'HEAD') -LogPath (Join-Path $logs 'nu-git-head.log') -WorkingDirectory $packageRoot
    if ($gitResult.ExitCode -ne 0) {
        throw 'Failed to resolve the Nu Git revision.'
    }
    $observedGitPin = $gitResult.Output.Trim()
    if ($observedGitPin -ne $expectedNuPin) {
        throw "Nu Git revision mismatch. Expected $expectedNuPin; observed $observedGitPin"
    }
    $identityEvidence.Add("git:$observedGitPin")
}

if ([string]::IsNullOrWhiteSpace($NuIntegrityManifest)) {
    $manifestPath = Join-Path (Split-Path $nuRoot -Parent) 'source-integrity.json'
}
else {
    $manifestPath = Resolve-TaskPath -Path $NuIntegrityManifest -BasePath $invocationRoot
    if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
        throw "Nu integrity manifest does not exist: $manifestPath"
    }
}

if (Test-Path -LiteralPath $manifestPath -PathType Leaf) {
    $manifest = [IO.File]::ReadAllText($manifestPath) | ConvertFrom-Json
    if ($manifest.pin -ne $expectedNuPin) {
        throw "Nu integrity manifest pin mismatch. Expected $expectedNuPin; observed $($manifest.pin)"
    }
    if (@($manifest.mismatches).Count -ne 0) {
        throw 'Nu integrity manifest reports source mismatches.'
    }
    $identityEvidence.Add("manifest:$($manifest.pin);files_checked=$($manifest.files_checked);mismatches=0")
}

if ($identityEvidence.Count -eq 0) {
    throw 'Nu identity could not be verified. Supply a Git checkout at the exact pin or -NuIntegrityManifest.'
}

$env:DOTNET_CLI_HOME = Join-Path $output '.dotnet-home'
$env:NUGET_PACKAGES = Join-Path $output '.nuget-packages'
$env:DOTNET_NOLOGO = '1'
$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'

$versionResult = Invoke-NativeLogged -FileName 'dotnet' -Arguments @('--version') -LogPath (Join-Path $logs 'dotnet-version.log') -WorkingDirectory $packageRoot
if ($versionResult.ExitCode -ne 0 -or $versionResult.Output.Trim() -ne '10.0.302') {
    throw "The pinned SDK did not resolve to 10.0.302. Observed: $($versionResult.Output.Trim())"
}
$null = Invoke-NativeLogged -FileName 'dotnet' -Arguments @('--info') -LogPath (Join-Path $logs 'dotnet-info.log') -WorkingDirectory $packageRoot
$null = Invoke-NativeLogged -FileName 'dotnet' -Arguments @('fsi', '--version') -LogPath (Join-Path $logs 'fsi-version.log') -WorkingDirectory $packageRoot

$cases = @(
    [pscustomobject]@{ Name = 'baseline'; ExpectedRunExit = 0; ExpectedUniqueFs0025 = 0 },
    [pscustomobject]@{ Name = 'successor-distinct-explicit'; ExpectedRunExit = 2; ExpectedUniqueFs0025 = 1 },
    [pscustomobject]@{ Name = 'successor-distinct-catchall'; ExpectedRunExit = 1; ExpectedUniqueFs0025 = 0 },
    [pscustomobject]@{ Name = 'successor-distinct-explicit-wrong'; ExpectedRunExit = 1; ExpectedUniqueFs0025 = 0 },
    [pscustomobject]@{ Name = 'successor-fallback-explicit'; ExpectedRunExit = 2; ExpectedUniqueFs0025 = 1 },
    [pscustomobject]@{ Name = 'successor-fallback-catchall'; ExpectedRunExit = 0; ExpectedUniqueFs0025 = 0 }
)

$rows = [Collections.Generic.List[string]]::new()
$rows.Add("case`tbuild_exit`trun_exit`tunique_fs0025`traw_fs0025_log_mentions`tmatches_original_receipt")
$mismatches = [Collections.Generic.List[string]]::new()

foreach ($case in $cases) {
    $caseName = $case.Name
    $caseBin = Join-Path $output "bin/$caseName/"
    $caseObj = Join-Path $output "obj/$caseName/"
    $buildLog = Join-Path $logs "$caseName.build.log"
    $runLog = Join-Path $logs "$caseName.run.log"
    $buildArgs = @(
        'build', $project,
        '--configuration', 'Release',
        '--nologo',
        '--verbosity', 'normal',
        "-p:ProbeCase=$caseName",
        "-p:BaseOutputPath=$caseBin",
        "-p:BaseIntermediateOutputPath=$caseObj"
    )
    $buildResult = Invoke-NativeLogged -FileName 'dotnet' -Arguments $buildArgs -LogPath $buildLog -WorkingDirectory $packageRoot
    $rawDiagnosticCount = ([regex]::Matches($buildResult.Output, 'FS0025')).Count
    $diagnosticKeys = @(
        $buildResult.Output -split "`r?`n" |
            ForEach-Object {
                if ($_ -match '\.fs\((?<line>\d+),(?<column>\d+)\): warning FS0025: (?<message>.+?)(?: \[.*)?$') {
                    "$($matches.line):$($matches.column):$($matches.message)"
                }
            } |
            Sort-Object -Unique
    )
    $uniqueDiagnosticCount = $diagnosticKeys.Count
    $runExit = 'not-run'
    if ($buildResult.ExitCode -eq 0) {
        $assembly = Join-Path $caseBin 'Release/net10.0/R04DiagnosticProbe.dll'
        $runResult = Invoke-NativeLogged -FileName 'dotnet' -Arguments @($assembly) -LogPath $runLog -WorkingDirectory $packageRoot
        $runExit = $runResult.ExitCode
    }

    $matchesReceipt = $buildResult.ExitCode -eq 0 -and
        $runExit -eq $case.ExpectedRunExit -and
        $uniqueDiagnosticCount -eq $case.ExpectedUniqueFs0025
    if (-not $matchesReceipt) {
        $mismatches.Add("$caseName expected build/run/FS0025 0/$($case.ExpectedRunExit)/$($case.ExpectedUniqueFs0025), observed $($buildResult.ExitCode)/$runExit/$uniqueDiagnosticCount")
    }
    $rows.Add("$caseName`t$($buildResult.ExitCode)`t$runExit`t$uniqueDiagnosticCount`t$rawDiagnosticCount`t$matchesReceipt")
}

$sourceHashAfter = (Get-FileHash -Algorithm SHA256 -LiteralPath $gameplayPath).Hash
if ($sourceHashAfter -ne $sourceHashBefore) {
    $mismatches.Add("Selected Nu source changed during execution: before=$sourceHashBefore after=$sourceHashAfter")
}

[IO.File]::WriteAllLines((Join-Path $output 'results.tsv'), $rows, [Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllLines((Join-Path $output 'commands.log'), $commands, [Text.UTF8Encoding]::new($false))

$assetsPath = Join-Path $output 'obj/baseline/project.assets.json'
if (Test-Path -LiteralPath $assetsPath) {
    $assets = [IO.File]::ReadAllText($assetsPath) | ConvertFrom-Json
    $fsharpCore = $assets.libraries.PSObject.Properties.Name | Where-Object { $_ -like 'FSharp.Core/*' }
    [IO.File]::WriteAllLines((Join-Path $output 'resolved-packages.txt'), @($fsharpCore), [Text.UTF8Encoding]::new($false))
}

$metadata = [ordered]@{
    started_utc = $startedUtc
    completed_utc = [DateTime]::UtcNow.ToString('o')
    package_root = $packageRoot
    output_root = $output
    nu_source_root = $nuRoot
    expected_nu_pin = $expectedNuPin
    identity_evidence = @($identityEvidence)
    expected_gameplay_sha256 = $expectedGameplaySha256
    gameplay_sha256_before = $sourceHashBefore
    gameplay_sha256_after = $sourceHashAfter
    result_mismatches = @($mismatches)
}
[IO.File]::WriteAllText((Join-Path $output 'run-metadata.json'), ($metadata | ConvertTo-Json -Depth 5), [Text.UTF8Encoding]::new($false))

$rows | ForEach-Object { Write-Output $_ }
Write-Output "Output retained at: $output"
if ($mismatches.Count -ne 0) {
    throw "Probe result differed from the original receipt: $($mismatches -join '; ')"
}
