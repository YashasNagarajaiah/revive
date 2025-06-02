from config import DARK_COLOR, LIGHT_COLOR, SECONDARY_COLOR, PRIMARY_COLOR

def load_css():
    return f"""
    <style>
    /* Main Container */
    .reportview-container .main .block-container{{
        max-width: 1200px;
        padding: 2rem 5rem;
        background-color: {LIGHT_COLOR};
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}

    /* Main Content */
    .reportview-container .main {{
        color: {DARK_COLOR};
        background: linear-gradient(135deg, {PRIMARY_COLOR}05, {SECONDARY_COLOR}05);
    }}

    /* Headers */
    h1 {{
        color: rgb(91, 189, 185);
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 1rem;
    }}

    h2 {{
        color: {DARK_COLOR};
        font-size: 24px;
        font-weight: 500;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {SECONDARY_COLOR}30;
    }}

    h3 {{
        color: {DARK_COLOR};
        font-size: 20px;
        font-weight: 500;
    }}

    /* Widgets */
    .Widget>label {{
        color: {DARK_COLOR};
        font-weight: 600;
        font-size: 15px;
    }}

    /* Buttons */
    .stButton>button {{
        color: {LIGHT_COLOR};
        background-color: {SECONDARY_COLOR};
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: none;
        transition: all 0.2s ease;
    }}

    .stButton>button:hover {{
        opacity: 0.9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}

    /* Input Fields */
    .stTextInput>div>div>input {{
        border-radius: 6px;
        border: 1px solid {SECONDARY_COLOR}30;
        padding: 0.5rem;
        transition: all 0.2s ease;
    }}

    .stTextInput>div>div>input:focus {{
        border-color: {DARK_COLOR};
        box-shadow: 0 0 0 2px {SECONDARY_COLOR}20;
    }}

    /* Select Box */
    .stSelectbox>div>div>select {{
        border-radius: 6px;
        border: 1px solid {SECONDARY_COLOR}30;
        padding: 0.5rem;
        transition: all 0.2s ease;
    }}

    .stSelectbox>div>div>select:hover {{
        border-color: {SECONDARY_COLOR};
    }}

    /* Metrics (KPI Cards) */
    .metric-card {{
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}

    .metric-card h4 {{
        color: {DARK_COLOR};
        font-size: 18px;
        margin: 0;
        padding-bottom: 5px;
    }}

    .metric-card p {{
        color: {PRIMARY_COLOR};
        font-size: 24px;
        font-weight: bold;
        margin: 0;
    }}

    .metric-card .delta {{
        font-size: 14px;
        font-weight: bold;
        color: #4CAF50;
    }}

    /* Cards */
    .card {{
        background: white;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid {SECONDARY_COLOR}20;
        margin: 0.5rem 0;
    }}

    /* Tables */
    .dataframe {{
        border: 1px solid {SECONDARY_COLOR}20;
        border-radius: 6px;
        overflow: hidden;
    }}

    .dataframe thead tr th {{
        background: {SECONDARY_COLOR}10;
        padding: 0.5rem;
        font-weight: 600;
    }}

    .dataframe tbody tr:nth-child(even) {{
        background: {PRIMARY_COLOR}05;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab"] {{
        height: 40px;
        background: white;
        border-radius: 4px;
        color: {DARK_COLOR};
        font-weight: 500;
        border: 1px solid {SECONDARY_COLOR}20;
        margin-right: 4px;
    }}

    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background: {SECONDARY_COLOR}10;
        border-color: {SECONDARY_COLOR};
    }}

    /* Progress Bar */
    .stProgress > div > div > div > div {{
        background: linear-gradient(to right, {PRIMARY_COLOR}, {SECONDARY_COLOR});
        border-radius: 4px;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] .sidebar-content {{
        background: {LIGHT_COLOR};
        border-right: 1px solid {SECONDARY_COLOR}20;
    }}

    /* Alerts */
    .element-container .alert {{
        border-radius: 6px;
        border-left: 4px solid {SECONDARY_COLOR};
    }}

    /* Success Message */
    .element-container .success {{
        background-color: #f0fff4;
        border-left-color: #48bb78;
    }}

    /* Warning Message */
    .element-container .warning {{
        background-color: #fffaf0;
        border-left-color: #ed8936;
    }}

    /* Error Message */
    .element-container .error {{
        background-color: #fff5f5;
        border-left-color: #f56565;
    }}
    </style>
    """
