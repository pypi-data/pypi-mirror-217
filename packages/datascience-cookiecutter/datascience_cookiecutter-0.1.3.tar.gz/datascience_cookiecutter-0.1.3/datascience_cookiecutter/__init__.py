from pathlib import Path

import click

from datascience_cookiecutter.folderbuilder import Cookiecutter, CookiecutterSettings

__all__ = ["Cookiecutter", "CookiecutterSettings"]

__version__ = "0.1.3"


@click.command()
@click.argument("projectname")
def main(projectname: str) -> None:
    # Set the default settings
    settings = CookiecutterSettings(
        name=projectname,
        path=Path("."),
        git=True,
    )

    # Create the cookiecutter instance and execute
    cookiecutter = Cookiecutter(settings)
    cookiecutter()


if __name__ == "__main__":
    main()
