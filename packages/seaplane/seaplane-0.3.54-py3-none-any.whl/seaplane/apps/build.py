import json
import os
from typing import Any, Dict

import toml

from ..logging import log
from ..model.errors import SeaplaneError
from .decorators import context
from .executor import RealTaskExecutor, SchemaExecutor


def validate_project() -> None:    
    if (
        not os.path.exists("src")
        and not os.path.exists("project.toml")
        and not os.path.exists("requirements.txt")
    ):
        raise SeaplaneError(
            "You aren't running Seaplane Apps in the root project directory, execute 'python3 src/main.py' in root project directory."
        )

    if not os.path.exists("src"):
        raise SeaplaneError("There isn't the 'src' source code directory.")

    if not os.path.exists("project.toml"):
        raise SeaplaneError("project.toml file missing, create a Seaplane project.toml file.")
    
    if not os.path.exists("requirements.txt"):
        raise SeaplaneError(
            "requirements.txt file missing, adds your project dependencies in requirements.txt"
        )

    project = read_project_file()
    
    if not project.get("name", None) or not project.get("main", None):
        raise SeaplaneError("project.toml not valid, missing name or main attributes.")
    


def read_project_file() -> None:
    file = open("project.toml", "r")
    data = toml.loads(file.read())
    return data


def persist_schema(schema: Dict[str, Any]) -> None:
    if not os.path.exists("build"):
        os.makedirs("build")

    file_path = os.path.join("build", "schema.json")

    with open(file_path, "w") as file:
        json.dump(schema, file, indent=2)


def build() -> Dict[str, Any]:
    validate_project()

    project_config = read_project_file()
    schema: Dict[str, Any] = {"apps": {}}

    context.set_executor(SchemaExecutor())

    for sm in context.apps:
        result = sm.func("entry_point")
        sm.return_source = result

    for sm in context.apps:
        app: Dict[str, Any] = {
            "id": sm.id,
            "entry_point": {"type": "API", "path": sm.path, "method": sm.method},
            "tasks": [],
            "io": {},
        }

        for c in sm.tasks:
            task = {"id": c.id, "name": c.name, "type": c.type, "model": c.model}

            for source in c.sources:
                if not app["io"].get(source, None):
                    app["io"][source] = [c.id]
                else:
                    app["io"][source].append(c.id)

            app["tasks"].append(task)

        app["io"]["returns"] = sm.return_source
        schema["apps"][sm.id] = app

    persist_schema(schema)

    log.debug("Apps build configuration done")

    context.set_executor(RealTaskExecutor(context.event_handler))

    return {"schema": schema, "config": project_config}
