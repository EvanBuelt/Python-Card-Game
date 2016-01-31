"""Name of module.

Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
  Examples can be given using either the ``Example`` or ``Examples``
  sections. Sections support any reStructuredText formatting, including
  literal blocks::

      $ python card.py

Section breaks are created by simply resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
  module_level_variable (int): Module level variables may be documented in
    either the ``Attributes`` section of the module docstring, or in an
    inline docstring immediately following the variable.

    Either form is acceptable, but the two should not be mixed. Choose
    one convention to document module level variables and be consistent
    with it.

.. _Google Python Style Guide:
   http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

"""
# @Author: Mathew Cosgrove
# @Date:   2016-01-21 11:29:33
# @Last Modified by:   cosgrma
# @Last Modified time: 2016-01-21 11:48:38
# REF: http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html#example-google
# REF: http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

__author__ = "Mathew Cosgrove"
__copyright__ = ""
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Mathew Cosgrove"
__email__ = "cosgroma@gmail.com"
__status__ = "Development"


card_constraints = {
    "gold": (0, 6),
    "diplomacy": (0, 6),
    "stealth": (0, 6),
    "might": (0, 6),
    "victory_point": (1, 3),
    "effect": None
}


class BadCardParamsExepction(BaseException):
  """docstring for BadCardParamsExepction"""

  def __init__(self, message):
    super(BadCardParamsExepction, self).__init__(message)


class Card:

  def __init__(self, gold=0, diplomacy=0, stealth=0, might=0, victory_point=0, effect="None"):
    # def __init__(self, **kwargs): -- look into how kwargs can make you life easier
    # defines card attributes
    self.gold = gold
    self.diplomacy = diplomacy
    self.stealth = stealth
    self.might = might
    self.effect = effect
    self.victory_point = victory_point
    # turns the object members into a dictionary
    attr_dict = self.__dict__

    # checks for impossible attributes
    card_sum = 0
    non_zero_count = 0
    attributes_are_bad = False
    #
    for attr in attr_dict.keys():
      print"attr --", attr
      if attr != "effect":
        val = attr_dict[attr]
        print "val --", val
        card_sum += val
        # checks inputs against card constraints
        if val < card_constraints[attr][0] or val > card_constraints[attr][1]:
          attributes_are_bad = True
          print "the attributes are bad"
          break
        # gets number of nonzero attributes
        elif val != 0:
          non_zero_count += 1
    # if card constraint is violated, nullifiy the caller
    if attributes_are_bad:
      raise BadCardParamsExepction("bad bad bad")
      print "setting self to None"
    # if number of non-zeroes is greater than 3, nullifiy the caller
    if non_zero_count > 3:
      raise BadCardParamsExepction("bad bad bad")
      print "setting self to None -- there are more than 3 with a non zero value"
    # if sum of attributes is greater than 6, nullifiy the caller
    if card_sum > 6:
      raise BadCardParamsExepction("bad bad bad")
      print "setting self to None -- card total sum is greater than 6"
    # if number of resources is odd, nullifiy the caller
    elif (card_sum - victory_point) % 2 != 0:
      raise BadCardParamsExepction("bad bad bad")
      print "setting self to None -- not even, makes the math too hard"

  def __str__(self):
    return "gold = %d\ndiplomacy = %d\nstealth = %d\nmight = %d\neffect = %s\nvictory_point = %d\n" % (self.gold, self.diplomacy, self.stealth, self.might, self.effect, self.victory_point)


def main():
  # Make this more pythonic
  #
  # tests for nonzeroes (more than 3)
  card_setup_test_1 = {
      "gold": 0,
      "diplomacy": 1,
      "stealth": 2,
      "might": 3,
      "victory_point": 2,
      "effect": "None",
  }
  # tests for card_sum(more than 6)
  card_setup_test_2 = {
      "gold": 0,
      "diplomacy": 99,
      "stealth": 2,
      "might": 0,
      "victory_point": 2,
      "effect": "None",
  }
  # tests for even resources
  card_setup_test_3 = {
      "gold": 0,
      "diplomacy": 3,
      "stealth": 2,
      "might": 0,
      "victory_point": 2,
      "effect": "None",
  }

  # mycard_default = Card()
  # print mycard_default

  test_passed = False
  try:
    mycard_test_1 = Card(**card_setup_test_1)
    print mycard_test_1
  except BadCardParamsExepction as e:
    print "got BadCardParamsExepction on test 1"
    test_passed = True
  except Exception as e:
    raise
  else:
    pass
  finally:
    pass


if __name__ == '__main__':
  main()


# my_test_1 = Card(**card_setup_test_1)
# if my_test_1 is None:
#   print "test_1 -- PASSED"

# my_test_2 = Card(**card_setup_test_2)
# if my_test_2 is None:
#   print "test_2 -- PASSED"

# my_test_3 = Card(**card_setup_test_3)
# if my_test_3 is None:
#   print "test_3 -- PASSED"


# mybadcard = Card(3, 3, 3, 3, 10, "destruction")
# if mybadcard is None:
#   print "test passed"#!/usr/bin/env python
# -*- coding: utf-8 -*-;
