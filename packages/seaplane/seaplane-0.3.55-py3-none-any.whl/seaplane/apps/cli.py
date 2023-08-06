"""
command line interface
"""
from argparse import ArgumentParser
from importlib.metadata import version
import os

from cookiecutter.main import cookiecutter

from .. import __version__
from .build import read_project_file, validate_project
from .deploy import deploy


def get_project():
    validate_project()
    return read_project_file()


def cli_deploy():
    parser = ArgumentParser(prog="deploy", description="Deploy Seaplane Apps command line")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--task",
        type=str,
        help="seaplane deploy which can includes a TASK_ID as param, to deploy an individual TASK",
    )
    args = parser.parse_args()

    task = ""
    if args.task:
        task = args.task

    project = get_project()
    project_name = project["tool"]["poetry"]["name"]
    main = project["tool"]["seaplane"]["main"]

    os.system(f"poetry run python3 {project_name}/{main} deploy {task}")

    exit(0)


def cli_build():
    project = get_project()
    project_name = project["tool"]["poetry"]["name"]
    main = project["tool"]["seaplane"]["main"]

    os.system(f"poetry run python3 {project_name}/{main} build")

    exit(0)


def init():
    parser = ArgumentParser(prog="init", description="Init Seaplane Apps project")
    parser.add_argument("app", help="Seaplane Apps name")
    args = parser.parse_args()

    cookiecutter_template = "https://github.com/seaplane-io/seaplane-app-python-template.git"
    project_directory = "."

    extra_context = {"project_slug": args.app, "seaplane_version": version("seaplane")}

    cookiecutter(
        cookiecutter_template,
        output_dir=project_directory,
        no_input=True,  # Disable any interactive prompts
        extra_context=extra_context,
    )

    print(f"🛩️ {args.app} project generated successfully!")
    exit(0)
