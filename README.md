#  Google Play Store Data Analysis & Prediction by rushikesh farakate

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-brightgreen.svg)
![Dash](https://img.shields.io/badge/Dash-Web%20App-008de4.svg)

Welcome to the **Google Play Store Data Analysis** repository! This project performs a detailed Exploratory Data Analysis (EDA) and predictive modeling on a comprehensive dataset of Google Play Store applications to uncover insights regarding app ratings, popularity, pricing strategies, and sizing.

## 📖 Overview
The Google Play Store is the largest app marketplace in the world. Understanding the crucial factors that drive an app's success—ranging from its category and size to pricing and update frequency—can provide developers and businesses with a distinct competitive advantage. 

This project cleans raw Play Store data, engineers new practical features, visualizes key trends, and lastly builds Machine Learning models to predict app outcomes (such as user ratings or install brackets). It also includes a fully interactive web dashboard built with Dash by Plotly to explore the dataset dynamically.

##  Key Features
- **Data Cleaning & Transformation**: Converts string-heavy columns (e.g., `Installs` ("10,000+"), `Size` ("19M"), `Price` ("$4.99")) into usable, clean numeric formats.
- **Feature Engineering**: Derives impactful features like `days_since_update`, log-transformed reviews/installs, and binary `is_paid` flags.
- **Exploratory Data Analysis (EDA)**: Utilizes rich visual libraries (Matplotlib, Seaborn, Plotly) to chart the distribution of categories, the relationship between size and ratings, and the breakdown of free vs. paid apps.
- **Predictive ML Modeling**: Leverages powerful algorithms from `scikit-learn` (Random Forest, Linear/Logistic Regression) to model quantitative targets such as continuous app ratings and categorical success metrics.

## 🛠 Tech Stack
- **Languages / Core**: `Python`, `pandas`, `numpy`
- **Machine Learning**: `scikit-learn`
- **Visualization**: `matplotlib`, `seaborn`, `plotly`
- **Web Dashboard**: `dash`, `dash-bootstrap-components`
- **Database Backend (Optional)**: `sqlite3`

##  Project Structure
```text
GOOGLE PLAYSTORE ANALYSIS/
├── app.py                                # Interactive web dashboard built with Dash
├── unified google playstore prj.ipynb    # Main Jupyter Notebook containing EDA and ML models
├── googleplaystore (1).csv               # Raw Dataset containing ~10k app records
├── Google Play Store Analysis.pptx       # Presentation slides summarizing key analytical findings
└── README.md                             # Project Documentation
```

## 🚀 Getting Started

### Prerequisites
Make sure you have Python installed on your system along with the Jupyter Notebook environment.

### Installation
1. Clone this repository (or download the directory).
2. Install the necessary Python packages:
   ```bash
   pip install pandas numpy matplotlib seaborn plotly scikit-learn dash dash-bootstrap-components
   ```

### Running the Dashboard
1. Run the `app.py` file to start the Dash server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://127.0.0.1:8050/`.

### Running the Analysis
1. Launch Jupyter environment:
   ```bash
   jupyter notebook
   ```
2. Open the primary analysis notebook: `unified google playstore prj.ipynb`.
3. The codebase expects the raw dataset `googleplaystore (1).csv` to be present in the directory. 
4. Run all notebook cells systematically to parse the data, view the exploratory graphs, and train the Machine Learning models.

##  Key Business Insights
- **Category Dominance**: The "Family" and "Game" categories dominate the store in terms of raw volume, but have fierce competition. 
- **Rating Dynamics**: A large majority of apps fall between the 4.0 - 4.5 rating threshold. Extremely large apps sometimes suffer in ratings due to download friction.
- **Pricing Strategy**: The overwhelming majority of the market is Free (monetized via ads/IAP). Paid apps must offer significant niche value to justify upfront costs. 

## Note
This repository was built by rushikesh  farakate for analytical and educational purposes to synthesize public Google Play Store data. The predictive models are meant as statistical baselines to inform data-driven app development strategies.
