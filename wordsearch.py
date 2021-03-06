#!/usr/bin/python
# Usage: script -f <grid_file> -l <min_string_length>
"""
Searches the grid for all words of length min_string_length or longer.
Output coordinates use 0,0 at the top left.

The grid file format is:
ABCDEFG
HIGHEED
...
The grid is assumed to be rectangular.
Any non-alphanumeric characters will be stripped. (So A B C is fine.)
"""

import argparse
import os
import sys
from pprint import PrettyPrinter

#DICT_FILE = "/usr/share/dict/words"
HUGE_DICT_FILE = "/usr/share/dict/american-english-huge"
RARE_DICT_FILE = "/usr/share/dict/american-english-insane"

def _LoadGridFromFile(f):
  """Returns an array of the contents of the file."""
  try:
    return [filter(str.isalnum,line.upper()) for line in open(f)]
  except FileNotFoundError as e:
    exit(e)


def _LoadWordsFromDictFile(dict_file):
  return set(word.strip().lower() for word in open(dict_file).readlines())


def _PrintIfWordEitherDirection(direction, rev_direction, word, row, col, words):
    if word.lower() in words:
      print '%s at %02i, %02i, %s' % (word, row, col, direction)

    reversed_word = word[::-1]
    if reversed_word.lower() in words:
      # Give human friendly coordinates for reversed words
      word_len = len(word)
      if direction == "across":
        col = col + word_len - 1
      else:
        row = row + word_len - 1
        if direction == "down right":
          col = col + (word_len - 1)
        elif direction == "down left":
          col = col - (word_len -1)
      print '%s at %02i, %02i, %s' % (reversed_word, row, col, rev_direction)


def _PrintWordsInGrid(words, grid, nrows, ncols, min_len):

  def _Check(direction, rev_direction, word):
    _PrintIfWordEitherDirection(direction, rev_direction, word, row, col, words)

  # When searching check A and reverse(A) at the same time 
  max_dimension = max(nrows, ncols)
  for strlen in range(min_len, max_dimension):
    for row in xrange(nrows):
      for col in xrange(ncols):

        # Check horizontal
        if col + strlen <= ncols:
          _Check("across", "left", grid[row][col:col+strlen])

        # If there are not enough rows, rule out all down combinations
        if row + strlen > nrows:
          continue

        _Check("down", "up", "".join([grid[row+i][col] for i in range(strlen)]))

        if col + strlen <= ncols:
          _Check("down right", "up left",
                 "".join([grid[row+i][col+i] for i in range(strlen)]))

        if col + 1 >= strlen:
          _Check("down left", "up right",
                 "".join([grid[row+i][col-i] for i in range(strlen)]))
          
def _ParseCommandLineArguments(argv):

    def _PrintHelpAndDie(error):
        print(error + "\n")
        parser.print_help()
        exit(1)

    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawTextHelpFormatter,
        description = __doc__)

    parser.add_argument("--grid_file", "-f", required=True,
        help="The file containing the grid to search.")

    parser.add_argument("--min_length", "-l", type=int, required=True,
        help="The minimum length of word to find.")

    parser.add_argument("--dict_file", "-d", default=HUGE_DICT_FILE,
        help="Dictionary to use. Default: %s" % HUGE_DICT_FILE)

    parser.add_argument("--print_grid", "-p", action="store_true",
        help="Print the grid to be searched.")

    parser.add_argument("--allow_rare_words", "-r", action="store_true",
        help="Allow rarer words in the solution (bigger dictionary)."
             "\nThis overrides --dict_file")

    args = parser.parse_args()
    if args.allow_rare_words:
      args.dict_file = RARE_DICT_FILE

    return args


def Main():
  args = _ParseCommandLineArguments(sys.argv)
  min_len = args.min_length
  dict_file = args.dict_file
  grid_file = args.grid_file
  print_grid_file = args.print_grid

  grid = _LoadGridFromFile(grid_file)

  if print_grid_file:
    PrettyPrinter(indent=2).pprint(grid)

  nrows=len(grid)
  ncols=len(grid[1])
  max_dimension = max(nrows, ncols)
  if (min_len > max_dimension):
    sys.exit('Minimum word length specified(%i) exceeds both row(%i)'
             ' and column(%i) size.' % (min_len, nrows, ncols))

  words = _LoadWordsFromDictFile(dict_file)

  _PrintWordsInGrid(words, grid, nrows, ncols, min_len)


if __name__ == '__main__':
  Main()
