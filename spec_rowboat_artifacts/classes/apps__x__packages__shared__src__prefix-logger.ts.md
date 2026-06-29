# apps/x/packages/shared/src/prefix-logger.ts

**File:** apps/x/packages/shared/src/prefix-logger.ts  
**Language:** typescript

## Purpose
Provide a logging utility that prefixes log messages and supports hierarchical logging with parent-child relationships.

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
log(...args: unknown[])
```
**Intent:** Log messages to the console, optionally passing them to a parent logger if one exists.

**Inputs:**
- args: unknown[] — the messages or data to log
**Side effects:**
- Logs messages to the console with a timestamp and prefix

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
- Use of class to encapsulate logging functionality with hierarchical relationships

## Behavioral notes
- If a parent logger is present, log messages are passed up the hierarchy; otherwise, they are logged directly.
