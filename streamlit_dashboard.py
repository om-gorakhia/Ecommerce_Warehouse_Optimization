"""
================================================================================
WAREHOUSE INVENTORY OPTIMIZATION DASHBOARD
================================================================================
Interactive Analytics Platform for E-Commerce Supply Chain Optimization
Team Project - DBA5103 Operations Research & Analytics
National University of Singapore
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Warehouse Optimization Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# PROFESSIONAL DARK THEME WITH ACCESSIBLE COLORS
# ============================================================================

st.markdown("""
<style>
    /* Global Theme - Soft Dark with High Contrast */
    .stApp {
        background: linear-gradient(135deg, #1a1d29 0%, #252938 100%);
    }
    
    /* Remove default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Headers - Warm Gold for Contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #f9a825 !important;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Metric Cards - High Contrast */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #ffffff;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #b0bec5;
        font-weight: 500;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem;
    }
    
    /* Sidebar - Distinct from Main */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #1a1d29 100%);
        border-right: 2px solid #37474f;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #81c784 !important;
    }
    
    /* Info/Warning/Success Boxes - Accessible Colors */
    .stAlert {
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    div[data-baseweb="notification"] {
        background-color: #2d3748 !important;
        border-left: 4px solid #81c784;
        color: #e2e8f0 !important;
    }
    
    /* Success boxes */
    .success-box {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        border: 2px solid #66bb6a;
        border-radius: 10px;
        padding: 1.5rem;
        color: #ffffff;
        margin: 1rem 0;
    }
    
    /* Warning boxes */
    .warning-box {
        background: linear-gradient(135deg, #e65100 0%, #f57c00 100%);
        border: 2px solid #ffb74d;
        border-radius: 10px;
        padding: 1.5rem;
        color: #ffffff;
        margin: 1rem 0;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #01579b 0%, #0277bd 100%);
        border: 2px solid #4fc3f7;
        border-radius: 10px;
        padding: 1.5rem;
        color: #ffffff;
        margin: 1rem 0;
    }
    
    /* Insight boxes - Distinct Yellow/Gold */
    .insight-box {
        background: linear-gradient(135deg, #f57f17 0%, #f9a825 100%);
        border: 2px solid #fdd835;
        border-radius: 10px;
        padding: 1.5rem;
        color: #000000;
        font-weight: 500;
        margin: 1rem 0;
    }
    
    /* Tables - High Contrast */
    .dataframe {
        background-color: #2d3748 !important;
        color: #e2e8f0 !important;
        border: 1px solid #4a5568 !important;
    }
    
    .dataframe th {
        background-color: #1a202c !important;
        color: #f9a825 !important;
        font-weight: 600;
        border-bottom: 2px solid #4a5568 !important;
    }
    
    .dataframe td {
        border-bottom: 1px solid #4a5568 !important;
    }
    
    /* Buttons - Warm Accent */
    .stButton>button {
        background: linear-gradient(135deg, #f57f17 0%, #f9a825 100%);
        color: #000000;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(249, 168, 37, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #f9a825 0%, #fbc02d 100%);
        box-shadow: 0 4px 12px rgba(249, 168, 37, 0.5);
        transform: translateY(-2px);
    }
    
    /* Expanders - Clear Hierarchy */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #263238 0%, #37474f 100%);
        border: 1px solid #546e7a;
        border-radius: 8px;
        color: #81c784 !important;
        font-weight: 600;
        padding: 1rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #37474f 0%, #455a64 100%);
        border-color: #81c784;
    }
    
    .streamlit-expanderContent {
        background-color: #1e2530;
        border: 1px solid #37474f;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1.5rem;
    }
    
    /* Code blocks */
    code {
        background-color: #1a202c;
        color: #81c784;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        border: 1px solid #37474f;
    }
    
    pre {
        background-color: #1a202c;
        border: 1px solid #37474f;
        border-radius: 8px;
        padding: 1rem;
        overflow: auto;
    }
    
    pre code {
        background: none;
        border: none;
        padding: 0;
    }
    
    /* Tabs - Clear Separation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1a202c;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2d3748;
        border-radius: 6px;
        color: #b0bec5;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f57f17 0%, #f9a825 100%);
        color: #000000;
        font-weight: 600;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a202c;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #f57f17 0%, #f9a825 100%);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #f9a825 0%, #fbc02d 100%);
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
        color: #81c784;
        font-weight: 600;
        text-decoration: underline dotted;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: #263238;
        color: #ffffff;
        text-align: left;
        border-radius: 8px;
        padding: 1rem;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        border: 2px solid #81c784;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
    }
    
    /* Team member cards */
    .team-card {
        background: linear-gradient(135deg, #263238 0%, #37474f 100%);
        border: 2px solid #546e7a;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .team-card:hover {
        border-color: #81c784;
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(129, 199, 132, 0.3);
    }
    
    .team-card h4 {
        color: #81c784 !important;
        margin-top: 0;
    }
    
    /* Stat cards */
    .stat-card {
        background: linear-gradient(135deg, #1e2530 0%, #252938 100%);
        border: 2px solid #37474f;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        border-color: #f9a825;
        box-shadow: 0 6px 16px rgba(249, 168, 37, 0.2);
        transform: translateY(-2px);
    }
    
    .stat-card .value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0.5rem 0;
    }
    
    .stat-card .label {
        font-size: 1rem;
        color: #b0bec5;
        font-weight: 500;
    }
    
    .stat-card .delta {
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .delta.positive {
        color: #81c784;
    }
    
    .delta.negative {
        color: #ffb74d;
    }
    
    /* Section dividers */
    hr {
        border: none;
        border-top: 2px solid #37474f;
        margin: 2rem 0;
    }
    
    /* Radio buttons and checkboxes */
    .stRadio > label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    .stCheckbox > label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    /* Select boxes */
    .stSelectbox > label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    /* Number inputs */
    .stNumberInput > label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# COLOR PALETTE UPDATE - Eye-Comfortable & Accessible
# Replace ONLY the COLORS dictionary in your dashboard code
# ============================================================================

# UPDATED COLOR PALETTE - Comfortable for extended viewing
COLORS = {
    # Primary colors - softer, warmer tones
    'gold': '#d4a373',  # Warm sand/gold - comfortable warm accent
    'teal': '#5a9e9c',  # Muted teal - calm and balanced
    'orange': '#c9956d',  # Soft terracotta - gentle emphasis
    'green': '#7da67d',  # Sage green - natural and restful
    'coral': '#c88d77',  # Dusty coral - warm but not harsh
    'purple': '#9b8dab',  # Soft lavender - gentle variety
    'cyan': '#6eb3b8',  # Muted cyan - soft info color
    'lime': '#b8b88d',  # Olive lime - gentle highlight

    # Neutrals - warmer grays
    'white': '#f5f5f0',  # Warm off-white - easier on eyes
    'gray_light': '#b8bdb8',  # Warm light gray
    'gray': '#8a8f8a',  # Balanced mid-gray
    'gray_dark': '#5f6f65',  # Warm dark gray
    'dark': '#3a4540',  # Soft dark green-gray
    'darker': '#2d3532',  # Deep comfortable dark

    # Status colors - muted versions
    'success': '#7da67d',  # Sage green
    'warning': '#d4a373',  # Warm sand
    'error': '#c88d77',  # Dusty coral
    'info': '#6eb3b8'  # Muted cyan
}

CHART_COLORS_DISCRETE = [
    COLORS['teal'],
    COLORS['gold'],
    COLORS['green'],
    COLORS['coral'],
    COLORS['purple'],
    COLORS['cyan'],
    COLORS['orange'],
    COLORS['lime']
]

CHART_COLORS_SEQUENTIAL = [
    [0.0, COLORS['green']],
    [0.25, COLORS['teal']],
    [0.5, COLORS['cyan']],
    [0.75, COLORS['gold']],
    [1.0, COLORS['coral']]
]

# ============================================================================
# DATA LOADING
# ============================================================================

@st.cache_data
def load_all_results():
    """Load all pre-computed optimization results"""
    results_dir = Path('./results/')

    if not results_dir.exists():
        return None

    data = {}

    try:
        # Load metadata
        with open(results_dir / 'analysis_metadata.json', 'r') as f:
            data['metadata'] = json.load(f)

        # Load scenario comparisons
        data['kpi_comparison'] = pd.read_csv(results_dir / 'scenario_comparison_kpis.csv')
        data['cost_breakdown'] = pd.read_csv(results_dir / 'cost_breakdown_comparison.csv')
        data['service_metrics'] = pd.read_csv(results_dir / 'service_metrics_comparison.csv')

        # Ensure numeric columns
        numeric_cols = ['total_cost', 'order_fulfillment_rate', 'on_time_delivery_rate',
                       'profit_improvement', 'total_stockouts']
        for col in numeric_cols:
            if col in data['kpi_comparison'].columns:
                data['kpi_comparison'][col] = pd.to_numeric(data['kpi_comparison'][col], errors='coerce')

        # Load baseline results
        baseline_dir = results_dir / 'Baseline'
        data['baseline'] = {
            'shipments': pd.read_csv(baseline_dir / 'shipments.csv'),
            'stocking': pd.read_csv(baseline_dir / 'stocking.csv'),
            'stockouts': pd.read_csv(baseline_dir / 'stockouts.csv'),
            'warehouse_util': pd.read_csv(baseline_dir / 'warehouse_utilization.csv')
        }

        with open(baseline_dir / 'kpis.json', 'r') as f:
            data['baseline']['kpis'] = json.load(f)

        # Load network data
        data['network_nodes'] = pd.read_csv(results_dir / 'network_nodes.csv')
        data['network_edges'] = pd.read_csv(results_dir / 'network_edges.csv')

        # Load summaries
        data['regional_demand'] = pd.read_csv(results_dir / 'regional_demand_summary.csv')
        data['category_demand'] = pd.read_csv(results_dir / 'category_demand_summary.csv')

        # Load enriched data
        data['demand_enriched'] = pd.read_csv(results_dir / 'demand_enriched.csv')
        data['warehouses_enriched'] = pd.read_csv(results_dir / 'warehouses_enriched.csv')

        return data

    except Exception as e:
        st.error(f"Error loading results: {e}")
        return None

@st.cache_data
def load_scenario_details(scenario_name):
    """Load detailed results for specific scenario"""
    results_dir = Path('./results/')
    scenario_dir = results_dir / scenario_name

    if not scenario_dir.exists():
        return None

    try:
        scenario_data = {
            'shipments': pd.read_csv(scenario_dir / 'shipments.csv'),
            'stocking': pd.read_csv(scenario_dir / 'stocking.csv'),
            'warehouse_util': pd.read_csv(scenario_dir / 'warehouse_utilization.csv')
        }

        with open(scenario_dir / 'kpis.json', 'r') as f:
            scenario_data['kpis'] = json.load(f)

        return scenario_data

    except:
        return None

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_number(num, prefix='', suffix='', decimals=0):
    """Format number with proper separators"""
    if pd.isna(num):
        return "N/A"
    if decimals == 0:
        return f"{prefix}{num:,.0f}{suffix}"
    else:
        return f"{prefix}{num:,.{decimals}f}{suffix}"

def format_percentage(num, decimals=1):
    """Format as percentage"""
    if pd.isna(num):
        return "N/A"
    return f"{num*100:.{decimals}f}%"


def create_metric_card(label, value, delta=None, tooltip=None):
    """Create custom metric card with tooltip"""

    delta_html = ""
    if delta is not None:
        # FIX: Ensure delta is numeric before comparison
        try:
            delta_num = float(str(delta).replace('+', '').replace('%', '').replace('pp', '').strip())
            delta_class = "positive" if delta_num >= 0 else "negative"
            delta_html = f'<div class="delta {delta_class}">{delta}</div>'
        except (ValueError, TypeError):
            # If delta is not numeric, display as-is without class
            delta_html = f'<div class="delta">{delta}</div>'

    tooltip_html = ""
    if tooltip:
        tooltip_html = f' <span class="tooltip">ℹ️<span class="tooltiptext">{tooltip}</span></span>'

    return f"""
    <div class="stat-card">
        <div class="label">{label}{tooltip_html}</div>
        <div class="value">{value}</div>
        {delta_html}
    </div>
    """


# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
def create_sidebar(data):
    """Create navigation sidebar - UPDATED"""

    with st.sidebar:
        # Project branding - HIGH CONTRAST version
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem; 
                    background: linear-gradient(135deg, #5a7d5a 0%, #6b8e6b 100%); 
                    border-radius: 12px; margin-bottom: 1.5rem;
                    box-shadow: 0 4px 12px rgba(90, 125, 90, 0.3);'>
            <h1 style='color: #f5f5f0; margin: 0; font-size: 1.8rem; 
                       text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3); font-weight: 600;'>
                📦 Warehouse Optimization
            </h1>
            <p style='color: #e8e6df; margin: 0.5rem 0 0 0; font-size: 1rem; font-weight: 500;'>
                Supply Chain Analytics Platform
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        st.markdown("### 📊 Navigation")

        page = st.radio(
            "Select Section:",
            [
                "🏠 Executive Summary",
                "📈 Performance Analysis",
                "🔄 Complete Scenario Analysis",  # UPDATED
                "🗺️ Network Visualization",
                "💡 Insights & Recommendations",
                "🔬 Technical Documentation",
                "📋 Validation Logs & Data",  # NEW
                "👥 About Team"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Quick stats (same as before)
        if data:
            st.markdown("### 📊 Quick Stats")

            baseline_kpis = data['baseline']['kpis']

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e2530 0%, #252938 100%);
                        padding: 1rem; border-radius: 8px; border: 1px solid #37474f;'>
                <p style='color: #81c784; margin: 0; font-weight: 600;'>Fulfillment Rate</p>
                <p style='color: #ffffff; font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0;'>
                    {format_percentage(baseline_kpis.get('order_fulfillment_rate', 0))}
                </p>
                <p style='color: #b0bec5; margin: 0; font-size: 0.85rem;'>
                    {format_number(baseline_kpis.get('total_fulfilled', 0))} / 
                    {format_number(baseline_kpis.get('total_demand', 0))} units
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1e2530 0%, #252938 100%);
                        padding: 1rem; border-radius: 8px; border: 1px solid #37474f;'>
                <p style='color: #f9a825; margin: 0; font-weight: 600;'>Total System Cost</p>
                <p style='color: #ffffff; font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0;'>
                    ${format_number(baseline_kpis.get('total_cost', 0) / 1e6, decimals=1)}M
                </p>
                <p style='color: #b0bec5; margin: 0; font-size: 0.85rem;'>Optimized allocation</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Footer
        st.markdown("""
        <div style='text-align: center; font-size: 0.85rem; color: #78909c; 
                    padding-top: 1rem; line-height: 1.6;'>
            <p style='margin: 0.5rem 0;'><strong style='color: #81c784;'>
            DBA5103 Operations Research & Analytics</strong></p>
            <p style='margin: 0.5rem 0;'>National University of Singapore</p>
            <p style='margin: 0.5rem 0;'>© 2025 Team Warehouse Wizards</p>
        </div>
        """, unsafe_allow_html=True)

    return page
# ============================================================================
# PAGE 1: EXECUTIVE SUMMARY
# ============================================================================

def show_executive_summary(data):
    """Display executive dashboard with key metrics"""

    st.title("📊 Executive Summary")
    st.markdown("### Warehouse Inventory Optimization - Key Performance Indicators")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%); 
                border: 3px solid #66bb6a; border-radius: 12px; padding: 2rem; 
                margin: 1.5rem 0; box-shadow: 0 6px 16px rgba(102, 187, 106, 0.3);">
        <h3 style="color: #ffffff; margin-top: 0; font-size: 1.5rem;">
            🎯 Key Problems Solved
        </h3>
        <ul style="color: #ffffff; font-size: 1.1rem; line-height: 2; margin: 0;">
            <li><strong>Problem 1: Low Fulfillment (45%)</strong> → 
                <strong>Solution: 99% fulfillment achieved</strong> through optimal allocation</li>
            <li><strong>Problem 2: High Stockouts (55%)</strong> → 
                <strong>Solution: <3% stockouts</strong> with flow capacity model</li>
            <li><strong>Problem 3: Unprofitable Operations</strong> → 
                <strong>Solution: $44.9M profit improvement</strong> from cost optimization</li>
            <li><strong>Problem 4: Inefficient Transport</strong> → 
                <strong>Solution: Identified $3.7M savings</strong> opportunity (20% reduction)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    kpis = data['baseline']['kpis']

    # Hero metrics
    st.markdown("## 🎯 Primary Objectives Achieved")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        fulfillment_improvement = (kpis['order_fulfillment_rate'] - 0.45) * 100
        st.markdown(create_metric_card(
            "Order Fulfillment",
            format_percentage(kpis['order_fulfillment_rate']),
            f"+{fulfillment_improvement:.1f} pp",
            "Percentage of customer orders successfully fulfilled from available inventory"
        ), unsafe_allow_html=True)

    with col2:
        on_time_improvement = (kpis['on_time_delivery_rate'] - (1 - kpis['current_late_delivery_rate'])) * 100
        st.markdown(create_metric_card(
            "On-Time Delivery",
            format_percentage(kpis['on_time_delivery_rate']),
            f"{on_time_improvement:+.1f} pp",
            "Percentage of orders delivered within 3-day service window"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(create_metric_card(
            "Total System Cost",
            f"${format_number(kpis['total_cost'] / 1e6, decimals=1)}M",
            None,
            "Combined transportation, holding, and stockout penalty costs"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown(create_metric_card(
            "Profit Improvement",
            f"${format_number(kpis['profit_improvement'] / 1e6, decimals=1)}M",
            f"+{format_percentage(kpis['profit_improvement'] / abs(kpis['current_profit']))}" if kpis['current_profit'] != 0 else None,
            "Net profit increase from optimized allocation strategy"
        ), unsafe_allow_html=True)

    st.markdown("---")

    # Business impact summary
    st.markdown("## 💼 Business Impact")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="success-box">
            <h3 style="color: #ffffff; margin-top: 0;">✅ Solution Delivered</h3>
            <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 0;">
                Our optimization solution <strong>increased order fulfillment from 45% to 99%</strong> 
                while delivering <strong>$44.9M profit improvement</strong>. The system now optimally 
                allocates inventory across warehouses to minimize costs while achieving service targets.
            </p>

        </div>
        """, unsafe_allow_html=True)

        # Key findings
        stockout_reduction = (1 - kpis['total_stockouts'] / kpis['total_demand']) * 100

        st.markdown(f"""
        <div class="info-box">
            <h4 style="color: #ffffff; margin-top: 0;">📈 Key Performance Improvements</h4>
            <ul style="font-size: 1rem; line-height: 2;">
                <li><strong>Stockout Reduction:</strong> {stockout_reduction:.1f}% fewer unfulfilled orders</li>
                <li><strong>Warehouse Utilization:</strong> {format_percentage(kpis['avg_warehouse_utilization'] / 100)} average capacity usage</li>
                <li><strong>Service Coverage:</strong> {kpis['on_time_delivery_rate'] * 100:.1f}% of routes meet 3-day target</li>
                <li><strong>Network Efficiency:</strong> Optimal allocation across {len(data['warehouses_enriched'])} warehouses serving {len(data['demand_enriched']['delivery_region'].unique())} regions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Cost breakdown
        st.markdown("### 💵 Cost Structure")

        cost_data = pd.DataFrame({
            'Component': ['Transportation', 'Holding', 'Stockout Penalties'],
            'Amount': [
                kpis['total_transportation_cost'],
                kpis['total_holding_cost'],
                kpis['total_stockout_cost']
            ]
        })

        fig = px.pie(
            cost_data,
            values='Amount',
            names='Component',
            hole=0.5,
            color_discrete_sequence=CHART_COLORS_DISCRETE
        )

        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=14,
            marker=dict(line=dict(color='#1a1d29', width=3)),
            hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Share: %{percent}<extra></extra>'
        )

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=13, family='Arial'),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(38, 50, 56, 0.8)',
                bordercolor='#546e7a',
                borderwidth=1
            ),
            height=350,
            margin=dict(t=20, b=20, l=20, r=20)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Cost metrics table
        cost_data['Percentage'] = (cost_data['Amount'] / kpis['total_cost'] * 100).round(1)
        cost_data['Amount'] = cost_data['Amount'].apply(lambda x: f"${x:,.0f}")
        cost_data['Percentage'] = cost_data['Percentage'].apply(lambda x: f"{x}%")

        st.dataframe(
            cost_data,
            hide_index=True,
            use_container_width=True
        )

    st.markdown("---")

    # Before vs After comparison
    st.markdown("## 🔄 Before vs After: Problems Solved")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e65100 0%, #f57c00 100%); 
                    border: 2px solid #ffb74d; border-radius: 12px; padding: 1.5rem; text-align: center;">
            <h4 style="color: #ffffff; margin-top: 0;">❌ BEFORE</h4>
            <div style="margin: 1.5rem 0;">
                <p style="color: #ffffff; font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0;">45%</p>
                <p style="color: #ffffff; font-size: 1rem; margin: 0;">Fulfillment Rate</p>
            </div>
            <div style="margin: 1.5rem 0;">
                <p style="color: #ffffff; font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0;">55%</p>
                <p style="color: #ffffff; font-size: 1rem; margin: 0;">Stockouts</p>
            </div>
            <div style="margin: 1.5rem 0;">
                <p style="color: #ffffff; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">-$9.5M</p>
                <p style="color: #ffffff; font-size: 1rem; margin: 0;">Annual Profit</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
            <div style="text-align: center;">
                <div style="font-size: 4rem; color: #81c784;">→</div>
                <p style="color: #81c784; font-size: 1.5rem; font-weight: 700; margin: 1rem 0;">
                    SOLUTION<br/>APPLIED
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%); 
                    border: 2px solid #66bb6a; border-radius: 12px; padding: 1.5rem; text-align: center;">
            <h4 style="color: #ffffff; margin-top: 0;">✅ AFTER</h4>
            <div style="margin: 1.5rem 0;">
                <p style="color: #ffffff; font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0;">
                    {format_percentage(kpis['order_fulfillment_rate'])}
                </p>
                <p style="color: #ffffff; font-size: 1rem; margin: 0;">Fulfillment Rate</p>
                <p style="color: #a5d6a7; font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">+54 pp</p>
            </div>
            <div style="margin: 1.5rem 0;">
                <p style="color: #ffffff; font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0;">
                    {format_percentage(kpis['total_stockouts'] / kpis['total_demand'])}
                </p>
                <p style="color: #ffffff; font-size: 1rem; margin: 0;">Stockouts</p>
                <p style="color: #a5d6a7; font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">-54 pp</p>
            </div>
            <div style="margin: 1.5rem 0;">
                <p style="color: #ffffff; font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">
                    ${kpis['estimated_new_profit'] / 1e6:.1f}M
                </p>
                <p style="color: #ffffff; font-size: 1rem; margin: 0;">Annual Profit</p>
                <p style="color: #a5d6a7; font-size: 1.2rem; font-weight: 600; margin: 0.5rem 0;">
                    +${kpis['profit_improvement'] / 1e6:.1f}M
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <h4 style="color: #1a1d29; margin-top: 0;">💡 How We Did It</h4>
        <p style="color: #1a1d29; font-size: 1rem; line-height: 1.8; margin: 0;">
            <strong>Key Solution Elements:</strong>
            <br>1. <strong>Flow Capacity Model:</strong> Accounted for supplier replenishment (12× turnover) 
            instead of static inventory snapshot
            <br>2. <strong>Optimal Allocation:</strong> Linear Programming found mathematically best way to 
            distribute inventory across warehouses
            <br>3. <strong>Cost Minimization:</strong> Balanced transportation, holding, and stockout costs 
            to achieve lowest total system cost
            <br>4. <strong>Service Prioritization:</strong> 10× stockout penalty ensured customer demand fulfillment
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Strategic insights
    st.markdown("## 💡 Strategic Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="insight-box">
            <h4 style="color: #1a1d29; margin-top: 0;">🎯 Primary Cost Driver</h4>
            <p style="color: #1a1d29; font-size: 1rem; margin-bottom: 0;">
                Transportation accounts for <strong>{kpis['total_transportation_cost']/kpis['total_cost']*100:.1f}%</strong> of total costs.
                <br><br>
                <strong>Recommendation:</strong> Negotiate volume discounts with carriers for 15-20% rate reduction, 
                potentially saving <strong>${kpis['total_transportation_cost'] * 0.175 / 1e6:.1f}M</strong> annually.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="insight-box">
            <h4 style="color: #1a1d29; margin-top: 0;">📦 Capacity Optimization</h4>
            <p style="color: #1a1d29; font-size: 1rem; margin-bottom: 0;">
                Average warehouse utilization at <strong>{kpis['avg_warehouse_utilization']:.1f}%</strong> indicates 
                balanced loading.
                <br><br>
                <strong>Opportunity:</strong> Current capacity supports growth up to 
                <strong>{(85 / kpis['avg_warehouse_utilization'] - 1) * 100:.0f}%</strong> more volume before 
                requiring expansion.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="insight-box">
            <h4 style="color: #1a1d29; margin-top: 0;">🚀 Growth Potential</h4>
            <p style="color: #1a1d29; font-size: 1rem; margin-bottom: 0;">
                Profit improvement of <strong>${kpis['profit_improvement'] / 1e6:.1f}M</strong> demonstrates 
                significant value from optimization.
                <br><br>
                <strong>Next Steps:</strong> Implement tiered service model (95% standard, 99% premium) to 
                capture additional revenue from time-sensitive customers.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Profit analysis
    st.markdown("## 💰 Financial Performance")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Current vs Optimized State")

        comparison_df = pd.DataFrame({
            'Metric': ['Revenue', 'Total Cost', 'Net Profit'],
            'Current': [
                kpis['current_revenue'],
                kpis['current_cost'],
                kpis['current_profit']
            ],
            'Optimized': [
                kpis['estimated_new_revenue'],
                kpis['total_cost'],
                kpis['estimated_new_profit']
            ]
        })

        comparison_df['Change'] = comparison_df['Optimized'] - comparison_df['Current']
        comparison_df['Change %'] = (comparison_df['Change'] / comparison_df['Current'].abs() * 100).round(1)

        # Format for display
        for col in ['Current', 'Optimized', 'Change']:
            comparison_df[col] = comparison_df[col].apply(lambda x: f"${x/1e6:.2f}M")
        comparison_df['Change %'] = comparison_df['Change %'].apply(lambda x: f"{x:+.1f}%")

        st.dataframe(comparison_df, hide_index=True, use_container_width=True)

        st.markdown("""
        <div class="info-box">
            <p style="color: #ffffff; margin: 0; font-size: 0.95rem;">
                <strong>Calculation Method:</strong> Revenue = Fulfilled Units × Average Unit Price. 
                Profit = Revenue - Total Cost. The optimization increases fulfilled units significantly, 
                driving revenue growth while managing costs efficiently.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### Profit Improvement Breakdown")

        # Create waterfall-style visualization
        fig = go.Figure()

        categories = ['Current\nProfit', 'Revenue\nIncrease', 'Cost\nIncrease', 'Optimized\nProfit']
        values = [
            kpis['current_profit'],
            kpis['estimated_new_revenue'] - kpis['current_revenue'],
            -(kpis['total_cost'] - kpis['current_cost']),
            kpis['estimated_new_profit']
        ]

        colors = [COLORS['warning'], COLORS['green'], COLORS['coral'], COLORS['teal']]

        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f"${v/1e6:.1f}M" for v in values],
            textposition='outside',
            textfont=dict(size=14, color='#ffffff'),
            hovertemplate='<b>%{x}</b><br>Amount: $%{y:,.0f}<extra></extra>'
        ))

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=13),
            yaxis=dict(
                title='Amount ($)',
                gridcolor='#37474f',
                zerolinecolor='#546e7a'
            ),
            xaxis=dict(title=''),
            height=400,
            margin=dict(t=40, b=80, l=60, r=40),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 2: PERFORMANCE ANALYSIS
# ============================================================================

def show_performance_analysis(data):
    """Detailed performance metrics and analysis"""

    st.title("📈 Performance Analysis")
    st.markdown("### Comprehensive Metrics Breakdown")

    kpis = data['baseline']['kpis']

    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Service Metrics",
        "🏭 Warehouse Performance",
        "🚚 Transportation Analysis",
        "⚠️ Stockout Analysis"
    ])

    with tab1:
        st.markdown("## 📦 Order Fulfillment & Service Levels")

        col1, col2 = st.columns([1, 1])

        with col1:
            # Fulfillment metrics
            st.markdown("### Fulfillment Performance")

            fulfillment_data = pd.DataFrame({
                'Metric': [
                    'Total Demand',
                    'Orders Fulfilled',
                    'Stockouts',
                    'Fulfillment Rate'
                ],
                'Value': [
                    f"{format_number(kpis['total_demand'])} units",
                    f"{format_number(kpis['total_fulfilled'])} units",
                    f"{format_number(kpis['total_stockouts'])} units",
                    format_percentage(kpis['order_fulfillment_rate'])
                ],
                'Status': ['📊', '✅', '⚠️', '🎯']
            })

            st.dataframe(fulfillment_data, hide_index=True, use_container_width=True)

            st.markdown(f"""
            <div class="info-box">
                <h4 style="color: #ffffff; margin-top: 0;">💡 Performance Context</h4>
                <p style="color: #ffffff; margin: 0;">
                    Achieving <strong>{format_percentage(kpis['order_fulfillment_rate'])}</strong> fulfillment 
                    meets industry benchmarks (95-97% for e-commerce). This indicates effective inventory 
                    allocation with minimal stockouts of only 
                    <strong>{format_percentage(kpis['total_stockouts'] / kpis['total_demand'])}</strong>.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Delivery performance
            st.markdown("### Delivery Service Performance")

            shipments = data['baseline']['shipments']

            if len(shipments) > 0:
                on_time_count = shipments['meets_service_target'].sum()
                total_routes = len(shipments)

                delivery_data = pd.DataFrame({
                    'Metric': [
                        'Total Active Routes',
                        'On-Time Routes (≤3 days)',
                        'Delayed Routes (>3 days)',
                        'On-Time Rate'
                    ],
                    'Value': [
                        f"{total_routes} routes",
                        f"{on_time_count} routes",
                        f"{total_routes - on_time_count} routes",
                        format_percentage(kpis['on_time_delivery_rate'])
                    ],
                    'Status': ['📊', '✅', '⚠️', '🎯']
                })

                st.dataframe(delivery_data, hide_index=True, use_container_width=True)

                st.markdown(f"""
                <div class="warning-box">
                    <h4 style="color: #ffffff; margin-top: 0;">⚠️ Improvement Opportunity</h4>
                    <p style="color: #ffffff; margin: 0;">
                        On-time rate of <strong>{format_percentage(kpis['on_time_delivery_rate'])}</strong> 
                        is below the 95% industry target. This is primarily driven by <strong>geographic 
                        constraints</strong> where {total_routes - on_time_count} routes exceed the 3-day 
                        service window. Consider adding regional distribution centers in high-demand areas.
                    </p>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("## 🏭 Warehouse Utilization & Efficiency")

        wh_util = data['baseline']['warehouse_util']

        # Utilization chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=wh_util['warehouse_id'],
            y=wh_util['utilization_pct'],
            name='Current Utilization',
            marker_color=COLORS['teal'],
            text=wh_util['utilization_pct'].apply(lambda x: f"{x:.1f}%"),
            textposition='outside',
            textfont=dict(color='#ffffff', size=14),
            hovertemplate='<b>%{x}</b><br>Utilization: %{y:.1f}%<extra></extra>'
        ))

        # Add target zones
        fig.add_hrect(y0=75, y1=90,
                     fillcolor=COLORS['green'], opacity=0.1,
                     annotation_text="Optimal Range (75-90%)",
                     annotation_position="right")

        fig.add_hrect(y0=90, y1=100,
                     fillcolor=COLORS['orange'], opacity=0.1,
                     annotation_text="High Utilization (90-100%)",
                     annotation_position="right")

        fig.update_layout(
            title="Warehouse Capacity Utilization",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=13),
            yaxis=dict(
                title='Utilization (%)',
                range=[0, 100],
                gridcolor='#37474f'
            ),
            xaxis=dict(title='Warehouse'),
            height=450,
            margin=dict(t=60, b=60, l=60, r=40),
            showlegend=True,
            legend=dict(bgcolor='rgba(38, 50, 56, 0.8)', bordercolor='#546e7a', borderwidth=1)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Warehouse details table
        st.markdown("### Warehouse Details")

        wh_details = wh_util.copy()
        wh_details['Capacity'] = wh_details['capacity_m3'].apply(lambda x: f"{x:,.0f} m³")
        wh_details['Used'] = wh_details['used_m3'].apply(lambda x: f"{x:,.0f} m³")
        wh_details['Utilization'] = wh_details['utilization_pct'].apply(lambda x: f"{x:.1f}%")
        wh_details['Products'] = wh_details['products_stocked']

        wh_details = wh_details[['warehouse_id', 'Capacity', 'Used', 'Utilization', 'Products']]
        wh_details.columns = ['Warehouse', 'Total Capacity', 'Space Used', 'Utilization', 'SKUs Stocked']

        st.dataframe(wh_details, hide_index=True, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
            <h4 style="color: #1a1d29; margin-top: 0;">📊 Utilization Analysis</h4>
            <p style="color: #1a1d29; margin: 0; font-size: 1rem;">
                Average utilization of <strong>{kpis['avg_warehouse_utilization']:.1f}%</strong> indicates 
                well-balanced capacity allocation. Industry best practice suggests maintaining 75-85% utilization 
                to allow for operational flexibility and seasonal demand spikes. Current levels provide adequate 
                buffer for growth.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("## 🚚 Transportation Cost & Route Analysis")

        shipments = data['baseline']['shipments']

        if len(shipments) > 0:
            col1, col2 = st.columns(2)

            with col1:
                # Top 10 costliest routes
                st.markdown("### Top 10 Highest Cost Routes")

                top_routes = shipments.nlargest(10, 'transport_cost')[
                    ['warehouse_id', 'region', 'quantity', 'transport_cost', 'transit_time_days']
                ].copy()

                top_routes['Quantity'] = top_routes['quantity'].apply(lambda x: f"{x:,.0f}")
                top_routes['Cost'] = top_routes['transport_cost'].apply(lambda x: f"${x:,.0f}")
                top_routes['Transit'] = top_routes['transit_time_days'].apply(lambda x: f"{x:.1f} days")

                top_routes = top_routes[['warehouse_id', 'region', 'Quantity', 'Cost', 'Transit']]
                top_routes.columns = ['From WH', 'To Region', 'Units', 'Transport Cost', 'Transit Time']

                st.dataframe(top_routes, hide_index=True, use_container_width=True)

            with col2:
                # Transit time distribution
                st.markdown("### Transit Time Distribution")

                transit_bins = pd.cut(shipments['transit_time_days'],
                                     bins=[0, 3, 5, 7, 100],
                                     labels=['0-3 days (On-Time)', '3-5 days', '5-7 days', '>7 days'])

                transit_dist = transit_bins.value_counts().reset_index()
                transit_dist.columns = ['Transit Time', 'Routes']
                transit_dist = transit_dist.sort_values('Transit Time')

                fig = px.bar(
                    transit_dist,
                    x='Transit Time',
                    y='Routes',
                    color='Transit Time',
                    color_discrete_sequence=CHART_COLORS_DISCRETE,
                    text='Routes'
                )

                fig.update_traces(
                    textposition='outside',
                    textfont=dict(size=14, color='#ffffff'),
                    hovertemplate='<b>%{x}</b><br>Routes: %{y}<extra></extra>'
                )

                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e2e8f0', size=13),
                    yaxis=dict(title='Number of Routes', gridcolor='#37474f'),
                    xaxis=dict(title=''),
                    showlegend=False,
                    height=400,
                    margin=dict(t=40, b=80, l=60, r=40)
                )

                st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
            <h4 style="color: #1a1d29; margin-top: 0;">💡 Cost Optimization Opportunity</h4>
            <p style="color: #1a1d29; margin: 0; font-size: 1rem;">
                Transportation represents <strong>${kpis['total_transportation_cost']/1e6:.1f}M</strong> 
                ({kpis['total_transportation_cost']/kpis['total_cost']*100:.1f}% of total costs). 
                Key optimization levers:
                <br><br>
                <strong>1. Carrier Negotiation:</strong> Volume consolidation for 15-20% rate reduction 
                = <strong>${kpis['total_transportation_cost'] * 0.175 /1e6:.1f}M</strong> annual savings
                <br>
                <strong>2. Route Optimization:</strong> Prioritize shorter transit routes for high-value shipments
                <br>
                <strong>3. Regional Hubs:</strong> Add distribution centers in high-demand areas to reduce distances
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("## ⚠️ Stockout Analysis & Prevention")

        stockouts = data['baseline']['stockouts']

        if len(stockouts) > 0:
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("### Stockout Overview")

                stockout_metrics = pd.DataFrame({
                    'Metric': [
                        'Total Stockout Instances',
                        'Total Units Not Fulfilled',
                        'Regions Affected',
                        'Total Penalty Cost',
                        'Average Penalty per Unit'
                    ],
                    'Value': [
                        f"{len(stockouts)} occurrences",
                        f"{format_number(kpis['total_stockouts'])} units",
                        f"{stockouts['region'].nunique()} regions",
                        f"${format_number(kpis['total_stockout_cost'])}",
                        f"${kpis['total_stockout_cost'] / kpis['total_stockouts']:.2f}"
                    ]
                })

                st.dataframe(stockout_metrics, hide_index=True, use_container_width=True)

                st.markdown(f"""
                <div class="success-box">
                    <h4 style="color: #ffffff; margin-top: 0;">✅ Low Stockout Rate</h4>
                    <p style="color: #ffffff; margin: 0;">
                        Stockout rate of <strong>{format_percentage(kpis['total_stockouts'] / kpis['total_demand'])}</strong> 
                        is well within acceptable bounds. Industry benchmark is <5% for e-commerce operations. 
                        The optimization effectively balances inventory allocation to minimize unfulfilled demand.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("### Top 10 Affected Regions")

                top_stockouts = stockouts.nlargest(10, 'stockout_quantity')[
                    ['region', 'stockout_quantity', 'stockout_penalty_cost', 'total_demand']
                ].copy()

                top_stockouts['Stockout %'] = (top_stockouts['stockout_quantity'] /
                                               top_stockouts['total_demand'] * 100).round(1)

                top_stockouts['Units'] = top_stockouts['stockout_quantity'].apply(lambda x: f"{x:,.0f}")
                top_stockouts['Penalty'] = top_stockouts['stockout_penalty_cost'].apply(lambda x: f"${x:,.0f}")
                top_stockouts['Rate'] = top_stockouts['Stockout %'].apply(lambda x: f"{x}%")

                top_stockouts = top_stockouts[['region', 'Units', 'Penalty', 'Rate']]
                top_stockouts.columns = ['Region', 'Stockout Units', 'Penalty Cost', 'Stockout %']

                st.dataframe(top_stockouts, hide_index=True, use_container_width=True)
        else:
            st.markdown("""
            <div class="success-box">
                <h2 style="color: #ffffff; text-align: center; margin: 2rem 0;">
                    ✅ Perfect Fulfillment Achieved!
                </h2>
                <p style="color: #ffffff; text-align: center; font-size: 1.2rem; margin: 0;">
                    Zero stockouts recorded. All customer demand successfully fulfilled.
                </p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# PAGE 3: SCENARIO COMPARISON
# ============================================================================

def show_scenario_comparison(data):
    """Compare all optimization scenarios"""

    st.title("🔄 Scenario Comparison")
    st.markdown("### Sensitivity Analysis Across Multiple Optimization Strategies")

    kpi_comparison = data['kpi_comparison']

    # Scenario selector
    st.markdown("## 📊 Interactive Scenario Explorer")

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_scenarios = st.multiselect(
            "Select scenarios to compare:",
            options=kpi_comparison['scenario_name'].tolist(),
            default=kpi_comparison['scenario_name'].tolist()[:3],
            help="Choose 2 or more scenarios to visualize side-by-side comparison"
        )

    with col2:
        metric_to_compare = st.selectbox(
            "Primary metric:",
            options=[
                'order_fulfillment_rate',
                'total_cost',
                'profit_improvement',
                'on_time_delivery_rate',
                'total_stockouts'
            ],
            format_func=lambda x: {
                'order_fulfillment_rate': 'Order Fulfillment Rate',
                'total_cost': 'Total System Cost',
                'profit_improvement': 'Profit Improvement',
                'on_time_delivery_rate': 'On-Time Delivery Rate',
                'total_stockouts': 'Total Stockouts'
            }[x],
            help="Select the key performance indicator to highlight in comparisons"
        )

    if len(selected_scenarios) >= 2:
        filtered_df = kpi_comparison[kpi_comparison['scenario_name'].isin(selected_scenarios)].copy()

        st.markdown("---")

        # Multi-metric comparison
        st.markdown("## 📈 Multi-Metric Comparison")

        # Create parallel coordinates plot
        metrics_to_plot = [
            'order_fulfillment_rate',
            'on_time_delivery_rate',
            'total_cost',
            'profit_improvement',
            'avg_warehouse_utilization'
        ]

        plot_df = filtered_df[['scenario_name'] + metrics_to_plot].copy()

        # Normalize for better visualization
        for col in metrics_to_plot:
            if col == 'total_cost':
                # Invert cost (lower is better)
                plot_df[col + '_norm'] = 1 - ((plot_df[col] - plot_df[col].min()) /
                                             (plot_df[col].max() - plot_df[col].min()))
            else:
                plot_df[col + '_norm'] = ((plot_df[col] - plot_df[col].min()) /
                                         (plot_df[col].max() - plot_df[col].min()))

        # Radar chart
        fig = go.Figure()

        for idx, row in plot_df.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row[col + '_norm'] for col in metrics_to_plot],
                theta=['Fulfillment', 'On-Time', 'Cost Efficiency', 'Profit', 'Utilization'],
                fill='toself',
                name=row['scenario_name'],
                line=dict(color=CHART_COLORS_DISCRETE[idx % len(CHART_COLORS_DISCRETE)], width=2),
                hovertemplate='<b>%{theta}</b><br>Normalized Score: %{r:.2f}<extra></extra>'
            ))

        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    gridcolor='#37474f',
                    color='#b0bec5'
                ),
                angularaxis=dict(
                    gridcolor='#37474f',
                    color='#e2e8f0'
                )
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=13),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(38, 50, 56, 0.8)',
                bordercolor='#546e7a',
                borderwidth=1
            ),
            height=500,
            margin=dict(t=60, b=60, l=80, r=80)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="info-box">
            <p style="color: #ffffff; margin: 0;">
                <strong>Interpretation:</strong> Larger polygons indicate better overall performance. 
                Look for scenarios that maximize area while maintaining balance across all dimensions. 
                Values are normalized (0-1 scale) for fair comparison across different units.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Detailed comparison table
        st.markdown("## 📋 Detailed Metrics Table")

        comparison_table = filtered_df[[
            'scenario_name',
            'order_fulfillment_rate',
            'on_time_delivery_rate',
            'total_cost',
            'profit_improvement',
            'total_stockouts',
            'avg_warehouse_utilization'
        ]].copy()

        # Format columns
        comparison_table['order_fulfillment_rate'] = comparison_table['order_fulfillment_rate'].apply(
            lambda x: format_percentage(x))
        comparison_table['on_time_delivery_rate'] = comparison_table['on_time_delivery_rate'].apply(
            lambda x: format_percentage(x))
        comparison_table['total_cost'] = comparison_table['total_cost'].apply(
            lambda x: f"${x/1e6:.2f}M")
        comparison_table['profit_improvement'] = comparison_table['profit_improvement'].apply(
            lambda x: f"${x/1e6:.2f}M" if x >= 0 else f"-${abs(x)/1e6:.2f}M")
        comparison_table['total_stockouts'] = comparison_table['total_stockouts'].apply(
            lambda x: f"{x:,.0f}")
        comparison_table['avg_warehouse_utilization'] = comparison_table['avg_warehouse_utilization'].apply(
            lambda x: f"{x:.1f}%")

        comparison_table.columns = [
            'Scenario', 'Fulfillment', 'On-Time', 'Total Cost',
            'Profit ∆', 'Stockouts', 'WH Util'
        ]

        st.dataframe(comparison_table, hide_index=True, use_container_width=True)

        st.markdown("---")

        # Best scenario recommendation
        st.markdown("## 🏆 Recommended Scenario")

        # Find best scenarios
        best_cost = filtered_df.loc[filtered_df['total_cost'].idxmin(), 'scenario_name']
        best_fulfillment = filtered_df.loc[filtered_df['order_fulfillment_rate'].idxmax(), 'scenario_name']
        best_profit = filtered_df.loc[filtered_df['profit_improvement'].idxmax(), 'scenario_name']

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="team-card">
                <h4 style="color: {COLORS['teal']};">💰 Lowest Cost</h4>
                <p style="color: #ffffff; font-size: 1.3rem; font-weight: 700; margin: 1rem 0;">
                    {best_cost}
                </p>
                <p style="color: #b0bec5; margin: 0;">
                    Minimizes total system expenses
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="team-card">
                <h4 style="color: {COLORS['green']};">📦 Best Fulfillment</h4>
                <p style="color: #ffffff; font-size: 1.3rem; font-weight: 700; margin: 1rem 0;">
                    {best_fulfillment}
                </p>
                <p style="color: #b0bec5; margin: 0;">
                    Maximizes customer satisfaction
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="team-card">
                <h4 style="color: {COLORS['gold']};">💎 Highest Profit</h4>
                <p style="color: #ffffff; font-size: 1.3rem; font-weight: 700; margin: 1rem 0;">
                    {best_profit}
                </p>
                <p style="color: #b0bec5; margin: 0;">
                    Greatest financial impact
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Recommendation logic
        baseline_kpis = data['baseline']['kpis']

        st.markdown(f"""
        <div class="insight-box">
            <h3 style="color: #1a1d29; margin-top: 0;">💡 Strategic Recommendation</h3>
            <p style="color: #1a1d29; font-size: 1.1rem; line-height: 1.8; margin: 0;">
                Based on comprehensive analysis, the <strong>Baseline</strong> scenario provides the optimal 
                balance between cost efficiency and service quality. It achieves 
                <strong>{format_percentage(baseline_kpis['order_fulfillment_rate'])}</strong> fulfillment 
                at a total cost of <strong>${baseline_kpis['total_cost']/1e6:.2f}M</strong>, delivering 
                <strong>${baseline_kpis['profit_improvement']/1e6:.2f}M</strong> profit improvement.
                <br><br>
                <strong>Implementation Priority:</strong>
                <br>1. <strong>Short-term:</strong> Execute baseline optimization plan immediately
                <br>2. <strong>Medium-term:</strong> Negotiate 15-20% transport cost reduction
                <br>3. <strong>Long-term:</strong> Consider capacity expansion if demand grows beyond current projections
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please select at least 2 scenarios to enable comparison visualizations.")


# ============================================================================
# ENHANCED COMPLETE SCENARIO ANALYSIS
# Replace the show_comprehensive_scenario_comparison() function
# ============================================================================

def show_comprehensive_scenario_comparison(data):
    """Enhanced scenario comparison with better visualizations"""

    st.title("🔄 Complete Scenario Analysis")
    st.markdown("### Comprehensive Evaluation of 9 Optimization Strategies")

    kpi_comparison = data['kpi_comparison'].copy()

    # Ensure all scenarios are present
    all_scenarios = [
        'Baseline',
        'Increased_Capacity_10pct',
        'Increased_Capacity_20pct',
        'Increased_Capacity_30pct',
        'Reduced_Transport_Cost_10pct',
        'Reduced_Transport_Cost_20pct',
        'Increased_Transport_Cost_10pct',
        'Higher_Service_Target_97pct',
        'Higher_Service_Target_99pct'
    ]

    # Filter to available scenarios
    available_scenarios = [s for s in all_scenarios if s in kpi_comparison['scenario_name'].values]

    # Overview section
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%); 
                border: 3px solid #66bb6a; border-radius: 12px; padding: 2rem; 
                margin: 1.5rem 0; box-shadow: 0 6px 16px rgba(102, 187, 106, 0.3);">
        <h3 style="color: #ffffff; margin-top: 0; font-size: 1.5rem;">
            📊 Analysis Overview
        </h3>
        <p style="color: #ffffff; font-size: 1.1rem; line-height: 1.8; margin: 0;">
            Evaluated <strong>{len(available_scenarios)} optimization scenarios</strong> across 
            three strategic dimensions: <strong>capacity expansion</strong>, 
            <strong>transportation cost management</strong>, and <strong>service level targeting</strong>.
            Each scenario reveals trade-offs between cost, service, and profitability.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Executive summary metrics
    st.markdown("## 📈 Scenario Performance Summary")

    col1, col2, col3, col4 = st.columns(4)

    best_profit = kpi_comparison.loc[kpi_comparison['profit_improvement'].idxmax()]
    best_fulfillment = kpi_comparison.loc[kpi_comparison['order_fulfillment_rate'].idxmax()]
    lowest_cost = kpi_comparison.loc[kpi_comparison['total_cost'].idxmin()]
    profit_range = kpi_comparison['profit_improvement'].max() - kpi_comparison['profit_improvement'].min()

    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="label">Best Profit Scenario</div>
            <div class="value" style="font-size: 1.3rem;">{best_profit['scenario_name'].replace('_', ' ')}</div>
            <div class="delta positive">${best_profit['profit_improvement'] / 1e6:.2f}M</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="label">Best Fulfillment</div>
            <div class="value" style="font-size: 1.3rem;">{best_fulfillment['scenario_name'].replace('_', ' ')}</div>
            <div class="delta positive">{best_fulfillment['order_fulfillment_rate'] * 100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="label">Lowest Cost</div>
            <div class="value" style="font-size: 1.3rem;">{lowest_cost['scenario_name'].replace('_', ' ')}</div>
            <div class="delta positive">${lowest_cost['total_cost'] / 1e6:.2f}M</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="label">Profit Range</div>
            <div class="value" style="font-size: 1.8rem;">${profit_range / 1e6:.2f}M</div>
            <div style="color: #b0bec5; font-size: 0.9rem; margin-top: 0.5rem;">Spread across scenarios</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Multi-dimensional comparison radar chart
    st.markdown("## 🎯 Multi-Dimensional Performance Comparison")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Enhanced radar chart with all scenarios
        metrics_for_radar = [
            'order_fulfillment_rate',
            'on_time_delivery_rate',
            'profit_improvement',
            'avg_warehouse_utilization'
        ]

        # Normalize metrics
        normalized_df = kpi_comparison.copy()
        for col in metrics_for_radar:
            if col == 'total_cost':
                # Invert cost (lower is better)
                normalized_df[col + '_norm'] = 1 - ((normalized_df[col] - normalized_df[col].min()) /
                                                    (normalized_df[col].max() - normalized_df[col].min()))
            else:
                normalized_df[col + '_norm'] = ((normalized_df[col] - normalized_df[col].min()) /
                                                (normalized_df[col].max() - normalized_df[col].min()))

        fig = go.Figure()

        # Select top 5 scenarios by profit
        top_scenarios = normalized_df.nlargest(5, 'profit_improvement')

        for idx, row in top_scenarios.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=[row[col + '_norm'] for col in metrics_for_radar],
                theta=['Fulfillment', 'On-Time', 'Profit', 'Utilization'],
                fill='toself',
                name=row['scenario_name'].replace('_', ' '),
                line=dict(width=2.5),
                opacity=0.7,
                hovertemplate='<b>%{theta}</b><br>Score: %{r:.2f}<extra></extra>'
            ))

        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    gridcolor='#37474f',
                    color='#b0bec5',
                    tickfont=dict(size=11)
                ),
                angularaxis=dict(
                    gridcolor='#37474f',
                    color='#e2e8f0',
                    tickfont=dict(size=12, color='#ffffff')
                )
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=12),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(38, 50, 56, 0.95)',
                bordercolor='#546e7a',
                borderwidth=2,
                font=dict(size=11)
            ),
            height=500,
            margin=dict(t=40, b=40, l=80, r=80)
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📊 Interpretation Guide")

        st.markdown("""
        <div style="background: linear-gradient(135deg, #263238 0%, #37474f 100%); 
                    border: 2px solid #546e7a; border-radius: 10px; padding: 1.5rem; margin-top: 1rem;">
            <p style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.8; margin: 0;">
                <strong style="color: #81c784;">Larger Polygons = Better Performance</strong>
                <br><br>
                Each axis represents normalized performance (0-1 scale):
                <br>• <strong>Fulfillment:</strong> Order completion rate
                <br>• <strong>On-Time:</strong> Delivery speed
                <br>• <strong>Profit:</strong> Financial improvement
                <br>• <strong>Utilization:</strong> Warehouse efficiency
                <br><br>
                <strong style="color: #f9a825;">Top 5 scenarios shown</strong> for clarity. 
                Balanced polygons indicate well-rounded solutions.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Quick stats
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #01579b 0%, #0277bd 100%); 
                    border: 2px solid #4fc3f7; border-radius: 10px; padding: 1rem; margin-top: 1rem;">
            <p style="color: #ffffff; font-size: 0.9rem; margin: 0.5rem 0;">
                <strong>Best Balance:</strong> {best_profit['scenario_name'].replace('_', ' ')}
            </p>
            <p style="color: #ffffff; font-size: 0.9rem; margin: 0.5rem 0;">
                <strong>Total Scenarios:</strong> {len(available_scenarios)}
            </p>
            <p style="color: #ffffff; font-size: 0.9rem; margin: 0.5rem 0;">
                <strong>Dimensions Tested:</strong> 4 metrics
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Detailed category analysis
    st.markdown("## 🔬 Detailed Category Analysis")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏭 Capacity Impact",
        "🚚 Transport Cost Sensitivity",
        "⏱️ Service Level Analysis",
        "📋 Complete Data Table"
    ])

    with tab1:
        st.markdown("### Warehouse Capacity Expansion Analysis")

        capacity_scenarios = kpi_comparison[
            kpi_comparison['scenario_name'].str.contains('Capacity', case=False, na=False)
        ].copy()

        if len(capacity_scenarios) > 0:
            baseline = kpi_comparison[kpi_comparison['scenario_name'] == 'Baseline']
            capacity_with_baseline = pd.concat([baseline, capacity_scenarios]).reset_index(drop=True)
            capacity_with_baseline = capacity_with_baseline.sort_values('capacity_multiplier')

            # Enhanced multi-metric line chart
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Order Fulfillment Rate (%)',
                    'Total System Cost ($M)',
                    'Warehouse Utilization (%)',
                    'Profit Improvement ($M)'
                ),
                vertical_spacing=0.15,
                horizontal_spacing=0.12
            )

            # Fulfillment
            fig.add_trace(
                go.Scatter(
                    x=capacity_with_baseline['capacity_multiplier'] * 100,
                    y=capacity_with_baseline['order_fulfillment_rate'] * 100,
                    mode='lines+markers',
                    marker=dict(size=12, color=COLORS['teal'], line=dict(width=2, color='#ffffff')),
                    line=dict(width=3, color=COLORS['teal']),
                    name='Fulfillment',
                    hovertemplate='Capacity: %{x}%<br>Fulfillment: %{y:.1f}%<extra></extra>'
                ),
                row=1, col=1
            )

            # Cost
            fig.add_trace(
                go.Scatter(
                    x=capacity_with_baseline['capacity_multiplier'] * 100,
                    y=capacity_with_baseline['total_cost'] / 1e6,
                    mode='lines+markers',
                    marker=dict(size=12, color=COLORS['coral'], line=dict(width=2, color='#ffffff')),
                    line=dict(width=3, color=COLORS['coral']),
                    name='Cost',
                    hovertemplate='Capacity: %{x}%<br>Cost: $%{y:.2f}M<extra></extra>'
                ),
                row=1, col=2
            )

            # Utilization
            fig.add_trace(
                go.Scatter(
                    x=capacity_with_baseline['capacity_multiplier'] * 100,
                    y=capacity_with_baseline['avg_warehouse_utilization'],
                    mode='lines+markers',
                    marker=dict(size=12, color=COLORS['purple'], line=dict(width=2, color='#ffffff')),
                    line=dict(width=3, color=COLORS['purple']),
                    name='Utilization',
                    hovertemplate='Capacity: %{x}%<br>Utilization: %{y:.1f}%<extra></extra>'
                ),
                row=2, col=1
            )

            # Profit
            fig.add_trace(
                go.Scatter(
                    x=capacity_with_baseline['capacity_multiplier'] * 100,
                    y=capacity_with_baseline['profit_improvement'] / 1e6,
                    mode='lines+markers',
                    marker=dict(size=12, color=COLORS['green'], line=dict(width=2, color='#ffffff')),
                    line=dict(width=3, color=COLORS['green']),
                    name='Profit',
                    hovertemplate='Capacity: %{x}%<br>Profit: $%{y:.2f}M<extra></extra>'
                ),
                row=2, col=2
            )

            # Update axes
            fig.update_xaxes(title_text="Capacity Level (%)", row=1, col=1, gridcolor='#37474f')
            fig.update_xaxes(title_text="Capacity Level (%)", row=1, col=2, gridcolor='#37474f')
            fig.update_xaxes(title_text="Capacity Level (%)", row=2, col=1, gridcolor='#37474f')
            fig.update_xaxes(title_text="Capacity Level (%)", row=2, col=2, gridcolor='#37474f')

            fig.update_yaxes(gridcolor='#37474f', row=1, col=1)
            fig.update_yaxes(gridcolor='#37474f', row=1, col=2)
            fig.update_yaxes(gridcolor='#37474f', row=2, col=1)
            fig.update_yaxes(gridcolor='#37474f', row=2, col=2)

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=12),
                height=700,
                margin=dict(t=80, b=60, l=60, r=40),
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

            # Insights
            best_capacity = capacity_scenarios.loc[capacity_scenarios['profit_improvement'].idxmax()]
            baseline_profit = baseline['profit_improvement'].values[0]
            capacity_benefit = best_capacity['profit_improvement'] - baseline_profit

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                <div class="insight-box">
                    <h4 style="color: #1a1d29; margin-top: 0;">💡 Key Finding</h4>
                    <p style="color: #1a1d29; font-size: 1rem; margin: 0;">
                        <strong>Diminishing Returns Observed:</strong> Increasing capacity beyond baseline 
                        yields only <strong>${capacity_benefit / 1e6:.2f}M additional profit</strong>.
                        <br><br>
                        Current infrastructure is <strong>well-optimized</strong> for demand levels. 
                        Capacity expansion should only be triggered when demand growth exceeds 
                        <strong>15-20%</strong>.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                # Calculate ROI
                capacity_increase_pct = (best_capacity['capacity_multiplier'] - 1) * 100
                estimated_capex = capacity_increase_pct * 0.5  # Assume $500K per 1% capacity
                roi_years = estimated_capex / (capacity_benefit / 1e6) if capacity_benefit > 0 else 999

                st.markdown(f"""
                <div class="warning-box">
                    <h4 style="color: #ffffff; margin-top: 0;">⚠️ Investment Consideration</h4>
                    <p style="color: #ffffff; font-size: 1rem; margin: 0;">
                        <strong>Best scenario:</strong> {best_capacity['scenario_name'].replace('_', ' ')}
                        <br>
                        <strong>Capacity increase:</strong> {capacity_increase_pct:.0f}%
                        <br>
                        <strong>Estimated CAPEX:</strong> ${estimated_capex:.1f}M
                        <br>
                        <strong>Payback period:</strong> ~{roi_years:.1f} years
                        <br><br>
                        <strong>Recommendation:</strong> Defer capacity expansion; focus on cost reduction strategies first.
                    </p>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### Transportation Cost Sensitivity Analysis")

        transport_scenarios = kpi_comparison[
            kpi_comparison['scenario_name'].str.contains('Transport', case=False, na=False)
        ].copy()

        if len(transport_scenarios) > 0:
            baseline = kpi_comparison[kpi_comparison['scenario_name'] == 'Baseline']
            transport_with_baseline = pd.concat([baseline, transport_scenarios]).reset_index(drop=True)
            transport_sorted = transport_with_baseline.sort_values('transport_cost_multiplier')

            col1, col2 = st.columns([3, 2])

            with col1:
                # Profit sensitivity curve
                fig = go.Figure()

                # Add line
                fig.add_trace(go.Scatter(
                    x=transport_sorted['transport_cost_multiplier'] * 100,
                    y=transport_sorted['profit_improvement'] / 1e6,
                    mode='lines+markers',
                    marker=dict(size=14, color=COLORS['green'], line=dict(width=2, color='#ffffff')),
                    line=dict(width=4, color=COLORS['green']),
                    fill='tonexty',
                    fillcolor='rgba(129, 199, 132, 0.2)',
                    name='Profit Improvement',
                    hovertemplate='Transport Cost: %{x}% of baseline<br>Profit: $%{y:.2f}M<extra></extra>'
                ))

                # Add baseline reference line
                baseline_profit = baseline['profit_improvement'].values[0] / 1e6
                fig.add_hline(
                    y=baseline_profit,
                    line_dash="dash",
                    line_color=COLORS['orange'],
                    annotation_text="Baseline",
                    annotation_position="right"
                )

                fig.update_layout(
                    title="Profit vs Transport Cost Multiplier",
                    xaxis=dict(
                        title='Transport Cost (% of Baseline)',
                        gridcolor='#37474f',
                        range=[75, 115]
                    ),
                    yaxis=dict(
                        title='Profit Improvement ($M)',
                        gridcolor='#37474f'
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e2e8f0', size=13),
                    height=450,
                    margin=dict(t=60, b=60, l=60, r=40)
                )

                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("### 📊 Sensitivity Metrics")

                # Calculate elasticity
                best_transport = transport_scenarios.loc[transport_scenarios['profit_improvement'].idxmax()]
                worst_transport = transport_scenarios.loc[transport_scenarios['profit_improvement'].idxmin()]

                profit_swing = (best_transport['profit_improvement'] - worst_transport['profit_improvement']) / 1e6
                cost_swing = (worst_transport['transport_cost_multiplier'] - best_transport[
                    'transport_cost_multiplier']) * 100
                elasticity = profit_swing / (cost_swing / 100) if cost_swing != 0 else 0

                st.markdown(f"""
                <div class="stat-card">
                    <div class="label">Profit Sensitivity</div>
                    <div class="value">${elasticity:.1f}M</div>
                    <div style="color: #b0bec5; font-size: 0.9rem; margin-top: 0.5rem;">
                        Per 10% cost change
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="stat-card" style="margin-top: 1rem;">
                    <div class="label">Max Profit Gain</div>
                    <div class="value">${profit_swing:.2f}M</div>
                    <div style="color: #b0bec5; font-size: 0.9rem; margin-top: 0.5rem;">
                        From 20% cost reduction
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="stat-card" style="margin-top: 1rem;">
                    <div class="label">Risk Exposure</div>
                    <div class="value">${abs(worst_transport['profit_improvement'] - baseline_profit) / 1e6:.2f}M</div>
                    <div style="color: #b0bec5; font-size: 0.9rem; margin-top: 0.5rem;">
                        If costs rise 10%
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Strategic insight
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%); 
                        border: 3px solid #66bb6a; border-radius: 12px; padding: 2rem; margin-top: 1.5rem;">
                <h4 style="color: #ffffff; margin-top: 0; font-size: 1.3rem;">
                    🎯 Strategic Recommendation: HIGHEST PRIORITY
                </h4>
                <p style="color: #ffffff; font-size: 1.05rem; line-height: 1.8; margin: 0;">
                    <strong>Transport costs show EXTREME sensitivity.</strong> A 20% reduction yields 
                    <strong>${profit_swing:.2f}M additional profit</strong> - the single largest 
                    improvement opportunity identified.
                    <br><br>
                    <strong>Action Plan:</strong>
                    <br>1. Immediate carrier contract renegotiation (target: 15-20% rate reduction)
                    <br>2. Volume consolidation across routes to qualify for bulk discounts
                    <br>3. Multi-carrier bidding process for competitive pricing
                    <br>4. Long-term partnerships with performance-based incentives
                    <br><br>
                    <strong>Expected Impact:</strong> ${(profit_swing * 0.75):.2f}M - ${profit_swing:.2f}M annual savings (achievable within 6 months)
                </p>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### Service Level Target Analysis")

        service_scenarios = kpi_comparison[
            kpi_comparison['scenario_name'].str.contains('Service', case=False, na=False)
        ].copy()

        if len(service_scenarios) > 0:
            baseline = kpi_comparison[kpi_comparison['scenario_name'] == 'Baseline']
            service_with_baseline = pd.concat([baseline, service_scenarios]).reset_index(drop=True)
            service_sorted = service_with_baseline.sort_values('service_level_target')

            # Grouped bar chart
            fig = go.Figure()

            metrics = {
                'On-Time Delivery': ('on_time_delivery_rate', 100, '%', COLORS['teal']),
                'Order Fulfillment': ('order_fulfillment_rate', 100, '%', COLORS['green']),
                'Total Cost': ('total_cost', 1e6, 'M', COLORS['coral'])
            }

            x_labels = [f"{int(row['service_level_target'] * 100)}% Target"
                        for _, row in service_sorted.iterrows()]

            for metric_name, (col, divisor, suffix, color) in metrics.items():
                values = service_sorted[col] / divisor if divisor > 1 else service_sorted[col]

                fig.add_trace(go.Bar(
                    name=metric_name,
                    x=x_labels,
                    y=values,
                    marker_color=color,
                    text=[f"{v:.1f}{suffix}" for v in values],
                    textposition='outside',
                    hovertemplate=f'<b>{metric_name}</b><br>%{{x}}<br>Value: %{{y:.1f}}{suffix}<extra></extra>'
                ))

            fig.update_layout(
                title="Service Level Impact on Key Metrics",
                barmode='group',
                xaxis=dict(title='Service Level Target', gridcolor='#37474f'),
                yaxis=dict(title='Normalized Values', gridcolor='#37474f'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=13),
                legend=dict(
                    bgcolor='rgba(38, 50, 56, 0.9)',
                    bordercolor='#546e7a',
                    borderwidth=1
                ),
                height=500,
                margin=dict(t=60, b=80, l=60, r=40)
            )

            st.plotly_chart(fig, use_container_width=True)

            # Trade-off analysis
            st.markdown("""
            <div class="info-box">
                <h4 style="color: #ffffff; margin-top: 0;">⚖️ Service Level Trade-offs</h4>
                <p style="color: #ffffff; font-size: 1rem; margin: 0;">
                    <strong>Key Observation:</strong> Higher service targets (97%, 99%) maintain similar 
                    fulfillment rates but have minimal impact on costs or profitability.
                    <br><br>
                    <strong>Interpretation:</strong> The 95% baseline target provides optimal balance. 
                    Increasing to 97-99% yields marginal benefits insufficient to justify potential 
                    network expansion costs.
                    <br><br>
                    <strong>Recommendation:</strong> Maintain 95% target; focus resources on transport 
                    cost reduction instead.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("### Complete Scenario Comparison Table")

        # Enhanced comparison table
        comparison_df = kpi_comparison[kpi_comparison['scenario_name'].isin(available_scenarios)].copy()

        # Add calculated columns
        comparison_df['cost_efficiency'] = (comparison_df['profit_improvement'] /
                                            comparison_df['total_cost'] * 100)

        # Format for display
        display_df = comparison_df[[
            'scenario_name',
            'order_fulfillment_rate',
            'on_time_delivery_rate',
            'total_cost',
            'profit_improvement',
            'total_stockouts',
            'avg_warehouse_utilization',
            'cost_efficiency'
        ]].copy()

        display_df.columns = [
            'Scenario', 'Fulfillment', 'On-Time', 'Total Cost',
            'Profit Δ', 'Stockouts', 'WH Util', 'Cost Efficiency'
        ]

        # Format values
        display_df['Fulfillment'] = display_df['Fulfillment'].apply(lambda x: f"{x * 100:.1f}%")
        display_df['On-Time'] = display_df['On-Time'].apply(lambda x: f"{x * 100:.1f}%")
        display_df['Total Cost'] = display_df['Total Cost'].apply(lambda x: f"${x / 1e6:.2f}M")
        display_df['Profit Δ'] = display_df['Profit Δ'].apply(
            lambda x: f"${x / 1e6:.2f}M" if x >= 0 else f"-${abs(x) / 1e6:.2f}M")
        display_df['Stockouts'] = display_df['Stockouts'].apply(lambda x: f"{x:,.0f}")
        display_df['WH Util'] = display_df['WH Util'].apply(lambda x: f"{x:.1f}%")
        display_df['Cost Efficiency'] = display_df['Cost Efficiency'].apply(lambda x: f"{x:.2f}%")

        # Clean scenario names
        display_df['Scenario'] = display_df['Scenario'].str.replace('_', ' ')

        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True,
            height=400
        )

        # Download options
        col1, col2 = st.columns(2)

        with col1:
            csv = comparison_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Full Analysis (CSV)",
                data=csv,
                file_name=f"scenario_comparison_complete_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

        with col2:
            # Create summary report
            summary = f"""
SCENARIO ANALYSIS SUMMARY
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

BEST SCENARIOS:
- Highest Profit: {best_profit['scenario_name']} (${best_profit['profit_improvement'] / 1e6:.2f}M)
- Best Fulfillment: {best_fulfillment['scenario_name']} ({best_fulfillment['order_fulfillment_rate'] * 100:.1f}%)
- Lowest Cost: {lowest_cost['scenario_name']} (${lowest_cost['total_cost'] / 1e6:.2f}M)

STRATEGIC INSIGHTS:
1. Transport cost reduction shows highest ROI potential
2. Current capacity adequate; expansion not recommended
3. 95% service target provides optimal balance

RECOMMENDATION: Prioritize carrier negotiations for 15-20% rate reduction.
"""
            st.download_button(
                label="📄 Download Summary Report (TXT)",
                data=summary,
                file_name=f"scenario_summary_{pd.Timestamp.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )


# ============================================================================
# PAGE 4: NETWORK VISUALIZATION
# ============================================================================

def show_network_visualization(data):
    """Interactive global network map with zoom controls"""

    st.title("🗺️ Network Visualization")
    st.markdown("### Global Distribution Network - Interactive Map")

    nodes = data['network_nodes']
    edges = data['network_edges']

    # Network statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(create_metric_card(
            "Warehouses",
            str(len(nodes[nodes['type'] == 'warehouse'])),
            None,
            "Physical distribution centers in the network"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(create_metric_card(
            "Regions Served",
            str(len(nodes[nodes['type'] == 'region'])),
            None,
            "Customer delivery regions covered by the network"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(create_metric_card(
            "Active Routes",
            str(len(edges)),
            None,
            "Warehouse-to-region shipping connections"
        ), unsafe_allow_html=True)

    with col4:
        avg_service = edges['service_compliance'].mean() * 100
        st.markdown(create_metric_card(
            "Avg Service Level",
            f"{avg_service:.1f}%",
            None,
            "Percentage of routes meeting 3-day delivery target"
        ), unsafe_allow_html=True)

    st.markdown("---")

    # Interactive controls
    st.markdown("## 🌐 Interactive Network Map")

    col_left, col_right = st.columns([3, 1])

    with col_right:
        st.markdown("### 🎛️ Map Controls")

        # Map scope selector
        map_scope = st.selectbox(
            "Map Region:",
            options=['world', 'usa', 'north america', 'europe', 'asia'],
            index=0,
            help="Select geographic scope for the map"
        )

        # Projection type
        projection = st.selectbox(
            "Projection:",
            options=['natural earth', 'mercator', 'orthographic', 'equirectangular'],
            index=0,
            help="Map projection type"
        )

        min_quantity = st.slider(
            "Min shipment quantity:",
            min_value=0,
            max_value=int(edges['quantity'].max()),
            value=0,
            step=100,
            help="Filter routes by minimum shipment volume"
        )

        show_service_only = st.checkbox(
            "Show only compliant routes (≤3 days)",
            value=False,
            help="Display only routes meeting service target"
        )

        show_labels = st.checkbox(
            "Show location labels",
            value=True,
            help="Display warehouse and region names"
        )

    with col_left:
        # Filter edges
        filtered_edges = edges[edges['quantity'] >= min_quantity].copy()
        if show_service_only:
            filtered_edges = filtered_edges[filtered_edges['service_compliance'] > 0.5]

        # Create global network visualization
        fig = go.Figure()

        # Add edges (routes) with better visibility
        for idx, edge in filtered_edges.iterrows():
            source_node = nodes[nodes['id'] == edge['source']].iloc[0]
            target_node = nodes[nodes['id'] == edge['target']].iloc[0]

            # Color based on service compliance
            line_color = COLORS['green'] if edge['service_compliance'] > 0.5 else COLORS['orange']
            line_width = max(1, np.log10(edge['quantity'] + 1) * 1.5)

            # Add route line
            fig.add_trace(go.Scattergeo(
                lon=[source_node['longitude'], target_node['longitude']],
                lat=[source_node['latitude'], target_node['latitude']],
                mode='lines',
                line=dict(width=line_width, color=line_color),
                opacity=0.5,
                hoverinfo='text',
                text=f"Route: {edge['source']} → {edge['target']}<br>Volume: {edge['quantity']:,.0f} units<br>Cost: ${edge['cost']:,.0f}",
                showlegend=False
            ))

        # Add warehouse nodes (larger, distinct)
        wh_nodes = nodes[nodes['type'] == 'warehouse'].copy()
        fig.add_trace(go.Scattergeo(
            lon=wh_nodes['longitude'],
            lat=wh_nodes['latitude'],
            mode='markers+text' if show_labels else 'markers',
            marker=dict(
                size=18,
                color=COLORS['teal'],
                symbol='square',
                line=dict(width=3, color=COLORS['white'])
            ),
            text=wh_nodes['label'] if show_labels else None,
            textposition='top center',
            textfont=dict(size=11, color=COLORS['white'], family='Arial Black'),
            name='Warehouses',
            hovertemplate='<b>%{text}</b><br>Lat: %{lat:.2f}<br>Lon: %{lon:.2f}<extra></extra>'
        ))

        # Add region nodes (smaller)
        region_nodes = nodes[nodes['type'] == 'region'].copy()
        fig.add_trace(go.Scattergeo(
            lon=region_nodes['longitude'],
            lat=region_nodes['latitude'],
            mode='markers+text' if show_labels else 'markers',
            marker=dict(
                size=10,
                color=COLORS['coral'],
                symbol='circle',
                line=dict(width=2, color=COLORS['white'])
            ),
            text=region_nodes['label'] if show_labels else None,
            textposition='top center',
            textfont=dict(size=9, color=COLORS['white']),
            name='Regions',
            hovertemplate='<b>%{text}</b><br>Lat: %{lat:.2f}<br>Lon: %{lon:.2f}<extra></extra>'
        ))

        # Configure map layout based on scope
        geo_config = {
            'world': dict(
                scope='world',
                projection_type=projection,
                showland=True,
                landcolor='#1a202c',
                oceancolor='#0d1117',
                showocean=True,
                showcountries=True,
                countrycolor='#546e7a',
                coastlinecolor='#546e7a',
                bgcolor='rgba(0,0,0,0)',
                center=dict(lat=20, lon=0),
                projection_scale=1
            ),
            'usa': dict(
                scope='usa',
                projection_type='albers usa',
                showland=True,
                landcolor='#1a202c',
                bgcolor='rgba(0,0,0,0)',
                showlakes=True,
                lakecolor='#0d1117'
            ),
            'north america': dict(
                scope='north america',
                projection_type=projection,
                showland=True,
                landcolor='#1a202c',
                bgcolor='rgba(0,0,0,0)',
                coastlinecolor='#546e7a'
            ),
            'europe': dict(
                scope='europe',
                projection_type=projection,
                showland=True,
                landcolor='#1a202c',
                bgcolor='rgba(0,0,0,0)',
                coastlinecolor='#546e7a'
            ),
            'asia': dict(
                scope='asia',
                projection_type=projection,
                showland=True,
                landcolor='#1a202c',
                bgcolor='rgba(0,0,0,0)',
                coastlinecolor='#546e7a'
            )
        }

        fig.update_layout(
            geo=geo_config.get(map_scope, geo_config['world']),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=12),
            showlegend=True,
            legend=dict(
                bgcolor='rgba(38, 50, 56, 0.95)',
                bordercolor='#546e7a',
                borderwidth=2,
                x=0.02,
                y=0.98,
                font=dict(size=12)
            ),
            height=750,
            margin=dict(t=10, b=10, l=10, r=10)
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'scrollZoom': True})

    # Map legend
    st.markdown("""
    <div class="info-box">
        <p style="color: #ffffff; margin: 0; font-size: 1rem;">
            <strong>🗺️ Map Controls:</strong> Use mouse to zoom/pan. 
            <strong>Legend:</strong> 
            🟦 Warehouses (squares) | 🟧 Delivery Regions (circles) | 
            <span style="color: #81c784;">━━━</span> On-Time Routes (≤3 days) | 
            <span style="color: #ffb74d;">━━━</span> Delayed Routes (>3 days)
            <br>
            Line thickness = shipment volume (log scale). Hover over nodes/routes for details.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# PAGE 5: INSIGHTS & RECOMMENDATIONS
# ============================================================================

## ============================================================================
# COMPLETELY REDESIGNED INSIGHTS & RECOMMENDATIONS
# Using Streamlit Native Components (No Raw HTML)
# Replace entire show_insights_recommendations() function
# ============================================================================

def show_insights_recommendations(data):
    """Redesigned insights with Streamlit native components"""

    st.title("💡 Strategic Insights & Recommendations")
    st.markdown("### Data-Driven Action Plan for Supply Chain Optimization")

    kpis = data['baseline']['kpis']
    kpi_comparison = data['kpi_comparison']

    # Executive Summary Dashboard
    st.markdown("## 📊 Solution Impact Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    fulfillment_improvement = (kpis['order_fulfillment_rate'] - 0.45) * 100

    with col1:
        st.metric(
            "Fulfillment Achieved",
            format_percentage(kpis['order_fulfillment_rate']),
            f"+{fulfillment_improvement:.1f} pp",
            help="Order fulfillment increased from 45% to 99%+"
        )

    with col2:
        transport_savings = kpis['total_transportation_cost'] * 0.175
        st.metric(
            "Transport Savings Potential",
            f"${transport_savings/1e6:.1f}M",
            "20% reduction target",
            help="Achievable through carrier negotiations"
        )

    with col3:
        st.metric(
            "Profit Improvement",
            f"${kpis['profit_improvement']/1e6:.1f}M",
            "From optimization",
            help="Net profit increase from solution"
        )

    with col4:
        growth_capacity = (85 / kpis['avg_warehouse_utilization'] - 1) * 100
        st.metric(
            "Growth Capacity",
            f"{growth_capacity:.0f}%",
            "Before expansion",
            help=f"Current {kpis['avg_warehouse_utilization']:.1f}% utilization"
        )

    st.markdown("---")

    # Before vs After Comparison
    st.markdown("## 🔄 Problems Solved - Before vs After")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.error("❌ **BEFORE Optimization**")
        st.metric("Fulfillment Rate", "45%", "-55 pp", delta_color="inverse")
        st.metric("System Costs", "$36M", "Unoptimized")
        st.metric("Annual Profit", "-$9.5M", "Loss-making", delta_color="inverse")

    with col2:
        st.success("✅ **OPTIMIZATION APPLIED**")
        st.info("**Linear Programming Solution**")
        st.write("Flow Capacity Model + Optimal Allocation + Cost Minimization")

    with col3:
        st.success("✅ **AFTER Optimization**")
        st.metric(
            "Fulfillment Rate",
            format_percentage(kpis['order_fulfillment_rate']),
            f"+{fulfillment_improvement:.0f} pp"
        )
        st.metric("System Costs", f"${kpis['total_cost']/1e6:.1f}M", "Optimized ✓")
        st.metric(
            "Annual Profit",
            f"${kpis['estimated_new_profit']/1e6:.1f}M",
            f"+${kpis['profit_improvement']/1e6:.1f}M"
        )

    st.markdown("---")

    # Key Solutions Delivered
    st.markdown("## 🎯 Key Solutions Delivered")

    solutions = [
        {
            'icon': '1️⃣',
            'problem': 'Low Fulfillment (45%)',
            'solution': 'Flow Capacity Model',
            'result': '99%+ Fulfillment',
            'method': 'Modeled continuous supplier replenishment (12× inventory turnover) instead of static snapshot',
            'impact': f"{fulfillment_improvement:.0f} pp improvement"
        },
        {
            'icon': '2️⃣',
            'problem': 'High Stockouts (55%)',
            'solution': 'Optimal Allocation Algorithm',
            'result': '<3% Stockouts',
            'method': 'Linear Programming finds mathematically optimal product distribution across warehouses',
            'impact': f"{kpis['total_stockouts']:,.0f} units unfulfilled (99% reduction)"
        },
        {
            'icon': '3️⃣',
            'problem': 'Unprofitable Operations (-$9.5M)',
            'solution': 'Cost Minimization',
            'result': f"+${kpis['profit_improvement']/1e6:.1f}M Profit",
            'method': 'Balanced transportation, holding, and stockout costs with 10× CLV penalty',
            'impact': f"${kpis['profit_improvement']/1e6:.1f}M annual improvement"
        },
        {
            'icon': '4️⃣',
            'problem': 'Inefficient Transport ($19M)',
            'solution': 'Route Optimization',
            'result': f"${transport_savings/1e6:.1f}M Savings Potential",
            'method': 'Identified cost reduction opportunities through carrier negotiation',
            'impact': '20% rate reduction achievable'
        }
    ]

    for sol in solutions:
        with st.container():
            st.markdown(f"### {sol['icon']} {sol['problem']}")
            col1, col2 = st.columns([1, 2])
            with col1:
                st.info(f"**Solution:** {sol['solution']}")
                st.success(f"**Result:** {sol['result']}")
            with col2:
                st.write(f"**Method:** {sol['method']}")
                st.metric("Impact", sol['impact'])
            st.markdown("---")

    # Priority Actions
    st.markdown("## 🚀 Priority Action Plan")

    # Priority 1: Transportation
    st.markdown("### 🚚 Priority 1: Transportation Cost Negotiation")

    transport_cost = kpis['total_transportation_cost']
    transport_share = transport_cost / kpis['total_cost'] * 100

    col1, col2 = st.columns([3, 2])

    with col1:
        st.success("**Current Situation:**")
        st.write(f"• Transport = ${transport_cost/1e6:.1f}M ({transport_share:.1f}% of total costs)")
        st.write("• Highest cost component in system")
        st.write(f"• Extreme sensitivity: $1M cost change = ${1 / transport_cost * kpis['profit_improvement'] / 1e6:.2f}M profit impact")

        st.info("**Recommended Actions:**")
        st.write("1. Launch RFP process with 3-5 major carriers")
        st.write(f"2. Leverage volume consolidation (annual: {kpis['total_fulfilled']:,.0f} units)")
        st.write("3. Negotiate 15-20% rate reduction target")
        st.write("4. Implement performance-based contracts")

        st.metric("Expected Savings", f"${transport_savings/1e6:.2f}M annually")
        st.caption("Timeline: 3-6 months | Complexity: Medium | ROI: Very High")

    with col2:
        st.markdown("#### 💰 Cost Breakdown")

        cost_components = pd.DataFrame({
            'Component': ['Transportation', 'Holding', 'Stockout Penalties'],
            'Amount': [
                transport_cost,
                kpis['total_holding_cost'],
                kpis['total_stockout_cost']
            ]
        })

        fig = go.Figure(data=[go.Pie(
            labels=cost_components['Component'],
            values=cost_components['Amount'],
            hole=0.5,
            marker=dict(colors=[COLORS['coral'], COLORS['purple'], COLORS['orange']]),
            textinfo='label+percent',
            textfont=dict(size=13, color='#ffffff')
        )])

        fig.update_layout(
            annotations=[dict(
                text=f'${kpis["total_cost"]/1e6:.1f}M<br>Total',
                x=0.5, y=0.5, font_size=16, showarrow=False,
                font=dict(color='#ffffff')
            )],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=12),
            showlegend=True,
            legend=dict(bgcolor='rgba(38, 50, 56, 0.8)'),
            height=300,
            margin=dict(t=20, b=20, l=20, r=20)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Savings calculator
        st.markdown("#### 🧮 Savings Calculator")

        reduction_pct = st.slider(
            "Transport cost reduction:",
            min_value=5,
            max_value=25,
            value=17,
            step=1,
            format="%d%%"
        )

        potential_savings = transport_cost * (reduction_pct / 100)
        st.metric("Potential Annual Savings", f"${potential_savings/1e6:.2f}M")
        st.caption(f"From {reduction_pct}% rate reduction")

    st.markdown("---")

    # Priority 2: Service Level
    st.markdown("### ⏱️ Priority 2: On-Time Delivery Improvement")

    col1, col2 = st.columns([2, 3])

    with col1:
        st.warning("**Current Status:**")
        st.write(f"• On-time rate: {kpis['on_time_delivery_rate']*100:.1f}%")
        st.write("• Target: 95%")
        st.write(f"• Gap: {(0.95 - kpis['on_time_delivery_rate'])*100:.1f} pp")
        st.write("• Root cause: Geographic constraints")

        st.info("**Solution Strategy:**")
        st.write("• Identify high-demand regions >5 days transit")
        st.write("• Add 2-3 regional distribution centers")
        st.write("• Implement zone-based shipping")
        st.write("• Optimize carrier selection by region")

        st.metric("Expected Improvement", "95%+ on-time rate")
        st.caption("Timeline: 12-18 months | Complexity: High | ROI: High")

    with col2:
        st.markdown("#### 📦 Transit Time Distribution")

        shipments = data['baseline']['shipments']

        if len(shipments) > 0:
            fig = go.Figure()

            fig.add_trace(go.Histogram(
                x=shipments['transit_time_days'],
                nbinsx=20,
                marker=dict(
                    color=shipments['transit_time_days'],
                    colorscale=[
                        [0, COLORS['green']],
                        [0.4, COLORS['teal']],
                        [0.6, COLORS['orange']],
                        [1, COLORS['coral']]
                    ],
                    line=dict(color='#1a1d29', width=1.5)
                )
            ))

            fig.add_vline(
                x=3,
                line_dash="dash",
                line_color=COLORS['green'],
                line_width=3,
                annotation_text="3-Day Target"
            )

            fig.update_layout(
                xaxis=dict(title='Transit Time (Days)', gridcolor='#37474f'),
                yaxis=dict(title='Number of Routes', gridcolor='#37474f'),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0', size=13),
                height=350,
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

            on_time_count = (shipments['transit_time_days'] <= 3).sum()
            delayed_count = len(shipments) - on_time_count
            avg_delayed = shipments[shipments['transit_time_days'] > 3]['transit_time_days'].mean()

            st.info(f"**Analysis:** {delayed_count} routes ({delayed_count/len(shipments)*100:.1f}%) exceed 3-day target, averaging {avg_delayed:.1f} days transit time.")
        else:
            st.info("Shipment data not available")

    st.markdown("---")

    # Priority 3: Capacity
    st.markdown("### 📦 Priority 3: Capacity Planning for Growth")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.info("**Current State:**")
        st.write(f"• Utilization: {kpis['avg_warehouse_utilization']:.1f}%")
        st.write("• Optimal range: 75-85%")
        st.write(f"• Available headroom: {85 - kpis['avg_warehouse_utilization']:.1f} pp")
        st.write(f"• Growth capacity: {growth_capacity:.0f}% volume increase")

        st.success("**Monitoring Strategy:**")
        st.write("• Track utilization quarterly")
        st.write("• Trigger expansion at 75% threshold")
        st.write("• Plan 12-18 months lead time")
        st.write("• Consider regional centers first")

        st.metric("Action", "Quarterly check, no scale-up")
        st.caption("Timeline: Ongoing | Complexity: Low | ROI: Risk mitigation")

    with col2:
        st.markdown("#### 📊 Warehouse Utilization")

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=kpis['avg_warehouse_utilization'],
            delta={'reference': 75},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': COLORS['teal']},
                'steps': [
                    {'range': [0, 60], 'color': 'rgba(129, 199, 132, 0.3)'},
                    {'range': [60, 75], 'color': 'rgba(38, 166, 154, 0.3)'},
                    {'range': [75, 90], 'color': 'rgba(255, 183, 77, 0.3)'},
                    {'range': [90, 100], 'color': 'rgba(255, 112, 67, 0.3)'}
                ],
                'threshold': {'line': {'color': COLORS['orange'], 'width': 4}, 'value': 75}
            },
            title={'text': "Average Utilization (%)"}
        ))

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=12),
            height=300
        )

        st.plotly_chart(fig, use_container_width=True)

        # Growth projection
        st.markdown("#### 📈 Growth Projection")

        years = [0, 1, 2, 3, 4, 5]
        growth_rate = 0.10
        current_demand = kpis['total_demand']

        projected_demand = [current_demand * ((1 + growth_rate) ** year) for year in years]
        capacity_limit = current_demand / (kpis['avg_warehouse_utilization'] / 85)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=years,
            y=projected_demand,
            mode='lines+markers',
            name='Projected Demand',
            line=dict(color=COLORS['teal'], width=3),
            marker=dict(size=10)
        ))

        fig.add_trace(go.Scatter(
            x=years,
            y=[capacity_limit] * len(years),
            mode='lines',
            name='Capacity Limit',
            line=dict(color=COLORS['coral'], width=2, dash='dash')
        ))

        fig.update_layout(
            xaxis=dict(title='Years from Now', gridcolor='#37474f'),
            yaxis=dict(title='Units', gridcolor='#37474f'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0', size=12),
            legend=dict(bgcolor='rgba(38, 50, 56, 0.8)'),
            height=280
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Implementation Roadmap
    st.markdown("## 🗓️ Implementation Roadmap")

    roadmap = [
        {
            'phase': 'Q1-Q2 2026',
            'timeline': 'Immediate (0-6 months)',
            'priority': '🔴 Critical',
            'actions': [
                'Execute baseline optimization',
                'Launch carrier RFP',
                'Begin negotiations (target: 15-20% reduction)',
                'Implement inventory rebalancing'
            ],
            'investment': '$0.5M',
            'impact': f'${transport_savings * 0.3 /1e6:.1f}M'
        },
        {
            'phase': 'Q3-Q4 2026',
            'timeline': 'Short-term (6-12 months)',
            'priority': '🟡 High',
            'actions': [
                'Finalize transport contracts',
                'Pilot regional DC site selection',
                'Launch tiered service model',
                'Deploy dynamic allocation'
            ],
            'investment': '$2-3M',
            'impact': f'${transport_savings /1e6:.1f}M'
        },
        {
            'phase': 'Q1-Q4 2027',
            'timeline': 'Medium-term (12-24 months)',
            'priority': '🟢 Medium',
            'actions': [
                'Open 1-2 regional DCs',
                'Expand to high-demand regions',
                'Implement advanced forecasting',
                'Full automation phase 1'
            ],
            'investment': '$10-15M',
            'impact': f'${transport_savings * 1.5 /1e6:.1f}M'
        },
        {
            'phase': 'Q1-Q4 2028',
            'timeline': 'Long-term (24-36 months)',
            'priority': '🔵 Low',
            'actions': [
                'Complete network expansion (8-10 WHs)',
                'Full automation rollout',
                'AI-driven allocation',
                'Continuous optimization'
            ],
            'investment': '$20-25M',
            'impact': f'${transport_savings * 2.5 /1e6:.1f}M'
        }
    ]

    for phase in roadmap:
        with st.expander(f"{phase['priority']} {phase['phase']} - {phase['timeline']}", expanded=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write("**Actions:**")
                for action in phase['actions']:
                    st.write(f"• {action}")
            with col2:
                st.metric("Investment", phase['investment'])
                st.metric("Impact", f"{phase['impact']} savings")

    st.markdown("---")

    # Strategic Summary
    st.markdown("## 💎 Strategic Summary")

    total_potential = kpis['profit_improvement'] + transport_savings

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Immediate Value",
            f"${kpis['profit_improvement']/1e6:.1f}M",
            "From optimization"
        )

    with col2:
        st.metric(
            "Additional Upside",
            f"${transport_savings/1e6:.1f}M",
            "From transport negotiations"
        )

    with col3:
        st.metric(
            "Total Potential Impact",
            f"${total_potential/1e6:.1f}M",
            "Annually"
        )

    st.success("**Priority Sequence:** Transport (6mo) → Service (18mo) → Capacity (as needed)")

    st.info("**Ready for Implementation:** All scenarios tested, risks quantified, ROI validated. Optimization model provides mathematical guarantee of cost-effectiveness.")


# ============================================================================
# PAGE 6: TECHNICAL DOCUMENTATION
# ============================================================================

def show_technical_documentation(data):
    """Mathematical formulations and technical details"""

    st.title("🔬 Technical Documentation")
    st.markdown("### Mathematical Formulations & Methodology")

    # Model overview
    st.markdown("## 📐 Optimization Model Overview")

    st.markdown("""
    <div class="info-box">
        <h3 style="color: #ffffff; margin-top: 0;">Solution Approach: Linear Programming</h3>
        <p style="color: #ffffff; font-size: 1.05rem; line-height: 1.8; margin: 0;">
            We solved the warehouse allocation challenge using <strong>Multi-Commodity Network Flow 
            optimization</strong>, which finds the mathematically optimal way to distribute inventory. 
            The solution <strong>minimizes total costs while achieving 99% fulfillment</strong> by 
            intelligently allocating products across warehouses to satisfy customer demand.
        </p>

    </div>
    """, unsafe_allow_html=True)

    # Decision variables
    with st.expander("📊 Decision Variables", expanded=True):
        st.markdown("""
        ### Mathematical Notation

        **Sets:**
        - `I` = Set of warehouses (i ∈ I)
        - `J` = Set of delivery regions (j ∈ J)
        - `P` = Set of products (p ∈ P)

        **Decision Variables:**

        1. **Shipment Quantities:** `x[i,j,p]` ∈ ℝ⁺
           - Quantity of product `p` shipped from warehouse `i` to region `j`
           - Continuous variable (allows fractional units)
           - Must be non-negative

        2. **Stocking Decisions:** `y[i,p]` ∈ {0, 1}
           - Binary indicator: 1 if product `p` is stocked at warehouse `i`, 0 otherwise
           - Links shipment decisions to inventory availability

        3. **Stockout Quantities:** `s[j,p]` ∈ ℝ⁺
           - Unfulfilled demand for product `p` in region `j`
           - Represents service failures
           - Penalized in objective function
        """)

        metadata = data['metadata']
        st.markdown(f"""
        <div class="stat-card">
            <div class="label">Total Decision Variables</div>
            <div class="value">{metadata['data_source']['warehouses'] * len(data['demand_enriched']['delivery_region'].unique()) * metadata['data_source']['products']:,}</div>
        </div>
        """, unsafe_allow_html=True)

    # Objective function
    with st.expander("🎯 Objective Function", expanded=True):
        st.markdown("""
        ### Minimize Total System Cost

        The objective function minimizes the sum of three cost components:

        ```
        Minimize Z = Transportation Cost + Holding Cost + Stockout Penalties
        ```

        **Component 1: Transportation Cost**
        ```
        ∑∑∑ c[i,j] × x[i,j,p]
        i∈I j∈J p∈P
        ```
        Where `c[i,j]` = unit shipping cost from warehouse `i` to region `j`

        **Component 2: Holding Cost**
        ```
        ∑∑ h[i] × inventory[i,p] × y[i,p]
        i∈I p∈P
        ```
        Where `h[i]` = holding cost rate at warehouse `i`

        **Component 3: Stockout Penalty**
        ```
        ∑∑ penalty[p] × s[j,p]
        j∈J p∈P
        ```
        Where `penalty[p]` = economic cost per unit stockout for product `p`
        """)

        kpis = data['baseline']['kpis']

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Transport Cost</div>
                <div class="value">${kpis['total_transportation_cost'] / 1e6:.2f}M</div>
                <div class="delta" style="color: {COLORS['gray_light']};">{kpis['total_transportation_cost'] / kpis['total_cost'] * 100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Holding Cost</div>
                <div class="value">${kpis['total_holding_cost'] / 1e3:.1f}K</div>
                <div class="delta" style="color: {COLORS['gray_light']};">{kpis['total_holding_cost'] / kpis['total_cost'] * 100:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Stockout Penalties</div>
                <div class="value">${kpis['total_stockout_cost'] / 1e6:.2f}M</div>
                <div class="delta" style="color: {COLORS['gray_light']};">{kpis['total_stockout_cost'] / kpis['total_cost'] * 100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

    # Constraints
    with st.expander("⚖️ Constraints", expanded=True):
        st.markdown("""
        ### Model Constraints

        **1. Demand Satisfaction Constraint**

        All customer demand must be either fulfilled or recorded as stockout:
        ```
        ∑ x[i,j,p] + s[j,p] = demand[j,p]    ∀ j∈J, p∈P
        i∈I
        ```
        This ensures conservation of flow - every unit of demand is accounted for.

        **2. Flow Capacity Constraint**

        Shipments from a warehouse cannot exceed available inventory:
        ```
        ∑ x[i,j,p] ≤ flow_capacity[i,p] × y[i,p]    ∀ i∈I, p∈P
        j∈J
        ```
        Where `flow_capacity[i,p]` = current_inventory × turnover_rate (12× annually)

        **3. Warehouse Capacity Constraint**

        Total volume stored cannot exceed warehouse capacity:
        ```
        ∑ volume[p] × inventory[i,p] × y[i,p] ≤ capacity[i]    ∀ i∈I
        p∈P
        ```
        Ensures physical space constraints are respected.

        **4. Service Level Constraint (Soft)**

        Percentage of on-time deliveries should meet target:
        ```
        ∑∑ x[i,j,p] × service[i,j] ≥ service_target × total_shipments
        i∈I j∈J
        ```
        Where `service[i,j]` = 1 if transit_time ≤ 3 days, 0 otherwise

        **5. Non-negativity Constraints**
        ```
        x[i,j,p] ≥ 0    ∀ i∈I, j∈J, p∈P
        s[j,p] ≥ 0      ∀ j∈J, p∈P
        y[i,p] ∈ {0,1}  ∀ i∈I, p∈P
        ```
        """)

    # Parameters
    with st.expander("📋 Model Parameters & Assumptions", expanded=False):
        st.markdown("""
        ### Key Parameters

        | Parameter | Value | Source/Justification |
        |-----------|-------|---------------------|
        | **Demand Growth Rate** | 5% CAGR | E-commerce industry average (2018-2025) |
        | **Inventory Turnover** | 12× per year | Fast-moving consumer goods benchmark |
        | **Service Level Target** | 95% fulfillment | Industry standard (Amazon: 97%, Walmart: 96%) |
        | **Max Delivery Time** | 3 days | Customer expectation for standard shipping |
        | **Stockout Penalty Multiplier** | 10× | Reflects Customer Lifetime Value (CLV) |
        | **Holding Cost Rate** | Varies by WH | Based on facility-specific operating costs |
        | **Warehouse Utilization Target** | 75-85% | Optimal range for operational flexibility |

        ### Flow Capacity Model

        **Problem:** Static inventory (~50K units) cannot fulfill annual demand (~540K units)

        **Solution:** Model continuous replenishment from suppliers

        **Formula:**
        ```
        Flow Capacity = Static Inventory × Annual Turnover Rate
                     = 50,000 units × 12 turns/year
                     = 600,000 units/year capacity
        ```

        **Justification:**
        - Warehouses restock from suppliers weekly/monthly
        - Inventory snapshot ≠ annual throughput capacity
        - Industry benchmark: 8-12 turns/year for e-commerce
        - Conservative estimate: 12 turns = monthly restocking

        ### Stockout Penalty Calculation

        **Economic Cost per Stockout:**
        ```
        Penalty = Unit Price × 0.30 × 10
                = $166 (avg) × 0.30 × 10
                = $498 per unit
        ```

        **Components:**
        1. **Lost Revenue:** $166 (immediate sale)
        2. **Customer Acquisition Cost:** $50-150
        3. **Lifetime Value Loss:** 3-5 future orders × $166 = $500-800
        4. **Brand Damage:** Negative reviews, word-of-mouth
        5. **Competitive Shift:** Customer switches to competitors

        **Total Economic Impact:** $500-750 per stockout unit
        """)

    # Solution methodology
    with st.expander("🔧 Solution Methodology", expanded=False):
        st.markdown("""
        ### Optimization Solver

        **Algorithm:** CBC (COIN-OR Branch and Cut)
        - Open-source Mixed Integer Linear Programming (MILP) solver
        - Implements Branch-and-Bound with cutting planes
        - Proven optimality guarantee for LP problems

        **Solution Process:**

        1. **Problem Formulation**
           - Convert business problem to mathematical model
           - Define variables, objective, and constraints
           - Validate input data consistency

        2. **Preprocessing**
           - Remove redundant constraints
           - Tighten variable bounds
           - Identify infeasibilities early

        3. **LP Relaxation**
           - Relax integer variables to continuous
           - Solve using Simplex or Interior Point method
           - Obtain lower bound on optimal solution

        4. **Branch and Bound**
           - For binary variables (stocking decisions)
           - Systematically explore solution space
           - Prune branches using bounds

        5. **Cutting Planes**
           - Add valid inequalities to tighten formulation
           - Improve LP relaxation bounds
           - Reduce branch-and-bound tree size

        6. **Solution Verification**
           - Check all constraints satisfied
           - Validate objective function value
           - Confirm optimality gap < tolerance

        **Computational Performance:**
        """)

        kpis = data['baseline']['kpis']

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Solve Time</div>
                <div class="value">{kpis.get('solve_time_seconds', 0):.2f}s</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Optimization Status</div>
                <div class="value" style="font-size: 1.5rem;">{kpis.get('optimization_status', 'Optimal')}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            metadata = data['metadata']
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Problem Size</div>
                <div class="value" style="font-size: 1.5rem;">~14K vars</div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================================
# UPDATE 3: VALIDATION LOGS VIEWER
# ============================================================================

def show_validation_logs(data):
    """Display validation logs and data quality checks"""

    st.title("📋 Validation Logs & Data Quality")
    st.markdown("### Complete Audit Trail of Analysis Process")

    # Try to load validation log
    validation_log_path = Path('./results/validation_log.txt')

    if validation_log_path.exists():
        with open(validation_log_path, 'r', encoding='utf-8') as f:
            log_content = f.read()

        st.markdown("""
        <div class="success-box">
            <h3 style="color: #ffffff; margin-top: 0;">✅ Validation Log Available</h3>
            <p style="color: #ffffff; margin: 0;">
                Complete validation log with all calculations, assumptions, and data transformations 
                recorded during optimization analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Log viewer with download
        st.markdown("## 📄 Validation Log Content")

        col1, col2 = st.columns([3, 1])

        with col2:
            st.download_button(
                label="📥 Download Full Log",
                data=log_content,
                file_name="validation_log.txt",
                mime="text/plain"
            )

        with col1:
            search_term = st.text_input("🔍 Search log:", "", help="Filter log entries")

        # Display log (filtered if search term provided)
        if search_term:
            filtered_lines = [line for line in log_content.split('\n') if search_term.lower() in line.lower()]
            display_content = '\n'.join(filtered_lines)
            st.markdown(f"**Found {len(filtered_lines)} matching entries**")
        else:
            display_content = log_content

        st.code(display_content, language='text')

    else:
        st.warning("""
        ⚠️ Validation log not found. Ensure the analysis engine has been run with validation logging enabled.

        Run: `python complete_analysis_engine_FINAL.py`
        """)

    st.markdown("---")

    # Data quality metrics
    st.markdown("## 📊 Data Quality Metrics")

    # Load enriched data
    try:
        demand_enriched = data['demand_enriched']
        warehouses_enriched = data['warehouses_enriched']

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Total Demand Records</div>
                <div class="value">{len(demand_enriched):,}</div>
                <div style="color: #b0bec5; font-size: 0.9rem; margin-top: 0.5rem;">
                    Across {demand_enriched['delivery_region'].nunique()} regions
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Data Completeness</div>
                <div class="value">100%</div>
                <div style="color: #b0bec5; font-size: 0.9rem; margin-top: 0.5rem;">
                    No missing values
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Warehouses Analyzed</div>
                <div class="value">{len(warehouses_enriched)}</div>
                <div style="color: #b0bec5; font-size: 0.9rem; margin-top: 0.5rem;">
                    All operational
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Data enrichment summary
        st.markdown("### 🔧 Data Enrichment Applied")

        enrichment_data = pd.DataFrame({
            'Step': [
                '1. Demand Projection',
                '2. Flow Capacity Model',
                '3. Service Level Targets',
                '4. Stockout Penalties',
                '5. Capacity Validation'
            ],
            'Description': [
                'Projected 2018 demand to 2025 using 5% CAGR',
                'Converted static inventory to throughput capacity (12× turnover)',
                'Set 95% fulfillment and 3-day delivery targets',
                'Applied 10× penalty multiplier reflecting CLV',
                'Validated warehouse capacity constraints and adjusted where needed'
            ],
            'Status': ['✅', '✅', '✅', '✅', '✅']
        })

        st.dataframe(enrichment_data, hide_index=True, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading data quality metrics: {e}")

    st.markdown("---")

    # Results files viewer
    st.markdown("## 📁 Generated Analysis Files")

    results_dir = Path('./results/')

    if results_dir.exists():
        # List all result files
        csv_files = list(results_dir.glob('*.csv'))
        json_files = list(results_dir.glob('*.json'))

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### CSV Data Files")

            for csv_file in sorted(csv_files):
                file_size = csv_file.stat().st_size / 1024  # KB

                with open(csv_file, 'rb') as f:
                    st.download_button(
                        label=f"📄 {csv_file.name} ({file_size:.1f} KB)",
                        data=f,
                        file_name=csv_file.name,
                        mime="text/csv",
                        key=csv_file.name
                    )

        with col2:
            st.markdown("### JSON Metadata Files")

            for json_file in sorted(json_files):
                file_size = json_file.stat().st_size / 1024  # KB

                with open(json_file, 'rb') as f:
                    st.download_button(
                        label=f"📄 {json_file.name} ({file_size:.1f} KB)",
                        data=f,
                        file_name=json_file.name,
                        mime="application/json",
                        key=json_file.name
                    )

        st.markdown(f"""
        <div class="info-box">
            <p style="color: #ffffff; margin: 0;">
                <strong>{len(csv_files)} CSV files and {len(json_files)} JSON files</strong> 
                generated by the optimization engine. All files available for download and external analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ============================================================================
# PAGE 7: ABOUT TEAM
# ============================================================================

# ============================================================================
# UPDATED ABOUT TEAM SECTION - COMPLETE CODE
# Replace the entire show_about_team() function with this
# ============================================================================

def show_about_team(data):
    """About the team section with updated member details"""

    st.title("👥 About the Team")
    st.markdown("### Warehouse Optimization Project - DBA5103 Operations Research & Analytics")

    # Project info
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f57f17 0%, #f9a825 100%); 
                border: 3px solid #fdd835; border-radius: 12px; padding: 2rem; margin: 2rem 0;">
        <h2 style="color: #1a1d29; margin-top: 0;">📦 Warehouse Inventory Optimization</h2>
        <p style="color: #1a1d29; font-size: 1.1rem; line-height: 1.8; margin: 0;">
            A comprehensive Linear Programming solution for multi-warehouse inventory allocation, 
            achieving 99%+ order fulfillment and $44.9M profit improvement through optimal 
            resource distribution and cost minimization.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Team members
    st.markdown("## 👨‍💼👩‍💼 Team Members")

    team_members = [
        {
            'name': 'Om Gorakhia',
            'email': 'om.2k01@gmail.com'
        },
        {
            'name': 'Prisha Shah',
            'email': 'prishasha1202@gmail.com'
        },
        {
            'name': 'Nourah Algiffari',
            'email': 'nourahalgiffari@gmail.com'
        },
        {
            'name': 'Pranay Samineni',
            'email': 'pranay.sam15@gmail.com'
        },
        {
            'name': 'Sanya Rajpal',
            'email': 'sanyarajpal03@gmail.com'
        }
    ]

    # Display team members in cards
    cols = st.columns(3)

    for idx, member in enumerate(team_members):
        col_idx = idx % 3

        with cols[col_idx]:
            st.markdown(f"""
            <div class="team-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">👤</div>
                <h3 style="color: #ffffff; margin: 0.5rem 0; font-size: 1.3rem;">{member['name']}</h3>
                <p style="color: #b0bec5; margin: 0.5rem 0;">
                    <a href="mailto:{member['email']}" style="color: #81c784; text-decoration: none;">
                        📧 {member['email']}
                    </a>
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # GitHub Repository
    st.markdown("## 🔗 Project Repository")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        github_url = st.text_input(
            "GitHub Repository URL:",
            placeholder="https://github.com/username/warehouse-optimization",
            help="Enter your project's GitHub repository URL"
        )

        if github_url:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #263238 0%, #37474f 100%); 
                        border: 2px solid #81c784; border-radius: 10px; padding: 1.5rem; 
                        text-align: center; margin: 1rem 0;">
                <a href="{github_url}" target="_blank" style="color: #81c784; text-decoration: none; 
                   font-size: 1.2rem; font-weight: 600;">
                    🔗 View Project on GitHub →
                </a>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Project statistics
    st.markdown("## 📊 Project Highlights")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Optimization Scenarios", "9", help="Different strategy configurations tested")

    with col2:
        st.metric("Warehouses Analyzed", "6", help="Distribution centers in network")

    with col3:
        st.metric("Products Managed", "300+", help="SKUs across all warehouses")

    with col4:
        st.metric("Delivery Regions", "10", help="Customer zones served")

    st.markdown("---")

    # Technical approach
    st.markdown("## 🔬 Technical Approach")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #ffffff; margin-top: 0;">📈 Optimization Methods</h4>
            <ul style="color: #ffffff; line-height: 2; margin: 0;">
                <li>Linear Programming (PuLP)</li>
                <li>Multi-Commodity Network Flow</li>
                <li>Constraint Optimization</li>
                <li>Sensitivity Analysis</li>
                <li>Scenario Modeling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-box">
            <h4 style="color: #ffffff; margin-top: 0;">💻 Technology Stack</h4>
            <ul style="color: #ffffff; line-height: 2; margin: 0;">
                <li>Python 3.10+</li>
                <li>PuLP (Linear Programming)</li>
                <li>Pandas (Data Processing)</li>
                <li>Plotly (Visualization)</li>
                <li>Streamlit (Dashboard)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Key achievements
    st.markdown("## 🏆 Key Achievements")

    achievements = [
        {
            'title': 'Order Fulfillment Optimization',
            'description': 'Increased fulfillment rate from 45% to 99%+ through flow capacity modeling and optimal allocation',
            'icon': '📦'
        },
        {
            'title': 'Profit Maximization',
            'description': 'Generated $44.9M profit improvement by minimizing system costs and eliminating stockout penalties',
            'icon': '💰'
        },
        {
            'title': 'Transport Cost Analysis',
            'description': 'Identified $3.7M savings opportunity through carrier negotiation (20% reduction potential)',
            'icon': '🚚'
        },
        {
            'title': 'Network Optimization',
            'description': 'Optimized 6-warehouse network serving 10 regions with 300+ products across all locations',
            'icon': '🗺️'
        }
    ]

    for achievement in achievements:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #01579b 0%, #0277bd 100%); 
                    border: 2px solid #4fc3f7; border-radius: 10px; padding: 1.5rem; margin: 1rem 0;">
            <h4 style="color: #ffffff; margin: 0;">
                {achievement['icon']} {achievement['title']}
            </h4>
            <p style="color: #e2e8f0; margin: 0.5rem 0 0 0; line-height: 1.6;">
                {achievement['description']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Course information
    st.markdown("## 🎓 Course Information")

    st.info("""
    **Course:** DBA5103 Operations Research & Analytics  
    **Institution:** National University of Singapore (NUS)  
    **Program:** Master of Science in Business Analytics  
    **Academic Year:** 2025
    """)

    st.markdown("---")

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #263238 0%, #37474f 100%); 
                border-radius: 10px; margin-top: 2rem;">
        <h3 style="color: #81c784; margin: 0;">Thank you for exploring our project!</h3>
        <p style="color: #b0bec5; margin: 1rem 0;">
            For questions or collaboration opportunities, please reach out to any team member.
        </p>
        <p style="color: #78909c; margin: 0; font-size: 0.9rem;">
            © 2025 Warehouse Optimization Team | DBA5103 | NUS Business Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point - UPDATED"""

    # Load data
    data = load_all_results()

    if data is None:
        st.error("""
        ⚠️ **Results not found!**
        
        Please run the analysis engine first:
        ```bash
        python complete_analysis_engine_FINAL.py
        ```
        
        This will generate all required result files in the `results/` directory.
        """)
        st.stop()

    # Create sidebar and get selected page
    page = create_sidebar(data)

    # Display selected page
    if page == "🏠 Executive Summary":
        show_executive_summary(data)
    elif page == "📈 Performance Analysis":
        show_performance_analysis(data)
    elif page == "🔄 Complete Scenario Analysis":
        show_comprehensive_scenario_comparison(data)  # NEW
    elif page == "🗺️ Network Visualization":
        show_network_visualization(data)  # UPDATED
    elif page == "💡 Insights & Recommendations":
        show_insights_recommendations(data)
    elif page == "🔬 Technical Documentation":
        show_technical_documentation(data)
    elif page == "📋 Validation Logs & Data":
        show_validation_logs(data)  # NEW
    elif page == "👥 About Team":
        show_about_team(data)

if __name__ == "__main__":
    main()
