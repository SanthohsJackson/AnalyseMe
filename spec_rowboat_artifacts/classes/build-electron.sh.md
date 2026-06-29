# build-electron.sh

**File:** build-electron.sh  
**Language:** bash

## Purpose
Builds the Next.js app and server for the rowboatx project.

## Flagged idioms
- Using subshells with (cd ... && ...) to change directories and execute commands in sequence.

## Behavioral notes
- The script stops execution on the first error due to 'set -e'.
- The script assumes npm is installed and available in the PATH.
