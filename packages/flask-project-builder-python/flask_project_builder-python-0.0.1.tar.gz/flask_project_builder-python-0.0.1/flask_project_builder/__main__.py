import os
import sys

def get_project_name():
    if len(sys.argv) > 1:
        project_name = sys.argv[1]
    else:
        project_name = input("Enter project name: ")
    
    if not project_name:
        print("Project name cannot be empty")
        sys.exit(1)

    if ' ' in project_name:
        print("Project name cannot have spaces")
        sys.exit(1)

    project_name = project_name.lower()
    project_name = project_name.replace("_", "-")

    return project_name

def create_project_folder(project_name: str):    
    # criar a pasta do projeto
    os.mkdir(project_name)

    # entrar na pasta do projeto
    os.chdir(project_name)

    # criar o venv
    os.system("python -m venv venv")

    # criar o .env
    create_env_file(project_name)

    # criar o README.md
    create_readme_file(project_name)

    # criar o .gitignore
    create_gitignore_file()

    # criar o setings.py
    create_settings_file()

    # criar o wsig.py
    create_wsgi_file(project_name)

def create_env_file(project_name: str):
    with open(".env", "w") as env_file:
        env_file.write(f"Prencha o arquivo .env com as variáveis de ambiente do projeto {project_name}")

def create_readme_file(project_name: str):
    with open("README.md", "w") as readme_file:
        readme_file.write(f"# {project_name}\n")

def create_gitignore_file():
    with open(".gitignore", "w") as gitignore_file:
        gitignore_file.write("venv\n__pycache__\n")

def create_settings_file():
    with open("settings.toml", "w") as settings_file:
        settings_file.write("[default]\nEXTENSIONS = []\n")

def create_wsgi_file(project_name: str):
    with open("wsgi.py", "w") as wsgi_file:
        wsgi_file.write(f'from {project_name.replace("-", "_")} import create_app\n\napp = create_app()\n\nif __name__ == "__main__":\n\tapp.run()\n')

def create_app_folder(project_name: str):
    app_folder_name = project_name.replace("-", "_")

    os.mkdir(app_folder_name)
    os.chdir(app_folder_name)

    create_app_file(app_folder_name)
    create_init_file()

    create_blueprint_folder()
    crete_extensions_folder()
    create_tests_folder()
    os.mkdir("static")
    os.mkdir("templates")
    
def create_app_file(app_folder_name: str):
    with open("app.py", "w") as app_file:
        app_file.write(f"from flask import Flask\n\nfrom {app_folder_name}.extensions import configuration\n\n\ndef create_app():\n\tapp = Flask(__name__)\n\tconfiguration.init_app(app)\n\treturn app\n")

def create_init_file():
    with open("__init__.py", "w") as init_file:
        init_file.write("from .app import create_app\n")

def create_blueprint_folder():
    os.mkdir("blueprints")
    with open("blueprints/__init__.py", "w") as init_file:
        init_file.write("\n")

def crete_extensions_folder():
    os.mkdir("extensions")
    with open("extensions/__init__.py", "w") as init_file:
        init_file.write("\n")

    with open("extensions/configuration.py", "w") as configuration_file:
        configuration_file.write("from importlib import import_module\n\nfrom dynaconf import FlaskDynaconf\nfrom flask import Flask\n\n\ndef load_extensions(app: Flask):\n\tfor extension in app.config.get('EXTENSIONS'):\n\t\tmodule = import_module(extension)\n\t\tmodule.init_app(app)\n\n\ndef init_app(app: Flask):\n\tFlaskDynaconf(app)\n\tload_extensions(app)\n\treturn app\n")

def create_tests_folder():
    os.mkdir("tests")
    with open("tests/__init__.py", "w") as init_file:
        init_file.write("\n")

def install_libs():
    os.chdir("..")
    dependencies = [
        "flask",
        "dynaconf",
        "python-dotenv",
    ]
    os.system(f"venv/bin/pip install {' '.join(dependencies)}")
    os.system(f"venv/bin/pip freeze > requirements.txt")

if __name__ == "__main__":
    project_name = get_project_name()
    create_project_folder(project_name)
    create_app_folder(project_name)
    install_libs()