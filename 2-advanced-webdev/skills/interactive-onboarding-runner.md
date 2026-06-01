---
name: interactive-onboarding-runner
description: Client-side sandboxed architecture guidelines for executing untrusted user code in highly secure, isolated iframe environments.
---

# Interactive Onboarding Sandbox Runner

## Overview

When building onboarding applications, developers often need to execute user-submitted JavaScript snippets client-side. Doing this safely requires a robust sandboxed architecture. By combining secure HTML5 `iframe` attributes with communication boundaries via standard Web APIs, you can evaluate untrusted scripts without compromising the main application context.

## Threat Model and Isolation Strategy

Executing untrusted code client-side presents risks like Cross-Site Scripting (XSS), DOM theft, cookies access, and page redirection. The sandboxed iframe runner addresses these via three primary boundaries:

1. **Host-Guest Separation**: The untrusted code is executed inside a guest context with a null origin.
2. **Resource Constraints**: The iframe prevents access to storage (local/session storage) and top-level page navigation.
3. **Execution Limits**: The execution is moved off the main thread where possible or constrained using strict sandbox policies.

```
+--------------------------------------------------------+
| Main Window (Host App)                                 |
| - Domain: app.yoursite.com                             |
| - Controls UI, displays feedback                       |
+--------------------------------------------------------+
                           |  (via postMessage)
                           v
+--------------------------------------------------------+
| Sandboxed iframe (Guest)                               |
| - srcdoc = isolated HTML wrapper                       |
| - sandbox="allow-scripts"                              |
| - Executes code & handles outputs                      |
+--------------------------------------------------------+
```

## The Iframe Sandbox Setup

To prevent the sandbox from accessing the host origin, configure the `iframe` element using strict sandbox flags.

### Required Attributes

- `sandbox="allow-scripts"`: Absolutely required. This allows execution of scripts while omitting `allow-same-origin`, forcing the iframe into a unique, null origin.
- `srcdoc`: Embedded HTML content containing the compiler/worker bridge. Using `srcdoc` ensures the document runs inside the unique null origin rather than inheriting the parent host domain.

```html
<iframe
  id="sandbox-frame"
  sandbox="allow-scripts"
  srcdoc="<!-- Embedded runner code goes here -->"
  style="display: none;"
></iframe>
```

## Security Protocols

- **Origin Validation**: When receiving messages inside the host page, always check `event.origin` or `event.source`. For `sandbox="allow-scripts"` contexts without `allow-same-origin`, the origin is returned as the string `"null"`. Therefore, your message handler must implement unique identifier mapping to correlate requests and responses.
- **Payload Sanitization**: Ensure code is passed as pure string data. Never execute functions passed directly as objects across communication portals.
- **Communication Flow**:
  1. The **Host Window** sends a structured message: `{ type: "EXECUTE", code: "return 1 + 2;", id: "req-101" }`.
  2. The **Sandboxed Iframe** executes the code inside a Web Worker or a scoped eval structure.
  3. The **Sandboxed Iframe** replies to the host window using `window.parent.postMessage({ type: "RESULT", data: 3, id: "req-101" }, "*")`.
