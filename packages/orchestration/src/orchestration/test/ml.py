import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.base import BaseEstimator
from sklearn.datasets import load_iris
from zenml import pipeline, step
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import mlflow
from zenml.config import DockerSettings
from zenml.integrations.skypilot_gcp.flavors.skypilot_orchestrator_gcp_vm_flavor import SkypilotGCPOrchestratorSettings


docker_settings = DockerSettings(
            parent_image='europe-north1-docker.pkg.dev/slmops-dev/images-dev/zenml-image-orchestration:latest',
            python_package_installer="uv",
            requirements=["zenml==0.71.0"],
            skip_build=False,
            prevent_build_reuse=True,
        )
skypilot_settings = SkypilotGCPOrchestratorSettings(
    # cpus="4",
    # ports=("5000","8000"),
    # memory="16",
    accelerators="l4:1",
    # accelerator_args={"tpu_vm": True, "runtime_version": "tpu-vm-base"},
    # use_spot=True,
    # job_recovery="recovery_strategy",
    # region="us-west1",
    # zone="us-west1-a",
    image_id="docker:nvcr.io/nvidia/cuda:12.1.1-cudnn8-devel-ubuntu20.04",
    # disk_size=100,
    # disk_tier="high",
    # cluster_name="my_cluster",
    # retry_until_up=True,
    # idle_minutes_to_autostop=60,
    # down=True,
    # stream_logs=True
)


@step(experiment_tracker="mlflow_tracker")
def train_model() -> BaseEstimator:
    mlflow.autolog()
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mlflow.log_metric("train_accuracy", accuracy_score(y_test, y_pred))
    return model


@pipeline(settings={
    "orchestrator": skypilot_settings,
    "docker": docker_settings},enable_cache=True)
def training_pipeline():
    train_model()



if __name__ == "__main__":
  training_pipeline()