from pathlib import Path
from omegaconf import OmegaConf
from ml.finetuning.unsloth import get_trainer_model
from ml.experiment.mlflow.artifact_ingest_gcs import upload_artifact_to_mlflow_gcs
from configparser import ConfigParser
import mlflow
import os
from datasets import load_dataset
import numpy as np

def main():
  model_config, mlflow_config = config()
  mlflow.set_tracking_uri(mlflow_config['mlflow']['URL'])
  random_int = np.random.randint(1000000)
  mlflow.create_experiment(f"artifact_checks_seperate_test_{random_int}",
                           artifact_location=mlflow_config['mlflow']['GCS_BUCKET'])
  # base_artifact_uri = mlflow_config['mlflow']['GCS_BUCKET']
  artifact_subpath = "model_path"
  local_file_path = Path(__file__).parent / "pyproject.toml"
  readme_path = Path(__file__).parent / "README.md"
  
  
  dataset = load_dataset(model_config.dataset.name, split = model_config.dataset.split)
  
  with mlflow.start_run() as run:
    mlflow.log_params(dict(model_config))
    sample_examples = dataset.select(range(5)).to_dict()
    sample_file = "sample_dataset.txt"
    with open(sample_file, "w") as f:
        f.write(str(sample_examples))
    mlflow.log_artifact(sample_file, artifact_path="dataset_samples")
    
    trainer_model = get_trainer_model(
      model_name = model_config.model_name,
      chat_template = model_config.chat_template,
      dataset = dataset,
      peft_adapters = model_config.peft_adapters,
      sft_configs = model_config.sft_configs,
      peft_configs = model_config.peft_configs,
      max_seq_length = model_config.max_seq_length,
      dtype = model_config.dtype,
      load_in_4bit = model_config.load_in_4bit,
    )
    trainer_stats = trainer.train()
    model = trainer.model
    if trainer.state.log_history and "loss" in trainer.state.log_history[-1]:
        final_loss = trainer.state.log_history[-1]["loss"]
        mlflow.log_metric("final_train_loss", final_loss)
    model_save_path = "saved_model"
    model.save_pretrained_gguf(model_save_path,tokenizer, quantization_method ="q5_k_m")  # Local saving
    os.makedirs(model_save_path, exist_ok=True)  
    mlflow.log_artifact("./saved_model/unsloth.Q5_K_M.gguf", artifact_path="model_path/unsloth.Q5_K_M.gguf")  
    print(f"MLflow run {run.info.run_id} completed.")

def config():
  config_path = Path(__file__).parent / "configs" / "finetuning.yaml"
  model_config = OmegaConf.load(config_path)
  OmegaConf.resolve(model_config)
  
  mlflow_config_path = Path(__file__).parent.parent.parent / "scripts/config.ini"
  mlflow_config = ConfigParser()
  mlflow_config.read(mlflow_config_path)
  os.environ['MLFLOW_TRACKING_USERNAME'] = mlflow_config['mlflow']['TRACKING_USERNAME']
  os.environ['MLFLOW_TRACKING_PASSWORD'] = mlflow_config['mlflow']['TRACKING_PASSWORD']
  return model_config, mlflow_config

if __name__ == "__main__":
  main()
