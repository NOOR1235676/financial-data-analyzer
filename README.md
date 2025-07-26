# Financial Data Analyzer

A comprehensive Python application designed for parsing, analyzing, and reconciling financial data from Excel files. This system implements automated transaction matching algorithms, generates statistical reports, and provides data visualization capabilities for financial analysis purposes.

## Project Overview

This financial data analysis tool was developed to address the challenges of processing large volumes of financial transactions from multiple sources. The system implements a four-phase processing pipeline that handles data ingestion, parsing, reconciliation, and reporting.

## Features

### Core Capabilities
- Automated Excel file structure detection and intelligent column recognition
- Advanced transaction reconciliation using fuzzy matching algorithms
- Professional report generation in PDF and Excel formats
- Web-based dashboard interface using Streamlit framework
- Command-line interface for batch processing and automation
- Comprehensive data visualization and trend analysis

### Processing Architecture
1. **Phase 1**: Basic Excel file processing and data structure analysis
2. **Phase 2**: Advanced transaction parsing with intelligent data cleaning
3. **Phase 3**: Automated reconciliation using similarity scoring algorithms
4. **Phase 4**: Report generation and statistical visualization

### Analytics and Insights
- Monthly transaction trend analysis
- Category-based transaction classification
- Match confidence scoring and validation
- Statistical summaries and key performance indicators
- Identification of unmatched transactions for manual review

## Installation and Setup

### System Requirements
- Python 3.8 or higher
- Git version control system
- Minimum 4GB RAM (8GB recommended for large datasets)

### Installation Process

```bash
# Clone the repository
git clone https://github.com/NOOR1235676/financial-data-analyzer.git
cd financial-data-analyzer

# Install required dependencies
pip install -r requirements.txt

# Run initial analysis
python quick_analysis.py
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

## Project Structure

```
financial-data-analyzer/
├── src/
│   ├── financial_analyzer.py      # Primary analysis engine
│   ├── phase2_parser.py           # Transaction parsing module
│   ├── phase3_reconciler.py       # Data reconciliation algorithms
│   ├── report_generator.py        # Report generation utilities
│   └── logging_setup.py           # System logging configuration
├── dashboard.py                   # Streamlit web interface
├── cli.py                         # Command-line interface
├── main.py                        # Interactive menu system
├── config.yaml                    # System configuration file
├── requirements.txt               # Python package dependencies
├── data/
│   └── sample/                    # Sample dataset files
├── tests/                         # Unit test modules
└── docs/                          # Project documentation
```

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
