import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px

# Data Cleaning Functions
def parse_installs(x):
    if pd.isna(x): return np.nan
    x = str(x).replace("+","").replace(",","")
    return int(x) if x.isdigit() else np.nan

def parse_price(x):
    if pd.isna(x): return 0.0
    return float(str(x).replace("$","")) if str(x).replace("$","").replace(".","").isdigit() else np.nan

def parse_size(x):
    if pd.isna(x): return np.nan
    s = str(x)
    if "Varies" in s: return np.nan
    if s.endswith("M"): return float(s[:-1])
    if s.endswith("k") or s.endswith("K"): return float(s[:-1]) / 1024
    return np.nan

# Load Data
file_path = "googleplaystore (1).csv"
try:
    df = pd.read_csv(file_path)
    df["installs_clean"] = df["Installs"].apply(parse_installs)
    df["price_clean"]    = df["Price"].apply(parse_price)
    df["size_mb"]        = df["Size"].apply(parse_size)
    df["reviews_num"]    = pd.to_numeric(df["Reviews"], errors="coerce")
    df["rating_num"]     = pd.to_numeric(df["Rating"], errors="coerce")
    
    df["size_mb"] = df["size_mb"].fillna(df["size_mb"].median())
    df["rating_num"] = df["rating_num"].fillna(df["rating_num"].median())
except Exception as e:
    df = pd.DataFrame()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)

# Define Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("📱 Google Play Store Dashboard", className="text-center text-primary mb-4 mt-4"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Apps", className="card-title"),
                    html.H2(f"{len(df):,}", className="card-text text-info")
                ])
            ], className="mb-4 shadow-sm text-center")
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Average Rating", className="card-title"),
                    html.H2(f"{df['rating_num'].mean():.2f}", className="card-text text-success")
                ])
            ], className="mb-4 shadow-sm text-center")
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Max Installs", className="card-title"),
                    html.H2(f"{df['installs_clean'].max():,.0f}", className="card-text text-warning")
                ])
            ], className="mb-4 shadow-sm text-center")
        ], width=4),
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H4("Filter by Category:", className="mb-2"),
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': cat, 'value': cat} for cat in sorted(df['Category'].dropna().unique())] if not df.empty else [],
                value='ART_AND_DESIGN' if not df.empty else None,
                clearable=False,
                className="mb-4"
            )
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='rating-dist-fig'), width=6),
        dbc.Col(dcc.Graph(id='installs-type-fig'), width=6),
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='scatter-size-rating-fig'), width=12)
    ], className="mt-4")
], fluid=True)

# Callbacks
@app.callback(
    [Output('rating-dist-fig', 'figure'),
     Output('installs-type-fig', 'figure'),
     Output('scatter-size-rating-fig', 'figure')],
    [Input('category-dropdown', 'value')]
)
def update_graphs(selected_category):
    if df.empty or selected_category is None:
        return px.scatter(title="No data"), px.scatter(title="No data"), px.scatter(title="No data")
        
    filtered_df = df[df['Category'] == selected_category]
    
    # 1. Rating Distribution
    fig_rating = px.histogram(filtered_df, x="rating_num", nbins=20, 
                              title=f"Rating Distribution - {selected_category}",
                              color_discrete_sequence=['#3498db'])
    
    # 2. Free vs Paid
    type_counts = filtered_df['Type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']
    fig_type = px.pie(type_counts, values='Count', names='Type', 
                      title=f"Free vs Paid - {selected_category}", hole=0.4,
                      color_discrete_sequence=['#2ecc71', '#e74c3c'])
                      
    # 3. Scatter Size vs Rating
    fig_scatter = px.scatter(filtered_df, x="size_mb", y="rating_num", size="installs_clean", 
                             color="Type", hover_name="App", title="App Size vs Rating (Bubble Size = Installs)",
                             color_discrete_sequence=['#2ecc71', '#e74c3c'])
                             
    return fig_rating, fig_type, fig_scatter

if __name__ == '__main__':
    app.run(debug=True, port=8050)
