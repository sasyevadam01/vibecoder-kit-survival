---
name: preflight-antislop-checker
description: Pre-flight validator rules to audit documentation and codebases, blocking AI-generated filler text, em-dashes, and forbidden fonts.
---

# Pre-Flight Anti-Slop Validator

## Overview

Automated systems can generate repetitive filler text, non-standard punctuation, and incorrect typography. The Pre-Flight Anti-Slop Checker defines command-line validation rules to scan files prior to commit or deployment, blocking typical AI clichés, em-dashes, and forbidden fonts.

## Validation Targets

The pre-flight script scans files against three primary classes of violations:

1. **AI Clichés (Slop Words)**: Repetitive filler words that indicate low-quality generation (e.g., *delve*, *testament*, *tapestry*, *furthermore*).
2. **Forbidden Fonts**: Brand violations (unapproved standard system sans-serif fonts). Only Outfit and Plus Jakarta Sans are approved.
3. **Typography Punctuation**: Violations of the absolute ban on em-dashes (unicode character \u2014) and en-dashes (unicode character \u2013). Only simple hyphens (-) or colons (:) are allowed.

## Regex Scan Rules and Match Criteria

You can execute these audits using standard search tools (`ripgrep`, `grep`, or PowerShell).

### 1. AI Cliché Detection Pattern
- **Target Terms**: `delve`, `testament`, `tapestry`, `moreover`, `furthermore`, `realm`, `demystify`, `beacon`
- **Regex Pattern**: `(?i)\b(delve|testament|tapestry|moreover|furthermore|realm|demystify|beacon)\b`
- **Action**: Return an error if any files contain these terms.

### 2. Forbidden Fonts Pattern
- **Target Terms**: `StandardSansA`, `StandardSansB`, `StandardSansC`
- **Regex Pattern**: `(?i)(standardsansa|standardsansb|standardsansc)`
- **Action**: Block commits containing styling blocks or references pointing to these font assets.

### 3. Em-Dash and En-Dash Punctuation Pattern
- **Target Characters**: unicode \u2014 (em-dash), unicode \u2013 (en-dash)
- **Regex Pattern**: `[\u2013\u2014]`
- **Action**: Block execution immediately. Force replacement with a standard hyphen (`-`).

---

## The Audit Script (PowerShell Validator)

This PowerShell script compiles these rules into an executable validation hook. Add this script to your CI pipeline or local pre-commit hook.

```powershell
# =====================================================================
# PRE-FLIGHT ANTI-SLOP AUDITOR
# =====================================================================

$TargetDirectory = "$PSScriptRoot/.."
$ViolationsFound = 0

# 1. Compile Audit Rules
$Rules = @{
    "AI Cliché Pattern" = "(?i)\b(delve|testament|tapestry|moreover|furthermore|realm|demystify|beacon)\b"
    "Forbidden Fonts"   = "(?i)(standardsansa|standardsansb|standardsansc)"
    "Dash Violations"   = "[\u2013\u2014]"
}

# Find all markdown and code files
$ScanFiles = Get-ChildItem -Path $TargetDirectory -Recurse -Include *.md, *.js, *.py, *.css, *.html -Exclude *preflight*

Write-Host "Starting Pre-Flight Anti-Slop Audit..." -ForegroundColor Cyan

foreach ($File in $ScanFiles) {
    $Content = Get-Content -Raw -Path $File.FullName
    if ([string]::IsNullOrEmpty($Content)) { continue }

    foreach ($RuleName in $Rules.Keys) {
        $Pattern = $Rules[$RuleName]
        if ($Content -match $Pattern) {
            $LineMatches = Select-String -Path $File.FullName -Pattern $Pattern
            foreach ($Match in $LineMatches) {
                Write-Error "Violation [$RuleName] detected in: $($File.Name) at line $($Match.LineNumber): '$($Match.Line.Trim())'"
                $ViolationsFound++
            }
        }
    }
}

if ($ViolationsFound -gt 0) {
    Write-Host "`nAudit Failed: $ViolationsFound violation(s) detected!" -ForegroundColor Red
    Exit 1
} else {
    Write-Host "`nAudit Passed: Documentation and Code are clean!" -ForegroundColor Green
    Exit 0
}
```
