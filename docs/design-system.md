# Design System Specification

> **Project**: Performance Review Tracker UI Modernization  
> **Version**: 1.0.0  
> **Last Updated**: 2025-08-15  

## Overview

This design system defines the visual language and component specifications for the modernized Performance Review Tracker interface. The system implements a sophisticated dark theme with glassmorphism effects, inspired by modern AI tools and professional applications.

## Visual Identity

### Design Principles
1. **Professional Sophistication**: Clean, modern aesthetic suitable for workplace tools
2. **Depth & Layering**: Glassmorphism effects create visual hierarchy and depth
3. **Accessibility First**: WCAG AA compliance with proper contrast ratios
4. **Consistent Experience**: Unified patterns across all interface components
5. **Performance Conscious**: Efficient animations and optimized visual effects

### Reference Design
- **Inspiration**: Modern AI tool interfaces (Easy-Peasy.AI style)
- **Theme**: Sophisticated dark theme with blue accents
- **Effects**: Subtle glassmorphism with backdrop blur
- **Typography**: Clean hierarchy with excellent readability

---

## Color Palette

### Primary Colors
```css
:root {
  /* Primary Brand Colors */
  --color-primary: #4299ff;           /* Bright blue accent */
  --color-primary-hover: #357ae8;     /* Darker blue for hover */
  --color-primary-light: #6bb3ff;     /* Lighter blue variant */
  
  /* Background Colors */
  --color-bg-primary: #1a1f36;        /* Deep navy background */
  --color-bg-secondary: #252b47;      /* Slightly lighter navy */
  --color-bg-tertiary: #2f3759;       /* Card backgrounds */
  
  /* Glass Effect Colors */
  --color-glass-light: rgba(255, 255, 255, 0.05);  /* Light glass */
  --color-glass-medium: rgba(255, 255, 255, 0.1);  /* Medium glass */
  --color-glass-strong: rgba(255, 255, 255, 0.15); /* Strong glass */
  
  /* Border Colors */
  --color-border-subtle: rgba(255, 255, 255, 0.08);  /* Subtle borders */
  --color-border-medium: rgba(255, 255, 255, 0.12);  /* Medium borders */
  --color-border-strong: rgba(255, 255, 255, 0.2);   /* Strong borders */
  
  /* Text Colors */
  --color-text-primary: #ffffff;      /* Primary text (white) */
  --color-text-secondary: #b8c5ef;    /* Secondary text (light blue-gray) */
  --color-text-muted: #8892b0;        /* Muted text (darker blue-gray) */
  --color-text-disabled: #566084;     /* Disabled text */
}
```

### Semantic Colors
```css
:root {
  /* Status Colors */
  --color-success: #10b981;           /* Green for success states */
  --color-success-bg: rgba(16, 185, 129, 0.1);
  
  --color-warning: #f59e0b;           /* Amber for warnings */
  --color-warning-bg: rgba(245, 158, 11, 0.1);
  
  --color-error: #ef4444;             /* Red for errors */
  --color-error-bg: rgba(239, 68, 68, 0.1);
  
  --color-info: #3b82f6;              /* Blue for information */
  --color-info-bg: rgba(59, 130, 246, 0.1);
}
```

### Color Usage Guidelines
- **Primary Blue**: CTA buttons, active states, progress indicators
- **Background Navy**: Main background, container backgrounds
- **Glass Effects**: Card overlays, modals, floating elements
- **Text Colors**: Maintain proper contrast ratios for accessibility

---

## Typography

### Font Stack
```css
:root {
  --font-primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
                  'Oxygen', 'Ubuntu', 'Cantarell', 'Open Sans', 'Helvetica Neue', sans-serif;
  --font-mono: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', 'Courier New', monospace;
}
```

### Type Scale
```css
:root {
  /* Font Sizes */
  --text-xs: 0.75rem;     /* 12px */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */
  
  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  
  /* Font Weights */
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

### Typography Classes
```css
.heading-1 {
  font-size: var(--text-4xl);
  font-weight: var(--font-light);
  line-height: var(--leading-tight);
  color: var(--color-text-primary);
}

.heading-2 {
  font-size: var(--text-3xl);
  font-weight: var(--font-normal);
  line-height: var(--leading-tight);
  color: var(--color-text-primary);
}

.heading-3 {
  font-size: var(--text-2xl);
  font-weight: var(--font-medium);
  line-height: var(--leading-normal);
  color: var(--color-text-primary);
}

.body-large {
  font-size: var(--text-lg);
  font-weight: var(--font-normal);
  line-height: var(--leading-relaxed);
  color: var(--color-text-secondary);
}

.body-base {
  font-size: var(--text-base);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
  color: var(--color-text-secondary);
}

.body-small {
  font-size: var(--text-sm);
  font-weight: var(--font-normal);
  line-height: var(--leading-normal);
  color: var(--color-text-muted);
}
```

---

## Spacing System

### Spacing Scale
```css
:root {
  --space-1: 0.25rem;     /* 4px */
  --space-2: 0.5rem;      /* 8px */
  --space-3: 0.75rem;     /* 12px */
  --space-4: 1rem;        /* 16px */
  --space-5: 1.25rem;     /* 20px */
  --space-6: 1.5rem;      /* 24px */
  --space-8: 2rem;        /* 32px */
  --space-10: 2.5rem;     /* 40px */
  --space-12: 3rem;       /* 48px */
  --space-16: 4rem;       /* 64px */
  --space-20: 5rem;       /* 80px */
}
```

### Component Spacing
- **Card Padding**: `var(--space-6)` (24px)
- **Button Padding**: `var(--space-3) var(--space-6)` (12px 24px)
- **Input Padding**: `var(--space-3) var(--space-4)` (12px 16px)
- **Section Margins**: `var(--space-8)` (32px)

---

## Effects & Animations

### Glassmorphism Effects
```css
:root {
  --glass-backdrop: blur(10px);
  --glass-backdrop-strong: blur(16px);
  --shadow-glass: 0 8px 32px rgba(0, 0, 0, 0.2);
  --shadow-elevated: 0 12px 40px rgba(0, 0, 0, 0.3);
}

.glass-effect {
  background: var(--color-glass-light);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border: 1px solid var(--color-border-subtle);
  box-shadow: var(--shadow-glass);
}

.glass-card {
  background: var(--color-glass-medium);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-glass);
}
```

### Border Radius
```css
:root {
  --radius-sm: 0.375rem;   /* 6px */
  --radius-base: 0.5rem;   /* 8px */
  --radius-lg: 0.75rem;    /* 12px */
  --radius-xl: 1rem;       /* 16px */
  --radius-full: 9999px;   /* Fully rounded */
}
```

### Transitions & Animations
```css
:root {
  /* Duration */
  --duration-fast: 0.15s;
  --duration-normal: 0.3s;
  --duration-slow: 0.5s;
  
  /* Easing */
  --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
}

.transition-smooth {
  transition: all var(--duration-normal) var(--ease-smooth);
}

.transition-fast {
  transition: all var(--duration-fast) var(--ease-smooth);
}
```

---

## Component Specifications

### Buttons

#### Primary Button
```css
.btn-primary {
  background: var(--color-primary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-base);
  padding: var(--space-3) var(--space-6);
  font-weight: var(--font-medium);
  transition: var(--duration-normal) var(--ease-smooth);
}

.btn-primary:hover {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(66, 153, 255, 0.3);
}
```

#### Glass Button
```css
.btn-glass {
  background: var(--color-glass-medium);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-base);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
}

.btn-glass:hover {
  background: var(--color-glass-strong);
  border-color: var(--color-border-strong);
}
```

### Form Elements

#### Input Fields
```css
.form-control {
  background: var(--color-glass-light);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-base);
  color: var(--color-text-primary);
  padding: var(--space-3) var(--space-4);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
}

.form-control:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(66, 153, 255, 0.2);
  outline: none;
}

.form-control::placeholder {
  color: var(--color-text-muted);
}
```

### Cards

#### Standard Card
```css
.card {
  background: var(--color-glass-light);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-lg);
  backdrop-filter: var(--glass-backdrop);
  -webkit-backdrop-filter: var(--glass-backdrop);
  box-shadow: var(--shadow-glass);
  padding: var(--space-6);
  transition: var(--duration-normal) var(--ease-smooth);
}

.card:hover {
  border-color: var(--color-border-medium);
  transform: translateY(-2px);
  box-shadow: var(--shadow-elevated);
}
```

#### Feature Card
```css
.card-feature {
  background: var(--color-glass-medium);
  border: 1px solid var(--color-border-medium);
  border-radius: var(--radius-xl);
  backdrop-filter: var(--glass-backdrop-strong);
  -webkit-backdrop-filter: var(--glass-backdrop-strong);
  padding: var(--space-8);
  text-align: center;
  transition: var(--duration-normal) var(--ease-smooth);
}

.card-feature:hover {
  background: var(--color-glass-strong);
  border-color: var(--color-primary);
  transform: translateY(-4px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.3);
}
```

---

## Layout System

### Container Sizes
```css
:root {
  --container-sm: 576px;
  --container-md: 768px;
  --container-lg: 992px;
  --container-xl: 1200px;
  --container-2xl: 1400px;
}
```

### Grid System
- **Base**: CSS Grid and Flexbox for layouts
- **Responsive**: Mobile-first breakpoints
- **Spacing**: Consistent gap using spacing scale

---

## Accessibility Standards

### Contrast Ratios
- **Primary Text**: 21:1 (white on navy background)
- **Secondary Text**: 7:1 (light blue-gray on navy)
- **Interactive Elements**: Minimum 4.5:1 contrast
- **Focus States**: Clear 3px outline with primary color

### Focus Management
```css
.focus-visible {
  outline: 3px solid var(--color-primary);
  outline-offset: 2px;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## Browser Support

### Modern Features
- **CSS Custom Properties**: All modern browsers
- **Backdrop Filter**: Chrome 76+, Safari 14+, Firefox 103+
- **CSS Grid**: All modern browsers
- **Flexbox**: All modern browsers

### Fallbacks
```css
/* Fallback for browsers without backdrop-filter */
@supports not (backdrop-filter: blur(10px)) {
  .glass-effect {
    background: var(--color-bg-tertiary);
  }
}
```

---

## Implementation Guidelines

### Phase Approach
1. **Foundation**: Implement CSS custom properties and base styles
2. **Components**: Update individual component styles
3. **Layouts**: Apply new design to page layouts
4. **Polish**: Add animations and micro-interactions
5. **Testing**: Cross-browser and accessibility validation

### Development Notes
- Use CSS custom properties for all colors and spacing
- Implement glassmorphism effects progressively
- Ensure all animations respect `prefers-reduced-motion`
- Test backdrop-filter support and provide fallbacks
- Maintain Bootstrap compatibility where possible

---

*Design System Version 1.0.0 - Ready for Implementation*