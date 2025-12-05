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
