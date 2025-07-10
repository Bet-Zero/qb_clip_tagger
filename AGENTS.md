# Agent Contribution Guidelines

This repository manages an NBA clip tagging tool built with Python, Flask, and an Electron popup interface.

## Setup

- Install Python dependencies with `pip install -r requirements.txt`.
- Install Electron dependencies with `npm install` inside the `electron_app/` directory if working on the popup.

## Code Style

- Use four spaces for indentation in Python files.
- Keep lines reasonably short (around 100 characters or less).
- End files with a newline.
- Use descriptive names and keep the code readable.

## Testing

- Run `pytest` from the repository root after making changes.
- If tests fail or cannot be executed due to environment issues, mention this in the PR description.

## Pull Requests

- Summaries should describe the change clearly and reference any affected components.
- The Testing section of the PR must state whether tests passed or include the provided disclaimer if they could not be run.
