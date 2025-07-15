from datetime import datetime
from typing import List

import numpy as np
import pandas as pd
import pyarrow as pa
from data.utils.lakefs import LakeFsDataset
from data.preprocess.bronze.dask_processes import (
    AddConversation,
    ExplodeProcess,
    ExtractNestedProcess,
    dd,
)
from loguru import logger


def agregation_function(df: pd.DataFrame) -> List[np.ndarray]:
    user_text = ("based on the content below answer the question:\n# content\n" +
                 df["context"].astype(str) +
                 "\n# question\nquestion : " +
                 df["question"].astype(str)).to_numpy()
    assistant_text = df["text"].astype(str).to_numpy()
    assistant_text = np.where((assistant_text != "") & (pd.Series(assistant_text).str.len() > 2).to_numpy(), 
                              "The answer to your question based on the provided information is: " + assistant_text, 
                              assistant_text)
    assistant_text = np.where((assistant_text == " ") | (pd.Series(assistant_text).str.len() <= 2).to_numpy(), 
                              "sorry, I don't know the answer to your question", 
                              assistant_text)
    return user_text, assistant_text

def agregation_function_empty_context(df: pd.DataFrame) -> List[np.ndarray]:
    # Add new rows with empty context but same question and answer
    empty_context_user_text = ("based on the content below answer the question:\n# content\n" +
                               "" +
                               "\n# question\nquestion : " +
                               df["question"].astype(str)).to_numpy()
    empty_context_assistant_text = np.full_like(df["question"].astype(str).to_numpy(), 
                                                "sorry, I don't know the answer to your question, please provide more information")
    
    return empty_context_user_text, empty_context_assistant_text
    
    

def silver_pipeline(df: pd.DataFrame , agregation_function) -> pd.DataFrame:
    get_text_from_answer = ExtractNestedProcess(new_expected_columns={"text": "object"}, nested_column="answers")(df)
    get_text_from_array_text = ExplodeProcess(new_expected_columns={"text": "string"})(meta=get_text_from_answer["meta"])
    get_human = AddConversation(agregation_function=agregation_function )(meta=get_text_from_array_text["meta"])
    new_df = df .map_partitions(**get_text_from_answer)\
                .map_partitions(**get_text_from_array_text)\
                .map_partitions(**get_human)\
                .map_partitions(lambda df: df[["conversation"]])
    return new_df

def silver_pipeline_execute(lakefs_dataset:LakeFsDataset,data_files,agregation_function ,split:str,

                            columns:List[str]= ["question", "context", "answers"]):
    
    _directory = lakefs_dataset.dataset.get_path()
    lakefs_client = lakefs_dataset.lakefs_client
    path = f"{lakefs_client.path}/{_directory}"
    logger.info(f"Processing split: {split} ...")
    ddf = dd.read_parquet( data_files[split], 
                            columns=columns, 
                            index=False, 
                            storage_options=None,
                            engine='pyarrow', 
                            gather_statistics=False, 
                            split_row_groups=True,
                            npartitions=10,
                            chunksize=4000,
                            )
    with lakefs_client.fs.transaction(lakefs_client.repo_manager.repo_name, lakefs_client.branch_manager.current_branch) as tx:
            new_df = silver_pipeline(ddf,agregation_function)
            schema = pa.schema([
                (
                    "conversation",
                    pa.list_(
                    pa.struct([
                        ("content", pa.string()),
                        ("role", pa.string())
                    ])
                )
            ),
            ("__null_dask_index__", pa.int64())
            ])
            new_df.to_parquet(
                path+f"/{split}",
                engine="pyarrow",
                write_metadata_file=True,
                filesystem=lakefs_client.fs,
                overwrite=True,
                schema=schema
            )
            tx.commit(f"Uploaded dataset silver from huggingface to lakefs in {datetime.now()}")
            logger.success(f"Uploaded dataset silver to lakefs") 