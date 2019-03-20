mlb
===================

CLI utility that prints baseball scores in your terminal

Requirements
===================

Python 3.6>= for f-Strings

Example
===================

```
-> ./mlb.py -t TEX

  ____________________________
 | Reds        |   0|   0|   0|   4:05 ET
 |----------------------------|
 | Rangers     |   0|   0|   0|
  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

-> ./mlb.py -h

usage: mlb.py [-h] [-t TEAM] [-l LEAGUE]

Prints MLB scores

optional arguments:
  -h, --help            show this help message and exit
  -t TEAM, --team TEAM  Prints out teams given. They should be given as their
                        abbreviation.
  -l LEAGUE, --league LEAGUE
                        Prints games from either AL or NL. A for American, N
                        for National
```
