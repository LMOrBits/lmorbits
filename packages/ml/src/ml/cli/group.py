import click


@click.group()
def cli():
    """
    Main CLI group for machine learning commands.
    """
    pass

@cli.group()
def embedding():
    """
    CLI for managing embeddings.
    """
    pass

