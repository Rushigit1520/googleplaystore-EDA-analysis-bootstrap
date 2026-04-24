"""
Google Play Store ML Intelligence System
=========================================
A futuristic Dash dashboard with dark neon glassmorphism theme,
ML-powered app rating predictions, interactive Plotly charts,
and animated UI elements.

Author: Rushikesh Farakate
"""

import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# ═══════════════════════════════════════════════════════════════
#  DATA LOADING & CLEANING
# ═══════════════════════════════════════════════════════════════

def parse_installs(x):
    if pd.isna(x): return np.nan
    x = str(x).replace("+", "").replace(",", "")
    return int(x) if x.isdigit() else np.nan

def parse_price(x):
    if pd.isna(x): return 0.0
    s = str(x).replace("$", "")
    try:
        return float(s)
    except ValueError:
        return np.nan

def parse_size(x):
    if pd.isna(x): return np.nan
    s = str(x)
    if "Varies" in s: return np.nan
    if s.endswith("M"): return float(s[:-1])
    if s.endswith("k") or s.endswith("K"): return float(s[:-1]) / 1024
    return np.nan

# Load dataset
file_path = "googleplaystore (1).csv"
try:
    df = pd.read_csv(file_path)

    # Drop corrupt rows (shifted columns — e.g., rating in Category)
    df = df[df["Category"].apply(lambda x: not str(x).replace(".", "").isdigit())]

    # Basic cleaning
    df["installs_clean"] = df["Installs"].apply(parse_installs)
    df["price_clean"]    = df["Price"].apply(parse_price)
    df["size_mb"]        = df["Size"].apply(parse_size)
    df["reviews_num"]    = pd.to_numeric(df["Reviews"], errors="coerce")
    df["rating_num"]     = pd.to_numeric(df["Rating"], errors="coerce")

    # Feature engineering
    df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")
    df["days_since_update"] = (pd.Timestamp.now() - df["Last Updated"]).dt.days
    df["log_reviews"]  = np.log1p(df["reviews_num"])
    df["log_installs"] = np.log1p(df["installs_clean"])
    df["is_paid"]      = (df["Type"] == "Paid").astype(int)

    # Fill missing values
    for col in ["size_mb", "rating_num", "days_since_update", "log_reviews",
                "log_installs", "price_clean"]:
        df[col] = df[col].fillna(df[col].median() if df[col].median() is not np.nan else 0)

    DATA_LOADED = True
except Exception as e:
    print(f"[ERROR] Data load failed: {e}")
    df = pd.DataFrame()
    DATA_LOADED = False

# ═══════════════════════════════════════════════════════════════
#  ML MODEL TRAINING
# ═══════════════════════════════════════════════════════════════

FEATURES = ["size_mb", "log_reviews", "log_installs", "price_clean",
            "is_paid", "days_since_update"]

model = None
r2 = 0.0
mae = 0.0
feature_importances = {}

if DATA_LOADED:
    try:
        ml_df = df.dropna(subset=FEATURES + ["rating_num"]).copy()
        X = ml_df[FEATURES]
        y = ml_df["rating_num"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = RandomForestRegressor(
            n_estimators=150,
            max_depth=12,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        feature_importances = dict(zip(FEATURES, model.feature_importances_))
        print(f"[ML] Model trained — R²: {r2:.4f}, MAE: {mae:.4f}")
    except Exception as e:
        print(f"[ERROR] ML training failed: {e}")

# ═══════════════════════════════════════════════════════════════
#  SUMMARY STATISTICS
# ═══════════════════════════════════════════════════════════════

if DATA_LOADED:
    total_apps       = len(df)
    avg_rating       = df["rating_num"].mean()
    total_installs   = df["installs_clean"].sum()
    total_categories = df["Category"].nunique()
    total_reviews    = df["reviews_num"].sum()
    categories_list  = sorted(df["Category"].dropna().unique())
else:
    total_apps = avg_rating = total_installs = total_categories = total_reviews = 0
    categories_list = []

# ═══════════════════════════════════════════════════════════════
#  PLOTLY CHART THEME
# ═══════════════════════════════════════════════════════════════

NEON_COLORS = ["#00f0ff", "#b44aff", "#ff2d95", "#00ff88", "#3d7aff", "#ff8c00"]

CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Outfit, sans-serif", color="#e8e8f0"),
    margin=dict(l=40, r=20, t=50, b=40),
    hoverlabel=dict(
        bgcolor="rgba(15,15,35,0.9)",
        font_size=12,
        font_family="JetBrains Mono, monospace"
    ),
)

# ═══════════════════════════════════════════════════════════════
#  DASH APP SETUP
# ═══════════════════════════════════════════════════════════════

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    title="PlayStore ML Intelligence",
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/tsparticles@2.12.0/tsparticles.bundle.min.js"
    ],
)

# ─── Helper: KPI Card ──────────────────────────────────────────
def _kpi_card(icon, label, value, suffix, color_class, sub_text, decimals=0):
    return html.Div(className=f"glass-card kpi-card {color_class}", children=[
        html.Span(icon, className="kpi-icon"),
        html.Div(label, className="kpi-label"),
        html.Div(
            className="counter-value",
            **{
                "data-target": str(value),
                "data-decimals": str(decimals),
                "data-suffix": suffix,
            }
        ),
        html.Div(sub_text, className="kpi-sub"),
    ])


# ─── Helper: Feature Importance Chart ──────────────────────────
def _build_feature_importance_chart():
    if not feature_importances:
        return go.Figure().update_layout(**CHART_LAYOUT, title="No model data")

    sorted_fi = sorted(feature_importances.items(), key=lambda x: x[1])
    names = [x[0].replace("_", " ").title() for x in sorted_fi]
    values = [x[1] for x in sorted_fi]

    fig = go.Figure(go.Bar(
        x=values, y=names, orientation="h",
        marker=dict(
            color=values,
            colorscale=[[0, "#3d7aff"], [0.5, "#b44aff"], [1, "#00f0ff"]],
            line=dict(width=0),
        ),
        hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>",
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title="Random Forest Feature Importance",
        xaxis_title="Importance",
        yaxis_title="",
        height=320,
    )
    return fig


# ═══════════════════════════════════════════════════════════════
#  LAYOUT
# ═══════════════════════════════════════════════════════════════

HEADING_TEXT = "Google Play Store ML Intelligence System"

app.layout = html.Div([
    # ── Particle background (tsParticles) ──
    html.Div(id="tsparticles"),

    # ── Main container ──
    html.Div(id="app-container", children=[

        # ── Typing Header ──
        html.Div(className="typing-header-wrapper", children=[
            html.Span(
                id="typing-text",
                className="typing-header",
                **{"data-text": HEADING_TEXT}
            ),
            html.Span(className="typing-cursor"),
        ]),
        html.P("Powered by RUSHIKESH FARAKATE.",
               className="subtitle"),

        # ── KPI Cards ──
        html.Div(className="section-title", children=[
            html.Span("📊", className="icon"),
            "Key Performance Indicators"
        ]),
        html.Div(className="kpi-grid", children=[
            _kpi_card("📱", "Total Apps", total_apps, "", "cyan", "In the dataset"),
            _kpi_card("⭐", "Avg Rating", avg_rating, "", "purple", "Out of 5.0",
                      decimals=2),
            _kpi_card("📥", "Total Installs", total_installs // 1_000_000 if total_installs else 0,
                      "M+", "green", "Million downloads"),
            _kpi_card("📂", "Categories", total_categories, "", "pink",
                      "Unique app categories"),
        ]),

        # ── ML Model Metrics ──
        html.Div(className="section-title", children=[
            html.Span("🤖", className="icon"),
            "ML Model Performance"
        ]),
        html.Div(className="ml-metrics-grid", children=[
            html.Div(className="glass-card text-center", children=[
                html.Div(f"{r2:.4f}", className="metric-value"),
                html.Div("R² Score", className="metric-label"),
                html.Div("Coefficient of determination", className="metric-desc"),
            ]),
            html.Div(className="glass-card text-center", children=[
                html.Div(f"{mae:.4f}", className="metric-value"),
                html.Div("Mean Absolute Error", className="metric-label"),
                html.Div("Average rating prediction error", className="metric-desc"),
            ]),
            html.Div(className="glass-card text-center", children=[
                html.Div(f"{len(FEATURES)}", className="metric-value"),
                html.Div("Features Used", className="metric-label"),
                html.Div("Input dimensions for the model", className="metric-desc"),
            ]),
        ]),

        # ── Feature Importance Chart ──
        html.Div(className="section-title", children=[
            html.Span("🎯", className="icon"),
            "Feature Importance"
        ]),
        html.Div(className="glass-card feature-importance-section mb-md", children=[
            dcc.Graph(id="feature-importance-chart", config={"displayModeBar": False},
                      figure=_build_feature_importance_chart()),
        ]),

        # ── Interactive Charts Section ──
        html.Div(className="section-title", children=[
            html.Span("📈", className="icon"),
            "Interactive Data Explorer"
        ]),

        html.Div(className="filter-bar", children=[
            html.Span("Filter by Category:", className="filter-label"),
            html.Div(style={"width": "300px"}, children=[
                dcc.Dropdown(
                    id="category-dropdown",
                    options=[{"label": c, "value": c} for c in categories_list],
                    value=categories_list[0] if categories_list else None,
                    clearable=False,
                    className="dash-dropdown",
                ),
            ]),
        ]),

        html.Div(className="charts-grid", children=[
            html.Div(className="glass-card chart-card", children=[
                dcc.Graph(id="rating-dist-fig", config={"displayModeBar": False}),
            ]),
            html.Div(className="glass-card chart-card", children=[
                dcc.Graph(id="installs-type-fig", config={"displayModeBar": False}),
            ]),
            html.Div(className="glass-card chart-card chart-full", children=[
                dcc.Graph(id="scatter-size-rating-fig", config={"displayModeBar": False}),
            ]),
        ]),

        # ── ML Prediction Section ──
        html.Div(className="section-title", children=[
            html.Span("🔮", className="icon"),
            "Predict App Rating"
        ]),

        html.Div(className="prediction-grid", children=[
            # Form
            html.Div(className="glass-card", children=[
                html.Div(className="form-group", children=[
                    html.Label("App Size (MB)", className="form-label"),
                    dcc.Input(id="input-size", type="number", value=20,
                              min=0.1, max=200, step=0.1,
                              className="dash-input"),
                ]),
                html.Div(className="form-group", children=[
                    html.Label("Number of Reviews", className="form-label"),
                    dcc.Input(id="input-reviews", type="number", value=1000,
                              min=0, max=100000000, step=1,
                              className="dash-input"),
                ]),
                html.Div(className="form-group", children=[
                    html.Label("Number of Installs", className="form-label"),
                    dcc.Input(id="input-installs", type="number", value=100000,
                              min=0, max=10000000000, step=1,
                              className="dash-input"),
                ]),
                html.Div(className="form-group", children=[
                    html.Label("Price ($)", className="form-label"),
                    dcc.Input(id="input-price", type="number", value=0,
                              min=0, max=500, step=0.01,
                              className="dash-input"),
                ]),
                html.Div(className="form-group", children=[
                    html.Label("Days Since Last Update", className="form-label"),
                    dcc.Input(id="input-days", type="number", value=180,
                              min=0, max=5000, step=1,
                              className="dash-input"),
                ]),
                html.Button("⚡ Predict Rating", id="predict-btn",
                            className="predict-btn", n_clicks=0),
            ]),

            # Result
            html.Div(id="prediction-output", className="glass-card prediction-result-card",
                     children=[
                         html.Div("Enter app details and hit Predict",
                                  className="prediction-waiting"),
                     ]),
        ]),

        # ── Footer ──
        html.Div(className="footer", children=[
            html.Span("Built with "),
            html.Span("♥", className="heart"),
            html.Span(" by Rushikesh Farakate ·"),
        ]),
    ]),
])




# ═══════════════════════════════════════════════════════════════
#  CALLBACKS
# ═══════════════════════════════════════════════════════════════

@app.callback(
    [Output("rating-dist-fig", "figure"),
     Output("installs-type-fig", "figure"),
     Output("scatter-size-rating-fig", "figure")],
    [Input("category-dropdown", "value")]
)
def update_charts(selected_category):
    empty = go.Figure().update_layout(**CHART_LAYOUT, title="No data available")
    if not DATA_LOADED or not selected_category:
        return empty, empty, empty

    fdf = df[df["Category"] == selected_category]
    if fdf.empty:
        return empty, empty, empty

    # 1) Rating Distribution
    fig_rating = px.histogram(
        fdf, x="rating_num", nbins=25,
        title=f"Rating Distribution — {selected_category}",
        color_discrete_sequence=["#00f0ff"],
    )
    fig_rating.update_layout(**CHART_LAYOUT, height=370)
    fig_rating.update_traces(
        marker_line_width=0,
        hovertemplate="Rating: %{x}<br>Count: %{y}<extra></extra>",
    )

    # 2) Free vs Paid
    type_counts = fdf["Type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]
    fig_type = px.pie(
        type_counts, values="Count", names="Type",
        title=f"Free vs Paid — {selected_category}",
        hole=0.55,
        color_discrete_sequence=["#00ff88", "#ff2d95"],
    )
    fig_type.update_layout(**CHART_LAYOUT, height=370)
    fig_type.update_traces(
        textinfo="percent+label",
        textfont_size=13,
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
    )

    # 3) Size vs Rating Bubble
    scatter_df = fdf.dropna(subset=["size_mb", "rating_num", "installs_clean"])
    fig_scatter = px.scatter(
        scatter_df, x="size_mb", y="rating_num",
        size="installs_clean", color="Type",
        hover_name="App",
        title="App Size vs Rating (bubble = installs)",
        color_discrete_sequence=["#00f0ff", "#ff2d95"],
        size_max=40,
    )
    fig_scatter.update_layout(**CHART_LAYOUT, height=420)
    fig_scatter.update_traces(
        marker=dict(line=dict(width=0)),
    )

    return fig_rating, fig_type, fig_scatter


@app.callback(
    Output("prediction-output", "children"),
    [Input("predict-btn", "n_clicks")],
    [State("input-size", "value"),
     State("input-reviews", "value"),
     State("input-installs", "value"),
     State("input-price", "value"),
     State("input-days", "value")],
    prevent_initial_call=True,
)
def predict_rating(n_clicks, size, reviews, installs, price, days):
    if model is None:
        return html.Div("Model not available", className="prediction-waiting")

    try:
        size      = float(size or 20)
        reviews   = float(reviews or 0)
        installs  = float(installs or 0)
        price     = float(price or 0)
        days      = float(days or 180)
        is_paid   = 1 if price > 0 else 0

        features = pd.DataFrame([[
            size,
            np.log1p(reviews),
            np.log1p(installs),
            price,
            is_paid,
            days,
        ]], columns=FEATURES)

        prediction = model.predict(features)[0]
        prediction = round(min(max(prediction, 1.0), 5.0), 2)

        # Star display
        full_stars = int(prediction)
        half_star  = 1 if (prediction - full_stars) >= 0.25 else 0
        empty_stars = 5 - full_stars - half_star
        stars_str = "★" * full_stars + ("✬" if half_star else "") + "☆" * empty_stars

        return [
            html.Div(f"{prediction}", className="prediction-result-value"),
            html.Div("Predicted Rating", className="prediction-result-label"),
            html.Div(stars_str, className="prediction-result-stars"),
            html.Div(
                f"Based on {size}MB, {int(reviews):,} reviews, "
                f"{int(installs):,} installs, ${price:.2f}, "
                f"{int(days)} days since update",
                className="metric-desc",
                style={"marginTop": "16px"},
            ),
        ]
    except Exception as e:
        return html.Div(f"Prediction error: {e}", className="prediction-waiting")


# ═══════════════════════════════════════════════════════════════
#  RUN SERVER
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(debug=True, port=8050)
