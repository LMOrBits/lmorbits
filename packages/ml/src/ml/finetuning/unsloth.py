from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template, standardize_sharegpt
from trl import SFTTrainer
from transformers import TrainingArguments, DataCollatorForSeq2Seq
from unsloth import is_bfloat16_supported
from unsloth.chat_templates import train_on_responses_only

# max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
# dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
# load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

# model_name ="unsloth/Llama-3.2-3B-Instruct"
# chat_template = "llama-3.1"

# sft_configs = dict(
#     max_seq_length = max_seq_length,
#     dataset_text_field = "text",
#     dataset_num_proc = 2,
#     packing = False, # Can make training 5x faster for short sequences.
# )
# peft_adapters = dict(
#     r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
#     target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
#                       "gate_proj", "up_proj", "down_proj",],
#     lora_alpha = 16,
#     lora_dropout = 0, # Supports any, but = 0 is optimized
#     bias = "none",    # Supports any, but = "none" is optimized
#     # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
#     use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
#     random_state = 3407,
#     use_rslora = False,  # We support rank stabilized LoRA
#     loftq_config = None, # And LoftQ
# )

# dataset = load_dataset("mlabonne/FineTome-100k", split = "train[:100]")


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

    tokenizer = get_chat_template(
        tokenizer,
        chat_template=chat_template,
        mapping=mapping,
    )

    # dataset = standardize_sharegpt(dataset)

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

    dataset = dataset.map(
        formatting_prompts_func,
        batched=True,
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer),
        **sft_configs,
        args=TrainingArguments(
            **peft_configs,
            fp16=not is_bfloat16_supported(),
            bf16=is_bfloat16_supported(),
        ),
    )

    trainer = train_on_responses_only(
        trainer,
        instruction_part="<|start_header_id|>user<|end_header_id|>\n\n",
        response_part="<|start_header_id|>assistant<|end_header_id|>\n\n",
    )
    return trainer, tokenizer
