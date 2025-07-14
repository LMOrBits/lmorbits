import pandas as pd
from datasets import load_dataset
from IPython.display import HTML, display

# dataset = load_dataset(dataset_name, split="train")
# dataset_name = "b-mc2/sql-create-context"


def main_display_table(dataset_or_sample):
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
    return html

def display_table(dataset_or_sample):
    html = main_display_table(dataset_or_sample)
    styled_html = (
        f"""<style> .dataframe th, .dataframe tbody td {{ text-align: left; padding-right: 30px; }} </style> {html}"""
    )
    return styled_html

def display_dict_of_tables(dict_of_tables):
    html_list= []
    for key, value in dict_of_tables.items():
        html_list.append(f"<h2>{key}</h2><div style='margin: 20px 0px;'>{main_display_table(value)}</div>")
    
    styled_html = (
        f"""<style> .dataframe th, .dataframe tbody td {{ text-align: left; padding-right: 30px; }} </style> {html_list}"""
    )
    return styled_html






# display_table(dataset.select(range(3)))
