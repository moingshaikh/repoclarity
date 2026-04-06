import typer
import json
import shutil
import tempfile
import subprocess
from pathlib import Path
from .agent import run_agent

app = typer.Typer(help="repoclarity: Understand any repo, locally.")


def is_github_url(value: str) -> bool:
    return value.startswith("https://github.com/") or value.startswith("git@github.com:")


def clone_repo(url: str, target_dir: str) -> bool:
    typer.echo(f"Cloning {url}...")
    result = subprocess.run(
        ["git", "clone", "--depth=1", url, target_dir],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        typer.echo(f"Error cloning repo: {result.stderr.strip()}", err=True)
        return False
    return True


@app.command()
def analyze(
    repo_path: str = typer.Argument(..., help="Local path or GitHub URL to analyze"),
    query: str = typer.Argument(..., help="What you want to understand about the repo"),
    pretty: bool = typer.Option(True, "--pretty/--raw", help="Pretty print JSON output"),
    keep: bool = typer.Option(False, "--keep", help="Keep the cloned repo after analysis")
):
    """Analyze a local or remote repository using a local LLM."""
    temp_dir = None

    if is_github_url(repo_path):
        temp_dir = tempfile.mkdtemp(prefix="repoclarity_")
        success = clone_repo(repo_path, temp_dir)
        if not success:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise typer.Exit(1)
        analysis_path = temp_dir
    else:
        path = Path(repo_path)
        if not path.exists():
            typer.echo(f"Error: path '{repo_path}' does not exist.", err=True)
            raise typer.Exit(1)
        if not path.is_dir():
            typer.echo(f"Error: '{repo_path}' is not a directory.", err=True)
            raise typer.Exit(1)
        analysis_path = repo_path

    typer.echo(f"Analyzing: {repo_path}")
    typer.echo(f"Query: {query}")
    typer.echo("Running local LLM (this may take a minute on CPU)...\n")

    try:
        result = run_agent(analysis_path, query)
    finally:
        if temp_dir:
            if keep:
                typer.echo(f"\nRepo kept at: {temp_dir}")
            else:
                shutil.rmtree(temp_dir, ignore_errors=True)

    if pretty:
        typer.echo(json.dumps(result, indent=2))
    else:
        typer.echo(json.dumps(result))


if __name__ == "__main__":
    app()
