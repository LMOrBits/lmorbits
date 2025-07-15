from orchestration.dev.steps.ml.finetune_unsloth.skypilot_fintuning_slm_step import sky_finetuning_slm 
from zenml import pipeline
from orchestration.cli.pipe import dev,click
from orchestration.utils.config import run_or_modify_config

# @pipeline(enable_cache=False)
# def finetune_slm_pipeline():
#     _ ,  hf_dataset = fineruning_dataset_ingestion()
#     fineruning_with_unsloth(hf_dataset=hf_dataset)

@pipeline
def sky_finetune_slm_pipeline():
    sky_finetuning_slm()

@dev.command()
@click.option("--config", is_flag=True, help="Modify the config file")
def sky_finetune_slm(config:bool):
    """
    ----
    Pipeline that performs finetuning of a SLM model
    ----
    """
    run_or_modify_config("dev/ml/sky_finetune_slm.yaml", sky_finetune_slm_pipeline, config=config)