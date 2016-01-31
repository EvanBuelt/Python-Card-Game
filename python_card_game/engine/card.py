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
# @Last Modified by:   Mathew Cosgrove
# @Last Modified time: 2016-01-31 03:22:50
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


class Card(object):
  """
  @summary: Card Class
  """

  def __init__(self, gold=0, diplomacy=0, stealth=0, might=0, victory_point=0, effect="None"):
    super(Card, self).__init__()
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
          # if card constraint is violated, raise and error
          raise BadCardParamsExepction("attributes_are_bad")
        # gets number of nonzero attributes
        elif val != 0:
          non_zero_count += 1

    # if number of non-zeroes is greater than 3, nullifiy the caller
    if non_zero_count > 3:
      raise BadCardParamsExepction("non_zero_count")
    # if sum of attributes is greater than 6, nullifiy the caller
    if card_sum > 6:
      raise BadCardParamsExepction("card_sum")
    # if number of resources is odd, nullifiy the caller
    elif (card_sum - victory_point) % 2 != 0:
      raise BadCardParamsExepction("odd_sum")

  def __str__(self):
    return "gold = %d\ndiplomacy = %d\nstealth = %d\nmight = %d\neffect = %s\nvictory_point = %d\n" % (self.gold, self.diplomacy, self.stealth, self.might, self.effect, self.victory_point)
