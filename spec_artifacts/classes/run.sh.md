# run.sh

**File:** run.sh  
**Language:** bash

## Purpose
Launch the Analyse Me UI using a virtual environment specific to the project.

## External dependencies
- venv
- pip

## Flagged idioms
- set -euo pipefail: ensures the script exits on error, unset variables, or failed pipes
- $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd): determines the script's directory

## Behavioral notes
- Creates a virtual environment if not present and installs dependencies from requirements.txt.
- Executes main.py with arguments passed to the script or defaults to 'menu'.
