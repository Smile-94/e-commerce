# Poe the Poet: A Task Runner for Poetry

# Table of Contents

- [1 Poe Th Poet](#1-poe-the-poet)
- [2 Why Use Poe the Poet](#2-why-use-poe-the-poet)
- [3 Key Features](#3-key-features)
- [4 Installation](#4-installation)
- [5 Poe the Poet in a Django Project](#5-poe-the-poet-in-a-django-project)
- [6 How to Use These Tasks](#6-how-to-use-these-tasks)

## 1 Poe The Poetss

Poe the Poet is a task runner designed to work seamlessly with Poetry, a popular dependency management and packaging tool for Python. Poe allows you to define and run tasks directly from your Poetry project, making it easier to automate repetitive tasks like testing, linting, formatting, and building.

## 2 Why Use Poe the Poet?

**Integration with Poetry:** Poe is built specifically for Poetry projects, so it integrates naturally with your `pyproject.toml` file. You don't need to install additional tools like Make or Invoke to manage tasks.

**Simple Configuration:** Tasks are defined in the `pyproject.toml` file, keeping everything in one place. Tasks can be shell commands, Python scripts, or references to external scripts.

**Cross-Platform:** Poe works on all major operating systems (Windows, macOS, Linux).

**Lightweight:** Poe is a small, focused tool that doesn't add unnecessary complexity to your project.

**Extensible:** You can define complex workflows with task dependencies, environment variables, and more.

## 3 Key Features

- Task Definitions: Define tasks in pyproject.toml under [tool.poe.tasks].

- Shell Commands: Run shell commands directly.

- Python Scripts: Execute Python code inline.

- Task Dependencies: Specify dependencies between tasks.

- Environment Variables: Set environment variables for tasks.

- Default Task: Define a default task to run when no task is specified.

- CI/CD Integration: Easily integrate tasks into CI/CD pipelines.

## 4 Installation

Add Poe the Poet to your Poetry project:

```zsh
poetry add --dev poethepoet
```

The poe executable will then be available anywhere in your system.

**Install Poe the Poet as a poetry plugin**

```zsh
poetry self add 'poethepoet[poetry_plugin]'
```

It’ll then be available as the poetry poe command anywhere in your system.

See the poetry plugin docs for more details about this option.

**Enable tab completion for your shell**

```zsh
# oh-my-zsh
mkdir -p ~/.oh-my-zsh/completions
poe _zsh_completion > ~/.oh-my-zsh/completions/_poe

# without oh-my-zsh
mkdir -p ~/.zfunc/
poe _zsh_completion > ~/.zfunc/_poe
```

## 5 Poe the Poet in a Django Project

Poe the Poet is a great tool for automating repetitive tasks in a Django project. Below is a guide on how to use Poe to manage common Django tasks like running the development server, creating migrations, applying migrations, and creating new apps or projects.

Here’s an example `pyproject.toml` configuration for a Django project:

```toml
[tool.poe.tasks]

# Run the Django development server
dev = "python manage.py runserver 0.0.0.0:8000"

# Create new migrations
migrations = "python manage.py makemigrations"

# Apply migrations
migrate = "python manage.py migrate"

# Create a new Django app
app = "python manage.py startapp"

# Create a new Django project
project = "django-admin startproject"

# Run a shell command
clean = "rm -rf .pytest_cache __pycache__"

collectstatic = "python manage.py collectstatic --noinput"
```

## 6 How to Use These Tasks

To start the Django development server, use the dev task:

```zsh
poetry run poe dev
```

This will start the server on `0.0.0.0:8000`, making it accessible from other devices on the same network.

To create new migrations for your Django models, use the migrations task:

```zsh
poetry run poe migrations
```

This runs `python manage.py makemigrations`, which generates migration files based on changes in your models.

To apply migrations to your database, use the migrate task:

```zsh
poetry run poe migrate
```

This runs `python manage.py migrate`, which applies all unapplied migrations to the database.

To create a new Django app, use the app task followed by the app name:

```zsh
poetry run poe app my_new_app
```

This runs `python manage.py startapp my_new_app`, creating a new app with the specified name.
