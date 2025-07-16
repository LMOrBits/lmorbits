from typing import Optional

from data.etl.hf_to_lakefs import stream_and_upload_from_hf_to_lakefs
from loguru import logger
from pydantic import BaseModel
from typing_extensions import Annotated
from zenml import log_metadata, step

from orchestration.utils.lakefs import get_lakefs_dataset


class Split(BaseModel):
    name: str
    chunk_size: int = 2000
    start: Optional[int] = None
    end: Optional[int] = None

class Splits(BaseModel):
    splits: list[Split]

class LakefsInfo(BaseModel):
    dataset_type: str
    ml_dataset_type: str
    namespace: str
    repo_name: str
    branch_name: str
    address: str
    split: str
    directory: str
    project_name: str
    


@step(enable_cache=False)
def etl_from_hf_to_lakefs(
    hf_dataset_name: str,
    project_name: str,
    directory: str,
    splits: Splits,
    config: str,
) -> Annotated[dict, "address_dict"]:
    address_dict = {}
    for split in splits.splits:
        address_dict[split.name] = etl_from_hf_to_lakefs_step(hf_dataset_name, project_name, directory, split, config)
    return address_dict

@step(enable_cache=False)
def etl_from_hf_to_lakefs_step(
    hf_dataset_name: str,
    project_name: str,
    directory: str,
    split: Split,
    config: str,
) -> Annotated[LakefsInfo, "lakefs_info"]:
    logger.info(f"---- \n Ingesting dataset {hf_dataset_name} into {project_name}/{directory}, split: {split} \n ----")
    lakefs_dataset = get_lakefs_dataset(directory, project_name)

    _ = stream_and_upload_from_hf_to_lakefs(
        hf_dataset_name=hf_dataset_name,
        dataset=lakefs_dataset,
        name=config,
        chunk_size=split.chunk_size,
        split=split.name,
        start=split.start,
        end=split.end,
    )

    lakefs_info = LakefsInfo(
        directory=directory,
        project_name=project_name,
        split=split.name,
        dataset_type="raw",
        ml_dataset_type=split.name,
        namespace=lakefs_dataset.credentials.namespace,
        repo_name=lakefs_dataset.lakefs_client.repo_manager.repo_name,
        branch_name=lakefs_dataset.lakefs_client.branch_manager.current_branch,
        address=lakefs_dataset.credentials.endpoint_url + "/repositories/"
                + lakefs_dataset.lakefs_client.repo_manager.repo_name
                + "/objects?ref=main&path="
                + lakefs_dataset.dataset.get_path()
    )
    log_metadata(
        metadata={
            "dataset_info": {
                "hf_dataset_name": hf_dataset_name,
                "project_name": project_name,
                "directory": directory,
                "split": split.name,
                "chunk_size": split.chunk_size,
                "start": split.start,
                "end": split.end,
            },
            "lakefs_info": lakefs_info.model_dump()
        }
    )

    return lakefs_info
