import click
import subprocess
from pathlib import Path
from serve.mlflow.main import download_model_artifact_from_gcs
from serve.mlflow.check import model_needs_update
from serve.mlflow.model_config import ModelConfig
import serve.mlflow.config as config
import mlflow
import os

CONTAINER_NAME = "llamacpp"
IMAGE_NAME = "ghcr.io/ggerganov/llama.cpp:server"
MODEL_MOUNT = f"{Path(__file__).parents[2]}/models:/models"
MODEL_PATH = "/models/model.gguf"
PORTS = ["-p", "8000:8000", "-p", "8080:8080"]

@click.group()
def cli():
    """CLI tool for model management and inference."""
    pass

@click.command()
@click.option("--update", is_flag=True, help="Update the model")
@click.option("--download", is_flag=True, help="Download the model")
@click.option("--run", is_flag=True, help="Run a sample inference")
@click.option("--stop", is_flag=True, help="Stop the model")
@click.option("--status", is_flag=True, help="Check the status of the model")
@click.option("--rebuild", is_flag=True, help="Rebuild the Docker image")
@click.option("--force-download", is_flag=True, help="Force download the model")
def model(update, download, run, stop, status, rebuild, force_download):
    """Manage Docker operations."""
    if update or force_download:
        click.echo("Checking for model updates 🎸...")
        mlflow_config = config.config_init()
        mlflow.set_tracking_uri(mlflow_config['mlflow']['URL'])
        download_model_artifact_from_gcs(
            model_name="qa_model",
            alias="champion",
            artifact_path="model_path",
            gcs_bucket="slmops-dev-ml-artifacts",
            force_download=force_download
        )
        subprocess.run(["docker", "pull", IMAGE_NAME], check=True)
        
    
    if download :
        click.echo("Downloading model...")
        mlflow_config = config.config_init()
        mlflow.set_tracking_uri(mlflow_config['mlflow']['URL'])
        download_model_artifact_from_gcs(
            model_name="qa_model",
            alias="champion",
            artifact_path="model_path",
            gcs_bucket="slmops-dev-ml-artifacts"
        )
    
    if run:
        click.echo("Starting model server...")
        try:
            cmd = ["docker", "run", "-d", "--name", CONTAINER_NAME]
            click.echo(f"Setting up Docker container '{CONTAINER_NAME}'...")
            cmd.extend(PORTS)
            click.echo(f"Mapping ports: {', '.join(PORTS[::2])} -> {', '.join(PORTS[1::2])}")
            cmd.extend(["-v", MODEL_MOUNT])
            click.echo(f"Mounting model directory: {MODEL_MOUNT}")
            cmd.extend([IMAGE_NAME, "-m", MODEL_PATH])
            click.echo(f"Using image: {IMAGE_NAME}")
            click.echo(f"Model path: {MODEL_PATH}")
            click.echo("Running command: " + " ".join(cmd))
            
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            click.secho("✅ Container started successfully!", fg="green")
            click.echo(f"Container ID: {result.stdout.strip()}")
            click.echo(f"🎉 Server is running! on ports: {', '.join(PORTS[1::2])} 🎉")
        except subprocess.CalledProcessError as e:
            click.secho("❌ Failed to start Docker container!", fg="red")
            click.echo(f"Error: {e.stderr}")
            raise click.ClickException("Docker container failed to start")
    
    if stop:
        click.echo("Stopping Docker container...")
        subprocess.run(["docker", "stop", CONTAINER_NAME], check=True)
        subprocess.run(["docker", "rm", CONTAINER_NAME], check=True)

    if status:
        click.echo("Checking model status 🎸 ......")
        model_config = ModelConfig()
        click.echo(model_config.load_config())
        update_status = model_needs_update()
        click.secho("new model is available please run --update to download the new model" if update_status else  "Model is up to date 🚀", fg="green" if not update_status else "yellow")
        
    if rebuild:
        click.echo("Pulling latest Docker image...")
        subprocess.run(["docker", "pull", IMAGE_NAME], check=True)
    
    if not any([update, download, run, stop, status, rebuild]):
        click.echo("Please specify an action: --update, --download, --run, --stop, --status, or --rebuild")
        
@click.command()
def status():
    """Check server status."""
    click.echo("Checking server status...")
    subprocess.run(["docker", "ps", "--filter", f"name={CONTAINER_NAME}"], check=True)

def main():
    cli.add_command(model)
    cli.add_command(status)
    cli() 

