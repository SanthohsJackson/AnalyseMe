# apps/x/apps/renderer/src/lib/calendar-event.ts

**File:** apps/x/apps/renderer/src/lib/calendar-event.ts  
**Language:** typescript

## Purpose
Extract video conference links from text or Google Calendar event data.

## Interfaces
### `findMeetingUrl` (function)
```
findMeetingUrl(value: unknown): string | undefined
```
**Intent:** Identify and return a video conference URL from a given string, supporting specific providers.

**Inputs:**
- value: unknown — the input to search for a meeting URL
**Outputs:**
- string | undefined — the first matching meeting URL or undefined if none found

### `extractConferenceLink` (function)
```
extractConferenceLink(raw: Record<string, unknown>): string | undefined
```
**Intent:** Extract a video conference link from Google Calendar event data, checking multiple fields and falling back to scanning text.

**Inputs:**
- raw: Record<string, unknown> — the Google Calendar event data to extract a conference link from
**Outputs:**
- string | undefined — the extracted conference link or undefined if none found

## Behavioral notes
- The regular expression captures URLs from specific video conferencing providers.
- HTML entities in URLs are decoded by replacing '&amp;' with '&'.
