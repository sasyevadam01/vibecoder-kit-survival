---
name: crm-deliverability-expert
description: Advanced setup configurations for email deliverability (SPF, DKIM, DMARC), GDPR/AI Act compliance protocols, and CRM intelligent agent architectures.
---

# CRM Deliverability and Compliance Expert

## Overview

High-performance customer relationship management requires pristine domain reputation and strict legal compliance. This document details the technical setup for SPF, DKIM, and DMARC protocols, frameworks for adhering to the EU GDPR and AI Act, and the functional logic for a CRM AI routing agent.

## Email Deliverability Architecture (DNS Setup)

To prevent outbound CRM communications from landing in spam folders, your sending domains must implement SPF, DKIM, and DMARC authentication records.

### 1. SPF (Sender Policy Framework)
An SPF record is a TXT record added to your DNS zone that lists the specific servers allowed to send mail on behalf of your domain.

- **Record Type**: TXT
- **Host**: `@` (or domain root)
- **Standard Value**: `v=spf1 include:mailgun.org include:sendgrid.net -all`
- **Explanation**: The `-all` directive ensures hard failure for any unauthorized sending IPs.

### 2. DKIM (DomainKeys Identified Mail)
DKIM provides cryptographic proof of sending authorization via a public-private key pair.

- **Record Type**: TXT
- **Host**: `s1._domainkey` (or your provider selector)
- **Value**: `v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0y6X...` (containing your public key payload)

### 3. DMARC (Domain-based Message Authentication, Reporting, and Conformance)
DMARC ties SPF and DKIM signatures together, instructing receiving servers how to handle alignment failures.

- **Record Type**: TXT
- **Host**: `_dmarc.yourdomain.com`
- **Standard Strict Policy**: `v=DMARC1; p=reject; pct=100; rua=mailto:dmarc-reports@yourdomain.com; ruf=mailto:dmarc-failures@yourdomain.com`
- **Explanation**: Setting `p=reject` enforces immediate blocking of non-aligned mail, while `rua` aggregates activity logs.

## GDPR and EU AI Act Compliance

Using AI within your CRM requires rigorous safeguard checkpoints to maintain privacy and structural compliance.

### GDPR Compliance Checkpoints
- **Article 22 (Automated Individual Decision-making)**: Users have a right not to be subject to a decision based solely on automated processing. Your CRM must provide an explicit "Opt-out of automated profiling" path and include a human-in-the-loop review workflow.
- **Article 17 (Right to Erasure)**: An automated workflow must cascade data-deletion commands to all integrated sub-processors (databases, vector stores, caching nodes) within 30 days.

### EU AI Act Compliance Checklist
- **System Classification**: CRM text classifiers fall into the minimal or low-risk category under standard workflows, but profiling systems used for recruiting or evaluating performance can be classified as high-risk.
- **Transparency Rules**: CRM bots must explicitly announce themselves to customers: "Hello, I am a virtual assistant." It must be instantly clear that the user is interacting with an AI agent.

## CRM Intelligent Agent Routing Engine

The CRM AI Agent analyzes incoming inquiries, parses sentiment, classifies topics, and routes messages to the correct department or triggers automated sequences.

### Decision Flow

```
[Inbound Email] ---> [SPF/DKIM/DMARC Validation]
                            |
                            +---> Pass ---> [GDPR Consent Verification]
                                                |
                                                +---> Approved ---> [AI Classifier Engine]
                                                                        |
                                         +------------------------------+-------------------------+
                                         |                              |                         |
                                         v                              v                         v
                                 [High-Risk Alert]             [Standard Support]         [Lead Opportunity]
                                 Route to Humans               Auto-suggest reply         Route to Sales
```

### Reference Prompt Template for Classification
```text
Role: CRM Inbound Intelligent Router
Font Guidelines Enforced: Outfit for text blocks, Plus Jakarta Sans for titles.

Instructions:
Categorize the incoming customer email strictly by department (Sales, Technical, Compliance, Spam).
Return JSON output with fields: 'category', 'urgency' (high/medium/low), and 'rationale'.
Ensure no regional slang or references are included in the rationale.
```
