from zenml import step, pipeline, log_metadata
from zenml.types import HTMLString
import plotly.graph_objects as go
from typing import Dict, Any
from orchestration.utils.plot import convert_figure_to_html_string
from pathlib import Path 


@step
def test_fineruning_with_unsloth(from_pretrained: Dict[str, Any], peft_adapters: Dict[str, Any],sft_configs: Dict[str, Any], peft_configs: Dict[str, Any]):
  log_metadata(metadata={"from_pretrained":from_pretrained,
                         "peft_adapters":peft_adapters,
                         "sft_configs":sft_configs,
                         "peft_configs":peft_configs})

@step
def test_fineruning_dataset_ingestion(chat_template: str, dataset: Dict[str, Any]):
  log_metadata(metadata={"chat_template":chat_template, "dataset":dataset})

@step
def test_quntization(quantization_method: str):
  log_metadata(metadata={"quantization_method":quantization_method})

@pipeline
def test_fineruning_pipeline():
  test_fineruning_dataset_ingestion()
  test_fineruning_with_unsloth()
  test_quntization()


if __name__ == "__main__":
  test_fineruning_pipeline.with_options(config_path="configs/ml_config.yaml")()