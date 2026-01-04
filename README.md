# Grit Browser: Neuro-Performance OS

A high-performance browser built in Kivy/KivyMD designed to train the aMCC and solve ADHD choice paralysis for universal browser work.

## Features

### I. The Heartbeat (10-Speed Vision)
- **FBO Capture**: GPU-accelerated texture capture for zero-lag monitoring using Kivy's `Fbo`.
- **Adaptive Gears**: Capture intervals driven by `(Velocity × 0.4) + (Image Delta × 0.6)`.
- **G10–G7**: 0.2s (5FPS) → 2s (Active Sprint).
- **G6–G4**: 10s → 60s (Reading/Review).
- **G3–G1**: 3m → 15m (Idle/Budget-Saver mode for $100 limit).
- **Delta Calculation**: 8x8 grayscale MSE for image delta detection.

### II. The Willpower Engine (Gamified UI)
- **Grit Bar**: 5px top progress bar pulsing at the active Gear rate.
- **15% Push**: Exit override with "Grit Challenge" modals and 2x XP rewards.
- **Dopamine/Rage Control**: GLSL Grayscale shader toggle and auto-trigger "Cool Down" (Blue-light filter + Brown noise) if clicks >10/2s.
- **aMCC Dashboard**: Skill tree visualizer tracking 6-month streaks for long-term projects.

### III. ADHD Scaffolding & Tunnels
- **Task Paging**: Semi-transparent overlay physically caging the URL bar; displays exactly ONE sub-task at a time.
- **Tunnels**: One-click PWA "Caging" to launch URLs as chrome-less standalone windows.
- **Fact-Catcher**: Sidebar for real-time AI extraction of specs/pinouts.
- **Cliff-Hanging**: SQLite persistence to restore visual snapshot and "Working Memory" notes from previous sessions.

### IV. Intelligence Logic
- **Stall Detection**: Socratic intervention if Delta <1% for 5 mins.
- **Fading Scaffolding**: AI shifts from providing answers to asking guided questions as user "Tenacity Rank" increases.
- **Zen Mode**: Full stimulus blackout hiding all non-essential UI and text colors.
- **Vibe Check**: Minimalist, dark-themed, and responsive engineering tool feel.

## Installation

```bash
pip install kivy kivymd pillow numpy sqlalchemy
python main.py
```

## Architecture
- `main.py`: Application entry point and UI layout.
- `grit_engine.py`: Core FBO capture and adaptive gear logic.
- `ui_components.py`: Gamified UI elements (Grit Bar, Dashboard).
- `adhd_scaffolding.py`: Task paging and sidebar components.
- `intelligence.py`: Stall detection and Socratic AI logic.
