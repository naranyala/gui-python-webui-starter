# Backend Core Logic

## Dependency Injection (DI)
To avoid "prop drilling" and tight coupling, we use a custom `DIContainer`.
- **Singletons**: Services are registered as singletons, ensuring only one instance of `Database` or `DocumentService` exists.
- **Resolution**: `container.resolve(ServiceClass)` handles the instantiation and dependency linking.

## Service Layer Pattern
All business logic is encapsulated in classes extending `BaseService`.
- **`on_initialize()`**: A lifecycle hook called during startup to setup DB connections or seed data.
- **Separation**: Services never handle HTTP/Bridge logic; they only return data or raise exceptions. This makes them 100% testable without a GUI.

## SQLite Persistence
The app uses SQLite with **WAL (Write-Ahead Logging)**.
- **Concurrent Access**: WAL allows one writer and multiple readers simultaneously, which is critical since the FastAPI thread and the WebUI main thread may both access the database.
