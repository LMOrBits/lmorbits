from plotly.graph_objects import Figure
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def convert_df_to_html_string(df: pd.DataFrame, header: str = "", paragraph: str = "") -> str:
    # Helper function to format cell values
    def format_cell(value):
        if isinstance(value, (list, tuple, np.ndarray)):
            return str(value)  # Convert list/array to string representation
        try:
            if pd.isna(value):
                return ""
        except ValueError:
            return str(value)
        return str(value)

    fig = go.Figure(data=[go.Table(
                        header=dict(
                            values=list(df.columns),
                            font=dict(size=14),  # Increased font size
                            align="left"
                        ),
                        cells=dict(
                            values=[[format_cell(row.get(col, "")) for row in df.to_dict(orient="records")] for col in df.columns],
                            font=dict(size=12),  # Increased font size
                            height=30,  # Added enough space
                            align="left"
                        )
        )])
    return convert_figure_to_html_string(fig, header, paragraph)

def convert_figure_to_html_string(fig: Figure, header: str = "", paragraph: str = "") -> str:
    """Convert Plotly figure to HTML string with custom header and paragraph.

    Args:
        fig: The Plotly figure.
        header: The header text.
        paragraph: The paragraph text.

    Returns:
        The HTML string.
    """
    return f"""
    <div style="text-align: center;">
        <h1>{header}</h1>
        <p>{paragraph}</p>
        <div>
            {fig.to_html(full_html=False)}
        </div>
    </div>
    """
