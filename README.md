```markdown
# War Card Game

A 4-player visual simulation of the classic War card game, built with Python, tkinter, and AI assistance.

## Table of Contents
1. [About The Project](#about-the-project)
2. [Built With](#built-with)
3. [Getting Started](#getting-started)
4. [Usage](#usage)
5. [Roadmap](#roadmap)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)
9. [Acknowledgments](#acknowledgments)

## About The Project

This is a fully playable visual simulation of War for 4 players. Cards are dealt evenly from a shuffled deck and each round the highest card wins all played cards. Ties trigger a WAR — 3 face-down cards are placed and a 4th face-up card determines the winner. The game ends when one player holds all 52 cards, or after 1,000 rounds (most cards wins).

Features:
- Step through rounds manually or use Auto Play with adjustable speed
- Live battle log tracking every round, war, and reshuffle
- Automatic reshuffle if a player runs out of cards
- Color-coded player panels with card count tracking

> Note: tkinter is built into Python — no additional installs required beyond the base language.

([back to top](#war-card-game))

## Built With

- [Python](https://www.python.org/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)

([back to top](#war-card-game))

## Getting Started

### Prerequisites

Just Python — no pip installs needed. tkinter comes bundled with standard Python installations.

```bash
python --version  # confirm Python is installed
```

### Installation

1. Clone the repo
```bash
git clone https://github.com/Sunjae4U/WarCards.git
```

2. Navigate to the project directory
```bash
cd WarCards
```

3. Run the game
```bash
python war.py
```

([back to top](#war-card-game))

## Usage

Once launched, use the three buttons at the bottom of the window:

- Next Round — plays one round at a time
- Auto Play — continuously plays rounds at the selected speed (adjustable via the speed slider)
- New Game — resets the deck and starts a fresh game

The battle log tracks every round result including wars and reshuffles. The winning player's panel is highlighted in gold when the game ends.

([back to top](#war-card-game))

## Roadmap

- [ ] Add 2-player and 3-player modes
- [ ] Track win/loss statistics across multiple games
- [ ] Add sound effects
- [ ] Export battle log to a text file

See the [open issues](https://github.com/Sunjae4U/WarCards/issues) for a full list of proposed features and known issues.

([back to top](#war-card-game))

## Contributing

Contributions are welcome and greatly appreciated!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

([back to top](#war-card-game))

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

([back to top](#war-card-game))

## Contact

Sunjae4U — [GitHub](https://github.com/Sunjae4U)

Project Link: [https://github.com/Sunjae4U/WarCards](https://github.com/Sunjae4U/WarCards)

([back to top](#war-card-game))

## Acknowledgments

- [tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Choose an Open Source License](https://choosealicense.com)

([back to top](#war-card-game))
```
