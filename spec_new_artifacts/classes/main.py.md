# main.py

**File:** main.py  
**Language:** python

## Purpose
Serve as the entry point for executing the CLI application.

## Internal dependencies
- cli/main.py

## External dependencies
- sys
- pathlib

## Flagged idioms
- sys.path modification: ensures the project root is on sys.path for imports

## Behavioral notes
- The script modifies sys.path to include the project root, allowing imports from 'graph' and 'cli'.
