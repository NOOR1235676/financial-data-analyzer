import pandas as pd
import numpy as np
import sqlite3
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import pickle
import time
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class QueryFilter:
    """Filter criteria for data queries"""
    column: str
    operator: str  # '==', '>', '<', '>=', '<=', 'in', 'between'
    value: Any
    value2: Optional[Any] = None  # For 'between' operator

class StorageStrategy(ABC):
    """Abstract base class for storage strategies"""
    
    @abstractmethod
    def store_data(self, df: pd.DataFrame, metadata: Dict) -> None:
        pass
    
    @abstractmethod
    def query_data(self, filters: List[QueryFilter]) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def aggregate_data(self, group_by: List[str], measures: List[str]) -> pd.DataFrame:
        pass

class PandasMultiIndexStorage(StorageStrategy):
    """Storage using Pandas DataFrame with MultiIndex for fast queries"""
    
    def __init__(self):
        self.data = None
        self.metadata = {}
        self.indexes = {}
    
    def store_data(self, df: pd.DataFrame, metadata: Dict) -> None:
        """Store data with optimized MultiIndex"""
        self.metadata = metadata
        
        # Create MultiIndex based on most commonly queried columns
        index_columns = []
        
        # Prioritize date columns for indexing
        date_cols = [col for col, info in metadata.items() 
                    if info.get('detected_type') == 'date']
        if date_cols:
            index_columns.extend(date_cols[:2])  # Use up to 2 date columns
        
        # Add categorical columns for secondary indexing
        cat_cols = [col for col, info in metadata.items() 
                   if info.get('detected_type') == 'string' and 
                   col not in index_columns]
        if cat_cols and len(index_columns) < 2:
            index_columns.extend(cat_cols[:2-len(index_columns)])
        
        if index_columns:
            # Convert date columns to datetime if needed
            df_copy = df.copy()
            for col in index_columns:
                if col in date_cols:
                    df_copy[col] = pd.to_datetime(df_copy[col], errors='coerce')
            
            try:
                self.data = df_copy.set_index(index_columns).sort_index()
            except:
                # Fallback to regular DataFrame if MultiIndex fails
                self.data = df_copy
        else:
            self.data = df
    
    def query_data(self, filters: List[QueryFilter]) -> pd.DataFrame:
        """Query data using optimized indexing"""
        if self.data is None:
            return pd.DataFrame()
        
        result = self.data
        
        for filter_obj in filters:
            column = filter_obj.column
            operator = filter_obj.operator
            value = filter_obj.value
            
            if column not in self.data.columns and column not in self.data.index.names:
                continue
            
            try:
                if operator == '==':
                    if column in self.data.index.names:
                        result = result.xs(value, level=column)
                    else:
                        result = result[result[column] == value]
                elif operator == '>':
                    result = result[result[column] > value]
                elif operator == '<':
                    result = result[result[column] < value]
                elif operator == '>=':
                    result = result[result[column] >= value]
                elif operator == '<=':
                    result = result[result[column] <= value]
                elif operator == 'in':
                    result = result[result[column].isin(value)]
                elif operator == 'between' and filter_obj.value2 is not None:
                    result = result[
                        (result[column] >= value) & 
                        (result[column] <= filter_obj.value2)
                    ]
            except Exception as e:
                print(f"Warning: Filter failed for {column}: {e}")
                continue
        
        return result
    
    def aggregate_data(self, group_by: List[str], measures: List[str]) -> pd.DataFrame:
        """Perform aggregations on the stored data"""
        if self.data is None:
            return pd.DataFrame()
        
        try:
            # Only group by columns that exist
            valid_group_cols = [col for col in group_by 
                              if col in self.data.columns or col in self.data.index.names]
            valid_measure_cols = [col for col in measures if col in self.data.columns]
            
            if not valid_group_cols or not valid_measure_cols:
                return pd.DataFrame()
            
            # Reset index to access index columns
            df_for_grouping = self.data.reset_index()
            
            return df_for_grouping.groupby(valid_group_cols)[valid_measure_cols].agg([
                'count', 'sum', 'mean', 'min', 'max', 'std'
            ]).round(2)
        except Exception as e:
            print(f"Aggregation failed: {e}")
            return pd.DataFrame()

class SQLiteStorage(StorageStrategy):
    """Storage using SQLite in-memory database for complex queries"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.table_name = "financial_data"
        self.metadata = {}
    
    def store_data(self, df: pd.DataFrame, metadata: Dict) -> None:
        """Store data in SQLite database with proper indexes"""
        self.metadata = metadata
        
        # Store DataFrame in SQLite
        df.to_sql(self.table_name, self.connection, if_exists='replace', index=False)
        
        # Create indexes for better query performance
        cursor = self.connection.cursor()
        
        # Create indexes on date and numeric columns
        for col, info in metadata.items():
            if info.get('detected_type') in ['date', 'number']:
                try:
                    cursor.execute(f"CREATE INDEX idx_{col} ON {self.table_name} ({col})")
                except:
                    pass  # Index might already exist
        
        self.connection.commit()
    
    def query_data(self, filters: List[QueryFilter]) -> pd.DataFrame:
        """Query data using SQL"""
        where_clauses = []
        params = []
        
        for filter_obj in filters:
            column = filter_obj.column
            operator = filter_obj.operator
            value = filter_obj.value
            
            if operator == '==':
                where_clauses.append(f"{column} = ?")
                params.append(value)
            elif operator in ['>', '<', '>=', '<=']:
                where_clauses.append(f"{column} {operator} ?")
                params.append(value)
            elif operator == 'in':
                placeholders = ','.join(['?' for _ in value])
                where_clauses.append(f"{column} IN ({placeholders})")
                params.extend(value)
            elif operator == 'between' and filter_obj.value2 is not None:
                where_clauses.append(f"{column} BETWEEN ? AND ?")
                params.extend([value, filter_obj.value2])
        
        query = f"SELECT * FROM {self.table_name}"
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        try:
            return pd.read_sql_query(query, self.connection, params=params)
        except Exception as e:
            print(f"SQL query failed: {e}")
            return pd.DataFrame()
    
    def aggregate_data(self, group_by: List[str], measures: List[str]) -> pd.DataFrame:
        """Perform SQL aggregations"""
        if not group_by or not measures:
            return pd.DataFrame()
        
        group_cols = ', '.join(group_by)
        agg_expressions = []
        
        for measure in measures:
            agg_expressions.extend([
                f"COUNT({measure}) as {measure}_count",
                f"SUM({measure}) as {measure}_sum",
                f"AVG({measure}) as {measure}_avg",
                f"MIN({measure}) as {measure}_min",
                f"MAX({measure}) as {measure}_max"
            ])
        
        agg_cols = ', '.join(agg_expressions)
        
        query = f"""
        SELECT {group_cols}, {agg_cols}
        FROM {self.table_name}
        GROUP BY {group_cols}
        """
        
        try:
            return pd.read_sql_query(query, self.connection)
        except Exception as e:
            print(f"SQL aggregation failed: {e}")
            return pd.DataFrame()
    
    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close()

class DictionaryHashStorage(StorageStrategy):
    """Custom hash table storage for specific query patterns"""
    
    def __init__(self):
        self.data = pd.DataFrame()
        self.hash_indexes = {}
        self.metadata = {}
    
    def store_data(self, df: pd.DataFrame, metadata: Dict) -> None:
        """Store data with custom hash indexes"""
        self.data = df.copy()
        self.metadata = metadata
        
        # Create hash indexes for commonly queried columns
        for col in df.columns:
            if metadata.get(col, {}).get('detected_type') in ['string', 'categorical']:
                self.hash_indexes[col] = {}
                for idx, value in enumerate(df[col]):
                    if pd.notna(value):
                        if value not in self.hash_indexes[col]:
                            self.hash_indexes[col][value] = []
                        self.hash_indexes[col][value].append(idx)
    
    def query_data(self, filters: List[QueryFilter]) -> pd.DataFrame:
        """Query using hash indexes where possible"""
        if self.data.empty:
            return pd.DataFrame()
        
        # Start with all row indices
        valid_indices = set(range(len(self.data)))
        
        for filter_obj in filters:
            column = filter_obj.column
            operator = filter_obj.operator
            value = filter_obj.value
            
            if column not in self.data.columns:
                continue
            
            if operator == '==' and column in self.hash_indexes:
                # Use hash index for exact matches
                if value in self.hash_indexes[column]:
                    valid_indices &= set(self.hash_indexes[column][value])
                else:
                    valid_indices = set()  # No matches
            else:
                # Fall back to pandas filtering
                mask = self._apply_filter(self.data[column], operator, value, filter_obj.value2)
                valid_indices &= set(self.data.index[mask])
        
        return self.data.iloc[list(valid_indices)]
    
    def _apply_filter(self, series: pd.Series, operator: str, value: Any, value2: Optional[Any] = None) -> pd.Series:
        """Apply filter operation to a pandas Series"""
        if operator == '==':
            return series == value
        elif operator == '>':
            return series > value
        elif operator == '<':
            return series < value
        elif operator == '>=':
            return series >= value
        elif operator == '<=':
            return series <= value
        elif operator == 'in':
            return series.isin(value)
        elif operator == 'between' and value2 is not None:
            return (series >= value) & (series <= value2)
        else:
            return pd.Series([True] * len(series), index=series.index)
    
    def aggregate_data(self, group_by: List[str], measures: List[str]) -> pd.DataFrame:
        """Perform aggregations using pandas"""
        if self.data.empty or not group_by or not measures:
            return pd.DataFrame()
        
        valid_group_cols = [col for col in group_by if col in self.data.columns]
        valid_measure_cols = [col for col in measures if col in self.data.columns]
        
        if not valid_group_cols or not valid_measure_cols:
            return pd.DataFrame()
        
        try:
            return self.data.groupby(valid_group_cols)[valid_measure_cols].agg([
                'count', 'sum', 'mean', 'min', 'max', 'std'
            ]).round(2)
        except Exception as e:
            print(f"Hash storage aggregation failed: {e}")
            return pd.DataFrame()

class FinancialDataStore:
    """Main data storage class with multiple strategy support"""
    
    def __init__(self, strategy: str = "pandas"):
        self.strategy_name = strategy
        
        if strategy == "pandas":
            self.storage = PandasMultiIndexStorage()
        elif strategy == "sqlite":
            self.storage = SQLiteStorage()
        elif strategy == "hash":
            self.storage = DictionaryHashStorage()
        else:
            raise ValueError(f"Unknown storage strategy: {strategy}")
        
        self.datasets = {}
        self.performance_stats = {}
    
    def add_dataset(self, name: str, df: pd.DataFrame, column_metadata: Dict) -> None:
        """Add a dataset with metadata"""
        start_time = time.time()
        
        self.storage.store_data(df, column_metadata)
        self.datasets[name] = {
            'rows': len(df),
            'columns': len(df.columns),
            'metadata': column_metadata
        }
        
        storage_time = time.time() - start_time
        self.performance_stats[f"{name}_storage"] = storage_time
    
    def query_by_criteria(self, filters: List[QueryFilter]) -> pd.DataFrame:
        """Query data using specified filters"""
        start_time = time.time()
        
        result = self.storage.query_data(filters)
        
        query_time = time.time() - start_time
        self.performance_stats["last_query"] = query_time
        
        return result
    
    def aggregate_data(self, group_by: List[str], measures: List[str]) -> pd.DataFrame:
        """Perform aggregations"""
        start_time = time.time()
        
        result = self.storage.aggregate_data(group_by, measures)
        
        agg_time = time.time() - start_time
        self.performance_stats["last_aggregation"] = agg_time
        
        return result
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics"""
        return self.performance_stats.copy()
    
    def benchmark_strategies(self, df: pd.DataFrame, metadata: Dict, 
                           test_queries: List[List[QueryFilter]]) -> Dict[str, Dict[str, float]]:
        """Benchmark different storage strategies"""
        strategies = ["pandas", "sqlite", "hash"]
        results = {}
        
        for strategy in strategies:
            try:
                # Create storage instance
                if strategy == "pandas":
                    storage = PandasMultiIndexStorage()
                elif strategy == "sqlite":
                    storage = SQLiteStorage()
                else:  # hash
                    storage = DictionaryHashStorage()
                
                # Measure storage time
                start_time = time.time()
                storage.store_data(df, metadata)
                storage_time = time.time() - start_time
                
                # Measure query times
                query_times = []
                for query_filters in test_queries:
                    start_time = time.time()
                    storage.query_data(query_filters)
                    query_times.append(time.time() - start_time)
                
                results[strategy] = {
                    'storage_time': storage_time,
                    'avg_query_time': np.mean(query_times),
                    'max_query_time': np.max(query_times),
                    'min_query_time': np.min(query_times)
                }
                
            except Exception as e:
                results[strategy] = {'error': str(e)}
        
        return results
