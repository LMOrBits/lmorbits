import argparse
import time

import yaml
from data.utils.hugging_face import get_info, get_one_sample
from loguru import logger
from rich import box
from rich.console import Console, Group
from rich.live import Live
from rich.table import Table


def make_renderable(samples):
      parts = []
      for split, sample in samples.items():
          # YAML-style header
          parts.append(f"[bold green]{split}:[/bold green]")
          # build a table of field→value
          tbl = Table(box=box.MINIMAL)
          tbl.add_column("Field", style="bold cyan", no_wrap=True)
          tbl.add_column("Value")
          for k, v in sample.items():
              # turn lists into multi-line strings
              val = "\n".join(v) if isinstance(v, list) else str(v)
              tbl.add_row(k, val)
          parts.append(tbl)
      return Group(*parts)

if __name__ == "__main__":
    console = Console()
    parser = argparse.ArgumentParser()
    parser.add_argument("--hf_dataset_name", type=str, required=True)
    args = parser.parse_args()
    logger.info(f"Getting splits for dataset {args.hf_dataset_name}")
    info , config_name = get_info(args.hf_dataset_name)
    logger.info(f"Info: {yaml.dump(info._to_yaml_dict())}")
    ## show one row of each split in a table
    samples = get_one_sample(args.hf_dataset_name, config_name)
    # 2) Live display (static here, but ready for updates)
    with Live(make_renderable(samples), refresh_per_second=4, console=console):
        time.sleep(3)

   