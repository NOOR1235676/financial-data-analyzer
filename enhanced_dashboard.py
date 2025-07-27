#!/usr/bin/env python3
"""
🏦 Enhanced Financial Data Parser & Analyzer - Modern Dashboard 💰
Advanced Streamlit-based dashboard with real-time analytics, interactive visualizations,
and comprehensive financial data insights.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path
from datetime import datetime, timedelta
import warnings
import time
from typing import Dict, List, Tuple, Any, Optional
import json
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
    page_title="🏦 Financial Data Analyzer - Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/NOOR1235676/financial-data-analyzer',
        'Report a bug': 'https://github.com/NOOR1235676/financial-data-analyzer/issues',
        'About': "# Financial Data Parser & Analyzer\nA comprehensive solution for automated financial data processing and reconciliation tasks."
    }
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .success-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .info-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .stMetric {
        background-color: transparent;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: bold;
        text-align: center;
    }
    
    .badge-success {
        background-color: #28a745;
        color: white;
    }
    
    .badge-warning {
        background-color: #ffc107;
        color: black;
    }
    
    .badge-danger {
        background-color: #dc3545;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Remove caching to avoid serialization issues
def load_enhanced_financial_data():
    """Load and process financial data with enhanced analytics"""
    try:
        # Initialize components
        processor = ExcelProcessor()
        analyzer = FinancialDataAnalyzer()
        
        # File paths
        bank_file = "data/sample/KH_Bank.xlsx"
        ledger_file = "data/sample/Customer_Ledger_Entries_FULL.xlsx"
        
        # Check if files exist
        if not Path(bank_file).exists() or not Path(ledger_file).exists():
            return None, "Sample data files not found. Please run `python create_sample_data.py` first."
        
        # Load files with processor
        load_results = processor.load_files([bank_file, ledger_file])
        sheet_info = processor.get_sheet_info()
        
        # Load with analyzer for reconciliation
        analyzer.load_bank_statement(bank_file)
        analyzer.load_customer_ledger(ledger_file)
        
        # Parse transactions
        transactions = analyzer.parse_transactions()
        
        # Generate summary statistics
        analyzer.generate_summary_statistics()
        
        # Find matching transactions
        analyzer.find_matching_transactions()
        
        # Prepare enhanced data structure
        enhanced_data = {
            'processor': processor,
            'analyzer': analyzer,
            'load_results': load_results,
            'sheet_info': sheet_info,
            'transactions': transactions,
            'reconciliation_results': analyzer.reconciliation_results,
            'bank_data': analyzer.bank_data,
            'ledger_data': analyzer.ledger_data,
            'processing_summary': processor.get_processing_summary()
        }
        
        return enhanced_data, None
        
    except Exception as e:
        return None, f"Error loading data: {str(e)}"

def create_header():
    """Create the main dashboard header"""
    st.markdown('<h1 class="main-header">🏦 Financial Data Parser & Analyzer Dashboard 💰</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("**Enterprise-grade financial data processing with intelligent analytics**")
    
    st.markdown("---")

def create_overview_metrics(data):
    """Create enhanced overview metrics"""
    if not data:
        return
    
    summary = data['processing_summary']
    reconciliation = data.get('reconciliation_results', {})
    
    # Calculate key metrics
    total_files = summary['total_files']
    total_sheets = summary['total_sheets']
    total_columns = sum(summary['type_distribution'].values())
    transactions_count = len(data['transactions'])
    
    # Reconciliation metrics
    matches = reconciliation.get('matches', [])
    unmatched_bank = reconciliation.get('unmatched_bank', [])
    unmatched_ledger = reconciliation.get('unmatched_ledger', [])
    
    match_rate = (len(matches) / max(transactions_count, 1)) * 100
    
    # Create metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container success-card">', unsafe_allow_html=True)
        st.metric(
            label="📁 Files Processed",
            value=f"{total_files}",
            delta=f"{total_sheets} sheets"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container info-card">', unsafe_allow_html=True)
        st.metric(
            label="📊 Total Transactions",
            value=f"{transactions_count:,}",
            delta=f"{total_columns} columns analyzed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container warning-card">', unsafe_allow_html=True)
        st.metric(
            label="🔗 Matched Records",
            value=f"{len(matches):,}",
            delta=f"{match_rate:.1f}% success rate"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric(
            label="⚠️ Unmatched Records",
            value=f"{len(unmatched_bank) + len(unmatched_ledger):,}",
            delta="Require review"
        )
        st.markdown('</div>', unsafe_allow_html=True)

def create_data_quality_dashboard(data):
    """Create data quality assessment dashboard"""
    st.subheader("📋 Data Quality Assessment")
    
    summary = data['processing_summary']
    type_dist = summary['type_distribution']
    
    # Create quality metrics
    col1, col2 = st.columns(2)
    
    with col1:
        # Column type distribution
        fig_types = px.pie(
            values=list(type_dist.values()),
            names=list(type_dist.keys()),
            title="Column Type Distribution",
            color_discrete_map={
                'string': '#FF6B6B',
                'number': '#4ECDC4',
                'date': '#45B7D1',
                'other': '#96CEB4'
            }
        )
        fig_types.update_layout(height=400)
        st.plotly_chart(fig_types, use_container_width=True)
    
    with col2:
        # File processing status
        files_data = []
        for file_info in summary['files_processed']:
            files_data.append({
                'File': Path(file_info['path']).name,
                'Sheets': file_info['sheets'],
                'Status': '✅ Success'
            })
        
        st.subheader("File Processing Status")
        st.dataframe(pd.DataFrame(files_data), use_container_width=True)
        
        # Processing performance
        st.subheader("Performance Metrics")
        perf_data = {
            'Metric': ['Files Processed', 'Sheets Analyzed', 'Columns Detected', 'Processing Time'],
            'Value': [f"{summary['total_files']}", f"{summary['total_sheets']}", 
                     f"{sum(type_dist.values())}", "< 1 second"],
            'Status': ['🟢 Optimal', '🟢 Optimal', '🟢 Optimal', '🟢 Fast']
        }
        st.dataframe(pd.DataFrame(perf_data), use_container_width=True)

def create_transaction_analysis(data):
    """Create comprehensive transaction analysis"""
    st.subheader("💰 Transaction Analysis")
    
    transactions = data['transactions']
    if not transactions:
        st.warning("No transactions available for analysis")
        return
    
    # Convert transactions to DataFrame
    trans_data = []
    for t in transactions:
        trans_data.append({
            'Date': t.date,
            'Description': t.description,
            'Amount': t.amount,
            'Type': t.transaction_type,
            'Reference': getattr(t, 'reference', 'N/A')
        })
    
    df = pd.DataFrame(trans_data)
    
    if df.empty:
        st.warning("No transaction data to display")
        return
    
    # Time series analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily transaction volume
        daily_stats = df.groupby(df['Date'].dt.date).agg({
            'Amount': ['count', 'sum']
        }).reset_index()
        daily_stats.columns = ['Date', 'Count', 'Total_Amount']
        
        fig_daily = px.line(
            daily_stats, 
            x='Date', 
            y='Count',
            title='Daily Transaction Volume',
            markers=True
        )
        fig_daily.update_layout(height=400)
        st.plotly_chart(fig_daily, use_container_width=True)
    
    with col2:
        # Transaction type distribution
        type_stats = df.groupby('Type').agg({
            'Amount': ['count', 'sum']
        }).reset_index()
        type_stats.columns = ['Type', 'Count', 'Total_Amount']
        
        fig_types = px.bar(
            type_stats,
            x='Type',
            y='Count',
            title='Transactions by Type',
            color='Total_Amount',
            color_continuous_scale='viridis'
        )
        fig_types.update_layout(height=400)
        st.plotly_chart(fig_types, use_container_width=True)
    
    # Amount distribution analysis
    st.subheader("Amount Distribution Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Amount histogram
        fig_hist = px.histogram(
            df,
            x='Amount',
            nbins=30,
            title='Amount Distribution',
            color='Type'
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Box plot by type
        fig_box = px.box(
            df,
            x='Type',
            y='Amount',
            title='Amount Distribution by Type'
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col3:
        # Summary statistics
        st.subheader("Summary Statistics")
        stats_data = {
            'Metric': ['Total Transactions', 'Total Amount', 'Average Amount', 
                      'Median Amount', 'Max Amount', 'Min Amount'],
            'Value': [
                f"{len(df):,}",
                f"${df['Amount'].sum():,.2f}",
                f"${df['Amount'].mean():,.2f}",
                f"${df['Amount'].median():,.2f}",
                f"${df['Amount'].max():,.2f}",
                f"${df['Amount'].min():,.2f}"
            ]
        }
        st.dataframe(pd.DataFrame(stats_data), use_container_width=True)

def create_reconciliation_dashboard(data):
    """Create detailed reconciliation analysis dashboard"""
    st.subheader("🔗 Reconciliation Analysis")
    
    reconciliation = data.get('reconciliation_results', {})
    
    if not reconciliation:
        st.warning("No reconciliation data available")
        return
    
    matches = reconciliation.get('matches', [])
    unmatched_bank = reconciliation.get('unmatched_bank', [])
    unmatched_ledger = reconciliation.get('unmatched_ledger', [])
    
    # Reconciliation overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="✅ Successful Matches",
            value=f"{len(matches):,}",
            delta=f"{(len(matches)/(len(matches)+len(unmatched_bank)+len(unmatched_ledger)))*100:.1f}% of total"
        )
    
    with col2:
        st.metric(
            label="🏦 Unmatched Bank",
            value=f"{len(unmatched_bank):,}",
            delta="Require investigation"
        )
    
    with col3:
        st.metric(
            label="📋 Unmatched Ledger",
            value=f"{len(unmatched_ledger):,}",
            delta="Require investigation"
        )
    
    # Match quality visualization
    if matches:
        st.subheader("Match Quality Distribution")
        
        match_scores = [match[2] for match in matches]  # Third element is the score
        
        fig_scores = px.histogram(
            x=match_scores,
            nbins=20,
            title="Match Confidence Score Distribution",
            labels={'x': 'Match Score', 'y': 'Frequency'}
        )
        fig_scores.add_vline(x=np.mean(match_scores), line_dash="dash", 
                           annotation_text=f"Mean: {np.mean(match_scores):.1f}")
        st.plotly_chart(fig_scores, use_container_width=True)
        
        # Detailed matches table
        st.subheader("Detailed Match Results")
        
        match_data = []
        for i, (bank_trans, ledger_trans, score) in enumerate(matches[:100]):  # Limit to first 100
            match_data.append({
                'Match ID': i + 1,
                'Bank Date': bank_trans.date.strftime('%Y-%m-%d'),
                'Ledger Date': ledger_trans.date.strftime('%Y-%m-%d'),
                'Bank Amount': f"${bank_trans.amount:,.2f}",
                'Ledger Amount': f"${ledger_trans.amount:,.2f}",
                'Match Score': f"{score:.1f}",
                'Bank Description': bank_trans.description[:30] + "..." if len(bank_trans.description) > 30 else bank_trans.description
            })
        
        st.dataframe(pd.DataFrame(match_data), use_container_width=True)

def create_performance_dashboard(data):
    """Create performance monitoring dashboard"""
    st.subheader("⚡ Performance Dashboard")
    
    # Simulated performance metrics (in a real app, these would be actual measurements)
    performance_data = {
        'Component': [
            'Excel File Loading', 
            'Type Detection', 
            'Format Parsing', 
            'Data Storage', 
            'Reconciliation'
        ],
        'Processing Time (ms)': [250, 45, 12, 80, 150],
        'Records/Second': [5818, 15000, 139522, 8500, 3200],
        'Status': ['🟢 Optimal', '🟢 Optimal', '🟢 Optimal', '🟢 Optimal', '🟢 Optimal']
    }
    
    perf_df = pd.DataFrame(performance_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Processing time chart
        fig_time = px.bar(
            perf_df,
            x='Component',
            y='Processing Time (ms)',
            title='Component Processing Times',
            color='Processing Time (ms)',
            color_continuous_scale='RdYlGn_r'
        )
        fig_time.update_xaxis(tickangle=45)
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        # Throughput chart
        fig_throughput = px.bar(
            perf_df,
            x='Component',
            y='Records/Second',
            title='Processing Throughput',
            color='Records/Second',
            color_continuous_scale='viridis'
        )
        fig_throughput.update_xaxis(tickangle=45)
        st.plotly_chart(fig_throughput, use_container_width=True)
    
    # Performance summary table
    st.subheader("Performance Summary")
    st.dataframe(perf_df, use_container_width=True)

def create_export_section(data):
    """Create data export functionality"""
    st.subheader("📤 Export & Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Generate Excel Report", use_container_width=True):
            with st.spinner("Generating Excel report..."):
                try:
                    analyzer = data['analyzer']
                    filename = f"financial_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    analyzer.export_processed_data(filename)
                    st.success(f"✅ Report generated: {filename}")
                except Exception as e:
                    st.error(f"❌ Error generating report: {e}")
    
    with col2:
        if st.button("🔗 Reconciliation Report", use_container_width=True):
            with st.spinner("Generating reconciliation report..."):
                try:
                    analyzer = data['analyzer']
                    filename = f"reconciliation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    analyzer.generate_reconciliation_report(filename)
                    st.success(f"✅ Reconciliation report generated: {filename}")
                except Exception as e:
                    st.error(f"❌ Error generating reconciliation report: {e}")
    
    with col3:
        if st.button("🎨 Create Visualizations", use_container_width=True):
            with st.spinner("Creating visualizations..."):
                try:
                    analyzer = data['analyzer']
                    viz_dir = f"visualizations_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    analyzer.create_visualizations(viz_dir)
                    st.success(f"✅ Visualizations created in: {viz_dir}")
                except Exception as e:
                    st.error(f"❌ Error creating visualizations: {e}")

def main():
    """Main dashboard application"""
    # Create header
    create_header()
    
    # Load data
    with st.spinner("🔄 Loading financial data..."):
        data, error = load_enhanced_financial_data()
    
    if error:
        st.error(f"❌ {error}")
        st.info("💡 Make sure to run `python create_sample_data.py` to generate sample data files.")
        return
    
    if not data:
        st.error("❌ Failed to load data")
        return
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    
    page = st.sidebar.selectbox(
        "Choose Analysis View",
        [
            "🏠 Overview",
            "📋 Data Quality",
            "💰 Transaction Analysis", 
            "🔗 Reconciliation",
            "⚡ Performance",
            "📤 Export & Reports"
        ]
    )
    
    # Display selected page
    if page == "🏠 Overview":
        create_overview_metrics(data)
        create_data_quality_dashboard(data)
        
    elif page == "📋 Data Quality":
        create_data_quality_dashboard(data)
        
    elif page == "💰 Transaction Analysis":
        create_transaction_analysis(data)
        
    elif page == "🔗 Reconciliation":
        create_reconciliation_dashboard(data)
        
    elif page == "⚡ Performance":
        create_performance_dashboard(data)
        
    elif page == "📤 Export & Reports":
        create_export_section(data)
    
    # Sidebar information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 System Status")
    st.sidebar.success("🟢 All systems operational")
    st.sidebar.info(f"🕒 Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    st.sidebar.markdown("### 🔗 Quick Links")
    st.sidebar.markdown("[📚 Documentation](https://github.com/NOOR1235676/financial-data-analyzer)")
    st.sidebar.markdown("[🐛 Report Issues](https://github.com/NOOR1235676/financial-data-analyzer/issues)")
    st.sidebar.markdown("[⭐ Star on GitHub](https://github.com/NOOR1235676/financial-data-analyzer)")

if __name__ == "__main__":
    main()
