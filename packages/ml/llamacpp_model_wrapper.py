
import mlflow.pyfunc
import pandas as pd
from pathlib import Path

class LlamaCppModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        from llama_cpp import Llama
        model_path = context.artifacts["model_path"]
        self.model = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=8,
            n_gpu_layers=0,
            verbose=True
        )
    
    def predict(self, context, model_input):
        if not isinstance(model_input, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")
        
        if "prompt" not in model_input.columns:
            raise ValueError("Input DataFrame must contain 'prompt' column")
        
        max_tokens = int(model_input.get("max_tokens", [128]).iloc[0]) if "max_tokens" in model_input.columns else 128
        prompt = model_input["prompt"].iloc[0]
        
        output = self.model(
            prompt=prompt,
            max_tokens=max_tokens,
            echo=False
        )
        
        return output["choices"][0]["text"] if output else ""
