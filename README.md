# Tic-Tac-Toe with AI

A classic Tic-Tac-Toe game built with Python and Pygame, featuring an AI opponent powered by the Minimax algorithm.

**[View on GitHub](https://github.com/serjstratu/tic-tac-toe-python-ai)**

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green)
![Tests](https://img.shields.io/badge/Tests-55%20passed-brightgreen)
![Coverage](https://img.shields.io/badge/Coverage-95%25-brightgreen)

## Features

- Interactive graphical interface built with Pygame
- Play as X or O
- AI opponent powered by the Minimax algorithm
- Optimal AI decision-making
- Win and draw detection
- Automatic score tracking
- Restart functionality
- Neon-inspired visual design
- AI thinking delay for a more natural gameplay experience

## AI Algorithm

The AI uses the **Minimax algorithm** to evaluate possible game states and select the optimal move.

The algorithm:
- Explores possible future moves recursively
- Maximizes the AI's score
- Minimizes the human player's score
- Prioritizes faster wins and delays inevitable losses

The result is an AI opponent that plays optimally and cannot be beaten in a correctly played game.

## Tech Stack

- Python 3.13
- Pygame 2.6.1
- pytest
- pytest-cov

## Project Structure

```text
tic-tac-toe/
├── ai.py
├── game_logic.py
├── game_ui.py
├── main.py
├── settings.py
├── tests/
│   ├── test_ai.py
│   ├── test_game_logic.py
│   ├── test_game_ui.py
│   └── test_main.py
├── pyproject.toml
├── pytest.ini
├── uv.lock
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.13+
- pip

### Installation

Clone the repository:

```bash
git clone https://github.com/serjstratu/tic-tac-toe-python-ai.git
cd tic-tac-toe-python-ai
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
python -m pytest --cov=. --cov-branch --cov-report=term-missing
```

### Test Results

- **55 tests passed**
- **95% total code coverage**
- 526 statements analyzed
- 104 branches analyzed

Coverage includes game logic, AI decision-making, UI rendering, and application behavior.

## Building an Executable

The project can be packaged into a standalone macOS application using PyInstaller.

Install PyInstaller:

```bash
pip install pyinstaller
```

Build the application:

```bash
pyinstaller --noconfirm --clean --windowed --name "TicTacToe" main.py
```

The resulting application will be available in:

```text
dist/TicTacToe.app
```

## Architecture

The project follows a modular structure with separated responsibilities:

| Module | Responsibility |
|---|---|
| `main.py` | Application entry point and game controller |
| `game_logic.py` | Core game rules and state validation |
| `ai.py` | Minimax algorithm and AI decision-making |
| `game_ui.py` | Graphical interface and rendering |
| `settings.py` | Game configuration and visual constants |
| `tests/` | Automated tests |

## Learning Goals

This project was developed as a hands-on Python learning project, focusing on:

- Python fundamentals and OOP
- Modular application architecture
- Separation of concerns
- Recursive algorithms and Minimax
- Game state management
- Automated testing with pytest
- Code coverage and quality assurance
- Packaging Python applications

---

**Built with Python, Pygame and a bit of AI.**

# Tic-Tac-Toe with AI

[![Download](https://img.shields.io/github/v/release/serjstratu/tic-tac-toe-python-ai)](https://github.com/serjstratu/tic-tac-toe-python-ai/releases/latest)

## Download

Download the latest standalone application for your platform:

- **macOS (Apple Silicon):** [Download TicTacToe for macOS](https://github.com/serjstratu/tic-tac-toe-python-ai/releases/latest)
- **Windows (x64):** [Download TicTacToe for Windows](https://github.com/serjstratu/tic-tac-toe-python-ai/releases/latest)

Both downloads are available on the [Latest GitHub Release](https://github.com/serjstratu/tic-tac-toe-python-ai/releases/latest) page.

No Python installation required.