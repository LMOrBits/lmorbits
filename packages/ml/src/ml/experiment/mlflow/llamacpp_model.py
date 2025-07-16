"""
Standalone LlamaCpp model for MLflow code-based logging.
This file contains the model definition that can be referenced by MLflow.
"""

import mlflow.pyfunc
import pandas as pd
from pathlib import Path


class LlamaCppModel(mlflow.pyfunc.PythonModel):
    """MLflow PythonModel wrapper for LLaMA.cpp GGUF models."""
    
    def load_context(self, context):
        """Load the GGUF model when the model is loaded by MLflow."""
        try:
            from llama_cpp import Llama
            
            if "model_path" not in context.artifacts:
                raise ValueError("No model_path found in artifacts")
                
            model_path = context.artifacts["model_path"]
            if not Path(model_path).exists():
                raise ValueError(f"Model file not found: {model_path}")
                
            # Use default settings that work well for most cases
            self.model = Llama(
                model_path=model_path,
                n_ctx=2048,
                n_threads=8,
                n_gpu_layers=0,
                verbose=True
            )
            
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")
    
    def predict(self, context, model_input):
        """Run inference with the model."""
        if not hasattr(self, 'model') or self.model is None:
            raise RuntimeError("Model not loaded. Call load_context first.")
            
        if not isinstance(model_input, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")
            
        if "prompt" not in model_input.columns:
            raise ValueError("Input DataFrame must contain 'prompt' column")
            
        # Get parameters from input or use defaults
        max_tokens = int(model_input.get("max_tokens", [128]).iloc[0])
        temperature = float(model_input.get("temperature", [0.8]).iloc[0])
        top_p = float(model_input.get("top_p", [0.95]).iloc[0])
        stop = model_input.get("stop", [[]]).iloc[0]
        
        # Get the prompt
        prompt = model_input["prompt"].iloc[0]
        
        # Run inference
        output = self.model(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=stop,
            echo=False
        )
        
        return output["choices"][0]["text"] if output else "" 