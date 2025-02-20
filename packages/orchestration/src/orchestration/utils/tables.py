import pandas as pd
from datasets import load_dataset
from IPython.display import HTML, display

# dataset = load_dataset(dataset_name, split="train")
# dataset_name = "b-mc2/sql-create-context"


def display_table(dataset_or_sample):
    # A helper fuction to display a Transformer dataset or single sample contains multi-line string nicely
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_rows", None)

    if isinstance(dataset_or_sample, dict):
        df = pd.DataFrame(dataset_or_sample, index=[0])
    elif isinstance(dataset_or_sample, pd.DataFrame):
        df = dataset_or_sample
    else:
        df = pd.DataFrame(dataset_or_sample)

    html = df.to_html().replace("\\n", "<br>")
    styled_html = f"""<style> .dataframe th, .dataframe tbody td {{ text-align: left; padding-right: 30px; }} </style> {html}"""
    display(HTML(styled_html))


# display_table(dataset.select(range(3)))
