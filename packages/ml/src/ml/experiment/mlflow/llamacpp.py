import mlflow.pyfunc
import pandas as pd
from loguru import logger
from pathlib import Path


class LlamaCppModel(mlflow.pyfunc.PythonModel):
    """MLflow PythonModel wrapper for LLaMA.cpp GGUF models."""
    
    def __init__(
        self,
        n_ctx: int = 2048,
        n_threads: int = 4,
        n_gpu_layers: int = 0,
        verbose: bool = True
    ):
        """Initialize the wrapper with model configuration.
        
        Args:
            n_ctx: Context window size
            n_threads: Number of CPU threads to use
            n_gpu_layers: Number of layers to offload to GPU
            verbose: Whether to enable verbose logging
        """
        # Store only primitive types to avoid serialization issues
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.n_gpu_layers = n_gpu_layers
        self.verbose = verbose
        # Do NOT initialize the model here - it will be loaded in load_context
        
    def load_context(self, context):
        """Load the GGUF model when the model is loaded by MLflow.
        
        Args:
            context: MLflow model context containing artifacts
        """
        try:
            # Import here to avoid serialization issues
            from llama_cpp import Llama
            
            if "model_path" not in context.artifacts:
                raise ValueError("No model_path found in artifacts")
                
            model_path = context.artifacts["model_path"]
            if not Path(model_path).exists():
                raise ValueError(f"Model file not found: {model_path}")
                
            logger.info(f"Loading LLaMA model from {model_path}")
            logger.info(f"Model config: n_ctx={self.n_ctx}, "
                       f"n_threads={self.n_threads}, "
                       f"n_gpu_layers={self.n_gpu_layers}")
            
            self.model = Llama(
                model_path=model_path,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                n_gpu_layers=self.n_gpu_layers,
                verbose=self.verbose
            )
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    def predict(self, context, model_input):
        """Run inference with the model.
        
        Args:
            context: MLflow context
            model_input: Pandas DataFrame containing:
                - 'prompt': Text prompt for the model
                - 'max_tokens': (optional) Maximum tokens to generate
                - 'temperature': (optional) Sampling temperature
                - 'top_p': (optional) Top-p sampling parameter
                - 'stop': (optional) List of stop sequences
                
        Returns:
            Model output as a string
        """
        if not hasattr(self, 'model') or self.model is None:
            raise RuntimeError("Model not loaded. Call load_context first.")
            
        if not isinstance(model_input, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")
            
        if "prompt" not in model_input.columns:
            raise ValueError("Input DataFrame must contain 'prompt' column")
            
        # Get parameters from input or use defaults
        max_tokens = int(model_input["max_tokens"].iloc[0]) if "max_tokens" in model_input.columns else 128
        temperature = float(model_input["temperature"].iloc[0]) if "temperature" in model_input.columns else 0.8
        top_p = float(model_input["top_p"].iloc[0]) if "top_p" in model_input.columns else 0.95
        stop = model_input["stop"].iloc[0] if "stop" in model_input.columns else []
        
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
