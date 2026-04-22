# App Settings Implementation

The Settings module implements a dynamic Key-Value store.

## Database Schema
A simple table `settings` with two columns: `key` (Primary Key) and `value` (Text/JSON).

## Serialization
Since SQLite only stores text, the `SettingsService` automatically:
- **Saves**: `json.dumps(value)` before inserting into the DB.
- **Loads**: `json.loads(value)` when reading, allowing the store to handle strings, numbers, and nested dictionaries/lists.

## Usage
Settings can be accessed globally by the backend to modify app behavior (e.g., changing the logging level or API port) without requiring a code change.
