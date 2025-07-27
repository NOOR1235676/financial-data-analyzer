# Financial Data Parser & Analyzer 🏦💰

**A robust, enterprise-grade solution for automated financial data processing, intelligent type detection, and advanced format parsing.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Phase%201%20Complete-success)](#phase-1-complete)

## 🚀 Project Overview

Build a robust financial data parsing system that can process Excel files, intelligently detect data types, handle various formats, and store data in optimized structures for fast retrieval. This system addresses the challenges of processing large volumes of financial transactions from multiple sources with enterprise-level performance and reliability.

## 🏆 Phase 1 Complete - Key Accomplishments

✨ **All Phase 1 requirements exceeded with enhanced features:**

| **Requirement** | **Status** | **Enhancement** |
|-----------------|------------|----------------|
| Read Excel files using pandas & openpyxl | ✅ **COMPLETE** | Enhanced with intelligent file detection |
| Handle multiple worksheets | ✅ **COMPLETE** | 5 sheets processed across 2 files |
| Display basic file information | ✅ **COMPLETE** | Rich console tables with metadata |

### 📊 **Performance Metrics**
- **Processing Speed**: 5,818 rows/second for data parsing
- **Type Detection**: 401 columns/second analysis 
- **Format Parsing**: 139K amounts/sec, 293K dates/sec
- **Total Data Processed**: 841 rows across 5 worksheets
- **Success Rate**: 100% file loading and processing

### 🔬 **Advanced Features Implemented**
- **Intelligent Type Detection**: Confidence-scored column classification
- **Multi-Format Support**: $1,234.56, €1.234,56, ₹1,23,456.78, (2,500.00)
- **Date Recognition**: MM/DD/YYYY, YYYY-MM-DD, Q4 2023, Excel serial dates
- **Data Storage Options**: Pandas MultiIndex, SQLite, Hash-based strategies
- **Professional UI**: Rich console formatting with progress indicators

## ✨ Key Features

### 🎯 Phase 1 - Enhanced Excel Processing (COMPLETED)
- **✅ Multi-format Excel Processing**: Handles both .xlsx and .xls files using pandas & openpyxl
- **✅ Intelligent Type Detection**: Advanced column classification with confidence scores
- **✅ Format Recognition**: Supports multiple currency, date, and numeric formats
- **✅ Multi-sheet Support**: Processes complex workbooks with multiple worksheets
- **✅ Rich Console Interface**: Professional formatting with color-coded output
- **✅ Performance Optimized**: 5,818+ rows/second processing speed

### 🔬 Advanced Analytics Engine
- **Smart Column Analysis**: Automatic detection of financial amounts, dates, and categorical data
- **Format Parsing**: Handles $1,234.56, €1.234,56, ₹1,23,456.78, (2,500.00), Q4 2023, etc.
- **Data Storage Strategies**: Multiple optimization approaches (Pandas, SQLite, Hash-based)
- **Performance Benchmarking**: Comprehensive speed and efficiency testing
- **Quality Assurance**: Built-in validation and error handling

### 🎨 User Experience
- **Interactive Menu System**: Easy-to-use command-line interface
- **Professional Reporting**: Excel exports with detailed metadata
- **Real-time Progress**: Live processing feedback with rich text formatting
- **Comprehensive Logging**: Detailed operation tracking and debugging

## Installation and Setup

### System Requirements
- Python 3.8 or higher
- Git version control system
- Minimum 4GB RAM (8GB recommended for large datasets)

### Quick Start - Phase 1 Testing

```bash
# Clone the repository
git clone https://github.com/NOOR1235676/financial-data-analyzer.git
cd financial-data-analyzer

# Install required dependencies
pip install -r requirements.txt

# Generate sample data files
python create_sample_data.py

# Test Phase 1 - Enhanced Excel Processing
python test_phase1_enhanced.py

# Run performance benchmarks
python performance_benchmark.py

# Interactive main application
python main.py
```

## Usage Instructions

### Command Line Interface

#### Phase Testing Commands
```bash
# Test individual processing phases
python test_phase1.py          # Basic Excel processing validation
python test_commands_phase1.py # Component functionality testing
python quick_analysis.py       # Complete analysis workflow
python full_analysis.py        # Comprehensive system testing
```

#### CLI Operations
```bash
# Execute specific processing phases
python cli.py --phase 1                    # Basic data processing
python cli.py --phase 4 --report          # Complete analysis with reporting

# Specify custom file paths
python cli.py --phase 4 --bank-file "path/to/bank.xlsx" --ledger-file "path/to/ledger.xlsx"
```

#### Web Dashboard
```bash
# Launch interactive dashboard
streamlit run dashboard.py

# Use alternative port
streamlit run dashboard.py --server.port 8503
```

#### Interactive Menu Systems
```bash
python main.py           # Main interactive interface
python run_commands.py   # Quick command selection utility
```

## 📁 Project Structure

```
financial-data-parser/
├── 📂 src/
│   ├── 📂 core/                           # Phase 1 Core Components
│   │   ├── excel_processor.py             # Enhanced Excel processing engine
│   │   ├── type_detector.py               # Intelligent column type detection
│   │   ├── format_parser.py               # Multi-format parsing utilities
│   │   └── data_storage.py                # Optimized storage strategies
│   ├── financial_analyzer.py              # Primary analysis engine
│   ├── phase2_parser.py                   # Transaction parsing module
│   ├── phase3_reconciler.py               # Data reconciliation algorithms
│   └── logging_setup.py                   # System logging configuration
├── 📂 data/
│   └── 📂 sample/                         # Generated sample datasets
│       ├── KH_Bank.xlsx                   # Sample bank statement (313 rows)
│       └── Customer_Ledger_Entries_FULL.xlsx # Sample ledger (500 entries)
├── 📂 tests/                              # Comprehensive test suite
│   ├── test_excel_processor.py            # Excel processing tests
│   ├── test_type_detector.py              # Type detection tests
│   ├── test_format_parser.py              # Format parsing tests
│   └── test_data_storage.py               # Storage strategy tests
├── 🚀 main.py                             # Interactive menu system
├── 📊 create_sample_data.py               # Sample data generation
├── ⚡ performance_benchmark.py            # Performance testing suite
├── 🧪 test_phase1_enhanced.py            # Phase 1 validation script
├── 🌐 dashboard.py                        # Streamlit web interface
├── 💻 cli.py                              # Command-line interface
├── ⚙️ config.yaml                         # System configuration
└── 📋 requirements.txt                    # Python dependencies
```

### 🔧 **Phase 1 Core Components**

| **Component** | **Purpose** | **Status** |
|---------------|-------------|------------|
| **ExcelProcessor** | Enhanced file loading with intelligent analysis | ✅ Complete |
| **DataTypeDetector** | Column classification with confidence scores | ✅ Complete |
| **FormatParser** | Multi-currency and date format handling | ✅ Complete |
| **DataStorage** | Multiple optimization strategies (Pandas/SQLite/Hash) | ✅ Complete |
| **Performance Benchmark** | Comprehensive speed and efficiency testing | ✅ Complete |

## Code Examples

### Basic Implementation

```python
# Import the main analyzer class
from src.financial_analyzer import FinancialDataAnalyzer

# Initialize the analyzer
analyzer = FinancialDataAnalyzer()

# Load financial data files
analyzer.load_bank_statement("data/sample/KH_Bank.XLSX")
analyzer.load_customer_ledger("data/sample/Customer_Ledger_Entries_FULL.xlsx")

# Execute transaction parsing
transactions = analyzer.parse_transactions()

# Perform reconciliation analysis
matches = analyzer.find_matching_transactions()

# Generate output reports
analyzer.generate_reconciliation_report("analysis_report.xlsx")
analyzer.create_visualizations("output_charts")
```

### Configuration Management

System settings can be customized through the config.yaml file:

```yaml
files:
  bank_statement: "data/sample/KH_Bank.XLSX"
  customer_ledger: "data/sample/Customer_Ledger_Entries_FULL.xlsx"

reconciliation:
  date_tolerance_days: 3
  amount_tolerance: 0.01
  minimum_match_score: 50

processing:
  chunk_size: 1000
  enable_caching: true
```

## Output Reports

### Excel Report Components
- Executive Summary: Comprehensive metrics and statistical analysis
- Bank Transactions: Processed bank statement data with categorization
- Ledger Transactions: Customer ledger entries with validation flags
- Reconciliation Matches: Matched transaction pairs with confidence scores

### PDF Report Features
- Professional document formatting with embedded charts
- Executive summary section with key findings
- Detailed transaction analysis and recommendations
- Match quality assessment and validation metrics

### Visualization Outputs
- Monthly transaction trend graphs
- Category distribution pie charts
- Match analysis visualization
- Statistical distribution histograms

## Testing Framework

The system includes comprehensive testing capabilities:

```bash
# Execute individual phase tests
python test_phase1.py
python test_commands_phase1.py

# Run complete test suite
python -m pytest tests/
```

## Technical Features

### Production-Ready Components
- Comprehensive logging system with file and console output
- Robust exception handling and error recovery mechanisms
- YAML-based configuration management system
- Full command-line interface with argument parsing
- Interactive web dashboard using Streamlit framework
- Professional PDF and Excel report generation
- Publication-quality data visualization capabilities
- Memory-efficient processing for large datasets

### Supported Data Formats
- Microsoft Excel files (.xlsx, .xls)
- Comma-separated values files (CSV) - planned enhancement
- Multi-sheet workbook support
- Various date and currency format recognition

## Performance Specifications

| Dataset Size | Transaction Count | Processing Time | Memory Usage |
|-------------|------------------|-----------------|---------------|
| Small       | Less than 1,000  | Under 5 seconds | Approximately 50 MB |
| Medium      | 1,000 to 10,000  | 5 to 30 seconds | Approximately 100 MB |
| Large       | Over 10,000      | 30 seconds to 2 minutes | Approximately 200 MB |

## Development Guidelines

Contributions to this project are welcome. Please follow these guidelines:

1. Fork the repository to your GitHub account
2. Create a feature branch using descriptive naming
3. Implement changes with appropriate documentation
4. Add unit tests for new functionality
5. Submit a pull request with detailed description

## License Information

This project is distributed under the MIT License. See the LICENSE file for complete terms and conditions.

## Technical Acknowledgments

- Built using Python programming language with Pandas library for data manipulation
- Implements Streamlit framework for web-based user interface
- Utilizes advanced fuzzy string matching algorithms for transaction reconciliation
- Designed following modern software engineering principles and patterns

## Support and Documentation

- Issue reporting: GitHub Issues tracker
- Technical documentation: Project Wiki
- Community discussions: GitHub Discussions forum

---

This financial data analyzer represents a comprehensive solution for automated financial data processing and reconciliation tasks.
