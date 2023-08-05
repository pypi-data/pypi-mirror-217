from importlib.metadata import version as get_version

import typer
from slugify import slugify as awslugify

app = typer.Typer(add_completion=False)


@app.command()
def slugify(text: str):
    print(f"\n\t{awslugify(text, to_lower=True)}")


@app.command()
def version():
    typer.echo(get_version("ambrosio"))


if __name__ == "__main__":
    app()
