
Author: Ronniekev

# Atomic Chess Game

This is a Python implementation of Atomic Chess, a variant of traditional chess with explosive captures. It allows two players to play in the console, supports piece movement validation, and ends the game when a king is captured via direct attack or explosion.

## Game rules
In Atomic Chess, whenever a piece is captured, an "explosion" occurs at the 8 squares immediately surrounding the captured piece in all the directions. This explosion kills all of the pieces in its range except for pawns. Different from regular chess, where only the captured piece is taken off the board, in Atomic Chess, every capture is suicidal. Even the capturing piece is affected by the explosion and must be taken off the board. As a result, a pawn can only be removed from the board when directly involved in a capture. If that is the case, both capturing and captured pawns must be removed from the board. Because every capture causes an explosion that affects not only the victim but also the capturing piece itself, the king is not allowed to make captures. Also, a player cannot blow up both kings at the same time. In other words, the move that would kill both kings in one step is not allowed. Blowing up a king has the same effect as capturing it, which will end the game. (https://www.chess.com/terms/atomic-chess#captures-and-explosions)

## 🎯 Features

- Fully functioning 8x8 chess board with labeled edges.
- Turn-based move handling (white and black).
- Valid move checking for all major pieces.
- Atomic capture logic (explosion on capture).
- Clear winner detection logic.
- Pure Python libraries.

## 💡 Why this project?

This was one of my first projects and an exploration into the fundamentals of game logic, conditionals, and class-based design in Python. I intentionally avoided external modules to focus on problem-solving and algorithmic thinking.

## 🚀 How to Run

```bash
python atomic_chess.py

🧪 Testing
To ensure the game behaves as expected, there's a dedicated unittest test suite in test_atomic_chess.py.

The tests cover typical opening sequences, longer move chains, invalid input handling, and edge cases like illegal captures or king explosions. There's even a test that confirms the game ends when a king is caught in an explosion. Each test uses Python’s built-in unittest library.

To run the tests:

```bash
python test_atomic_chess.py


