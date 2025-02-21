# Git Hooks and Pre-Commit Framework Documentation

Git hooks are scripts that run automatically at specific points in the Git workflow (e.g., before a commit, after a commit, before a push, etc.). They are used to enforce code quality, run tests, validate commit messages, and more. The `pre-commit` framework simplifies the management of these hooks, especially for pre-commit checks.

This guide explains how to set up and use Git hooks with the `pre-commit` framework, including custom scripts for commit message validation, pre-commit checks, and pre-push actions.

# Table of Contents

- [1. What Are Git Hooks?](#1-what-are-git-hooks)
- [2. Setting Up the Pre-Commit Framework](#2-setting-up-the-pre-commit-framework)
  - [2.1 Install Pre-Commit Framework](#21-install-pre-commit-framework)
  - [2.2 Create .pre-commit-config.yaml](#22-create-pre-commit-configyaml)
  - [2.3 Install Git Hooks](#23-install-git-hooks)
- [3 Custom Git Hooks ](#3-custom-git-hooks)
  - [3.1 Shared Hooks Directory ](#31-shared-hooks-directory)
  - [3.2 Commit Message Validation](#32-commit-message-validation)
  - [3.3 Pre-Commit Hook](#33-pre-commit-hook)
  - [3.4 Pre-Push Hook](#34-pre-push-hook)
  - [3.5 Git Hooks Configuration](#35-git-hooks-configuration)
  - [3.6 Running Hooks Manually](#36-running-hooks-manually)
  - [3.7 Updating Hooks](#37-updating-hooks)

## 1 What Are Git Hooks?

Git hooks are scripts that Git executes before or after events such as:

- **Pre-commit: Runs before a commit is created.**

- **Commit-msg: Validates the commit message.**

- **Pre-push: Runs before pushing to a remote repository.**

These hooks are stored in the .git/hooks directory of your repository. By default, Git provides sample hooks, but you can replace them with your own scripts.

## 2 Setting Up the Pre-Commit Framework

The `pre-commit` framework simplifies the management of pre-commit hooks. It allows you to define hooks in a configuration file (`.pre-commit-config.yaml`) and automatically installs them in your repository.

### 2.1 Install Pre-Commit Framework

Install the pre-commit package using Poetry:

```zsh
poetry add pre-commit
```

### 2.2 Create .pre-commit-config.yaml

Create a .pre-commit-config.yaml file in the root of your repository. Here’s an example configuration:

```yaml
default_language_version:
  python: python3.12
fail_fast: true
exclude: "^docs/|/migrations/|.conf.py|migrations|.git|.tox"
default_stages: [pre-commit]

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-ast
      - id: check-json
      - id: check-toml
      - id: check-xml
      - id: check-yaml
      - id: debug-statements
      - id: check-builtin-literals
      - id: check-case-conflict
      - id: check-merge-conflict
      - id: check-docstring-first
      - id: check-added-large-files
      - id: detect-aws-credentials
        args: ["--allow-missing-credentials"]
      - id: pretty-format-json
        args: ["--autofix"]
      - id: requirements-txt-fixer

  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.7.1
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/asottile/pyupgrade
    rev: v3.19.0
    hooks:
      - id: pyupgrade
        args: [--py312-plus]
        exclude: hooks/

  - repo: https://github.com/adamchainz/django-upgrade
    rev: "1.22.1"
    hooks:
      - id: django-upgrade
        args: ["--target-version", "5.1"]
```

### 2.3 Install Git Hooks

Install the hooks into your Git repository:

```zsh
poetry run pre-commit install
```

This sets up the hooks in .git/hooks. Now, every time you run git commit, the hooks defined in .pre-commit-config.yaml will run.

## 3 Custom Git Hooks

You can also create custom Git hooks for specific workflows, such as validating commit messages or running pre-push checks.

### 3.1 Shared Hooks Directory

Instead of using `.git/hooks`, you can store hooks in a shared directory (e.g., `.githooks`) and configure Git to use it:

```zsh
mkdir -p .githooks
git config core.hooksPath .githooks
```

### 3.2 Commit Message Validation

Create a `commit-msg` hook to enforce conventional commit messages. Save this script as `.githooks/commit-msg.sh` and configure:

```sh
#!/usr/bin/env bash
#
# @author : Mak Sophea
# @version : 1.0
#
# Create a regex for a conventional commit.
commit_types="(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test|wip|update|remove)"
convetional_commit_regex="^${commit_types}(\([a-z \-]+\))?!?: .+$"

# Get the commit message (the parameter we're given is just the path to the
# temporary file which holds the message).
commit_message=$(cat "$1")

# Check the message, if we match, all good baby.
if [[ "$commit_message" =~ $convetional_commit_regex ]]; then
   echo -e "\e[32mCommit message meets Conventional Commit standards...\e[0m"
   exit 0
fi

# Uh-oh, this is not a conventional commit, show an example and link to the spec.
echo -e "\e[31mThe commit message does not meet the Conventional Commit standard\e[0m"
echo "An example of a valid message is: "
echo "  feat(login): add the 'remember me' button"
echo "More details at: https://www.conventionalcommits.org/en/v1.0.0/#summary"
echo "***********************************************************************"
echo "Here are the  list of message type : ${commit_types}"
echo "  <type>: <subject> max 50char ex :- fix: invalid request for login api"
echo "  <type(<scope>):> <subject> (Max 50 char) - <scope> is option ex: - fix(user): email address is empty on profile api"
echo "***********************************************************************"

exit 1
```

Make the script executable:

```zsh
chmod +x .githooks/commit-msg.sh
```

### 3.3 Pre-Commit Hook

Create a `pre-commit` hook to run additional checks. Save this script as `.githooks/pre-commit.sh`:

```sh
#!/usr/bin/env bash

echo "pre-commit template by https://github.com/Smile-94"
set -eux ;\
    poetry run pre-commit run -a ;\
    poetry run ruff check ;
```

Make the script executable:

```zsh
chmod +x .githooks/pre-commit.sh
```

### 3.4 Pre-Push Hook

Create a `pre-push` hook to run checks before pushing. Save this script as `.githooks/pre-push.sh`:

```sh
#!/bin/sh

# @author : Mak Sophea
# @version : 1.0

# Confirm Docker/Podman availability
if ! command -v "docker" >/dev/null 2>&1 && ! command -v "podman" >/dev/null 2>&1; then
  echo "Error: Neither Docker nor Podman found. Please install one of them."
  exit 1
fi

# Get Container Runner
RUNNER=$(command -v podman || command -v docker)  # Use whichever is available

# Carebox
CONTAINER_IMAGE="carebox"
CONTAINER_NAME="carebox"
CONTAINER_PORT="8000"
HOST_PORT="8000"

$RUNNER build \
    -f "docker/Dockerfile.wolfi" \
    -t "carebox" .

CONTAINER_ID=$($RUNNER run \
	--rm \
	--detach \
	--name $CONTAINER_NAME \
	--publish 8050:8001 \
	--publish $HOST_PORT:$CONTAINER_PORT \
	--volume carebox_data:/home/nonroot/project/ \
	$CONTAINER_IMAGE)

# Check if the container started successfully
if [[ $? -eq 0 ]]; then
  # Print the success message with the container ID
  echo "Container $CONTAINER_NAME started successfully with ID: $CONTAINER_ID"
  $RUNNER kill $CONTAINER_NAME
else
  echo "Error starting container $CONTAINER_NAME!"
  exit 1
fi
```

Make the script executable:

```zsh
chmod +x .githooks/pre-push.sh
```

### 3.5 Git Hooks Configuration

Create a `git-hooks-config` to configure the git hooks. Save this script as `.githooks/git-hooks-config.sh`:

```sh
#!/bin/sh
# This script will config git hook path into specific folder in your project. This script will invoked by maven build.
# @version : 1.0#
#
echo "config git hooksPath to .githooks folder for commit-msg and pre-push"
git config core.hooksPath .githooks
```

Make the script executable:

```zsh
chmod +x .githooks/git-hooks-config.sh
```

### 3.6 Running Hooks Manually

You can manually run all hooks on your repository:

```zsh
poetry run pre-commit run --all-files
```

### 3.7 Updating Hooks

o update the hooks to their latest versions, run:

```zsh
poetry run pre-commit autoupdate
```
