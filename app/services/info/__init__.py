from pathlib import Path

import tomlkit


class Info:
    toml = None

    def __init__(self) -> None:
        pass

    @classmethod
    def get_pyproject_toml(cls, filename=__file__):
        d = Path(filename)
        result = None
        while d.parent != d and result is None:
            d = d.parent
            pyproject_toml_path = d / "pyproject.toml"
            if pyproject_toml_path.exists():
                break

        return pyproject_toml_path

    @classmethod
    def parse_pyproject_toml(cls, filename=__file__):
        if cls.toml is not None:
            return cls.toml

        path = cls.get_pyproject_toml(filename)
        f = open(path, "r")

        cls.toml = tomlkit.parse(f.read())
        f.close()

        return cls.toml

    @classmethod
    def get_project_info(cls, filename=__file__):
        toml = cls.parse_pyproject_toml(filename)
        if "project" in toml:
            return toml["project"]

        return None

    @classmethod
    def get_name(cls, filename=__file__) -> str:
        project = cls.get_project_info(filename)

        if "name" in project:
            return project["name"]

        return None

    @classmethod
    def get_description(cls, filename=__file__) -> str:
        project = cls.get_project_info(filename)

        if "description" in project:
            return project["description"]

        return None

    @classmethod
    def get_version(cls, filename=__file__) -> str:
        project = cls.get_project_info(filename)

        if "version" in project:
            return project["version"]

        return None
