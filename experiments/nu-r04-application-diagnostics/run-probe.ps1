[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $NuArchive,

    [Parameter(Mandatory = $true)]
    [string] $OutputRoot
)

$ErrorActionPreference = 'Stop'
$startedUtc = [DateTime]::UtcNow.ToString('o')
$packageRoot = $PSScriptRoot
$invocationRoot = (Get-Location).Path
$expectedPin = '064f7ae92a8506689cd91aff5e6804a375d6ef3d'
$expectedArchiveHash = 'EB0AA77197DE1971D79AA0657C2AF5CF33B99BA8302A24BA44F3306CCA4BF92B'
$expectedOriginalHash = '571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423'

function Resolve-TaskPath {
    param([string] $Path, [string] $BasePath)
    if ([IO.Path]::IsPathRooted($Path)) {
        return [IO.Path]::GetFullPath($Path)
    }
    return [IO.Path]::GetFullPath((Join-Path $BasePath $Path))
}

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
            if ($backslashes -gt 0) {
                $null = $builder.Append(('\' * $backslashes))
                $backslashes = 0
            }
            $null = $builder.Append($character)
        }
    }
    if ($backslashes -gt 0) { $null = $builder.Append(('\' * ($backslashes * 2))) }
    $null = $builder.Append('"')
    return $builder.ToString()
}

$commands = [Collections.Generic.List[string]]::new()

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
    $timer = [Diagnostics.Stopwatch]::StartNew()
    if (-not $process.Start()) { throw "Failed to start $FileName" }
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    $stdout = $stdoutTask.GetAwaiter().GetResult()
    $stderr = $stderrTask.GetAwaiter().GetResult()
    $timer.Stop()
    $combined = $stdout + $stderr
    [IO.File]::WriteAllText($LogPath, $combined, [Text.UTF8Encoding]::new($false))
    return [pscustomobject]@{
        ExitCode = $process.ExitCode
        Output = $combined
        DurationSeconds = [Math]::Round($timer.Elapsed.TotalSeconds, 3)
    }
}

function Get-TreeManifest {
    param([string] $Root)
    $rootPath = [IO.Path]::GetFullPath($Root).TrimEnd([IO.Path]::DirectorySeparatorChar)
    $rows = [Collections.Generic.List[string]]::new()
    foreach ($file in Get-ChildItem -LiteralPath $rootPath -Recurse -Force -File | Sort-Object FullName) {
        $relative = $file.FullName.Substring($rootPath.Length + 1).Replace('\', '/')
        $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash
        $rows.Add("$relative`t$($file.Length)`t$hash")
    }
    return $rows
}

function Get-VariantText {
    param([string] $Name, [string] $Original, [string] $NewLine)
    $union = "type GameplayState =$NewLine    | Playing$NewLine    | Quit"
    $terminal = '        | Playing | Quit -> gameplay'
    if ([regex]::Matches($Original, [regex]::Escape($union)).Count -ne 1) {
        throw 'Expected exactly one GameplayState source block.'
    }
    if ([regex]::Matches($Original, [regex]::Escape($terminal)).Count -ne 1) {
        throw 'Expected exactly one terminal source clause.'
    }
    switch ($Name) {
        'baseline-explicit' { return $Original }
        'baseline-wildcard' { return $Original.Replace($terminal, '        | _ -> gameplay') }
        'paused-explicit' { return $Original.Replace($union, $union + "$NewLine    | Paused") }
        'paused-wildcard' {
            return $Original.Replace($union, $union + "$NewLine    | Paused").Replace($terminal, '        | _ -> gameplay')
        }
        default { throw "Unknown variant: $Name" }
    }
}

function Normalize-DiagnosticLine {
    param([string] $Line, [string] $SourceRoot, [string] $OutputRootPath)
    # MSBuild prints a diagnostic once with a node prefix such as `1>` and
    # again without it in the summary. Remove only that presentation prefix.
    $normalized = [regex]::Replace($Line, '^\s*[0-9]+>', '').Trim()
    $normalized = $normalized.Replace($SourceRoot, '<SOURCE_ROOT>')
    $normalized = $normalized.Replace($OutputRootPath, '<OUTPUT_ROOT>')
    return $normalized
}

$archive = Resolve-TaskPath -Path $NuArchive -BasePath $invocationRoot
$output = Resolve-TaskPath -Path $OutputRoot -BasePath $invocationRoot
if (-not (Test-Path -LiteralPath $archive -PathType Leaf)) { throw "Nu archive does not exist: $archive" }
if (Test-Path -LiteralPath $output) {
    if ($null -ne (Get-ChildItem -LiteralPath $output -Force | Select-Object -First 1)) {
        throw "OutputRoot is not empty; use a fresh directory: $output"
    }
}
$null = New-Item -ItemType Directory -Force -Path $output
$logs = Join-Path $output 'logs'
$sourceRoot = Join-Path $output 'source'
$privateInputs = Join-Path $output 'variant-sources'
$receipts = Join-Path $output 'assembly-receipts'
foreach ($directory in @($logs, $sourceRoot, $privateInputs, $receipts)) {
    $null = New-Item -ItemType Directory -Force -Path $directory
}

$archiveHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $archive).Hash
if ($archiveHash -ne $expectedArchiveHash) {
    throw "Archive hash mismatch. Expected $expectedArchiveHash; observed $archiveHash"
}

$env:DOTNET_CLI_HOME = Join-Path $output '.dotnet-home'
$env:NUGET_PACKAGES = Join-Path $output '.nuget-packages'
$env:DOTNET_NOLOGO = '1'
$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'

$version = Invoke-NativeLogged -FileName 'dotnet' -Arguments @('--version') -LogPath (Join-Path $logs 'dotnet-version.log') -WorkingDirectory $packageRoot
if ($version.ExitCode -ne 0 -or $version.Output.Trim() -ne '10.0.302') {
    throw "The pinned SDK did not resolve to 10.0.302. Observed: $($version.Output.Trim())"
}
$null = Invoke-NativeLogged -FileName 'dotnet' -Arguments @('--info') -LogPath (Join-Path $logs 'dotnet-info.log') -WorkingDirectory $packageRoot
$null = Invoke-NativeLogged -FileName 'dotnet' -Arguments @('fsi', '--version') -LogPath (Join-Path $logs 'fsi-version.log') -WorkingDirectory $packageRoot

$extract = Invoke-NativeLogged -FileName 'tar' -Arguments @('-xf', $archive, '-C', $sourceRoot) -LogPath (Join-Path $logs 'archive-extract.log') -WorkingDirectory $packageRoot
if ($extract.ExitCode -ne 0) { throw 'Archive extraction failed.' }

$gameplayPath = Join-Path $sourceRoot 'Projects/Breakout Mmcc/Gameplay.fs'
$projectPath = Join-Path $sourceRoot 'Projects/Breakout Mmcc/Breakout Mmcc.fsproj'
if (-not (Test-Path -LiteralPath $gameplayPath -PathType Leaf)) { throw 'Selected Gameplay.fs is missing after extraction.' }
if (-not (Test-Path -LiteralPath $projectPath -PathType Leaf)) { throw 'Breakout Mmcc.fsproj is missing after extraction.' }
$originalBytesHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $gameplayPath).Hash
if ($originalBytesHash -ne $expectedOriginalHash) {
    throw "Original Gameplay.fs hash mismatch. Expected $expectedOriginalHash; observed $originalBytesHash"
}
$originalText = [IO.File]::ReadAllText($gameplayPath)
$newLine = if ($originalText.Contains("`r`n")) { "`r`n" } else { "`n" }
$encoding = [Text.UTF8Encoding]::new($true)
$projectHashBefore = (Get-FileHash -Algorithm SHA256 -LiteralPath $projectPath).Hash
[IO.File]::Copy($gameplayPath, (Join-Path $privateInputs 'Gameplay.original.fs'))
[IO.File]::Copy($projectPath, (Join-Path $privateInputs 'Breakout Mmcc.fsproj'))

$manifestBefore = Get-TreeManifest -Root $sourceRoot
[IO.File]::WriteAllLines((Join-Path $output 'source-manifest-before.tsv'), $manifestBefore, [Text.UTF8Encoding]::new($false))

$propertyResult = Invoke-NativeLogged -FileName 'dotnet' -Arguments @(
    'msbuild', $projectPath, '-nologo', '-p:Configuration=Release', '-p:Platform=AnyCpu',
    '-getProperty:TargetFramework', '-getProperty:WarningLevel', '-getProperty:WarnOn',
    '-getProperty:NoWarn', '-getProperty:WarningsAsErrors', '-getProperty:TreatWarningsAsErrors'
) -LogPath (Join-Path $logs 'effective-properties.log') -WorkingDirectory $packageRoot
if ($propertyResult.ExitCode -ne 0) { throw 'Effective property query failed.' }

$expectedHashes = @{
    'baseline-explicit' = '571E2A5CE3F0630972F2FBE4E9A6A3C376BCF4D1A74589D14C882B2EE0DB1423'
    'baseline-wildcard' = '5FF5CB277FAD9359405EE0341C70837319221EC710F2178E632675A856E38566'
    'paused-explicit' = '8FD9F60DB811FF5E791F8B2FBB2EDEE6C11F732F98EBF67F33C30C31F78FCDC6'
    'paused-wildcard' = '9268684F8024D98E0C8BC6E802B12D1F87B21EE8E7C6CD11770A2780C9708630'
}
$expectedFs0025 = @{
    'baseline-explicit' = 0
    'baseline-wildcard' = 0
    'paused-explicit' = 1
    'paused-wildcard' = 0
}
$variants = @('baseline-explicit', 'baseline-wildcard', 'paused-explicit', 'paused-wildcard')
$resultRows = [Collections.Generic.List[string]]::new()
$resultRows.Add("variant`tgameplay_sha256`tbuild_exit`tbuild_seconds`tsummary_warnings`tsummary_errors`tunique_warnings`tunique_errors`tselected_fs0025`tall_fs0025`tassembly_version`tassembly_sha256`tprediction_pass")
$diagnosticRows = [Collections.Generic.List[string]]::new()
$diagnosticRows.Add("variant`tseverity`tcode`traw_count`tunique_count")
$allDiagnosticRows = [Collections.Generic.List[string]]::new()
$allDiagnosticRows.Add("variant`tseverity`tcode`tnormalized_diagnostic")
$mismatches = [Collections.Generic.List[string]]::new()

foreach ($variant in $variants) {
    $variantText = Get-VariantText -Name $variant -Original $originalText -NewLine $newLine
    [IO.File]::WriteAllText($gameplayPath, $variantText, $encoding)
    $variantHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $gameplayPath).Hash
    if ($variantHash -ne $expectedHashes[$variant]) {
        throw "$variant source hash mismatch. Expected $($expectedHashes[$variant]); observed $variantHash"
    }
    $variantInputDir = Join-Path $privateInputs $variant
    $null = New-Item -ItemType Directory -Force -Path $variantInputDir
    [IO.File]::Copy($gameplayPath, (Join-Path $variantInputDir 'Gameplay.fs'))

    $caseArtifacts = Join-Path $output "build/$variant"
    $buildLog = Join-Path $logs "$variant.build.log"
    $build = Invoke-NativeLogged -FileName 'dotnet' -Arguments @(
        'build', $projectPath, '--configuration', 'Release', '--nologo', '--verbosity', 'normal',
        '--artifacts-path', $caseArtifacts, '-p:Platform=AnyCpu', '-p:PostBuildEvent='
    ) -LogPath $buildLog -WorkingDirectory $packageRoot

    $rawDiagnostics = [Collections.Generic.List[object]]::new()
    foreach ($line in ($build.Output -split "`r?`n")) {
        if ($line -match '(?i)(?<severity>warning|error) (?<code>[A-Z]+[0-9]+):') {
            $normalized = Normalize-DiagnosticLine -Line $line -SourceRoot $sourceRoot -OutputRootPath $output
            $rawDiagnostics.Add([pscustomobject]@{
                Severity = $matches.severity.ToLowerInvariant()
                Code = $matches.code.ToUpperInvariant()
                Normalized = $normalized
                Original = $line
            })
        }
    }
    $uniqueDiagnostics = @($rawDiagnostics | Sort-Object Severity, Code, Normalized -Unique)
    $rawLinesPath = Join-Path $logs "$variant.diagnostic-lines.log"
    [IO.File]::WriteAllLines($rawLinesPath, @($rawDiagnostics | ForEach-Object { $_.Original }), [Text.UTF8Encoding]::new($false))

    foreach ($group in $rawDiagnostics | Group-Object Severity, Code) {
        $first = $group.Group[0]
        $uniqueCount = @($group.Group | Select-Object -ExpandProperty Normalized -Unique).Count
        $diagnosticRows.Add("$variant`t$($first.Severity)`t$($first.Code)`t$($group.Count)`t$uniqueCount")
    }
    foreach ($diagnostic in $uniqueDiagnostics) {
        $safe = $diagnostic.Normalized.Replace("`t", ' ')
        $allDiagnosticRows.Add("$variant`t$($diagnostic.Severity)`t$($diagnostic.Code)`t$safe")
    }

    $summaryWarnings = ''
    $summaryErrors = ''
    $warningMatches = [regex]::Matches($build.Output, '(?m)^\s*(?<count>[0-9]+) Warning\(s\)\s*$')
    $errorMatches = [regex]::Matches($build.Output, '(?m)^\s*(?<count>[0-9]+) Error\(s\)\s*$')
    if ($warningMatches.Count -gt 0) { $summaryWarnings = $warningMatches[$warningMatches.Count - 1].Groups['count'].Value }
    if ($errorMatches.Count -gt 0) { $summaryErrors = $errorMatches[$errorMatches.Count - 1].Groups['count'].Value }
    $uniqueWarnings = @($uniqueDiagnostics | Where-Object { $_.Severity -eq 'warning' }).Count
    $uniqueErrors = @($uniqueDiagnostics | Where-Object { $_.Severity -eq 'error' }).Count
    $allFs0025 = @($uniqueDiagnostics | Where-Object { $_.Code -eq 'FS0025' }).Count
    $selectedFs0025 = @($uniqueDiagnostics | Where-Object {
        $_.Code -eq 'FS0025' -and $_.Original.IndexOf($gameplayPath, [StringComparison]::OrdinalIgnoreCase) -ge 0
    }).Count

    $assemblyVersion = ''
    $assemblyHash = ''
    if ($build.ExitCode -eq 0) {
        $assemblyCandidates = @(Get-ChildItem -LiteralPath $caseArtifacts -Recurse -File -Filter 'Breakout Mmcc.dll' | Where-Object {
            $_.FullName -match '[\\/]bin[\\/]' -and $_.FullName -notmatch '[\\/]ref[\\/]'
        })
        if ($assemblyCandidates.Count -ne 1) {
            $mismatches.Add("$variant expected one output assembly, found $($assemblyCandidates.Count)")
        }
        else {
            $assembly = $assemblyCandidates[0]
            $assemblyHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $assembly.FullName).Hash
            $assemblyVersion = [Reflection.AssemblyName]::GetAssemblyName($assembly.FullName).Version.ToString()
            $receiptDir = Join-Path $receipts $variant
            $null = New-Item -ItemType Directory -Force -Path $receiptDir
            [IO.File]::Copy($assembly.FullName, (Join-Path $receiptDir 'Breakout Mmcc.dll'))
        }
    }

    $predictionPass = $build.ExitCode -eq 0 -and $selectedFs0025 -eq $expectedFs0025[$variant]
    if (-not $predictionPass) {
        $mismatches.Add("$variant predicted build/selected-FS0025 0/$($expectedFs0025[$variant]); observed $($build.ExitCode)/$selectedFs0025")
    }
    $resultRows.Add("$variant`t$variantHash`t$($build.ExitCode)`t$($build.DurationSeconds)`t$summaryWarnings`t$summaryErrors`t$uniqueWarnings`t$uniqueErrors`t$selectedFs0025`t$allFs0025`t$assemblyVersion`t$assemblyHash`t$predictionPass")
    Write-Output "$variant build_exit=$($build.ExitCode) warnings=$summaryWarnings errors=$summaryErrors selected_fs0025=$selectedFs0025 seconds=$($build.DurationSeconds)"
}

[IO.File]::WriteAllText($gameplayPath, $originalText, $encoding)
$restoredHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $gameplayPath).Hash
if ($restoredHash -ne $expectedOriginalHash) { $mismatches.Add("Gameplay.fs was not restored: $restoredHash") }
$projectHashAfter = (Get-FileHash -Algorithm SHA256 -LiteralPath $projectPath).Hash
if ($projectHashAfter -ne $projectHashBefore) { $mismatches.Add('Breakout project file changed during the run.') }

$manifestAfter = Get-TreeManifest -Root $sourceRoot
[IO.File]::WriteAllLines((Join-Path $output 'source-manifest-after.tsv'), $manifestAfter, [Text.UTF8Encoding]::new($false))
$manifestDifference = @(Compare-Object -ReferenceObject $manifestBefore -DifferenceObject $manifestAfter)
[IO.File]::WriteAllLines((Join-Path $output 'source-manifest-diff.txt'), @($manifestDifference | ForEach-Object { "$( $_.SideIndicator )`t$( $_.InputObject )" }), [Text.UTF8Encoding]::new($false))
if ($manifestDifference.Count -ne 0) { $mismatches.Add("Extracted source tree changed outside retained variant snapshots: $($manifestDifference.Count) manifest differences") }

[IO.File]::WriteAllLines((Join-Path $output 'results.tsv'), $resultRows, [Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllLines((Join-Path $output 'diagnostic-counts.tsv'), $diagnosticRows, [Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllLines((Join-Path $output 'all-diagnostics.tsv'), $allDiagnosticRows, [Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllLines((Join-Path $output 'commands.log'), $commands, [Text.UTF8Encoding]::new($false))

$dotnetCommand = (Get-Command dotnet).Source
$fscPath = Join-Path (Split-Path $dotnetCommand -Parent) 'sdk/10.0.302/FSharp/fsc.dll'
$fscMetadata = $null
if (Test-Path -LiteralPath $fscPath -PathType Leaf) {
    $fscMetadata = [ordered]@{
        product_version = (Get-Item -LiteralPath $fscPath).VersionInfo.ProductVersion
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $fscPath).Hash
    }
}
$metadata = [ordered]@{
    started_utc = $startedUtc
    completed_utc = [DateTime]::UtcNow.ToString('o')
    expected_pin = $expectedPin
    archive_sha256 = $archiveHash
    original_gameplay_sha256 = $originalBytesHash
    restored_gameplay_sha256 = $restoredHash
    project_sha256_before = $projectHashBefore
    project_sha256_after = $projectHashAfter
    source_manifest_entries = $manifestBefore.Count
    source_manifest_differences = $manifestDifference.Count
    sdk_version = $version.Output.Trim()
    fsc = $fscMetadata
    build_path_adaptation = 'PostBuildEvent cleared; distinct --artifacts-path per variant'
    package_cache_policy = 'one task-private cache shared by the four builds'
    result_mismatches = @($mismatches)
}
[IO.File]::WriteAllText((Join-Path $output 'run-metadata.json'), ($metadata | ConvertTo-Json -Depth 6), [Text.UTF8Encoding]::new($false))

$resultRows | ForEach-Object { Write-Output $_ }
Write-Output "Output retained at: $output"
if ($mismatches.Count -ne 0) {
    throw "Probe mismatch: $($mismatches -join '; ')"
}
