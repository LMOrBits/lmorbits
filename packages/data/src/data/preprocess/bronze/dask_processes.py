from abc import ABC, abstractmethod
import dask.dataframe as dd
import pandas as pd
import ast

class DaskDataProcess(ABC):
    """Abstract base class for data processing tasks.""" 
    
    def __init__(self, new_expected_columns: dict):
        self.new_expected_columns = new_expected_columns  # Fix attribute name

    def infer_meta(self, df: pd.DataFrame | dd.DataFrame, default_dtype="object") -> pd.DataFrame:
        """Infer metadata (Dask dtypes) after processing."""
        inferred_dtypes = {col: df[col].dtype.name for col in df.columns}
        inferred_dtypes.update({col: default_dtype for col in self.new_expected_columns.keys() if col not in inferred_dtypes})
        return pd.DataFrame({col: pd.Series(dtype=dtype) for col, dtype in inferred_dtypes.items()})

    def __call__(self, df: pd.DataFrame | dd.DataFrame) -> dict:
        """Returns the function reference and inferred metadata."""
        return {
            "func": self.process, 
            "meta": self.infer_meta(df) 
        }

    @abstractmethod
    def process(self, df: pd.DataFrame | dd.DataFrame) -> pd.DataFrame:
        """Apply the transformation and return the modified DataFrame."""
        pass

class ExplodeProcess(DaskDataProcess):
    """Handles exploding list-like columns."""
   
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        column = list(self.new_expected_columns.keys())[0]
        df[column] = df[column].apply(lambda x: list(eval(x)) if isinstance(x, str) else x)
        return df.explode(column)

class ExtractNestedProcess(DaskDataProcess):
    """Handles extracting key-value pairs from a nested dictionary column."""
    def __init__(self, new_expected_columns:dict , nested_column:str):
        super().__init__(new_expected_columns)
        self.nested_column = nested_column

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        # Convert string representations of dictionaries to actual dictionaries
        df[self.nested_column] = df[self.nested_column].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        # Ensure all values are dictionaries
        if not df[self.nested_column].apply(lambda x: isinstance(x, dict)).all():
            raise TypeError(f"Column '{self.nested_column}' must contain dictionaries.")

        # Extract keys
        for key in self.new_expected_columns.keys():
            df[key] = df[self.nested_column].apply(lambda x: x.get(key, None))

        return df
    
class IncludeOnlyCleaner(DaskDataProcess):
    """Keeps only specified columns and drops the rest."""
    def process(self, df: pd.DataFrame | dd.DataFrame) -> pd.DataFrame:
        """Drops columns that are NOT in `columns_to_keep`."""
        return df[list(self.new_expected_columns.keys())] 

    def infer_meta(self,df: pd.DataFrame | dd.DataFrame , **kwargs) -> pd.DataFrame:
        return pd.DataFrame({col: pd.Series(dtype=dtype) for col, dtype in self.new_expected_columns.items()})   