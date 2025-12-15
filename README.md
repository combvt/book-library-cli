# Book Library Tracker
A FastAPI-based application for managing a personal book library, supporting
both SQL and JSON storage backends, Google Books API integration, and a CLI
for browsing and searching books.

## Features

## Tech stack
- Python - core language
- FastAPI - REST api framework
- SQLite / JSON - data storage
- Google Books API - external book data source
- Pydantic - request/response validation
- Requests - HTTP client
- Pytest - automated testing
## Project Structure

## Setup
install, venv, dependencies
## Environment variables

## How to run

- ### Run the CLI

- ### Run the API

## API endpoints overview

## Data model notes
#### Book 
- Core domain model representing a book fetched from Google Books
- Stored fields include title, author, publication date, page count, categories, description, ISBN and Google Books ID

#### SQL metadata
- When using SQL storage, books are assigned an auto-increment SQL ID
- A `created_at` timestamp is automatically stored when the book is added

#### Storage differences
- JSON storage persists only the core book fields without additional metadata
- SQL storage supports additional metadata and statistical queries

#### API schemas (Pydantic)
- Request and response models are defined using Pydantic
- These models control validation and API responses but are not used internally by the CLI

## Tests

## Common issues / troubleshooting
- Missing API KEY” → create `.env` and set `API_KEY`  

- If using SQLite: DB file location controlled by `DB_PATH`

- If JSON file corrupted/invalid → app treats it as empty (your JSON storage returns [] )

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for a history of feature additions and the evolution of the project over time.
## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
## Notes
- This project was built to practice backend fundamentals such as API design,
data persistence, external API integration, and testing.
- FastAPI endpoints currently support SQL storage only 

