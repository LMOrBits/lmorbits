from zenml.client import Client
from argparse import ArgumentParser
from loguru import logger

client = Client()

# Get the list of pipelines that start with "test_pipeline"
# use a large size to ensure we get all of them
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--pipeline_name", type=str, required=False, default="test_pipeline")
    parser.add_argument("-y", "--yes", action="store_true", required=False, default=False)
    args = parser.parse_args()
    pipelines_list = client.list_pipelines(name="startswith:" + args.pipeline_name, size=100)

    target_pipeline_ids = [p.id for p in pipelines_list.items]

    logger.info(f"Found {len(target_pipeline_ids)} pipelines to delete")

    confirmation = "y" if args.yes else input("Do you really want to delete these pipelines? (y/n): ").lower()

    if confirmation == "y":
        logger.info(f"Deleting {len(target_pipeline_ids)} pipelines")
        for pid in target_pipeline_ids:
            client.delete_pipeline(pid)
        logger.info("Deletion complete")
    else:
        logger.info("Deletion cancelled")
