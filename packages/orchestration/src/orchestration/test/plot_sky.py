from zenml import pipeline, step 
from zenml.types import HTMLString
from zenml.config import DockerSettings
import plotly.graph_objects as go
import numpy as np
from orchestration.utils.plot import convert_figure_to_html_string
from pathlib import Path 
from zenml.integrations.skypilot_gcp.flavors.skypilot_orchestrator_gcp_vm_flavor import SkypilotGCPOrchestratorSettings

skypilot_settings = SkypilotGCPOrchestratorSettings(
    instance_type="g2-standard-4",
    accelerators="L4:1",
    image_id="docker:nvcr.io/nvidia/cuda:12.1.1-cudnn8-devel-ubuntu20.04",
)
docker_settings =DockerSettings(
            parent_image='europe-north1-docker.pkg.dev/slmops-dev/images-dev/zenml-image-orchestration:latest',
            python_package_installer="uv",
            requirements=["zenml==0.71.0"],
            skip_build=True,
            prevent_build_reuse=False,
        )

@step(
        enable_cache=False
    )
def html_plotly() -> HTMLString:
    # Create some sample data
    x = np.linspace(0, 10, 200)
    y = np.sin(x)
    
    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='sin(x)'))
    
    # Customize layout
    fig.update_layout(
        title='Interactive Sine Wave Plot',
        xaxis_title='x',
        yaxis_title='sin(x)',
        template='plotly_white'
    )
    
    # Convert to HTML string
    html_string = convert_figure_to_html_string(fig, "Plotly Visualization", "test2")

    return HTMLString(html_string)

@pipeline(
    settings={"docker": docker_settings,
              "orchestrator": skypilot_settings},
    enable_cache=False
)
def html_plotly_pipeline():
    html_plotly()


if __name__ == "__main__":
  html_plotly_pipeline()