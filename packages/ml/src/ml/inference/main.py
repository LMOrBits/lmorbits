from unsloth import FastLanguageModel
import torch
def main():
  max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
  dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
  load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

  # 4bit pre quantized models we support for 4x faster downloading + no OOMs.
  fourbit_models = [
      "unsloth/Meta-Llama-3.1-8B-bnb-4bit",      # Llama-3.1 15 trillion tokens model 2x faster!
      "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
      "unsloth/Meta-Llama-3.1-70B-bnb-4bit",
      "unsloth/Meta-Llama-3.1-405B-bnb-4bit",    # We also uploaded 4bit for 405b!
      "unsloth/Mistral-Nemo-Base-2407-bnb-4bit", # New Mistral 12b 2x faster!
      "unsloth/Mistral-Nemo-Instruct-2407-bnb-4bit",
      "unsloth/mistral-7b-v0.3-bnb-4bit",        # Mistral v3 2x faster!
      "unsloth/mistral-7b-instruct-v0.3-bnb-4bit",
      "unsloth/Phi-3.5-mini-instruct",           # Phi-3.5 2x faster!
      "unsloth/Phi-3-medium-4k-instruct",
      "unsloth/gemma-2-9b-bnb-4bit",
      "unsloth/gemma-2-27b-bnb-4bit",            # Gemma 2x faster!
  ] # More models at https://huggingface.co/unsloth

  model, tokenizer = FastLanguageModel.from_pretrained(
      model_name = "unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
      max_seq_length = max_seq_length,
      dtype = dtype,
      load_in_4bit = load_in_4bit,
      # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
  )
  from transformers import TextStreamer
  alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

  ### Instruction:
  {}

  ### Input:
  {}

  ### Response:
  {}"""

  # alpaca_prompt = Copied from above
  FastLanguageModel.for_inference(model) # Enable native 2x faster inference
  inputs = tokenizer(
  [
      alpaca_prompt.format(
          "Continue the fibonnaci sequence.", # instruction
          "1, 1, 2, 3, 5, 8", # input
          "", # output - leave this blank for generation!
      )
  ], return_tensors = "pt").to("cuda")

  outputs = model.generate(**inputs, max_new_tokens = 64, use_cache = True)
  decoded_output = tokenizer.batch_decode(outputs)
  return decoded_output

if __name__ == "__main__" :
  response = main()
  print(response)