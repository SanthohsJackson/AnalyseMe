# apps/experimental/tools_webhook/function_map.py

**File:** apps/experimental/tools_webhook/function_map.py  
**Language:** python

## Purpose
Defines callable functions and a mapping from string names to these functions.

## Interfaces
### `greet` (function)
```
greet(name: str, message: str)
```
**Intent:** Generate a personalized greeting message.

**Inputs:**
- name: str — the name of the person to greet
- message: str — the greeting message
**Outputs:**
- str — a formatted greeting message

### `add` (function)
```
add(a: int, b: int)
```
**Intent:** Calculate the sum of two integers.

**Inputs:**
- a: int — the first integer to add
- b: int — the second integer to add
**Outputs:**
- int — the sum of the two integers

### `get_account_balance` (function)
```
get_account_balance(user_id: str)
```
**Intent:** Return a mock account balance for a given user ID.

**Inputs:**
- user_id: str — the identifier of the user
**Outputs:**
- str — a mock account balance message for the user
