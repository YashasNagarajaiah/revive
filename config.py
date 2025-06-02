import os
import pandas as pd
import numpy as np

# Define Colors for UI and Visualizations
PRIMARY_COLOR = "#80C895"
SECONDARY_COLOR = "#26A9E0"
DARK_COLOR = "#231F20"
LIGHT_COLOR = "#FFFFFF"
ACCENT_COLOR_1 = "#FFD700"  # Gold
ACCENT_COLOR_2 = "#FF6B6B"  # Coral

# Directory Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
VIDEO_DIR = os.path.join(BASE_DIR, 'videos')

# File Paths
FILE_PATH = os.path.join(DATA_DIR, 'Outgoing.xlsx')
DOWNLOADS_PATH = os.path.join(DATA_DIR, 'downloads.xlsx')
INVOICE_PATH = os.path.join(DATA_DIR, 'Invoice.xlsx')
URLS_PATH = os.path.join(DATA_DIR, 'urls.csv')

# System Configuration
ZERO_WASTE_TARGET = 95.0  # % target for waste diversion
DAILY_CAPACITY_LIMIT = 150000  # kg per day capacity limit

# Emission Factors (kg CO2 per tonne)
EMISSION_FACTORS = {
    'Construction Waste': 1.24,
    'Consumer Goods': 467.05,
    'E-Waste': 8.9,
    'Fabric & Textile': 444.94,
    'General': 467.05,
    'Glass': 8.9,
    'Green Waste': 1041.8,
    'Metal': 8.9,
    'Organics': 626.87,
    'Paper & Carton': 1041.8,
    'Pharma & Health Care': 467.05,
    'Plastics': 8.9,
    'Wood': 1041.8,
    'Wood(Pallets)': 1041.8
}

# Waste Ecosystem Categories
ECOSYSTEM_CATEGORIES = ['Recova', 'Recycle', 'Refeed', 'Reproco', 'Sewage', 'Landfill']

# Visualization Color Mapping
CHART_COLORS = {
    'Recova': '#1f77b4',
    'Recycle': '#2ca02c',
    'Refeed': '#ff7f0e',
    'Reproco': '#9467bd',
    'Sewage': '#8c564b',
    'Landfill': '#d62728'
}


# 1. Metrics Calculation Functions
def calculate_metrics(df):
    """
    Calculate key metrics for waste management.
    """
    metrics = {}

    total_weight = df['Weight (Kg)'].sum() if not df.empty else 0
    metrics['total_weight'] = total_weight

    # Calculate outgoing weight and net weight
    metrics['total_outgoing_weight'] = df[df['Weight (Kg)'] > 0]['Weight (Kg)'].sum()
    metrics['net_weight'] = total_weight - metrics['total_outgoing_weight']

    # Calculate weights and percentages for ecosystem categories
    for category in ECOSYSTEM_CATEGORIES:
        category_weight = df[df['Category Ecosystem'] == category]['Weight (Kg)'].sum() if not df.empty else 0
        metrics[f'{category.lower()}_weight'] = category_weight
        metrics[f'{category.lower()}_percentage'] = (category_weight / total_weight * 100) if total_weight > 0 else 0

    # Calculate waste diversion rate
    landfill_weight = metrics.get('landfill_weight', 0)
    metrics['waste_diversion_rate'] = ((total_weight - landfill_weight) / total_weight * 100) if total_weight > 0 else 0
    metrics['zero_waste_percentage'] = metrics['waste_diversion_rate']

    return metrics


def calculate_week_metrics(df):
    """
    Add weekly metrics to the dataframe for performance tracking.
    """
    if df.empty:
        return df

    df = df.copy()
    df['Date'] = pd.to_datetime(df['Incoming Date'])
    df['WeekOfMonth'] = df['Date'].dt.isocalendar().week
    df['MonthYear'] = df['Date'].dt.strftime('%Y-%m')
    df['MonthYearWeek'] = df['MonthYear'] + '-W' + df['WeekOfMonth'].astype(str)
    df['TotalWeightPerDay'] = df.groupby('Date')['Weight (Kg)'].transform('sum')

    # Calculate capacity metrics
    df['CapacityExceeded'] = df['TotalWeightPerDay'] > DAILY_CAPACITY_LIMIT
    df['CapacityExcessAmount'] = np.where(df['CapacityExceeded'],
                                          df['TotalWeightPerDay'] - DAILY_CAPACITY_LIMIT,
                                          0)
    return df


def calculate_co2_emission(weight_kg, waste_stream):
    """
    Calculate CO2 emission for a given weight and waste stream.
    """
    return (weight_kg / 1000) * EMISSION_FACTORS.get(waste_stream, 0)


def calculate_environmental_impact(weight_kg, waste_stream):
    """
    Calculate environmental impact metrics for a given weight and waste stream.
    """
    co2_emission = calculate_co2_emission(weight_kg, waste_stream)
    return {
        'co2_emission': co2_emission,
        'carbon_emission': co2_emission / 3.67,
        'trees_equivalent': 0.0164 * co2_emission,
        'diesel_saved': 0.372 * co2_emission,
        'lamp_hours': 0.04 * co2_emission,
        'coal_avoided': 0.5 * co2_emission
    }


# 2. File Operations and Validations
def load_data(filepath):
    """
    Load waste management data from the specified file.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return pd.read_excel(filepath)


# 3. Utility Functions for Charts
def prepare_category_chart(df):
    """
    Prepare data for category chart visualization.
    """
    category_data = df.groupby('Category Ecosystem')['Weight (Kg)'].sum().reset_index()
    return category_data


# Ensure directories exist for the application
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)
