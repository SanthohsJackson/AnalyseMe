# run.sh

**File:** run.sh  
**Language:** bash

## Purpose
Launch the Analyse Me UI using a virtual environment specific to the project.

## External dependencies
- venv
- pip

## Flagged idioms
- set -euo pipefail: ensures the script exits on error, unset variables, or pipe failures
- $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd): determines the script's directory

## Behavioral notes
- The script creates a virtual environment if it doesn't exist and installs dependencies from requirements.txt.
- Executes main.py with arguments passed to the script, defaulting to 'menu' if none are provided.
