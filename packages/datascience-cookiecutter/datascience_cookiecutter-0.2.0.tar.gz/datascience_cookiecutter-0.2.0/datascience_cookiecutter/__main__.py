import click
from pathlib import Path
from datascience_cookiecutter import Cookiecutter, CookiecutterSettings

@click.command()
@click.argument("projectname")
def create_project(projectname: str) -> None:
    # Set the default settings
    if projectname is None:
        projectname = "my_project"
    settings = CookiecutterSettings(
        name=projectname,
        path=Path("."),
        git=True,
    )

    # Create the cookiecutter instance and execute
    cookiecutter = Cookiecutter(settings)
    cookiecutter()