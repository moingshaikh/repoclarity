import typer
import json
from pathlib import Path
from .agent import run_agent

app = typer.Typer(help="repoclarity: Understand any repo, locally.")


@app.command()
def analyze(
    repo_path: str = typer.Argument(..., help="Path to the local repository"),
    query: str = typer.Argument(..., help="What you want to understand about the repo"),
    pretty: bool = typer.Option(True, "--pretty/--raw", help="Pretty print JSON output")
):
    """Analyze a local repository using a local LLM."""
    path = Path(repo_path)
    if not path.exists():
        typer.echo(f"Error: path '{repo_path}' does not exist.", err=True)
        raise typer.Exit(1)
    if not path.is_dir():
        typer.echo(f"Error: '{repo_path}' is not a directory.", err=True)
        raise typer.Exit(1)

    typer.echo(f"Analyzing: {repo_path}")
    typer.echo(f"Query: {query}")
    typer.echo("Running local LLM (this may take a minute on CPU)...\n")

    result = run_agent(repo_path, query)

    if pretty:
        typer.echo(json.dumps(result, indent=2))
    else:
        typer.echo(json.dumps(result))


if __name__ == "__main__":
    app()
