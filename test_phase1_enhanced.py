#!/usr/bin/env python3
"""
Phase 1 Enhanced Test - Demonstrates the improved Excel processing capabilities
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from core.excel_processor import ExcelProcessor
from rich.console import Console
from rich.table import Table

def test_phase1_enhanced():
    """Test Phase 1 with enhanced capabilities"""
    console = Console()
    
    console.print("[bold blue]🧪 PHASE 1 ENHANCED TEST[/bold blue]")
    console.print("=" * 50)
    
    # Initialize processor
    processor = ExcelProcessor()
    
    # Define test files
    file_paths = [
        "data/sample/KH_Bank.xlsx",
        "data/sample/Customer_Ledger_Entries_FULL.xlsx"
    ]
    
    # Test 1: Load files
    console.print("\n[yellow]📂 Testing File Loading...[/yellow]")
    load_results = processor.load_files(file_paths)
    
    for file_path, success in load_results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        console.print(f"  {status}: {file_path}")
    
    # Test 2: Get comprehensive sheet information with type detection
    console.print("\n[yellow]🔍 Testing Enhanced Sheet Analysis...[/yellow]")
    sheet_info = processor.get_sheet_info()
    
    for file_path, info in sheet_info.items():
        console.print(f"\n[cyan]📁 File: {Path(file_path).name}[/cyan]")
        
        for sheet_name, sheet_data in info['sheet_info'].items():
            if 'error' in sheet_data:
                console.print(f"  ❌ {sheet_name}: {sheet_data['error']}")
                continue
            
            # Create detailed analysis table
            table = Table(title=f"Sheet: {sheet_name}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="white")
            
            table.add_row("Rows", str(sheet_data['rows']))
            table.add_row("Columns", str(sheet_data['columns']))
            
            # Show column types
            if 'column_types' in sheet_data:
                type_summary = sheet_data['type_summary']
                table.add_row("String Columns", str(len(type_summary.get('string', []))))
                table.add_row("Number Columns", str(len(type_summary.get('number', []))))
                table.add_row("Date Columns", str(len(type_summary.get('date', []))))
                table.add_row("Other Columns", str(len(type_summary.get('other', []))))
            
            console.print(table)
            
            # Show column type details
            if 'column_types' in sheet_data and 'type_confidence' in sheet_data:
                console.print(f"\n[green]Column Type Analysis for {sheet_name}:[/green]")
                
                for col_name in sheet_data['column_names'][:8]:  # Show first 8 columns
                    col_type = sheet_data['column_types'].get(col_name, 'unknown')
                    confidence = sheet_data['type_confidence'].get(col_name, 0.0)
                    console.print(f"  📊 {col_name}: {col_type} (confidence: {confidence:.2f})")
    
    # Test 3: Parse and clean data
    console.print("\n[yellow]🧹 Testing Data Parsing and Cleaning...[/yellow]")
    
    for file_path in file_paths:
        if file_path in processor.files:
            console.print(f"\n[cyan]Processing: {Path(file_path).name}[/cyan]")
            
            for sheet_name in processor.files[file_path].sheet_names:
                try:
                    cleaned_df = processor.parse_and_clean_data(file_path, sheet_name)
                    console.print(f"  ✅ {sheet_name}: {len(cleaned_df)} rows processed")
                    
                    # Show data types after cleaning
                    if not cleaned_df.empty:
                        console.print(f"    📈 Data types: {cleaned_df.dtypes.to_dict()}")
                        
                except Exception as e:
                    console.print(f"  ❌ {sheet_name}: Error - {e}")
    
    # Test 4: Get processing summary
    console.print("\n[yellow]📋 Testing Processing Summary...[/yellow]")
    summary = processor.get_processing_summary()
    
    summary_table = Table(title="Processing Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="white")
    
    summary_table.add_row("Total Files", str(summary['total_files']))
    summary_table.add_row("Total Sheets", str(summary['total_sheets']))
    summary_table.add_row("String Columns", str(summary['type_distribution']['string']))
    summary_table.add_row("Number Columns", str(summary['type_distribution']['number']))
    summary_table.add_row("Date Columns", str(summary['type_distribution']['date']))
    summary_table.add_row("Other Columns", str(summary['type_distribution']['other']))
    
    console.print(summary_table)
    
    # Test 5: Export analysis report
    console.print("\n[yellow]📊 Testing Analysis Report Export...[/yellow]")
    try:
        processor.export_analysis_report("phase1_analysis_report.xlsx")
    except Exception as e:
        console.print(f"❌ Export failed: {e}")
    
    console.print("\n[bold green]🎉 PHASE 1 ENHANCED TEST COMPLETED![/bold green]")
    console.print("\n[blue]Key Improvements Over Basic Requirements:[/blue]")
    console.print("✨ Intelligent column type detection with confidence scores")
    console.print("✨ Advanced format parsing for amounts and dates")
    console.print("✨ Data cleaning and normalization")
    console.print("✨ Comprehensive analysis reporting")
    console.print("✨ Rich console interface with professional formatting")

if __name__ == "__main__":
    test_phase1_enhanced()
