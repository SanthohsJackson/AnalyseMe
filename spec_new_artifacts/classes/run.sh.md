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
- $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd): determines the directory of the script

## Behavioral notes
- The script checks for the existence of a virtual environment and creates one if it doesn't exist.
- The script installs dependencies from requirements.txt if the virtual environment is newly created.
- The script defaults to launching the 'menu' if no arguments are provided.
