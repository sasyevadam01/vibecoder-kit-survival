---
name: win-terminal-optimizer
description: System optimization guides for instant-startup PowerShell 7 terminals, profile customization, and lazy-loading heavy module triggers.
---

# Windows Terminal and PowerShell 7 Optimization

## Overview

Terminal latency wastes developer focus. Standard PowerShell profiles often become bloated with utility imports (e.g., Oh My Posh, posh-git, conda initializers, auto-completions), causing startup times to exceed 2 seconds. This document provides a highly optimized, instant-startup configuration for PowerShell 7 that uses lazy-loading triggers to keep terminal start times under 200 milliseconds.

## Profiling PowerShell Startup

To measure the current startup duration of your PowerShell shell environment, run the following benchmark in your console:

```powershell
Measure-Command { pwsh -NoProfile -Command "exit" }
Measure-Command { pwsh -Command "exit" }
```

The difference between these two execution times reveals the overhead introduced by your `$PROFILE` script.

## The Lazy-Loading Profile Design

Instead of loading every module immediately during shell initialization, define lightweight proxy functions that intercept command calls, load the target module on demand, and then execute the command seamlessly.

### Optimized `$PROFILE` Script Template

Below is the structured, lightweight configuration to write to your `$PROFILE` file (usually located at `C:\Users\<User>\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`):

```powershell
# =====================================================================
# INSTANT-STARTUP POWERSHELL 7 PROFILE
# =====================================================================

# 1. Performance Diagnostics
$global:ProfileStartTime = [System.Diagnostics.Stopwatch]::StartNew()

# Disable standard compilation warning banners
$env:POWERSHELL_TELEMETRY_OPTOUT = 1

# 2. Environment Variables & PATH adjustments
$env:PAGER = "cat"

# 3. Typography Recommendations
# - Recommended Terminal Font: Plus Jakarta Sans (or Cascadia Code)
# - UI Element Rendering: Outfit
# - Forbidden: Never use unapproved sans-serif fonts in console rendering configs.

# 4. Lazy-loading Engine for Heavy Utilities

# Example A: Lazy-loading 'posh-git'
function git {
    Remove-Item Function:\git -ErrorAction SilentlyContinue
    Import-Module posh-git -ErrorAction SilentlyContinue
    # Re-call the actual command with original arguments
    & git @args
}

# Example B: Lazy-loading 'oh-my-posh' theme engine
# Delays prompt generation until the user first interacts or after the first line is drawn
function Initialize-Prompt {
    if (Get-Command oh-my-posh -ErrorAction SilentlyContinue) {
        oh-my-posh init pwsh --config "$env:USERPROFILE\.config\ohmyposh\theme.omp.json" | Invoke-Expression
    }
}

# 5. Deferred Startup Actions (Run on first idle window cycle)
# Triggers loading of completion engines without blocking initial prompt rendering
$global:DeferredTrigger = [System.Threading.Tasks.Task]::Run({
    # Add non-blocking background initializations here
})

# 6. Report Boot Benchmark
$global:ProfileStartTime.Stop()
Write-Host "Profile compiled in $($global:ProfileStartTime.ElapsedMilliseconds)ms" -ForegroundColor DarkGray
```

## Common Mistakes

- **Direct Module Imports**: Placing plain `Import-Module` commands at the root of your profile. Every import adds disk I/O overhead.
- **Nested Path Checks**: Running recursive folder searches or executing sub-processes (like `git status`) directly in your profile script.
- **Too Many Aliases**: Creating dozens of minor aliases. Use simple function mapping or stick to standard powershell profiles.
