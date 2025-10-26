# Token Economics Calculator

An interactive application for calculating token economics for ICO/Presale events.

Available in two versions:
- **🌐 Web Version** (`app.py`) - Run in browser, can be hosted online
- **🖥️ Desktop Version** (`run.py`) - Native GUI application

## Features

- **Interactive Sliders** to adjust:
  - Team Allocation (0-30%)
  - Funds to Raise ($10K - $2M)
  - Public Sale Allocation (0-100%)
  - LP Allocation (auto-calculated)

- **Real-time Calculations** showing:
  - Token distribution across all categories
  - Funds distribution (20% to LP, 80% to team)
  - Pre-Market FDV (at ICO price)
  - Market FDV (at LP price)
  - FDV Multiple

## Installation & Usage

### 🌐 Web Version (Recommended for sharing)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the web app:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

**To deploy online**: See [DEPLOYMENT.md](DEPLOYMENT.md) for free hosting options.

### 🖥️ Desktop Version

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Run the desktop app:
```bash
python run.py
```

## How to Use

1. Adjust the sliders to see real-time updates:
   - **Team Token Allocation**: Set the percentage for team tokens (0-30%)
   - **Funds to Raise**: Set the total funding target ($10K - $2M)
   - **Public Sale Token Alloc**: Set the percentage for public sale tokens
   - **LP Alloc**: Automatically calculated as 100 - Team - Public

2. View the results:
   - Token distribution in billions
   - Fund allocation  
   - Pre-Market FDV and Market FDV valuations

## Notes

- Total allocation (Team + Public + LP) must equal 100%
- 20% of raised funds are allocated to LP
- **LP must be > 0%** - sliders will be blocked if Team + Public would reach 100%
- **LP FDV cannot drop below ICO FDV** - sliders will be blocked if this constraint would be violated
- LP Allocation bar shows orange warning (⚠️) when at any constraint limit
- All values update in real-time as you adjust the sliders
- Sliders will "snap back" if you try to move them to invalid positions

## Requirements

- Python 3.x with tkinter (included in standard Python installation)

