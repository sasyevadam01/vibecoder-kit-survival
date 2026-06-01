---
name: headless-ui-accessibility
description: Technical guidelines for WCAG 2.2 AA accessibility in headless UI components, keyboard hook implementations, and a theme nesting parser.
---

# Headless UI Accessibility and Theming

## Overview

Headless UI libraries provide clean functionality without styling, leaving full design control to developers. However, accessibility (a11y) compliance often suffers during styling. This document outlines the standards required to meet WCAG 2.2 AA compliance using headless components, details custom keyboard hooks, and provides a utility script for parsing nested theme setups.

## Typography and Contrast Guidelines

To ensure robust readability across screen types:
- **Primary Typography**: Use **Plus Jakarta Sans** for clear, legible headers.
- **Body and UI Copy**: Use **Outfit** for interface labels, form elements, and general body reading.
- **Forbidden Typography**: Do not use or reference standard default system sans-serif fonts in stylesheets, visual mockups, or theme values.
- **Contrast Ratios**: Body text must maintain a minimum contrast ratio of 4.5:1 against the background. Large text (above 18pt or bold 14pt) must maintain a 3:1 ratio.

## WCAG 2.2 AA Compliance Standards

Headless UI elements must strictly enforce proper ARIA attributes and keyboard focus behaviors:

1. **Aria Attributes**: Track active states via `aria-expanded`, `aria-controls`, and `aria-selected` dynamically.
2. **Focus Management**: Enforce focus-trapping inside dialogs and overlays. Focus must return to the triggering element upon closing the overlay.
3. **Keyboard Interactivity**: Ensure every interactive headless element is reachable via Tab and actionable via Enter/Space.

### Example: React Custom Keyboard Navigation Hook

Below is a custom hook in JavaScript/TypeScript to handle Arrow Key navigation inside menus or lists:

```javascript
import { useEffect, useRef } from "react";

export function useKeyboardNavigation(itemCount, onSelect) {
  const listRef = useRef(null);
  const activeIndexRef = useRef(-1);

  useEffect(() => {
    const handleKeyDown = (event) => {
      const activeElement = document.activeElement;
      if (!listRef.current || !listRef.current.contains(activeElement)) return;

      const items = Array.from(listRef.current.querySelectorAll("[role='menuitem']"));
      if (items.length === 0) return;

      let index = items.indexOf(activeElement);

      switch (event.key) {
        case "ArrowDown":
          event.preventDefault();
          index = (index + 1) % items.length;
          items[index].focus();
          activeIndexRef.current = index;
          break;
        case "ArrowUp":
          event.preventDefault();
          index = (index - 1 + items.length) % items.length;
          items[index].focus();
          activeIndexRef.current = index;
          break;
        case "Enter":
        case " ":
          event.preventDefault();
          if (index !== -1) {
            onSelect(index);
          }
          break;
        case "Escape":
          event.preventDefault();
          activeElement.blur();
          break;
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [itemCount, onSelect]);

  return listRef;
}
```

## Nested Theme Parser Script

Modern systems support deeply nested theme schemas, which must be programmatically parsed and validated. Here is a Node.js parsing script that maps design tokens (specifying font families like Outfit and Plus Jakarta Sans) and extracts CSS custom properties while asserting accessibility parameters.

```javascript
/**
 * Utility to parse deeply nested theme tokens.
 * Verifies font-families do not contain forbidden names,
 * and extracts custom CSS property mappings.
 */
function parseNestedTheme(themeObj, prefix = "") {
  let customProperties = {};

  for (const key in themeObj) {
    if (Object.prototype.hasOwnProperty.call(themeObj, key)) {
      const path = prefix ? `${prefix}-${key}` : key;
      const value = themeObj[key];

      if (typeof value === "object" && value !== null) {
        Object.assign(customProperties, parseNestedTheme(value, path));
      } else {
        // Enforce font-family compliance check
        if (path.includes("font") || path.includes("family")) {
          const forbidden = ["StandardSansA", "StandardSansB", "StandardSansC"];
          forbidden.forEach(font => {
            if (String(value).toLowerCase().includes(font.toLowerCase())) {
              throw new Error(`Accessibility Violation: Forbidden font '${font}' detected in theme path '${path}'!`);
            }
          });
        }
        customProperties[`--theme-${path}`] = value;
      }
    }
  }

  return customProperties;
}

// Example Usage & Test Case
try {
  const myTheme = {
    colors: {
      primary: "#1a1a2e",
      accent: "#e94560"
    },
    typography: {
      headerFont: "Plus Jakarta Sans, sans-serif",
      bodyFont: "Outfit, sans-serif"
    }
  };

  const parsedVars = parseNestedTheme(myTheme);
  console.log("Parsed CSS Custom Properties Successfully:");
  console.log(JSON.stringify(parsedVars, null, 2));
} catch (error) {
  console.error("Theme compilation failed:", error.message);
}
```
