# UI Observations Template

## Purpose
Capture observations from a provided Figma reference without redesigning the experience.

Automatically consume Figma URL from `specification.md` if present. If absent, continue normally without warnings.

## Metadata
- Version: [Version]
- Author: [Author]
- Date: [Date]
- Status: [Draft | In Review | Approved]
- Workflow ID: [Workflow ID]
- Figma Reference: [URL]

## Figma Design Intake
- Design Extraction Status: [Direct asset export available | URL only | Pending]
- Typography: [Type scale, font families, weights, leading, letter spacing]
- Spacing: [Spacing scale, layout grid, padding, gaps, margins]
- Color Tokens: [Primary, secondary, surface, text, border, feedback, semantic colors]
- Iconography: [Icon set, size rules, usage patterns, states]
- Component States: [Default, hover, focus, active, disabled, selected, loading, empty, error, success]
- Screen Coverage: [List of screens covered by the design reference]
- Interaction Notes: [Primary interactions, hover/focus/selected/error/loading/empty states]
- Responsive Notes: [Breakpoints, stack behavior, overflow expectations]
- Accessibility Notes: [Contrast, focus visibility, semantics, reduced motion expectations]
- Missing Design Details: [Any details not yet available from the design reference]

## Screen Contracts
- Screen Name: [Name]
- Purpose: [Purpose]
- Business Goal: [Goal]
- Navigation: [From -> Trigger -> To]
- User Actions: [Required actions]
- Required Fields: [Business fields]
- Validation Expectations: [Business-visible validation behavior]
- Permission Visibility: [Who can view/act and when]
- Empty State: [Expected user-visible behavior]
- Success State: [Expected user-visible behavior]
- Error State: [Expected user-visible behavior]
- Accessibility Expectations: [Business-level accessibility expectations]
- Responsive Expectations: [Business-level responsiveness expectations]
- Visual Detail Notes: [Layout, spacing, hierarchy, component patterns, notable states]
- Default Route (mandatory): [The literal screen/route shown when no authenticated session exists]
- Unauthenticated Access Behavior (mandatory): [What happens if a protected screen/route is requested without a session]

## OpenLog References
- Raise only necessary UI questions in `openlog.md`.

## Rules
- Describe business behavior only.
- Do not prescribe implementation.
- Keep this artifact focused on the user experience, navigation, and screen-level behavior; do not duplicate the detailed element inventory captured in screen-elements.md.
