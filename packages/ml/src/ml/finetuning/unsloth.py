from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template, standardize_sharegpt
from trl import SFTTrainer
from transformers import TrainingArguments, DataCollatorForSeq2Seq
from unsloth import is_bfloat16_supported
from unsloth.chat_templates import train_on_responses_only
from loguru import logger
from pathlib import Path
import os 

def llama_cpp_build_path():
    return Path(__file__).parents[3] 
    
def cd_llama_cpp():
    os.chdir(llama_cpp_build_path())

def get_trainer_model(
    chat_template,
    dataset,
    from_pretrained,
    sft_configs,
    peft_configs,
    peft_adapters,
    mapping,
    column_to_be_used="conversations",
):
    model, tokenizer = FastLanguageModel.from_pretrained(
        dtype=None,
        **from_pretrained,
        # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
    )

    model = FastLanguageModel.get_peft_model(
        model,
        **peft_adapters,
    )

    if mapping:
        tokenizer = get_chat_template(
            tokenizer,
            chat_template=chat_template,
            mapping=mapping,
        )
    else:
        tokenizer = get_chat_template(
            tokenizer,
            chat_template=chat_template,
        )

    def formatting_prompts_func(examples):
        convos = examples[column_to_be_used]
        texts = [
            tokenizer.apply_chat_template(
                convo, tokenize=False, add_generation_prompt=False
            )
            for convo in convos
        ]
        return {
            "text": texts,
        }
    logger.info(f"dataset: \n { dataset.select(range(1)).to_pandas().iloc[0][column_to_be_used] }")
    
    new_dataset = dataset.map(
        formatting_prompts_func,
        batched=True,
        remove_columns=dataset.column_names  # Remove original columns
    )
    logger.info(f"new_dataset: \n { new_dataset.select(range(1)).to_pandas().iloc[0]['text'] }")
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=new_dataset,
        data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer),
        **sft_configs,
        args=TrainingArguments(
            **peft_configs,
            fp16=not is_bfloat16_supported(),
            bf16=is_bfloat16_supported(),
        ),
    )
    #TODO: make this more dynamic  
    begin_token = tokenizer.bos_token
    end_token = tokenizer.eos_token
    
    instruction_part = tokenizer.apply_chat_template([{"role":"user"}, ], tokenize=False)
    instruction_part = instruction_part[len(begin_token):-len(end_token)].strip()
    response_part = tokenizer.apply_chat_template([{"role":"assistant"}, ], tokenize=False)
    response_part = response_part[len(begin_token):-len(end_token)].strip()
    trainer = train_on_responses_only(
        trainer,
        instruction_part=instruction_part,
        response_part=response_part
    )
    return trainer, tokenizer