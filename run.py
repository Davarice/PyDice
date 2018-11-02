"""

d6
1d8
2d4
2d10+2
2(d10+2)
(2d10)+2

"""

import re
from numpy import random as npr

DicePattern = re.compile(r"(\b\dd\d+([-+*/]\d+)?\b)")
Last = []


def get_number(nmin, nmax):
    return npr.randint(nmin, nmax + 1)


class DieRoll:
    def __init__(self, *results, add_each=0, add_sum=0):
        self.res = results
        self.add_each = add_each
        self.add_sum = add_sum

    @property
    def results(self):
        return [n + self.add_each for n in self.res]

    @property
    def total(self):
        return sum(self.results) + self.add_sum


class Dice:
    def __init__(self, size, quantity=1, add_each=0, add_sum=0):
        self.size = size
        self.quantity = quantity
        self.add_each = add_each
        self.add_sum = add_sum

    def roll(self):
        result = []
        for i in range(self.quantity):
            die = get_number(1, self.size)
            result.append(die)


def parse_dice(expr):
    # Parse a "word" into a number of dice and maybe additions, and return one Dice object for them

    # left = re.search(r"(.*", expr)  # Find everything to the right of the first parenthesis
    # right = re.FindFromRight(".*)", expr)  # Find everything to the left of the last parenthesis
    #
    # if (left and not right) or (right and not left):
    #     raise ValueError("Dice expression '{}' contains unmatched parenthesis".format(expr))

    # subex = intersection_of(left, right)
    # expr = re.sub(expr, subex, "{d}")
    # expr = expr.format(d="asdf")

    return expr


def roll(istr):
    global Last

    if not istr:
        dice = Last
    else:
        expressions = list(DicePattern.finditer(istr.lower()))
        dice = [parse_dice(expr.group(0)) for expr in expressions]
        # for expr in expressions:
            # dice.append(parse_dice(expr))
        Last = dice
    print(dice)

    results = [DieRoll(die) for die in dice]
    return results


def roll_and_print(istr):
    results = roll(istr)
    # print(results)


if __name__ == "__main__":
    while 1:
        roll_and_print(input("Roll dice: "))
