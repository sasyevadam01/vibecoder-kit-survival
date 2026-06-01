---
name: local-seo-whatsapp-marketing
description: Technical guide to local SEO NAP optimization, structured JSON-LD schema injection, and WhatsApp decision tree marketing engines.
---

# Local SEO and WhatsApp Marketing Integration

## Overview

For businesses targeting physical territories, integrating local search engine optimization with conversational messaging channels increases local visibility and customer conversion. This document outlines NAP (Name, Address, Phone) consistency principles, structured JSON-LD schema setups, and conversational decision trees for WhatsApp automation.

## NAP Consistency Optimization

Search engines rely on directory consistency to verify a business's coordinates.

1. **Name**: Use the official, legal business name. Avoid appending descriptive keywords unless they are registered parts of the brand.
2. **Address**: Format addresses identically across Google Business Profile, Apple Maps, Bing Places, and directory databases.
3. **Phone**: Provide a primary local phone number with your country code. Avoid using toll-free numbers for local directories, as they dilute regional signals.

## Structured Data (JSON-LD LocalBusiness Schema)

Embed the following JSON-LD script inside the global HTML header to supply search engine crawlers with direct structured business data.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Global Tech Services",
  "image": "https://www.yourdomain.com/assets/logo.png",
  "@id": "https://www.yourdomain.com/#professional-service",
  "url": "https://www.yourdomain.com",
  "telephone": "+1-800-555-0199",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "100 Innovation Boulevard, Suite 300",
    "addressLocality": "Austin",
    "addressRegion": "TX",
    "postalCode": "78701",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 30.2672,
    "longitude": -97.7431
  },
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": [
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday"
    ],
    "opens": "09:00",
    "closes": "18:00"
  }
}
</script>
```

## WhatsApp Decision Tree Marketing

WhatsApp marketing requires highly structured, permission-based workflows. The following state chart maps out a client onboarding decision tree.

```
       [User sends "START" or scans QR]
                       |
                       v
     [State 1: Send Opt-In & Language Menu]
                       |
        +--------------+--------------+
        |                             |
     [User clicks "YES"]        [User clicks "NO"]
        |                             |
        v                             v
[State 2: Send Main Menu]      [State 4: Send Opt-Out Confirmation]
 - 1. Book Appointment         "No problem. We won't message you again."
 - 2. Read FAQ
 - 3. Talk to human
        |
        +---> Choose Option 1 ---> [State 3: Provide booking link]
```

### Scripted Rules for WhatsApp Automations
- **Consent First**: Never message a user without active opt-in. Keep records of opt-in metadata (timestamp and IP).
- **Fallback Trigger**: If the user sends raw text instead of selecting quick-reply buttons, the system must trigger an automatic fallback: "I didn't quite catch that. Please select one of the options below or reply with 'HELP'."
- **Exit Keyword**: Ensure the system responds to exit keywords like "STOP", "UNSUBSCRIBE", or "EXIT" at any point, instantly setting their contact status to unsubscribed in your CRM database.
