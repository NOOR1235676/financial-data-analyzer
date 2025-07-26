# 🏦 Financial Data Analyzer 💰

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)](https://streamlit.io)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#)

A comprehensive, production-ready Python tool for parsing, analyzing, and reconciling financial data from Excel files. Features automated transaction matching, professional reporting, interactive dashboards, and advanced analytics.

![Financial Data Analyzer Demo](https://via.placeholder.com/800x400?text=Financial+Data+Analyzer+Dashboard)

## ✨ Features

### 🎯 **Core Capabilities**
- **Smart Excel Processing**: Automatic structure detection and intelligent column recognition
- **Transaction Reconciliation**: Advanced fuzzy matching with configurable tolerances
- **Professional Reporting**: PDF and Excel reports with charts and statistics
- **Interactive Dashboard**: Streamlit-based web interface with real-time visualizations
- **CLI Interface**: Command-line tools for automation and scripting
- **Data Visualization**: Comprehensive charts and trend analysis

### 🔄 **Processing Pipeline**
1. **Phase 1**: Basic Excel file processing and structure analysis
2. **Phase 2**: Advanced transaction parsing with intelligent data cleaning
3. **Phase 3**: Automated reconciliation with similarity scoring
4. **Phase 4**: Report generation and data visualization

### 📊 **Analytics & Insights**
- Monthly transaction trends and patterns
- Category-based analysis and classification
- Match confidence scoring and validation
- Statistical summaries and KPIs
- Unmatched transaction identification

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git (for cloning)

### Installation

```bash
# Clone the repository
git clone https://github.com/NOOR1235676/financial-data-analyzer.git
cd financial-data-analyzer

# Install dependencies
pip install -r requirements.txt

# Run quick analysis
python quick_analysis.py
```

### 🎯 **Command Reference**

#### **Phase Testing**
```bash
# Test individual phases
python test_phase1.py          # Phase 1: Basic Excel Processing
python test_commands_phase1.py # Phase 2: Component Tests
python quick_analysis.py       # Phase 3: Quick Analysis
python full_analysis.py        # Phase 4: Complete Analysis
```

#### **CLI Interface**
```bash
# Run specific phases
python cli.py --phase 1                    # Basic processing only
python cli.py --phase 4 --report          # Full analysis with reports

# Custom file paths
python cli.py --phase 4 --bank-file "path/to/bank.xlsx" --ledger-file "path/to/ledger.xlsx"
```

#### **Interactive Dashboard**
```bash
# Launch web dashboard
streamlit run dashboard.py

# Custom port
streamlit run dashboard.py --server.port 8503
```

#### **Menu Systems**
```bash
python main.py           # Interactive menu
python run_commands.py   # Quick command selector
```

## 📁 Project Structure

```
financial-data-analyzer/
├── 📊 src/
│   ├── financial_analyzer.py      # Core analysis engine
│   ├── phase2_parser.py           # Advanced transaction parsing
│   ├── phase3_reconciler.py       # Data reconciliation logic
│   ├── report_generator.py        # PDF/Excel report generation
│   └── logging_setup.py           # Production logging
├── 📈 dashboard.py                # Streamlit web interface
├── 🖥️ cli.py                      # Command-line interface
├── ⚡ main.py                     # Interactive menu system
├── 🔧 config.yaml                # Configuration settings
├── 📋 requirements.txt           # Python dependencies
├── 🗂️ data/
│   └── sample/                    # Sample Excel files
├── 🧪 tests/                     # Test files
└── 📚 docs/                      # Documentation
```

## 🎨 Usage Examples

### Interactive Dashboard
![Dashboard Screenshot](https://via.placeholder.com/600x300?text=Interactive+Dashboard)

### CLI Analysis
```bash
$ python cli.py --phase 4 --report
🏦 FINANCIAL DATA PARSER CLI 💰
==================================================
🔍 Phase 1: Basic Excel Processing
✅ Found bank statement: data/sample/KH_Bank.XLSX
✅ Found customer ledger: data/sample/Customer_Ledger_Entries_FULL.xlsx
⚡ Phase 2: Advanced Transaction Parsing
✅ Parsed 5,505 transactions
🔍 Phase 3: Data Reconciliation
✅ Found 0 potential matches
🚀 Phase 4: Complete Analysis
📊 Visualizations saved to cli_charts/
📋 Data exported to cli_processed_data.xlsx
📄 PDF report generated: cli_financial_report.pdf
🎉 CLI execution completed successfully!
```

### Programmatic Usage

```python
from src.financial_analyzer import FinancialDataAnalyzer

# Initialize analyzer
analyzer = FinancialDataAnalyzer()

# Load and process data
analyzer.load_bank_statement("data/sample/KH_Bank.XLSX")
analyzer.load_customer_ledger("data/sample/Customer_Ledger_Entries_FULL.xlsx")

# Run analysis
transactions = analyzer.parse_transactions()
matches = analyzer.find_matching_transactions()

# Generate reports
analyzer.generate_reconciliation_report("report.xlsx")
analyzer.create_visualizations("charts")
```

## ⚙️ Configuration

Customize settings in `config.yaml`:

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

## 📊 Generated Reports

### Excel Reports
- **Executive Summary**: Key metrics and statistics
- **Bank Transactions**: Processed bank statement data
- **Ledger Transactions**: Customer ledger entries
- **Reconciliation Matches**: Matched transactions with confidence scores

### PDF Reports
- Professional formatting with charts and tables
- Executive summary with key findings
- Detailed transaction analysis
- Match quality assessment

### Visualizations
- Monthly transaction trends
- Category distribution charts
- Match analysis pie charts
- Amount distribution histograms

## 🧪 Testing

Run the test suite:

```bash
# Individual phase tests
python test_phase1.py
python test_commands_phase1.py

# Complete test suite
python -m pytest tests/
```

## 🔧 Advanced Features

### Production-Ready Components
- ✅ **Logging**: Comprehensive logging with file and console output
- ✅ **Error Handling**: Robust exception handling and recovery
- ✅ **Configuration**: YAML-based configuration management
- ✅ **CLI Tools**: Full command-line interface with arguments
- ✅ **Web Dashboard**: Interactive Streamlit interface
- ✅ **Report Generation**: Professional PDF and Excel reports
- ✅ **Data Visualization**: Publication-ready charts and graphs
- ✅ **Performance Optimization**: Memory-efficient processing

### Supported File Formats
- Excel files (.xlsx, .xls)
- CSV files (planned)
- Multiple sheet support
- Various date and currency formats

## 📈 Performance

| File Size | Transactions | Processing Time | Memory Usage |
|-----------|-------------|-----------------|---------------|
| Small     | < 1K        | < 5 seconds     | ~50 MB       |
| Medium    | 1K-10K      | 5-30 seconds    | ~100 MB      |
| Large     | > 10K       | 30s-2 minutes   | ~200 MB      |

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python, Pandas, and Streamlit
- Uses advanced fuzzy matching algorithms
- Inspired by modern financial technology solutions

## 📞 Support

- 📧 **Issues**: [GitHub Issues](https://github.com/NOOR1235676/financial-data-analyzer/issues)
- 📖 **Documentation**: [Wiki](https://github.com/NOOR1235676/financial-data-analyzer/wiki)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/NOOR1235676/financial-data-analyzer/discussions)

---

<div align="center">
  <h3>🎉 Ready to analyze your financial data? Get started now! 🚀</h3>
  <p><strong>Star ⭐ this repository if you find it helpful!</strong></p>
</div>
