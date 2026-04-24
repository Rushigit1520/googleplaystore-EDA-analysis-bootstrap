# 🚀 Google Play Store ML Intelligence System

### By Rushikesh Farakate

A **futuristic, dark-neon themed** ML Intelligence Dashboard that performs deep Exploratory Data Analysis (EDA) and live **machine learning predictions** on 10,000+ Google Play Store applications — built with Dash, scikit-learn, and Plotly.

---

## ✨ Highlights

| Feature | Description |
|---|---|
| 🎨 **Dark Neon Glassmorphism UI** | Premium dark theme with blur-glass cards, neon cyan/purple gradients, and hover glow effects |
| ✨ **Animated Particle Background** | Self-contained vanilla JS particle system with mouse interaction |
| ⌨️ **Typing Animation Header** | Character-by-character typing effect on the title |
| 📊 **Animated KPI Counters** | Scroll-triggered count-up animations for key metrics |
| 🤖 **Random Forest ML Model** | Trained at startup to predict app ratings from 6 engineered features |
| 🔮 **Live Prediction Form** | Enter app details → get instant rating prediction with star display |
| 📈 **Interactive Plotly Charts** | Rating histograms, Free vs Paid donut charts, Size vs Rating bubble plots |
| 📱 **Fully Responsive** | Adaptive layout for desktop, tablet, and mobile |

---

## 📸 Dashboard Sections

- **Header** — Gradient typing animation with subtitle
- **KPI Cards** — Total Apps (10,841), Avg Rating (4.21), Total Installs (167B+), Categories (34)
- **ML Model Performance** — R² Score, MAE, Features Used
- **Feature Importance** — Horizontal bar chart of Random Forest feature importances
- **Interactive Data Explorer** — Category dropdown filter with 3 reactive charts
- **ML Prediction** — Input form → Predict Rating button → Animated result with stars
- **Footer** — Credits with heartbeat animation

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python, Dash, pandas, numpy |
| **Machine Learning** | scikit-learn (RandomForestRegressor) |
| **Visualization** | Plotly (dark template, neon color palette) |
| **Frontend Styling** | Custom CSS (glassmorphism, gradients, animations) |
| **Frontend Interactivity** | Vanilla JavaScript (particles, typing, counters) |
| **Typography** | Google Fonts (Outfit, JetBrains Mono) |

---

## 📁 Project Structure

```text
GOOGLE PLAYSTORE ANALYSIS/
├── assets/
│   ├── style.css                             # Dark neon glassmorphism CSS theme
│   └── custom.js                             # Particle background, typing animation, counter animations
├── app.py                                    # Dash app — ML pipeline + futuristic layout
├── unified google playstore prj.ipynb        # Jupyter Notebook with EDA and ML models
├── googleplaystore (1).csv                   # Raw dataset (~10,841 app records)
├── Google Play Store Analysis.pptx           # Presentation slides
└── README.md                                 # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rushigit1520/googleplaystore-EDA-analysis-bootstrap.git
   cd googleplaystore-EDA-analysis-bootstrap
   ```

2. **Install dependencies:**
   ```bash
   pip install pandas numpy matplotlib seaborn plotly scikit-learn dash
   ```

### Running the Dashboard

```bash
python app.py
```

Open your browser at **http://127.0.0.1:8050/** — the ML model trains automatically at startup (~2 seconds).

### Running the Jupyter Analysis

```bash
jupyter notebook
```

Open `unified google playstore prj.ipynb` and run all cells sequentially.

---

## 🤖 ML Model Details

| Parameter | Value |
|---|---|
| **Algorithm** | Random Forest Regressor |
| **Target** | App Rating (1.0 – 5.0) |
| **Features** | `size_mb`, `log_reviews`, `log_installs`, `price_clean`, `is_paid`, `days_since_update` |
| **Estimators** | 150 trees |
| **Max Depth** | 12 |
| **Train/Test Split** | 80/20 |

### Feature Engineering
- `log_reviews` — Log-transformed review count
- `log_installs` — Log-transformed install count
- `is_paid` — Binary flag (Free = 0, Paid = 1)
- `days_since_update` — Days since the app's last update

---

## 📊 Key Business Insights

- **Category Dominance**: "Family" and "Game" categories dominate in volume but face fierce competition.
- **Rating Dynamics**: Most apps cluster between 4.0 – 4.5 ratings. Extremely large apps sometimes suffer due to download friction.
- **Pricing Strategy**: The overwhelming majority of apps are Free (monetized via ads/IAP). Paid apps must offer significant niche value.
- **Top Predictive Feature**: `log_reviews` (number of reviews) is the strongest predictor of app ratings.

---

## 📝 Note

This project was built by **Rushikesh Farakate** for analytical and educational purposes using public Google Play Store data. The ML models serve as statistical baselines to inform data-driven app development strategies.
