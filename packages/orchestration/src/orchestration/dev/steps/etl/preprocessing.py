from typing import Annotated

import dask.dataframe as dd
from data.utils.lakefs import LakeFsDataset
from zenml import step
from zenml.types import HTMLString

from orchestration.dev.steps.data.preprocessing import (
    agregation_function,
    bronze_pipeline_execute,
)
from orchestration.dev.steps.etl.data_ingestion_hf_to_lakefs import LakefsInfo
from orchestration.utils.lakefs import get_lakefs_dataset

ipy_html = lambda df,h : f"<h2>{h}</h2>" + df.to_html()

def view_data_from_lakefs(lakefs_dataset: LakeFsDataset, tilte:str) -> Annotated[HTMLString, "html"]:
    html = ""
    data_files = lakefs_dataset.load_data_files()
    for title, path in data_files.items():
      if title == tilte:
        sample_df = dd.read_parquet(path[0], columns=None, 
                              index=False, 
                              storage_options=None,
                              engine='pyarrow', 
                              gather_statistics=False, 
                              split_row_groups=True,
                              chunksize=10)
        html += ipy_html(sample_df.head(2),h=title)
    return html



@step(enable_cache=False)
def bronze_pipeline_step(lakefsinfo: LakefsInfo , split:str) -> Annotated[LakefsInfo, "lakefs_info"]:
  lakefs_dataset = get_lakefs_dataset(lakefsinfo.directory,lakefsinfo.project_name)
  data_files = lakefs_dataset.load_data_files()
  bronze_pipeline_execute(lakefs_dataset,data_files,agregation_function ,split,
                            columns=["question", "context", "answers"])
  return lakefsinfo