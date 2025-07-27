import pandas as pd
from .type_detector import DataTypeDetector, TypeDetectionResult
from .format_parser import FormatParser
from typing import Dict, List, Any, Optional

class ExcelProcessor:
    """Enhanced Excel processing with intelligent type detection and format parsing"""
    
    def __init__(self):
        self.files = {}
        self.type_detector = DataTypeDetector()
        self.format_parser = FormatParser()
        self.sheet_metadata = {}

    def load_files(self, file_paths: List[str]) -> Dict[str, bool]:
        """Load multiple Excel files and return success status"""
        results = {}
        
        for path in file_paths:
            try:
                self.files[path] = pd.ExcelFile(path, engine='openpyxl')
                results[path] = True
                print(f"✅ Successfully loaded: {path}")
            except Exception as e:
                print(f"❌ Error loading {path}: {e}")
                results[path] = False
        
        return results

    def get_sheet_info(self) -> Dict[str, Any]:
        """Get comprehensive information about all sheets including data types"""
        info = {}
        
        for file_path, xls in self.files.items():
            info[file_path] = {
                'sheet_names': xls.sheet_names,
                'sheet_info': {}
            }
            
            for sheet in xls.sheet_names:
                try:
                    df = xls.parse(sheet)
                    
                    # Analyze column types
                    type_results = self.type_detector.analyze_dataframe(df)
                    type_summary = self.type_detector.get_detection_summary(type_results)
                    
                    info[file_path]['sheet_info'][sheet] = {
                        'rows': df.shape[0],
                        'columns': df.shape[1],
                        'column_names': df.columns.tolist(),
                        'column_types': {col: result.detected_type for col, result in type_results.items()},
                        'type_summary': type_summary,
                        'type_confidence': {col: result.confidence for col, result in type_results.items()}
                    }
                    
                    # Store metadata for later use
                    self.sheet_metadata[f"{file_path}_{sheet}"] = type_results
                    
                except Exception as e:
                    info[file_path]['sheet_info'][sheet] = {'error': str(e)}
        
        return info

    def extract_data(self, file_path: str, sheet_name: str) -> pd.DataFrame:
        """Extract data from a specific sheet"""
        try:
            return self.files[file_path].parse(sheet_name)
        except Exception as e:
            print(f"Error extracting sheet {sheet_name} from {file_path}: {e}")
            return pd.DataFrame()

    def preview_data(self, file_path: str, sheet_name: str, rows: int = 5) -> pd.DataFrame:
        """Preview data from a specific sheet"""
        df = self.extract_data(file_path, sheet_name)
        return df.head(rows)
    
    def get_column_analysis(self, file_path: str, sheet_name: str, column_name: str) -> Optional[TypeDetectionResult]:
        """Get detailed analysis for a specific column"""
        metadata_key = f"{file_path}_{sheet_name}"
        if metadata_key in self.sheet_metadata:
            return self.sheet_metadata[metadata_key].get(column_name)
        return None
    
    def parse_and_clean_data(self, file_path: str, sheet_name: str) -> pd.DataFrame:
        """Parse and clean data using format parsers"""
        df = self.extract_data(file_path, sheet_name)
        if df.empty:
            return df
        
        metadata_key = f"{file_path}_{sheet_name}"
        if metadata_key not in self.sheet_metadata:
            # Analyze types if not already done
            type_results = self.type_detector.analyze_dataframe(df)
            self.sheet_metadata[metadata_key] = type_results
        
        type_results = self.sheet_metadata[metadata_key]
        cleaned_df = df.copy()
        
        # Apply format parsing based on detected types
        for column, type_result in type_results.items():
            if column not in cleaned_df.columns:
                continue
                
            if type_result.detected_type == 'number':
                # Parse amounts using format parser
                cleaned_df[column] = cleaned_df[column].apply(
                    lambda x: self._safe_parse_amount(x) if pd.notna(x) else x
                )
            elif type_result.detected_type == 'date':
                # Parse dates using pandas with error handling
                cleaned_df[column] = pd.to_datetime(cleaned_df[column], errors='coerce')
        
        return cleaned_df
    
    def _safe_parse_amount(self, value) -> float:
        """Safely parse amount values"""
        try:
            if isinstance(value, (int, float)):
                return float(value)
            
            # Try format parser for string amounts
            parsed = self.format_parser.parse_amount(str(value))
            return parsed if parsed is not None else 0.0
        except:
            return 0.0
    
    def export_analysis_report(self, output_path: str) -> None:
        """Export a comprehensive analysis report"""
        report_data = []
        
        for file_path, xls in self.files.items():
            for sheet_name in xls.sheet_names:
                metadata_key = f"{file_path}_{sheet_name}"
                if metadata_key in self.sheet_metadata:
                    type_results = self.sheet_metadata[metadata_key]
                    
                    for column, result in type_results.items():
                        report_data.append({
                            'File': file_path,
                            'Sheet': sheet_name,
                            'Column': column,
                            'Detected_Type': result.detected_type,
                            'Confidence': result.confidence,
                            'Format_Pattern': result.format_pattern,
                            'Sample_Values': str(result.sample_values[:3]) if result.sample_values else ''
                        })
        
        if report_data:
            report_df = pd.DataFrame(report_data)
            report_df.to_excel(output_path, index=False)
            print(f"📊 Analysis report exported to: {output_path}")
        else:
            print("⚠️ No analysis data available to export")
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """Get a summary of all processed files and sheets"""
        summary = {
            'total_files': len(self.files),
            'total_sheets': 0,
            'files_processed': [],
            'type_distribution': {'string': 0, 'number': 0, 'date': 0, 'other': 0}
        }
        
        for file_path, xls in self.files.items():
            file_info = {
                'path': file_path,
                'sheets': len(xls.sheet_names),
                'sheet_names': xls.sheet_names
            }
            summary['files_processed'].append(file_info)
            summary['total_sheets'] += len(xls.sheet_names)
        
        # Count type distribution across all columns
        for metadata in self.sheet_metadata.values():
            for result in metadata.values():
                detected_type = result.detected_type
                if detected_type in summary['type_distribution']:
                    summary['type_distribution'][detected_type] += 1
                else:
                    summary['type_distribution']['other'] += 1
        
        return summary

