
imagePath = "img/Cards/"
imageType = ".png"

suits = {1: "Clubs",
         2: "Diamonds",
         3: "Spades",
         4: "Hearts"}

values = {1: "Ace",
          2: "2",
          3: "3",
          4: "4",
          5: "5",
          6: "6",
          7: "7",
          8: "8",
          9: "9",
          10: "10",
          11: "Jack",
          12: "Queen",
          13: "King"}

print type(suits)
for s in suits:
  print type(s)


# class dumclass(object):
#   """docstring for dumclass"""

#   def __init__(self):
#     self.count = 0
#     self.name = "my_dum_name"

#   def set_my_name(self, new_name):
#     self.name = new_name

#   def __str__(self):
#     return "hello I have a count of %d and my name is %s" % (self.count, self.name)


# mdo = dumclass()

# # print mdo.count
# # print mdo.name

# mdo.set_my_name("new_name")

# # print mdo.name
# #

# myobj = object()

# print dir(myobj)

# print mdo
