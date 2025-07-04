import os

import mlflow
from datasets import load_dataset
from loguru import logger

from ml.config import config
from ml.data_module.lakefs import get_dataset
from ml.experiment.mlflow.llamacpp import LlamaCppModel
from ml.finetuning.unsloth import get_trainer_model
from ml.config import enable_multipart_upload


def main():
    model_config, mlflow_config = config()
    mlflow.set_tracking_uri(mlflow_config["mlflow"]["URL"])
    enable_multipart_upload()
    num_proc = model_config.dataset.get("num_proc", 2)
    if model_config.dataset.get("lakefs"):
        dataset = get_dataset(
            directory=model_config.dataset.lakefs.directory,
            project_name=model_config.dataset.lakefs.project_name,
            dataset_type=model_config.dataset.lakefs.dataset_type,
            branch_name=model_config.dataset.lakefs.branch_name,
            split=model_config.dataset.lakefs.split,
            num_proc=num_proc,
        )
    elif model_config.dataset.get("hf"):
        dataset = load_dataset(
            model_config.dataset.hf.name,
            split=model_config.dataset.hf.split,
            num_proc=num_proc,
        )


    column_to_be_used = model_config.dataset.get("column_to_be_used", None)
    chat_template = model_config.chat_template
    chat_mapping = model_config.dataset.get("chat_mapping", None)
    model_save_path = "saved_model"

    mlflow.set_experiment("qa_model_training")
    with mlflow.start_run() as run:
        mlflow.log_params(dict(model_config))
        sample_examples = dataset.select(range(5)).to_pandas().to_html()
        sample_file = "sample_dataset.html"
        with open(sample_file, "w") as f:
            f.write(sample_examples)
        mlflow.log_artifact(sample_file, artifact_path="dataset_samples")

        trainer_model, tokenizer = get_trainer_model(
            chat_template=chat_template,
            dataset=dataset,
            from_pretrained=model_config.from_pretrained,
            sft_configs=model_config.sft_configs,
            peft_configs=model_config.peft_configs,
            peft_adapters=model_config.peft_adapters,
            mapping=chat_mapping,
            column_to_be_used=column_to_be_used,
        )
        trainer_model.train()
        model = trainer_model.model

        if (
            trainer_model.state.log_history
            and "loss" in trainer_model.state.log_history[-1]
        ):
            final_loss = trainer_model.state.log_history[-1]["loss"]
            mlflow.log_metric("final_train_loss", final_loss)

        logger.info(f"starting to save model at {model_save_path}")
        model.save_pretrained_gguf(
            model_save_path,
            tokenizer,
            quantization_method=model_config.quantization_method,
            max_shard_size="500MB"
        )
        logger.info(f"Model saved at {model_save_path}")

        # old_model_path = os.path.join(
        #     model_save_path, f"unsloth.{model_config.quantization_method.upper()}.gguf"
        # )
        # new_model_path = os.path.join(model_save_path, "model.gguf")  # New name
        # os.rename(old_model_path, new_model_path)

        # mlflow.pyfunc.log_model(
        #     artifact_path="model_path",
        #     python_model=LlamaCppModel(),
        #     artifacts={"model_path": f"{model_save_path}/model.gguf"},
        #     pip_requirements=["mlflow==2.4.0", "llama-cpp-python", "pandas"],
        # )
        # run_id = run.info.run_id
        # model_uri = f"runs:/{run_id}/model"
        # logger.info(f"Model logged at URI: {model_uri}")
        # registered_model_name = "qa_model"
        # model_details = mlflow.register_model(
        #     model_uri=model_uri, name=registered_model_name
        # )
        # logger.info(
        #     f"Registered model '{model_details.name}' with version {model_details.version}"
        # )


if __name__ == "__main__":
    main()
