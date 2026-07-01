# UI/UX Developer Skills

This document defines reusable capabilities for the UI/UX Developer agent in interface design and user experience.

---

## Skill: Generate UI Structure

### Purpose
Create the structural blueprint of the user interface, defining pages, sections, layouts, and component hierarchy.

### When to Use
- Designing page layouts from requirements
- Defining screen hierarchies
- Planning responsive layouts
- Creating wireframes or structural specifications

### Inputs
- `features` (array): Features requiring UI
- `user_workflows` (array): User journeys and tasks
- `content_model` (object): Data to display
- `device_targets` (array, optional): Target devices/screen sizes
- `design_system` (object, optional): UI component library to use

### Outputs
- `page_structures` (array): Layout of each page/screen
- `component_hierarchy` (object): Component structure
- `layout_specs` (array): Layout definitions (grids, spacing, etc.)
- `responsive_definitions` (object): Breakpoints and responsive behavior
- `wireframes` (array): Wireframe descriptions

### Dependencies
- Features and requirements clear
- User workflows understood
- Content/data model defined

### Execution Steps
1. Map user workflows to pages/screens
2. Identify content to display on each page
3. Organize content into logical sections
4. Define component hierarchy
5. Design responsive breakpoints
6. Create layout specifications
7. Define spacing and alignment rules
8. Plan navigation between pages
9. Document layout rationale

### Validation Checklist
- [ ] All features have corresponding UI
- [ ] User workflows map to page flows
- [ ] Content is organized logically
- [ ] Responsive behavior defined for all breakpoints
- [ ] Layout follows design system conventions
- [ ] Accessibility considered in structure

### Success Criteria
- UI structure supports all user workflows
- Layout is responsive across devices
- Structure is implementable
- Clear hierarchy of information

### Failure Conditions
- User workflows not supported
- Responsive behavior undefined
- Content organization confusing
- Component hierarchy unclear
- Too many pages/components

---

## Skill: Define Navigation Flow

### Purpose
Design how users move through the interface, specifying navigation patterns, transitions, and information architecture.

### When to Use
- Planning user navigation through features
- Designing information architecture
- Defining navigation patterns (tabs, menus, breadcrumbs, etc.)
- Planning user workflows

### Inputs
- `user_workflows` (array): User tasks and journeys
- `pages` (array): All pages/screens in the system
- `features` (array): Features and their relationships
- `user_mental_models` (object, optional): How users think about information

### Outputs
- `navigation_structure` (object): Information architecture
- `navigation_patterns` (array): Navigation UI patterns used
- `user_flows` (array): Flow diagrams for each user journey
- `breadcrumb_definitions` (array): Breadcrumb hierarchies
- `menu_structures` (array): Menu organization and items

### Dependencies
- Pages and features defined
- User workflows understood
- Mental models of target users

### Execution Steps
1. Analyze user tasks and workflows
2. Define information hierarchy
3. Identify natural groupings for navigation
4. Select appropriate navigation patterns
5. Design primary and secondary navigation
6. Plan breadcrumb hierarchies if applicable
7. Define transitions between pages
8. Create user flow diagrams
9. Validate flows with user workflows

### Validation Checklist
- [ ] Navigation supports all user tasks
- [ ] Information hierarchy is logical
- [ ] Navigation is consistent
- [ ] Users can reach any page in few clicks
- [ ] Navigation patterns are appropriate for content
- [ ] Flow supports mobile and desktop views

### Success Criteria
- Users can complete tasks efficiently
- Navigation is intuitive
- No dead ends or confusing paths
- Users know where they are (context)
- Users know how to get where they want to go

### Failure Conditions
- Users lost or confused about location
- Important pages hard to reach
- Navigation inconsistent
- Too many navigation options
- Workflows require too many steps

---

## Skill: Generate Component Layout

### Purpose
Design the detailed layout and styling of individual UI components, defining their structure, states, and responsive behavior.

### When to Use
- Designing buttons, forms, cards, etc.
- Specifying component styling
- Defining component states
- Planning component interactions

### Inputs
- `components` (array): Components to design
- `design_system` (object, optional): Design tokens and guidelines
- `accessibility_requirements` (object): Accessibility standards to meet
- `responsive_definitions` (object): Responsive behavior requirements

### Outputs
- `component_layouts` (array): Component layout specifications
- `component_states` (object): Visual states for each component
- `styling_specs` (object): Colors, typography, spacing
- `interaction_specs` (array): Hover, focus, active states
- `accessibility_specs` (array): ARIA labels, roles, etc.

### Dependencies
- Components identified
- Design system or guidelines available
- Accessibility standards known

### Execution Steps
1. Define component boundaries and structure
2. Specify internal layout and spacing
3. Define visual states (default, hover, focus, active, disabled)
4. Create styling specifications
5. Plan responsive adjustments
6. Add accessibility attributes
7. Document interaction behavior
8. Provide component variants
9. Create component documentation

### Validation Checklist
- [ ] Component layout is clear and implementable
- [ ] All states are defined
- [ ] Spacing follows design system
- [ ] Accessibility requirements met
- [ ] Responsive behavior specified
- [ ] Styling is consistent with system

### Success Criteria
- Developers can implement from spec
- Component is reusable
- All states are accessible
- Component looks and behaves consistently

### Failure Conditions
- Spec ambiguous for implementation
- Missing states or edge cases
- Accessibility requirements not met
- Inconsistent with design system
- Can't adapt to different content

---

## Skill: Validate Accessibility

### Purpose
Verify that the UI design meets accessibility standards (WCAG), ensuring the interface is usable by all users including those with disabilities.

### When to Use
- Reviewing designs for accessibility
- Checking contrast ratios and text sizes
- Validating keyboard navigation
- Verifying screen reader compatibility

### Inputs
- `ui_design` (object): UI design to validate
- `accessibility_standards` (string, optional): WCAG level to comply with (A, AA, AAA)
- `user_capabilities` (array, optional): Specific disabilities to support
- `content` (string, optional): Actual content for validation

### Outputs
- `accessibility_score` (number): Overall accessibility score
- `issues` (array): Accessibility issues found
- `recommendations` (array): Improvements to make
- `wcag_compliance` (object): Compliance level for each guideline
- `remediation_guide` (object): How to fix identified issues

### Dependencies
- UI design documented
- Accessibility standards specified
- Content available for review

### Execution Steps
1. Validate color contrast ratios
2. Check text sizing and readability
3. Verify keyboard navigation path
4. Validate semantic HTML structure
5. Check ARIA labels and roles
6. Verify focus indicators
7. Test with assistive technologies
8. Validate form accessibility
9. Check link and button labels

### Validation Checklist
- [ ] Contrast ratios meet WCAG AA minimums
- [ ] Text is readable (font size, line height)
- [ ] Keyboard navigation works completely
- [ ] Screen reader announces content correctly
- [ ] Focus is visible and logical
- [ ] Sufficient color is not only way to convey info
- [ ] Form labels are associated with inputs

### Success Criteria
- WCAG AA compliance achieved
- Keyboard navigation complete
- Screen reader works properly
- Users with disabilities can use interface

### Failure Conditions
- Poor contrast or readability
- Keyboard navigation broken
- Screen reader cannot access content
- Missing or incorrect labels
- Cannot meet accessibility requirements
