from taskpy import TaskCLI
from pathlib import Path
ml_task = TaskCLI(Path(__file__).parent)


def build_llama_cpp():
  ml_task.run("llama-cpp-build")







