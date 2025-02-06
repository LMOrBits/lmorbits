import sys
import os
from pathlib import Path
from convert_hf_to_gguf import main

def convert_model_to_gguf(model_path: str, output_file: str, output_type: str = "q8_0"):
    # Store original argv
    original_argv = sys.argv.copy()
    
    # Set up the arguments as they would be passed via command line
    sys.argv = [
        "convert_hf_to_gguf.py",
        model_path,
        "--outfile", output_file,
        "--outtype", output_type
    ]
    
    try:
        # Call the main function
        main()
    finally:
        # Restore original argv
        sys.argv = original_argv

