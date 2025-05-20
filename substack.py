import typer
from bs4 import BeautifulSoup
from pathlib import Path

app = typer.Typer()

@app.command()
def latest(
    site_blog_dir: str = typer.Option("site/blog", help="Directory with blog HTML files"),
    output: str = typer.Option(None, help="Output file (default: stdout)")
):
    """Extract the latest blog article's content."""
    blog_dir = Path(site_blog_dir)
    html_files = sorted(blog_dir.glob("*.html"), reverse=True)
    if not html_files:
        typer.echo("No blog articles found.", err=True)
        raise typer.Exit(1)
    latest_file = html_files[0]
    with open(latest_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    article_content = soup.find("div", class_="md-content")
    if not article_content:
        typer.echo("Main content not found in the latest article.", err=True)
        raise typer.Exit(1)
    content = article_content.prettify()
    if output:
        Path(output).write_text(content, encoding="utf-8")
        typer.echo(f"Content written to {output}")
    else:
        typer.echo(content)

if __name__ == "__main__":
    app()