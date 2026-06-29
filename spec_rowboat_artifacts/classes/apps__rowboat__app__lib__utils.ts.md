# apps/rowboat/app/lib/utils.ts

**File:** apps/rowboat/app/lib/utils.ts  
**Language:** typescript

## Purpose
Provide a logging utility that prefixes log messages and supports hierarchical logging.

## Interfaces
### `PrefixLogger` (class)
```
PrefixLogger(prefix: string, parent: PrefixLogger | null = null)
```
**Intent:** Initialize a logger with a specific prefix and an optional parent logger.

**Inputs:**
- prefix: string — the prefix to prepend to log messages
- parent: PrefixLogger | null — an optional parent logger for hierarchical logging

### `log` (method)
```
log(...args: any[])
```
**Intent:** Log messages to the console, optionally passing them to a parent logger if one exists.

**Inputs:**
- args: any[] — the messages or objects to log
**Side effects:**
- Outputs log messages to the console with a timestamp and prefix

### `child` (method)
```
child(childPrefix: string) -> PrefixLogger
```
**Intent:** Create a new logger instance that is a child of the current logger, inheriting its hierarchy.

**Inputs:**
- childPrefix: string — the prefix for the child logger
**Outputs:**
- PrefixLogger — a new logger instance with the specified child prefix

## Flagged idioms
- Use of class to encapsulate logging behavior with prefixing and hierarchy support

## Behavioral notes
- If a parent logger is present, log messages are passed up the hierarchy.
