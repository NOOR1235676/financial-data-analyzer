# 🏦 FINANCIAL DATA PARSER - COMPLETE COMMAND REFERENCE 💰

##  **ALL WORKING COMMANDS**

### ** Phase Testing Commands**

#### **Phase 1: Basic Excel Processing**
```bash
python test_phase1.py
```
-  Tests basic Excel file reading
-  Analyzes data structure
-  Shows file information and column details

#### **Phase 2: Component Testing**
```bash
python test_commands_phase1.py
```
-  Individual component tests
-  Pandas and OpenPyXL functionality
-  Memory usage assessment

#### **Phase 3: Quick Analysis**
```bash
python quick_analysis.py
```
-  Complete automated analysis
-  Transaction parsing and reconciliation
-  Report generation

#### **Phase 4: Complete Analysis**
```bash
python full_analysis.py
```
-  Full system integration
-  Advanced parsing and categorization
-  Professional reporting

### **🖥️ CLI Commands**

#### **Individual Phase Execution**
```bash
# Phase 1 only
python cli.py --phase 1

# Phase 2 only  
python cli.py --phase 2

# Phase 3 only
python cli.py --phase 3

# Phase 4 only
python cli.py --phase 4
```

#### **Complete Analysis with Reports**
```bash
python cli.py --phase 4 --report
```
-  Runs all phases sequentially
-  Generates PDF and Excel reports
-  Creates visualizations
-  Exports processed data

#### **Custom File Paths**
```bash
python cli.py --phase 4 --bank-file "path/to/bank.xlsx" --ledger-file "path/to/ledger.xlsx"
```

### ** Interactive Dashboard**

#### **Launch Streamlit Dashboard**
```bash
streamlit run dashboard.py
```
-  Interactive web interface
-  Real-time data visualization
-  Multiple analysis views
-  Export capabilities

#### **Dashboard with Custom Port**
```bash
streamlit run dashboard.py --server.port 8503
```

### **📄 Interactive Menu**

#### **Main Menu System**
```bash
python main.py
```
-  Menu-driven interface
-  Step-by-step execution
-  User-friendly prompts

#### **Quick Commands Menu**
```bash  
python run_commands.py
```
-  Batch execution options
-  All commands in one place
-  Easy selection interface

##  **RECOMMENDED WORKFLOW**

### **For Quick Testing:**
1. `python test_phase1.py` - Verify file access
2. `python quick_analysis.py` - Complete analysis

### **For Detailed Analysis:**
1. `python cli.py --phase 4 --report` - Full CLI analysis
2. `streamlit run dashboard.py` - Interactive exploration

### **For Interactive Use:**
1. `python main.py` - Menu-driven experience
2. `python run_commands.py` - Quick command selection

##  **Generated Files**

After running complete analysis, you'll get:

### **Reports**
- `cli_financial_report.pdf` - Professional PDF report
- `cli_financial_report.xlsx` - Detailed Excel report
- `quick_reconciliation_report.xlsx` - Reconciliation details

### **Data Exports**
- `cli_processed_data.xlsx` - All processed transactions
- `quick_processed_data.xlsx` - Quick analysis data

### **Visualizations**
- `cli_charts/` - CLI-generated charts
- `quick_charts/` - Quick analysis charts

## 🛠️ **Configuration**

### **Config File**
Edit `config.yaml` to customize:
- File paths
- Processing parameters
- Output directories
- Email settings

### **Requirements**
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

##  **All Systems Working!**

 **Phase 1-4 Testing** - Complete  
 **CLI Interface** - Functional  
 **Streamlit Dashboard** - Interactive  
 **Report Generation** - PDF & Excel  
 **Data Visualization** - Charts & Graphs  
 **Configuration** - YAML-based  
 **Error Handling** - Production-ready  

---

**Happy Analyzing! **
