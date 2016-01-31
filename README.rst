===============================
Python-Card-Game
===============================

.. image:: https://img.shields.io/pypi/v/python_card_game.svg
        :target: https://pypi.python.org/pypi/python_card_game

.. image:: https://img.shields.io/travis/cosgroma/python_card_game.svg
        :target: https://travis-ci.org/cosgroma/python_card_game

.. image:: https://readthedocs.org/projects/python_card_game/badge/?version=latest
        :target: https://readthedocs.org/projects/python_card_game/?badge=latest
        :alt: Documentation Status


A simple python module that implements a few classes need to contruct a card game

* Free software: ISC license
* Documentation: https://python_card_game.readthedocs.org.

Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
# Python-Card-Game
Card game using pygame.  Uses a custom card engine to help with GUI

# For Fun
https://daringfireball.net/projects/markdown/syntax

# Setup
use the requirements document in CardEngine and run the following
```shell
pip install `cat pycardgame.req`
```

let me know if you have issues getting your python configured
Mine is:
Python 2.7.10 (default, May 23 2015, 09:44:00) [MSC v.1500 64 bit (AMD64)] on win32

We don't want python-3000

# TODO:
## Continue Testing Card Class (DUE: 1/24/16 00:00:00)
* Make the test cases more extensible by combining them into a list
* The list element should have:
    * a card configuration 
    * an expected output
## Think about the Player Class (DUE: 1/30/16 00:00:00)
* It will have a list of cards 
* Think about how the player want to know about his hand as a collective
* Any deep analysis you want to do on a card push into helper methods of the Card class
* 




