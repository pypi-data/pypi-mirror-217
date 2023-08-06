import typer

app = typer.Typer()

@app.callback()
def callback():
    """Holos platform manager"""
    ...

@app.command()
def version():
    """Print version to standard output and exit."""
    typer.echo("0.1.0")
