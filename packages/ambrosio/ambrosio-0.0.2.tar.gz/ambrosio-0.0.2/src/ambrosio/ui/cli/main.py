import importlib.metadata
from importlib.metadata import version as get_version

import typer
from slugify import slugify as awslugify


def get_package_summary(package_name):
    try:
        package = importlib.metadata.metadata(package_name)
        description = package["Summary"]
        return description
    except importlib.metadata.PackageNotFoundError:
        return None


package_name = "ambrosio"
app = typer.Typer(add_completion=False, help=get_package_summary(package_name))


@app.command()
def slugify(
    text: str = typer.Argument(..., help="The string to slugify, between commas."),
):
    """
    Slugifies a string to lower case by default.
    """
    print(f"\n\t{awslugify(text, to_lower=True)}")


@app.command()
def version():
    """
    Shows the current version.
    """
    typer.echo(get_version(package_name))


if __name__ == "__main__":
    app()
