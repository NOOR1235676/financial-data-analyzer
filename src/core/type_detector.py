import pandas as pd
import numpy as np
import re
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass

@dataclass
class TypeDetectionResult:
    """Result of data type detection with confidence score"""
    detected_type: str
    confidence: float
    sample_values: List[Any]
    format_pattern: Optional[str] = None
    additional_info: Optional[Dict] = None

class DataTypeDetector:
    """Intelligent column classification for financial data"""
    
    def __init__(self):
        self.string_indicators = [
            'name', 'description', 'category', 'reference', 'note', 'memo',
            'account', 'company', 'address', 'type', 'status', 'comment'
        ]
        
        self.number_indicators = [
            'amount', 'balance', 'total', 'sum', 'value', 'price', 'cost',
            'revenue', 'expense', 'asset', 'liability', 'quantity', 'qty',
            'percent', 'percentage', 'ratio', 'rate'
        ]
        
        self.date_indicators = [
            'date', 'time', 'created', 'updated', 'due', 'start', 'end',
            'maturity', 'period', 'year', 'month', 'day', 'fiscal'
        ]
    
    def detect_column_type(self, column_data: pd.Series, column_name: str = "") -> TypeDetectionResult:
        """Detect the type of a column with confidence score"""
        # Remove null values for analysis
        clean_data = column_data.dropna()
        if len(clean_data) == 0:
            return TypeDetectionResult("string", 0.0, [])
        
        sample_values = clean_data.head(min(50, len(clean_data))).tolist()
        
        # Try detecting in priority order: dates, numbers, then strings
        date_result = self._detect_date_type(clean_data, column_name)
        if date_result.confidence > 0.7:
            return date_result
        
        number_result = self._detect_number_type(clean_data, column_name)
        if number_result.confidence > 0.7:
            return number_result
        
        string_result = self._detect_string_type(clean_data, column_name)
        
        # Return the type with highest confidence
        results = [date_result, number_result, string_result]
        best_result = max(results, key=lambda x: x.confidence)
        
        return best_result
    
    def _detect_date_type(self, data: pd.Series, column_name: str) -> TypeDetectionResult:
        """Detect if column contains dates"""
        confidence = 0.0
        detected_format = None
        sample_values = data.head(20).tolist()
        
        # Check column name for date indicators
        name_score = 0.0
        if column_name:
            col_lower = column_name.lower()
            if any(indicator in col_lower for indicator in self.date_indicators):
                name_score = 0.3
        
        # Check if already datetime
        if pd.api.types.is_datetime64_any_dtype(data):
            return TypeDetectionResult("date", 1.0, sample_values, "datetime", {"pandas_dtype": True})
        
        # Try parsing as dates
        date_patterns = [
            (r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', 'MM/DD/YYYY or DD/MM/YYYY'),
            (r'\d{4}[/-]\d{1,2}[/-]\d{1,2}', 'YYYY-MM-DD'),
            (r'\d{1,2}-\w{3}-\d{2,4}', 'DD-MON-YYYY'),
            (r'\w{3,9}\s+\d{1,2},?\s+\d{4}', 'Month DD, YYYY'),
            (r'Q[1-4][\s-]?\d{2,4}', 'Quarter notation'),
            (r'^\d{5}$', 'Excel serial date'),  # Excel dates are typically 5-digit numbers
        ]
        
        successful_parses = 0
        total_attempts = 0
        
        for value in sample_values:
            if pd.isna(value):
                continue
                
            total_attempts += 1
            str_val = str(value).strip()
            
            # Try pandas date parsing
            try:
                pd.to_datetime(str_val)
                successful_parses += 1
                continue
            except:
                pass
            
            # Try pattern matching
            for pattern, format_name in date_patterns:
                if re.search(pattern, str_val):
                    successful_parses += 1
                    detected_format = format_name
                    break
        
        if total_attempts > 0:
            parse_rate = successful_parses / total_attempts
            confidence = min(parse_rate + name_score, 1.0)
        
        return TypeDetectionResult(
            "date", 
            confidence, 
            sample_values, 
            detected_format,
            {"parse_rate": parse_rate if total_attempts > 0 else 0}
        )
    
    def _detect_number_type(self, data: pd.Series, column_name: str) -> TypeDetectionResult:
        """Detect if column contains numbers (including currency)"""
        confidence = 0.0
        detected_format = None
        sample_values = data.head(20).tolist()
        
        # Check column name for number indicators
        name_score = 0.0
        if column_name:
            col_lower = column_name.lower()
            if any(indicator in col_lower for indicator in self.number_indicators):
                name_score = 0.3
        
        # Check if already numeric
        if pd.api.types.is_numeric_dtype(data):
            # Additional checks for financial amounts
            non_zero = data[data != 0].dropna()
            if len(non_zero) > 0:
                # Check if values are in reasonable monetary ranges
                if non_zero.abs().min() >= 0.01 and non_zero.abs().max() <= 1e10:
                    detected_format = "numeric_financial"
                    confidence = 0.9 + name_score
                else:
                    confidence = 0.8 + name_score
            else:
                confidence = 0.7 + name_score
            
            return TypeDetectionResult(
                "number", 
                min(confidence, 1.0), 
                sample_values, 
                detected_format
            )
        
        # Try parsing string values as numbers
        successful_parses = 0
        total_attempts = 0
        format_patterns = []
        
        currency_patterns = [
            (r'^\$[\d,]+\.?\d*$', 'USD'),
            (r'^€[\d.,]+$', 'EUR'),
            (r'^£[\d,]+\.?\d*$', 'GBP'),
            (r'^₹[\d,]+\.?\d*$', 'INR'),
            (r'^[\d,]+\.\d{2}$', 'Decimal'),
            (r'^\([\d,]+\.?\d*\)$', 'Negative_Parentheses'),
            (r'^[\d,]+\.?\d*-$', 'Negative_Trailing'),
            (r'^[\d.]+[KMB]$', 'Abbreviated'),
        ]
        
        for value in sample_values:
            if pd.isna(value):
                continue
                
            total_attempts += 1
            str_val = str(value).strip()
            
            # Try direct float conversion
            try:
                float(str_val)
                successful_parses += 1
                continue
            except:
                pass
            
            # Try currency pattern matching
            for pattern, format_name in currency_patterns:
                if re.search(pattern, str_val, re.IGNORECASE):
                    successful_parses += 1
                    if format_name not in format_patterns:
                        format_patterns.append(format_name)
                    break
            else:
                # Try cleaning common currency symbols
                cleaned = re.sub(r'[,$€£¥₹\s()%]', '', str_val)
                cleaned = cleaned.replace('-', '') if cleaned.endswith('-') else cleaned
                try:
                    float(cleaned)
                    successful_parses += 1
                except ValueError:
                    pass
        
        if total_attempts > 0:
            parse_rate = successful_parses / total_attempts
            confidence = min(parse_rate + name_score, 1.0)
        
        detected_format = ', '.join(format_patterns) if format_patterns else "unknown"
        
        return TypeDetectionResult(
            "number", 
            confidence, 
            sample_values, 
            detected_format,
            {"parse_rate": parse_rate if total_attempts > 0 else 0, "formats": format_patterns}
        )
    
    def _detect_string_type(self, data: pd.Series, column_name: str) -> TypeDetectionResult:
        """Detect string column types with subcategories"""
        sample_values = data.head(20).tolist()
        
        # Calculate base confidence for string type
        confidence = 0.5  # Default string confidence
        
        # Check column name for string indicators
        if column_name:
            col_lower = column_name.lower()
            if any(indicator in col_lower for indicator in self.string_indicators):
                confidence += 0.3
        
        # Analyze string characteristics
        str_values = [str(val) for val in sample_values if pd.notna(val)]
        if not str_values:
            return TypeDetectionResult("string", 0.3, sample_values)
        
        # Determine string subcategory
        avg_length = np.mean([len(s) for s in str_values])
        unique_ratio = len(set(str_values)) / len(str_values)
        
        string_type = "string"
        additional_info = {
            "avg_length": avg_length,
            "unique_ratio": unique_ratio,
            "total_values": len(str_values)
        }
        
        if avg_length > 50:
            string_type = "long_text"
        elif unique_ratio < 0.1:
            string_type = "categorical"
            additional_info["categories"] = list(set(str_values))
        elif all(len(s.split()) > 3 for s in str_values[:5]):
            string_type = "description"
        
        return TypeDetectionResult(
            string_type, 
            min(confidence, 1.0), 
            sample_values, 
            None,
            additional_info
        )
    
    def analyze_dataframe(self, df: pd.DataFrame) -> Dict[str, TypeDetectionResult]:
        """Analyze all columns in a DataFrame"""
        results = {}
        
        for column in df.columns:
            result = self.detect_column_type(df[column], column)
            results[column] = result
        
        return results
    
    def get_detection_summary(self, results: Dict[str, TypeDetectionResult]) -> Dict[str, List[str]]:
        """Get a summary of detected types"""
        summary = {
            "string": [],
            "number": [],
            "date": [],
            "other": []
        }
        
        for column, result in results.items():
            if result.detected_type in summary:
                summary[result.detected_type].append(column)
            else:
                summary["other"].append(column)
        
        return summary
