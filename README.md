# Grit Browser: Neuro-Performance OS

A high-performance browser built in Kivy/KivyMD designed to train the aMCC and solve ADHD choice paralysis for universal browser work.

## Features

### I. The Heartbeat (10-Speed Vision)
- **FBO Capture**: GPU-accelerated texture capture for zero-lag monitoring.
- **Adaptive Gears**: Capture intervals driven by `(Velocity × 0.4) + (Image Delta × 0.6)`.
- **G10–G1**: Dynamic shifting from 0.2s (Active Sprint) to 15m (Idle/Budget-Saver).

### II. The Willpower Engine (Gamified UI)
- **Grit Bar**: 5px top progress bar pulsing at the active Gear rate.
- **15% Push**: Exit override with "Grit Challenge" modals and 2x XP rewards.
- **aMCC Dashboard**: Skill tree visualizer tracking 6-month streaks.

### III. ADHD Scaffolding & Tunnels
- **Task Paging**: Semi-transparent overlay caging the URL bar; displays exactly ONE sub-task.
- **Tunnels**: One-click PWA "Caging" for standalone windows.
- **Fact-Catcher**: Sidebar for real-time AI extraction of specs/pinouts.

### IV. Intelligence Logic
- **Stall Detection**: Socratic intervention if Delta <1% for 5 mins.
- **Fading Scaffolding**: AI shifts from answers to guided questions as "Tenacity Rank" increases.
- **Zen Mode**: Full stimulus blackout for non-essential UI.

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
