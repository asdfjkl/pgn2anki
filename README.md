# pgn2anki
Convert (chess) PGN with opening repertoire to Anki deck 

# The Problem

You are building an opening repertoire but you just cannot memorize
the moves.

# The solution

- You create an opening repertoire as a PGN file (e.g. with 
[Jerry](https://www.github.com/asdfjkl/jerry))
- use pgn2anki to automatically create a number of board images and a textfile
- import these into [Jerry](http://http://ankisrs.net)
- memorize your lines with Anki
- PROFIT!!!

# Steps

Install `python 2.7` and `python-pil`

open command prompt. clone repo:

`git clone https://github.com/asdfjkl/pgn2anki`

`cd pgn2anki`

then 

`./pgn2anki -pgn FILENAME.pgn -depth 5 -player White`

will take the first 5 moves from root of FILENAME.pgn and
create board images whenever White is to move.

Next, copy all generated images to your Anki `collections.media` 
directory, i.e. in Linux that is 

`~/Anki/profile name/collection.media` 

For other OS'es check the [Anki manual](http://ankisrs.net/docs/manual.html#managing-files-and-your-collection)

Start Anki. Create new deck. Open deck. 

File-> Import

Navigate to pgn2anki folder

Open "import_anki.txt"

Mark "Allow HTML" in Import Dialog, set card type to "Basic".

# FINALLY

Learn, learn, leran. And remember to not just memorize the
moves, but also the strategy and concepts of the opening...

