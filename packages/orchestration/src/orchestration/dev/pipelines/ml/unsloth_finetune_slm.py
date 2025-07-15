from orchestration.dev.steps.ml.finetune_unsloth.finetuning import fineruning_dataset_ingestion, fineruning_with_unsloth
from orchestration.utils.config import run_or_modify_config
from zenml import pipeline



@pipeline
def unsloth_finetune_slm_pipeline():
    _ ,  hf_dataset = fineruning_dataset_ingestion()
    fineruning_with_unsloth(hf_dataset=hf_dataset)


if __name__ == "__main__":
    run_or_modify_config("dev/ml/.yaml", unsloth_finetune_slm_pipeline, config=False)
    
