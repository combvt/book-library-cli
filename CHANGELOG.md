# Changelog

## v1 - initial release (2 Dec 2025)
- Basic CLI for adding, listing, removing books
- Data stored in a local JSON file

## v2 - add SQL storage backend (5 Dec 2025)

### Added
- Full SQL storage integration alongside the existing JSON storage
- CLI option to choose between SQL or JSON storage types

### Changed
- Improved CLI user experience for navigating and managing the library
- Restructured project into a src/ directory

### Fixed
- Resolved several errors (TypeError, IndexError, ValueError) that could cause the program to crash

## v3 - implement FastAPI and basic tests (14 Dec 2025)

### Added
- FastAPI application and routes (SQL storage only)
- CRUD endpoints to add, update, delete, fetch books from library
- Utility endpoints like /random and /stats to fetch random book and view library stats
- Basic tests for SQL storage, mocked Google Books API, and FastAPI endpoints
- Project is now structured as a package using the src/ layout
- Option to view detailed info in library (SQL and JSON storage)
- Option to let user choose between viewing and searching books whenever launching the library (CLI only)

### Changed
- Slightly refactored CLI logic
- Formatted the entire codebase with Black

