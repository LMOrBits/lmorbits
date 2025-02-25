import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Annotated
from zenml.types import HTMLString
from orchestration.utils.plot import convert_df_to_html_string
import pandas as pd
import mlflow
from datasets import load_dataset
from loguru import logger
from ml.config import enable_multipart_upload
from ml.data_module.lakefs import get_dataset_from_lakefs, Dataset
from ml.experiment.mlflow.llamacpp import LlamaCppModel

from ml.finetuning.unsloth import get_trainer_model
from ml.finetuning.unsloth import cd_llama_cpp
from zenml import log_metadata, pipeline, step
from zenml.integrations.mlflow.flavors.mlflow_experiment_tracker_flavor import MLFlowExperimentTrackerSettings
import transformers

from orchestration.secrets.data_secrets import get_lakefs_credentials


mlflow_settings = MLFlowExperimentTrackerSettings(
    experiment_name="qa_model_training_zenml",
)

@step
def test_fineruning_dataset_ingestion( dataset: Dict[str, Any]) -> Tuple[Annotated[HTMLString | None, "HTML Representation of Dataset"], Annotated[Dataset | None, "Dataset"]]:
    log_metadata(metadata={"dataset": dataset})
    hf_dataset = None
    lakefs_credentials = get_lakefs_credentials()

    if dataset.get("lakefs", None):
        hf_dataset = get_dataset_from_lakefs(
            directory=dataset["lakefs"]["directory"],
            project_name=dataset["lakefs"]["project_name"],
            dataset_type=dataset["lakefs"]["dataset_type"],
            branch_name=dataset["lakefs"]["branch_name"],
            split=dataset["lakefs"]["split"],
            num_proc=dataset["num_proc"],
            lakefs_credentials=lakefs_credentials,
        )

    elif dataset.get("hf"):
        hf_dataset = load_dataset(
            dataset["hf"]["name"],
            split=dataset["hf"]["split"],
            num_proc=dataset["num_proc"],
        )

    if isinstance(hf_dataset, Dataset):
        hf_dataset_df = hf_dataset.select(range(5)).to_pandas()
        html_string = convert_df_to_html_string(hf_dataset_df , "Dataset", f"This is a sample of the dataset")
        return HTMLString(html_string) , hf_dataset
    return None,hf_dataset



@step(experiment_tracker="mlflow_tracker",
      settings={"experiment_tracker": mlflow_settings})
# @step
def test_fineruning_with_unsloth(
    hf_dataset: Dataset,
    from_pretrained: Dict[str, Any],
    peft_adapters: Dict[str, Any],
    sft_configs: Dict[str, Any],
    peft_configs: Dict[str, Any],
    quantization_method: str,
    chat_template: str,
    column_to_be_used: Optional[str] = None,
    chat_mapping: Optional[Dict[str, str]] = None
):
    metadata = {
        "from_pretrained": from_pretrained,
        "peft_adapters": peft_adapters,
        "sft_configs": sft_configs,
        "peft_configs": peft_configs,
        "quantization_method": quantization_method,
    }
    log_metadata(metadata=metadata)
    enable_multipart_upload()
    model_save_path = "saved_model"
    mlflow.log_params(metadata)
    sample_examples = hf_dataset.select(range(5)).to_pandas().to_html()
    sample_file = "sample_dataset.html"
    with open(sample_file, "w") as f:
        f.write(sample_examples)
    mlflow.log_artifact(sample_file, artifact_path="dataset_samples")
    logger.warning(f"chat_mapping: {chat_mapping=}")
    logger.warning(f"chat_template: {chat_template=}")
    logger.warning(f"metadata: {metadata=}")



    trainer_model, tokenizer = get_trainer_model(
        chat_template=chat_template,
        dataset=hf_dataset,
        from_pretrained=from_pretrained,
        sft_configs=sft_configs,
        peft_configs=peft_configs,
        peft_adapters=peft_adapters,
        mapping=chat_mapping,
        column_to_be_used=column_to_be_used,
        
    )
    trainer_model.train()
    model = trainer_model.model

    if trainer_model.state.log_history and "loss" in trainer_model.state.log_history[-1]:
        final_loss = trainer_model.state.log_history[-1]["loss"]
        mlflow.log_metric("final_train_loss", final_loss)
    # Define the signature
    components = {"model": model, "tokenizer": tokenizer}
    mlflow.transformers.log_model(
        transformers_model=components,
        artifact_path="model"
    )
    cd_llama_cpp()
    logger.info(f"starting to save model at {model_save_path}")
    model.save_pretrained_gguf(
        model_save_path,
        tokenizer,
        quantization_method=quantization_method,
    )
    logger.info(f"Model saved at {model_save_path}")
    old_model_path = os.path.join(model_save_path, f"unsloth.{quantization_method.upper()}.gguf")
    new_model_path = os.path.join(model_save_path, "model.gguf")  # New name
    os.rename(old_model_path, new_model_path)

    mlflow.pyfunc.log_model(
        artifact_path="model_path",
        python_model=LlamaCppModel(),
        artifacts={"model_path": f"{model_save_path}/model.gguf"},
        pip_requirements=["mlflow==2.4.0", "llama-cpp-python", "pandas"],
    )
    run_id = mlflow.active_run().info.run_id
    model_uri = f"runs:/{run_id}/model"
    logger.info(f"Model logged at URI: {model_uri}")
    registered_model_name = "qa_model"
    model_details = mlflow.register_model(model_uri=model_uri, name=registered_model_name)
    logger.info(f"Registered model '{model_details.name}' with version {model_details.version}")



@pipeline
def test_fineruning_pipeline():
    _ ,  hf_dataset = test_fineruning_dataset_ingestion()
    test_fineruning_with_unsloth(hf_dataset=hf_dataset)


if __name__ == "__main__":
    test_fineruning_pipeline.with_options(config_path=f"{Path(__file__).parents[1]}/configs/ml_config.yaml")()
