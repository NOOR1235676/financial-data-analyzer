#!/usr/bin/env python3
"""
🏦 Financial Data Parser & Analyzer - Interactive Dashboard 💰
Comprehensive Streamlit-based dashboard with advanced analytics and visualizations
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path
from datetime import datetime, timedelta
import warnings
import io
import base64
import time
from typing import Dict, List, Tuple, Any
warnings.filterwarnings('ignore')

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from core.excel_processor import ExcelProcessor
    from core.type_detector import DataTypeDetector
    from core.format_parser import FormatParser
    from core.data_storage import FinancialDataStore, QueryFilter
    from financial_analyzer import FinancialDataAnalyzer
except ImportError as e:
    st.error(f"❌ Import error: {e}")
    st.error("Please ensure all required modules are available in the src directory.")
    st.info("💡 Tip: Run `python create_sample_data.py` first to generate sample data.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Financial Data Analysis Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 10px;
    border-left: 5px solid #1f77b4;
}
.success-metric {
    border-left-color: #28a745;
}
.warning-metric {
    border-left-color: #ffc107;
}
.danger-metric {
    border-left-color: #dc3545;
}
</style>
""", unsafe_allow_html=True)

def load_financial_data():
    """Load and process financial data"""
    try:
        analyzer = FinancialDataAnalyzer()
        
        # Load data
        bank_file = "data/sample/KH_Bank.XLSX"
        ledger_file = "data/sample/Customer_Ledger_Entries_FULL.xlsx"
        
        bank_data = analyzer.load_bank_statement(bank_file)
        ledger_data = analyzer.load_customer_ledger(ledger_file)
        
        # Parse transactions using the original analyzer method
        transactions = analyzer.parse_transactions()
        
        # Separate bank and ledger transactions
        bank_transactions = [t for t in transactions if t.transaction_type == "Bank Statement"]
        ledger_transactions = [t for t in transactions if t.transaction_type == "Customer Ledger"]
        
        # Find matches using the original analyzer method
        reconciliation_results = analyzer.find_matching_transactions(tolerance_days=3, amount_tolerance=0.01)
        matches = reconciliation_results.get('matches', [])
        
        return {
            'bank_transactions': bank_transactions,
            'ledger_transactions': ledger_transactions,
            'matches': matches,
            'total_transactions': len(transactions)
        }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def create_summary_metrics(data):
    """Create summary metrics display"""
    if not data:
        return
    
    bank_trans = data['bank_transactions']
    ledger_trans = data['ledger_transactions']
    matches = data['matches']
    
    # Calculate metrics
    total_bank = len(bank_trans)
    total_ledger = len(ledger_trans)
    total_matches = len(matches)
    
    bank_amount = sum(t.amount for t in bank_trans)
    ledger_amount = sum(t.amount for t in ledger_trans)
    matched_amount = sum(match[0].amount for match in matches)
    
    match_rate = (total_matches / max(total_bank, 1)) * 100
    amount_recovery_rate = (matched_amount / max(bank_amount, 1)) * 100
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card success-metric">', unsafe_allow_html=True)
        st.metric("Total Transactions", f"{total_bank + total_ledger:,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card warning-metric">', unsafe_allow_html=True)
        st.metric("Matched Transactions", f"{total_matches:,}", f"{match_rate:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Amount", f"${bank_amount + ledger_amount:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card success-metric">', unsafe_allow_html=True)
        st.metric("Amount Recovery", f"${matched_amount:,.2f}", f"{amount_recovery_rate:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)

def create_match_analysis_chart(data):
    """Create matched vs unmatched transactions chart"""
    if not data:
        return
    
    bank_trans = data['bank_transactions']
    ledger_trans = data['ledger_transactions']
    matches = data['matches']
    
    # Calculate matched/unmatched
    matched_bank = len(matches)
    unmatched_bank = len(bank_trans) - matched_bank
    matched_ledger = len(matches)
    unmatched_ledger = len(ledger_trans) - matched_ledger
    
    # Create subplot
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Bank Transactions', 'Ledger Transactions'),
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )
    
    # Bank transactions pie
    fig.add_trace(
        go.Pie(
            labels=['Matched', 'Unmatched'],
            values=[matched_bank, unmatched_bank],
            name="Bank",
            marker_colors=['#28a745', '#dc3545']
        ),
        row=1, col=1
    )
    
    # Ledger transactions pie
    fig.add_trace(
        go.Pie(
            labels=['Matched', 'Unmatched'],
            values=[matched_ledger, unmatched_ledger],
            name="Ledger",
            marker_colors=['#28a745', '#dc3545']
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title_text="Transaction Matching Analysis",
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_monthly_trends_chart(data):
    """Create monthly trends chart"""
    if not data:
        return
    
    bank_trans = data['bank_transactions']
    ledger_trans = data['ledger_transactions']
    
    # Prepare data
    bank_df = pd.DataFrame([{
        'date': t.date,
        'amount': t.amount if t.debit_credit == 'CREDIT' else -t.amount,
        'type': 'Bank'
    } for t in bank_trans])
    
    ledger_df = pd.DataFrame([{
        'date': t.date,
        'amount': t.amount if t.debit_credit == 'CREDIT' else -t.amount,
        'type': 'Ledger'
    } for t in ledger_trans])
    
    if bank_df.empty and ledger_df.empty:
        st.warning("No transaction data available for trends")
        return
    
    # Combine and group by month
    all_df = pd.concat([bank_df, ledger_df], ignore_index=True)
    all_df['month'] = all_df['date'].dt.to_period('M')
    
    monthly_data = all_df.groupby(['month', 'type']).agg({
        'amount': ['sum', 'count']
    }).reset_index()
    
    monthly_data.columns = ['month', 'type', 'total_amount', 'transaction_count']
    monthly_data['month'] = monthly_data['month'].astype(str)
    
    # Create chart
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Monthly Transaction Amounts', 'Monthly Transaction Counts'),
        vertical_spacing=0.1
    )
    
    # Amount chart
    for trans_type in monthly_data['type'].unique():
        type_data = monthly_data[monthly_data['type'] == trans_type]
        fig.add_trace(
            go.Bar(
                x=type_data['month'],
                y=type_data['total_amount'],
                name=f'{trans_type} Amount',
                showlegend=True
            ),
            row=1, col=1
        )
    
    # Count chart
    for trans_type in monthly_data['type'].unique():
        type_data = monthly_data[monthly_data['type'] == trans_type]
        fig.add_trace(
            go.Bar(
                x=type_data['month'],
                y=type_data['transaction_count'],
                name=f'{trans_type} Count',
                showlegend=False
            ),
            row=2, col=1
        )
    
    fig.update_layout(
        title_text="Monthly Financial Trends",
        height=600,
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_category_analysis(data):
    """Create category analysis charts"""
    if not data:
        return
    
    bank_trans = data['bank_transactions']
    ledger_trans = data['ledger_transactions']
    
    # Combine transactions for category analysis
    all_transactions = bank_trans + ledger_trans
    
    if not all_transactions:
        st.warning("No transactions available for category analysis")
        return
    
    # Category distribution
    category_counts = {}
    category_amounts = {}
    
    for t in all_transactions:
        category = t.category if t.category else 'Other'
        category_counts[category] = category_counts.get(category, 0) + 1
        category_amounts[category] = category_amounts.get(category, 0) + t.amount
    
    # Create charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_count = px.pie(
            values=list(category_counts.values()),
            names=list(category_counts.keys()),
            title="Transaction Count by Category"
        )
        st.plotly_chart(fig_count, use_container_width=True)
    
    with col2:
        fig_amount = px.pie(
            values=list(category_amounts.values()),
            names=list(category_amounts.keys()),
            title="Transaction Amount by Category"
        )
        st.plotly_chart(fig_amount, use_container_width=True)

def create_reconciliation_details(data):
    """Create detailed reconciliation view"""
    if not data or not data['matches']:
        st.warning("No matches found for detailed analysis")
        return
    
    matches = data['matches']
    
    # Prepare match data
    match_data = []
    for bank_trans, ledger_trans, score in matches:
        match_data.append({
            'Bank Date': bank_trans.date.strftime('%Y-%m-%d'),
            'Ledger Date': ledger_trans.date.strftime('%Y-%m-%d'),
            'Bank Amount': f"${bank_trans.amount:,.2f}",
            'Ledger Amount': f"${ledger_trans.amount:,.2f}",
            'Match Score': f"{score:.1f}",
            'Bank Description': bank_trans.description[:50] + "..." if len(bank_trans.description) > 50 else bank_trans.description,
            'Ledger Description': ledger_trans.description[:50] + "..." if len(ledger_trans.description) > 50 else ledger_trans.description
        })
    
    df = pd.DataFrame(match_data)
    st.dataframe(df, use_container_width=True)

def main():
    """Main dashboard function"""
    # Header
    st.markdown('<h1 class="main-header">🏦 Financial Data Analysis Dashboard 💰</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Dashboard Controls")
    
    # Load data
    with st.spinner("Loading financial data..."):
        data = load_financial_data()
    
    if not data:
        st.error("Failed to load financial data. Please check your files.")
        return
    
    # Sidebar options
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        ["Overview", "Transaction Matching", "Monthly Trends", "Category Analysis", "Reconciliation Details"]
    )
    
    # Main content based on selection
    if analysis_type == "Overview":
        st.header("📊 Financial Overview")
        create_summary_metrics(data)
        
        st.subheader("Quick Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            create_match_analysis_chart(data)
        
        with col2:
            create_category_analysis(data)
    
    elif analysis_type == "Transaction Matching":
        st.header("🔗 Transaction Matching Analysis")
        create_summary_metrics(data)
        create_match_analysis_chart(data)
    
    elif analysis_type == "Monthly Trends":
        st.header("📈 Monthly Financial Trends")
        create_monthly_trends_chart(data)
    
    elif analysis_type == "Category Analysis":
        st.header("📊 Category Analysis")
        create_category_analysis(data)
    
    elif analysis_type == "Reconciliation Details":
        st.header("🔍 Detailed Reconciliation")
        create_reconciliation_details(data)
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("Financial Data Analysis Dashboard v2.0")
    st.sidebar.success(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()
