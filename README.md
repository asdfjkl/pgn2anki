# pgn2anki

Convert the positions of a (chess) PGN file with opening lines into an [Anki](http://ankisrs.net)
deck.

# The Problem

You are building an opening repertoire but you just cannot memorize
the moves.

# The solution

- You create an opening repertoire as a PGN file (e.g. with 
[Jerry](https://www.github.com/asdfjkl/jerry))
- use pgn2anki to automatically create a CSV file
- import this CSV into [Anki](http://http://ankisrs.net)
- memorize your lines with Anki
- PROFIT!!!

# Steps

## Preliminaries

- For Anki Desktop you need to install the [FEN chess visualizer](https://ankiweb.net/shared/info/2923601993) first.
- Ankidroid (Android) can already display FEN strings.

## Windows

- Download the binary package from the [release page](https://github.com/asdfjkl/pgn2anki/releases/)
- unzip into a directory
- open a DOS-Shell (cmd.exe) and change to the directory
- run `pgn2anki.exe --pgn FILENAME.pgn --depth 5 --player White`. 
This will take the first 5 moves from root of FILENAME.pgn and extract positions whenever White is to move.
You can omit the depth parameter if you want, then the whole PGN is used.
- a file `import_anki.csv` is created.
- import this file as a basic deck (front/back) into Anki (File -> Import).

## Linux / OS X

Ensure you have a working installation of python 2.7 and git (default on OS X).

open command prompt. clone repo:

`git clone https://github.com/asdfjkl/pgn2anki`

`cd pgn2anki`

then 

`./pgn2anki --pgn FILENAME.pgn --depth 5 --player White`

will take the first 5 moves from root of FILENAME.pgn and
extract positions whenever White is to move.

Start Anki. Create new deck. Open deck. 

File-> Import

Navigate to pgn2anki folder

Open "import_anki.csv"

# FINALLY

Learn, learn, learn. And remember to not just memorize the
moves, but also the strategy and concepts of the opening...

# CREDITS

Niklas Fikas for [python-chess](https://github.com/niklasf/python-chess)
