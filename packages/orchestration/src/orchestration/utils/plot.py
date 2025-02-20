from plotly.graph_objects import Figure


def convert_figure_to_html_string(
    fig: Figure, header: str = "", paragraph: str = ""
) -> str:
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
