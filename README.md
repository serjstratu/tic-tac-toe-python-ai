# Tic-Tac-Toe

A classic Tic-Tac-Toe game built with Python and Pygame.

The project started as a way to practice Python fundamentals, game development, code organization, and automated testing.

## Features

- Interactive Tic-Tac-Toe game with a graphical interface
- Player turns (X and O)
- AI opponent
- Win and draw detection
- Game restart functionality
- Separated game logic and UI
- Automated unit tests with pytest

## Tech Stack

- **Python 3.13**
- **Pygame** — game interface and rendering
- **pytest** — automated testing
- **pytest-cov** — test coverage reporting

## Project Structure

```text
tic-tac-toe/
├── ai.py
├── game_logic.py
├── game_ui.py
├── main.py
├── settings.py
├── tests/
│   └── test_game_logic.py
├── pytest.ini
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.13+
- pip

### Installation

Clone the repository:

```bash
git clone <repository-url>
cd tic-tac-toe
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install pygame pytest pytest-cov
```

### Run the Game

```bash
python main.py
```

## Running Tests

Run all tests:

```bash
python -m pytest -v
```

Run tests with coverage:

```bash
python -m pytest --cov=game_logic --cov-report=term-missing
```

## Architecture

The project separates responsibilities into independent modules:

- **main.py** — application entry point and game loop
- **game_logic.py** — core game rules, winner detection, draw detection, and player switching
- **game_ui.py** — rendering and user interface
- **ai.py** — AI opponent logic
- **settings.py** — game configuration, dimensions, colors, and fonts
- **tests/** — automated tests for game logic

## Learning Goals

This project explores:

- Python functions, modules, and imports
- Separation of concerns
- Game state management
- Basic AI decision-making
- Unit testing with pytest
- Test coverage and code quality

---

*Built as a hands-on Python learning project.*