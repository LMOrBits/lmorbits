import click

@click.group()
def pipeline():
    """ml commands."""
    pass

@pipeline.command()
@click.option('--dev', is_flag=True, help='Run in development environment')
@click.option('--stage', is_flag=True, help='Run in staging environment')
@click.option('--prod', is_flag=True, help='Run in production environment')
def pipe(dev_flag, stage_flag, prod_flag):
    """Pipelines CLI with environment selection."""
    if sum([dev, stage, prod]) > 1:
        raise click.UsageError("Please specify only one environment (--dev, --stage, or --prod)")
    if not any([dev, stage, prod]):
        raise click.UsageError("Please specify an environment (--dev, --stage, or --prod)")
    if dev_flag:
         dev()
    elif stage_flag:
        stage()
    elif prod_flag:
        prod()

@pipeline.group()
def dev():
    """Development environment commands."""
    pass

@pipeline.group()
def stage():
    """Staging environment commands."""
    pass

@pipeline.group()
def prod():
    """Production environment commands."""
    pass
   