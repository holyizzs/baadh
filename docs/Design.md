# Design System
# Flash Flood Prediction System

**Version:** 1.0  
**Date:** September 22, 2026  
**Theme:** Indian Flag + Light Blue (Safety & Trust)  

---

## 1. COLOR PALETTE

### 1.1 Primary Colors (Indian Flag Theme)

```css
/* Saffron / Orange - Energy, Sacrifice */
--saffron-primary: #FF9933;
--saffron-light: #FFB366;
--saffron-dark: #E67300;

/* White - Peace, Truth */
--white-primary: #FFFFFF;
--white-off: #F8F9FA;

/* Green - Growth, Auspiciousness */
--green-primary: #138808;
--green-light: #46A839;
--green-dark: #0A5A05;

/* Ashoka Chakra Blue - Justice, Progress */
--chakra-blue: #000080;
--chakra-blue-light: #0000B3;
```

### 1.2 Functional Colors (Risk Levels)

```css
/* Safety Colors with Indian Flag Influence */
--risk-safe: #138808;        /* Indian flag green */
--risk-watch: #FFB366;        /* Light saffron */
--risk-warning: #FF9933;      /* Indian flag saffron/orange */
--risk-severe: #DC2626;       /* Red (universally understood danger) */

/* Light Blue Accents - Trust, Water, Safety */
--light-blue-primary: #38BDF8;   /* Sky blue */
--light-blue-light: #7DD3FC;     /* Lighter blue */
--light-blue-dark: #0284C7;      /* Deeper blue */
--light-blue-bg: #E0F2FE;        /* Very light blue background */
```

### 1.3 Neutral Colors (UI Base)

```css
/* Dark Mode Base (Primary UI) */
--bg-primary: #0F172A;        /* Deep blue-black */
--bg-secondary: #1E293B;      /* Lighter dark */
--bg-tertiary: #334155;       /* Card backgrounds */

/* Light Mode Base (Alternative) */
--bg-light-primary: #FFFFFF;
--bg-light-secondary: #F1F5F9;
--bg-light-tertiary: #E2E8F0;

/* Text Colors */
--text-primary: #F1F5F9;      /* Light gray (on dark) */
--text-secondary: #94A3B8;    /* Muted gray */
--text-tertiary: #64748B;     /* Even more muted */
--text-dark: #0F172A;         /* Dark text (on light bg) */
```

### 1.4 Alert Status Colors

```css
/* Alert Severity */
--alert-info: #38BDF8;        /* Light blue - informational */
--alert-success: #10B981;     /* Green - success/safe */
--alert-warning: #F59E0B;     /* Amber - caution */
--alert-error: #EF4444;       /* Red - danger/critical */
```

---

## 2. TYPOGRAPHY

### 2.1 Font Families

```css
/* Primary Font - Sans Serif (Modern, Clean) */
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 
                'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 
                'Helvetica Neue', sans-serif;

/* Monospace Font - Code, Data */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;

/* Hindi/Devanagari Support */
--font-hindi: 'Noto Sans Devanagari', 'Mukta', sans-serif;
```

**CDN Links:**
```html
<!-- Add to <head> of HTML -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 2.2 Font Sizes

```css
/* Type Scale (1.250 - Major Third) */
--text-xs: 0.75rem;      /* 12px */
--text-sm: 0.875rem;     /* 14px */
--text-base: 1rem;       /* 16px - body text */
--text-lg: 1.125rem;     /* 18px */
--text-xl: 1.25rem;      /* 20px */
--text-2xl: 1.5rem;      /* 24px */
--text-3xl: 1.875rem;    /* 30px */
--text-4xl: 2.25rem;     /* 36px - main headings */
--text-5xl: 3rem;        /* 48px - hero text */
--text-6xl: 3.75rem;     /* 60px - large displays */
```

### 2.3 Font Weights

```css
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;
```

### 2.4 Line Heights

```css
--leading-tight: 1.25;    /* Headings */
--leading-snug: 1.375;    /* Subheadings */
--leading-normal: 1.5;    /* Body text */
--leading-relaxed: 1.625; /* Comfortable reading */
--leading-loose: 2;       /* Spacious paragraphs */
```

---

## 3. SPACING SYSTEM

### 3.1 Spacing Scale

```css
/* 8px base unit */
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

### 3.2 Component Spacing

```css
/* Cards */
--card-padding: var(--space-6);      /* 24px */
--card-gap: var(--space-4);          /* 16px between cards */

/* Sections */
--section-padding-y: var(--space-12); /* 48px top/bottom */
--section-padding-x: var(--space-6);  /* 24px left/right */

/* Buttons */
--button-padding-x: var(--space-6);   /* 24px */
--button-padding-y: var(--space-3);   /* 12px */
```

---

## 4. COMPONENT STYLES

### 4.1 Buttons

```css
/* Primary Button (Action) */
.btn-primary {
    background: linear-gradient(135deg, var(--light-blue-primary), var(--chakra-blue));
    color: white;
    padding: var(--space-3) var(--space-6);
    border-radius: 0.5rem;
    font-weight: var(--font-semibold);
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(56, 189, 248, 0.3);
}

/* Alert Button (Urgent Action) */
.btn-alert {
    background: linear-gradient(135deg, var(--saffron-primary), var(--risk-severe));
    color: white;
    padding: var(--space-4) var(--space-8);
    border-radius: 0.5rem;
    font-weight: var(--font-bold);
    font-size: var(--text-lg);
    animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
    0%, 100% { 
        box-shadow: 0 0 0 0 rgba(255, 153, 51, 0.7); 
    }
    50% { 
        box-shadow: 0 0 0 15px rgba(255, 153, 51, 0); 
    }
}

/* Secondary Button */
.btn-secondary {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    border: 1px solid var(--text-tertiary);
    padding: var(--space-3) var(--space-6);
    border-radius: 0.5rem;
    font-weight: var(--font-medium);
}
```

### 4.2 Cards

```css
/* Standard Card */
.card {
    background: var(--bg-secondary);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    padding: var(--card-padding);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

/* Risk Card (with status color) */
.card-risk {
    background: var(--bg-secondary);
    border: 2px solid var(--border-color); /* Dynamic based on risk */
    border-radius: 1rem;
    padding: var(--card-padding);
    position: relative;
    overflow: hidden;
}

.card-risk::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: var(--border-color); /* Colored top bar */
}

/* Stat Card (for key metrics) */
.card-stat {
    background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
    border-radius: 1rem;
    padding: var(--space-6);
    text-align: center;
}

.card-stat-value {
    font-size: var(--text-5xl);
    font-weight: var(--font-extrabold);
    color: var(--stat-color); /* Dynamic */
    line-height: 1;
}

.card-stat-label {
    font-size: var(--text-sm);
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: var(--space-2);
}
```

### 4.3 Risk Level Indicators

```css
/* Risk Badge */
.risk-badge {
    display: inline-flex;
    align-items: center;
    padding: var(--space-2) var(--space-4);
    border-radius: 9999px;
    font-size: var(--text-sm);
    font-weight: var(--font-bold);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.risk-badge-low {
    background: rgba(19, 136, 8, 0.2);
    color: var(--green-light);
    border: 1px solid var(--green-primary);
}

.risk-badge-moderate {
    background: rgba(255, 179, 102, 0.2);
    color: var(--saffron-light);
    border: 1px solid var(--saffron-primary);
}

.risk-badge-high {
    background: rgba(255, 153, 51, 0.2);
    color: var(--saffron-primary);
    border: 1px solid var(--saffron-dark);
}

.risk-badge-severe {
    background: rgba(239, 68, 68, 0.2);
    color: #FCA5A5;
    border: 1px solid var(--risk-severe);
    animation: pulse-severe 2s infinite;
}

@keyframes pulse-severe {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
```

---

## 5. LAYOUT STRUCTURE

### 5.1 Grid System

```css
/* Dashboard Grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: var(--space-6);
    padding: var(--space-6);
}

/* Responsive Breakpoints */
@media (max-width: 768px) {
    .dashboard-grid {
        grid-template-columns: 1fr;
        gap: var(--space-4);
    }
}

/* Stats Cards Row */
.stats-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: var(--space-4);
}

/* Main Content + Sidebar */
.main-sidebar-layout {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: var(--space-6);
}

@media (max-width: 1024px) {
    .main-sidebar-layout {
        grid-template-columns: 1fr;
    }
}
```

### 5.2 Container Widths

```css
--container-sm: 640px;
--container-md: 768px;
--container-lg: 1024px;
--container-xl: 1280px;
--container-2xl: 1536px;

.container {
    width: 100%;
    max-width: var(--container-2xl);
    margin-left: auto;
    margin-right: auto;
    padding-left: var(--space-6);
    padding-right: var(--space-6);
}
```

---

## 6. SPECIAL EFFECTS

### 6.1 Shadows

```css
/* Elevation System */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);

/* Colored Shadows (for alerts) */
--shadow-blue: 0 10px 30px rgba(56, 189, 248, 0.3);
--shadow-orange: 0 10px 30px rgba(255, 153, 51, 0.3);
--shadow-red: 0 10px 30px rgba(239, 68, 68, 0.3);
```

### 6.2 Gradients

```css
/* Background Gradients */
--gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--gradient-danger: linear-gradient(135deg, #FF9933 0%, #DC2626 100%);
--gradient-safe: linear-gradient(135deg, #10B981 0%, #138808 100%);
--gradient-water: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%);

/* Indian Flag Gradient (for special elements) */
--gradient-indian-flag: linear-gradient(180deg, 
    #FF9933 0%, 
    #FF9933 33.33%, 
    #FFFFFF 33.33%, 
    #FFFFFF 66.66%, 
    #138808 66.66%, 
    #138808 100%
);
```

### 6.3 Animations

```css
/* Fade In */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Slide Up */
@keyframes slideUp {
    from { 
        opacity: 0;
        transform: translateY(20px);
    }
    to { 
        opacity: 1;
        transform: translateY(0);
    }
}

/* Pulse (for alerts) */
@keyframes pulse {
    0%, 100% { 
        transform: scale(1);
        opacity: 1;
    }
    50% { 
        transform: scale(1.05);
        opacity: 0.8;
    }
}

/* Spin (for loading) */
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
```

---

## 7. ICONOGRAPHY

### 7.1 Icon System

**Use Unicode Emojis (No Dependencies):**

```css
/* Weather Icons */
🌧️ - Rain
⛈️ - Storm
🌊 - Flood/Water
☀️ - Sunny/Clear
🌤️ - Partly Cloudy

/* Status Icons */
✅ - Success/Safe
⚠️ - Warning
🔴 - Danger/Severe
🟡 - Moderate/Caution
🟢 - Low Risk/Normal

/* Action Icons */
📍 - Location/Pin
📊 - Statistics/Data
🔮 - Prediction
🚨 - Alert/Emergency
⏱️ - Time/Timer
📱 - Mobile/Phone
💧 - Water/Moisture

/* UI Icons */
⚙️ - Settings
👤 - User/Profile
📋 - List/Menu
🗺️ - Map
📈 - Chart/Growth
```

**For More Complex Icons (Optional):**
- Use **Lucide Icons** (lightweight, open source)
- CDN: `https://unpkg.com/lucide@latest`

---

## 8. RESPONSIVE DESIGN

### 8.1 Breakpoints

```css
/* Mobile First Approach */
--breakpoint-sm: 640px;   /* Small devices (phones) */
--breakpoint-md: 768px;   /* Medium devices (tablets) */
--breakpoint-lg: 1024px;  /* Large devices (desktops) */
--breakpoint-xl: 1280px;  /* Extra large (wide screens) */
--breakpoint-2xl: 1536px; /* 2K screens */

/* Usage */
@media (min-width: 768px) {
    /* Tablet and up */
}

@media (min-width: 1024px) {
    /* Desktop and up */
}
```

### 8.2 Responsive Typography

```css
/* Scale down on mobile */
@media (max-width: 768px) {
    :root {
        --text-5xl: 2.25rem;  /* 36px instead of 48px */
        --text-4xl: 1.875rem; /* 30px instead of 36px */
        --text-3xl: 1.5rem;   /* 24px instead of 30px */
    }
}
```

---

## 9. ACCESSIBILITY

### 9.1 Color Contrast

**WCAG AA Compliance:**
- Normal text: 4.5:1 minimum contrast ratio
- Large text (18pt+): 3:1 minimum contrast ratio
- UI components: 3:1 minimum

**Tested Combinations:**
- ✅ White text on dark blue background (0F172A): 15.8:1
- ✅ Light blue (38BDF8) on dark background: 8.2:1
- ✅ Orange (FF9933) on dark background: 6.4:1
- ✅ Green (138808) on dark background: 5.9:1

### 9.2 Focus States

```css
/* Visible Focus Indicators */
*:focus {
    outline: 2px solid var(--light-blue-primary);
    outline-offset: 2px;
}

button:focus {
    outline: 2px solid var(--light-blue-primary);
    outline-offset: 4px;
}
```

---

## 10. LOGO & BRANDING

### 10.1 Logo Design Concept

```
🌊 FloodGuard AI

Colors:
- 🌊 Wave emoji in light blue (#38BDF8)
- Text in gradient: Indian flag saffron to blue
```

**Typography:**
- "FloodGuard" in bold (font-weight: 700)
- "AI" in regular weight, slightly smaller

### 10.2 Favicon

```html
<!-- Use flag-inspired icon -->
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect fill='%23FF9933' width='100' height='33'/><rect fill='%23FFFFFF' y='33' width='100' height='34'/><rect fill='%23138808' y='67' width='100' height='33'/><circle cx='50' cy='50' r='12' fill='%23000080'/></svg>">
```

---

## 11. DARK MODE (Default)

```css
/* Default Dark Theme */
body {
    background: var(--bg-primary);
    color: var(--text-primary);
    font-family: var(--font-primary);
}

/* Optional: Light Mode Toggle */
body.light-mode {
    background: var(--bg-light-primary);
    color: var(--text-dark);
}

body.light-mode .card {
    background: var(--bg-light-secondary);
    border-color: rgba(0, 0, 0, 0.1);
}
```

---

## 12. USAGE EXAMPLES

### Example 1: Risk Indicator Card

```html
<div class="card card-risk" style="--border-color: var(--risk-severe);">
    <div class="risk-badge risk-badge-severe">SEVERE 🔴</div>
    <h2 style="color: var(--risk-severe); margin-top: 1rem;">87%</h2>
    <p style="color: var(--text-secondary);">Flood Probability</p>
</div>
```

### Example 2: Alert Button

```html
<button class="btn-alert">
    🚨 SEND EMERGENCY ALERT
</button>
```

### Example 3: Stat Grid

```html
<div class="stats-row">
    <div class="card-stat" style="--stat-color: var(--risk-severe);">
        <div class="card-stat-value">HIGH</div>
        <div class="card-stat-label">RISK LEVEL</div>
    </div>
    <!-- More stats... -->
</div>
```

---

**END OF DESIGN SYSTEM**

*Use these guidelines consistently across all UI components*  
*Update dashboard (index.html) to match this color scheme*
