# System Monitor Technical Guide

The System Monitor demonstrates real-time OS integration.

## Implementation Details
- **Backend**: Uses the `psutil` library to gather hardware metrics.
- **Service**: `SystemService` provides a `get_stats()` method that aggregates CPU, RAM, and Disk usage into a single JSON object.
- **Polling**: The frontend uses a `setInterval` (every 2 seconds) to poll the `/api/system` endpoint.

## Data Flow
`psutil` $\rightarrow$ `SystemService` $\rightarrow$ `ApiRoutes` $\rightarrow$ `ApiClient` $\rightarrow$ `SystemPage.jsx` $\rightarrow$ React State $\rightarrow$ CSS Progress Bars.
