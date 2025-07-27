#!/usr/bin/env python3
"""
Performance Benchmarking Script for Financial Data Parser
Tests different storage strategies and parsing approaches
"""

import sys
import time
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from core.excel_processor import ExcelProcessor
from core.type_detector import DataTypeDetector
from core.format_parser import FormatParser
from core.data_storage import FinancialDataStore, QueryFilter
from rich.console import Console
from rich.table import Table
from rich.progress import track

class PerformanceBenchmark:
    """Comprehensive performance benchmarking for the financial data parser"""
    
    def __init__(self):
        self.console = Console()
        self.results = {}
        
    def benchmark_excel_processing(self, file_paths: List[str]) -> Dict[str, float]:
        """Benchmark Excel file processing performance"""
        self.console.print("\n[blue]📊 Benchmarking Excel Processing...[/blue]")
        
        processor = ExcelProcessor()
        results = {}
        
        # Test file loading speed
        start_time = time.time()
        load_results = processor.load_files(file_paths)
        load_time = time.time() - start_time
        results['file_loading'] = load_time
        
        # Test sheet info extraction
        start_time = time.time()
        sheet_info = processor.get_sheet_info()
        info_time = time.time() - start_time
        results['sheet_info_extraction'] = info_time
        
        # Test data parsing and cleaning
        total_parse_time = 0
        total_rows = 0
        
        for file_path in file_paths:
            if file_path in processor.files:
                for sheet_name in processor.files[file_path].sheet_names:
                    start_time = time.time()
                    cleaned_df = processor.parse_and_clean_data(file_path, sheet_name)
                    parse_time = time.time() - start_time
                    total_parse_time += parse_time
                    total_rows += len(cleaned_df)
        
        results['data_parsing'] = total_parse_time
        results['rows_per_second'] = total_rows / total_parse_time if total_parse_time > 0 else 0
        results['total_rows_processed'] = total_rows
        
        return results
    
    def benchmark_type_detection(self, test_data: pd.DataFrame) -> Dict[str, float]:
        """Benchmark type detection performance"""
        self.console.print("\n[blue]🔍 Benchmarking Type Detection...[/blue]")
        
        detector = DataTypeDetector()
        results = {}
        
        # Test single column detection
        times = []
        for column in test_data.columns:
            start_time = time.time()
            result = detector.detect_column_type(test_data[column], column)
            detection_time = time.time() - start_time
            times.append(detection_time)
        
        results['avg_column_detection'] = np.mean(times)
        results['max_column_detection'] = np.max(times)
        results['min_column_detection'] = np.min(times)
        
        # Test full DataFrame analysis
        start_time = time.time()
        full_results = detector.analyze_dataframe(test_data)
        full_time = time.time() - start_time
        results['full_dataframe_analysis'] = full_time
        results['columns_per_second'] = len(test_data.columns) / full_time if full_time > 0 else 0
        
        return results
    
    def benchmark_format_parsing(self, test_amounts: List[str], test_dates: List[str]) -> Dict[str, float]:
        """Benchmark format parsing performance"""
        self.console.print("\n[blue]🔧 Benchmarking Format Parsing...[/blue]")
        
        parser = FormatParser()
        results = {}
        
        # Test amount parsing
        start_time = time.time()
        parsed_amounts = [parser.parse_amount(amount) for amount in test_amounts * 100]  # Scale up for timing
        amount_time = time.time() - start_time
        results['amount_parsing'] = amount_time
        results['amounts_per_second'] = len(parsed_amounts) / amount_time if amount_time > 0 else 0
        
        # Test date parsing
        start_time = time.time()
        parsed_dates = [parser.parse_date(date) for date in test_dates * 100]  # Scale up for timing
        date_time = time.time() - start_time
        results['date_parsing'] = date_time
        results['dates_per_second'] = len(parsed_dates) / date_time if date_time > 0 else 0
        
        return results
    
    def benchmark_storage_strategies(self, test_data: pd.DataFrame, metadata: Dict) -> Dict[str, Dict[str, float]]:
        """Benchmark different storage strategies"""
        self.console.print("\n[blue]💾 Benchmarking Storage Strategies...[/blue]")
        
        strategies = ["pandas", "sqlite", "hash"]
        results = {}
        
        # Create test queries
        test_queries = [
            [QueryFilter("Date", ">=", "2024-01-01")],
            [QueryFilter("Amount", ">", 100)],
            [QueryFilter("Description", "==", "Direct Deposit - Salary")],
            [QueryFilter("Date", "between", "2024-01-01", "2024-06-30")]
        ]
        
        for strategy in track(strategies, description=f"Testing storage strategies..."):
            try:
                store = FinancialDataStore(strategy=strategy)
                strategy_results = {}
                
                # Test storage time
                start_time = time.time()
                store.add_dataset("test", test_data, metadata)
                storage_time = time.time() - start_time
                strategy_results['storage_time'] = storage_time
                
                # Test query performance
                query_times = []
                for query_filters in test_queries:
                    start_time = time.time()
                    result = store.query_by_criteria(query_filters)
                    query_time = time.time() - start_time
                    query_times.append(query_time)
                
                strategy_results['avg_query_time'] = np.mean(query_times)
                strategy_results['max_query_time'] = np.max(query_times)
                strategy_results['min_query_time'] = np.min(query_times)
                
                # Test aggregation performance
                start_time = time.time()
                agg_result = store.aggregate_data(["Transaction_Type"], ["Amount"])
                agg_time = time.time() - start_time
                strategy_results['aggregation_time'] = agg_time
                
                # Memory efficiency (simplified)
                strategy_results['data_size'] = len(test_data) * len(test_data.columns)
                
                results[strategy] = strategy_results
                
            except Exception as e:
                self.console.print(f"[red]Error testing {strategy}: {e}[/red]")
                results[strategy] = {"error": str(e)}
        
        return results
    
    def benchmark_end_to_end(self, file_paths: List[str]) -> Dict[str, float]:
        """Benchmark complete end-to-end processing"""
        self.console.print("\n[blue]🚀 Benchmarking End-to-End Processing...[/blue]")
        
        results = {}
        
        # Complete processing pipeline
        start_time = time.time()
        
        # Step 1: Load files
        processor = ExcelProcessor()
        processor.load_files(file_paths)
        
        # Step 2: Analyze structure
        sheet_info = processor.get_sheet_info()
        
        # Step 3: Process all data
        all_data = []
        for file_path in file_paths:
            if file_path in processor.files:
                for sheet_name in processor.files[file_path].sheet_names:
                    df = processor.parse_and_clean_data(file_path, sheet_name)
                    if not df.empty:
                        all_data.append(df)
        
        # Step 4: Combine and store
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Create metadata
            detector = DataTypeDetector()
            metadata = detector.analyze_dataframe(combined_df)
            
            # Store in different strategies
            for strategy in ["pandas", "sqlite", "hash"]:
                try:
                    store = FinancialDataStore(strategy=strategy)
                    store.add_dataset("complete", combined_df, metadata)
                except:
                    pass
        
        total_time = time.time() - start_time
        results['total_processing_time'] = total_time
        results['total_rows_processed'] = len(combined_df) if all_data else 0
        results['rows_per_second'] = (len(combined_df) / total_time) if total_time > 0 and all_data else 0
        
        return results
    
    def create_performance_report(self) -> None:
        """Create a comprehensive performance report"""
        self.console.print("\n[blue]📈 Creating Performance Report...[/blue]")
        
        # Create summary table
        table = Table(title="Performance Benchmark Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        table.add_column("Unit", style="green")
        
        for category, metrics in self.results.items():
            if isinstance(metrics, dict) and "error" not in metrics:
                table.add_row(f"[bold]{category.upper()}[/bold]", "", "")
                for metric, value in metrics.items():
                    if isinstance(value, (int, float)):
                        if "time" in metric.lower():
                            table.add_row(f"  {metric}", f"{value:.4f}", "seconds")
                        elif "per_second" in metric.lower():
                            table.add_row(f"  {metric}", f"{value:.0f}", "ops/sec")
                        else:
                            table.add_row(f"  {metric}", f"{value:.2f}", "")
        
        self.console.print(table)
        
        # Export detailed results to Excel
        report_data = []
        for category, metrics in self.results.items():
            if isinstance(metrics, dict):
                for metric, value in metrics.items():
                    report_data.append({
                        'Category': category,
                        'Metric': metric,
                        'Value': value,
                        'Timestamp': datetime.now().isoformat()
                    })
        
        if report_data:
            report_df = pd.DataFrame(report_data)
            report_path = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            report_df.to_excel(report_path, index=False)
            self.console.print(f"\n[green]📊 Detailed report saved to: {report_path}[/green]")
    
    def run_full_benchmark(self, file_paths: List[str]) -> None:
        """Run complete benchmark suite"""
        self.console.print("[bold blue]🎯 STARTING COMPREHENSIVE PERFORMANCE BENCHMARK[/bold blue]")
        self.console.print("=" * 60)
        
        # Benchmark 1: Excel Processing
        self.results['excel_processing'] = self.benchmark_excel_processing(file_paths)
        
        # Load test data for other benchmarks
        processor = ExcelProcessor()
        processor.load_files(file_paths)
        
        # Get sample data
        test_data = None
        for file_path in file_paths:
            if file_path in processor.files:
                sheet_name = processor.files[file_path].sheet_names[0]
                test_data = processor.parse_and_clean_data(file_path, sheet_name)
                if not test_data.empty:
                    break
        
        if test_data is not None:
            # Benchmark 2: Type Detection
            self.results['type_detection'] = self.benchmark_type_detection(test_data)
            
            # Benchmark 3: Format Parsing
            test_amounts = ["$1,234.56", "(2,500.00)", "€1.234,56", "1.5K", "₹1,23,456.78"]
            test_dates = ["12/31/2023", "2023-12-31", "Q4 2023", "Dec-23", "March 2024"]
            self.results['format_parsing'] = self.benchmark_format_parsing(test_amounts, test_dates)
            
            # Benchmark 4: Storage Strategies
            detector = DataTypeDetector()
            metadata = detector.analyze_dataframe(test_data)
            self.results['storage_strategies'] = self.benchmark_storage_strategies(test_data, metadata)
        
        # Benchmark 5: End-to-End Processing
        self.results['end_to_end'] = self.benchmark_end_to_end(file_paths)
        
        # Create comprehensive report
        self.create_performance_report()
        
        self.console.print("\n[bold green]✅ BENCHMARK COMPLETED SUCCESSFULLY![/bold green]")

def main():
    """Main function to run performance benchmarks"""
    benchmark = PerformanceBenchmark()
    
    # Define test files
    file_paths = [
        "data/sample/KH_Bank.xlsx",
        "data/sample/Customer_Ledger_Entries_FULL.xlsx"
    ]
    
    # Check if files exist
    missing_files = [f for f in file_paths if not Path(f).exists()]
    if missing_files:
        benchmark.console.print("[red]❌ Missing required files:[/red]")
        for file in missing_files:
            benchmark.console.print(f"  - {file}")
        benchmark.console.print("\n[yellow]Please run create_sample_data.py first to generate test files.[/yellow]")
        return
    
    # Run benchmarks
    benchmark.run_full_benchmark(file_paths)

if __name__ == "__main__":
    main()
