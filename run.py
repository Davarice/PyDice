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


DicePattern = re.compile(r"(\b\d+d\d+([-+*/]\d+)?\b)")
Last = []


def get_number(nmin, nmax):
    """Return a number between nmin and nmax, inclusive"""
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
    def __init__(self, size, quantity=1, add_each=0, add_sum=0, low=1):
        self.low = low
        self.high = size
        self.quantity = quantity
        self.add_each = add_each
        self.add_sum = add_sum

    def roll(self):
        result = []
        for i in range(self.quantity):
            die = get_number(self.low, self.high)
            result.append(die)
        return DieRoll(*result, self.add_each, self.add_sum)

    def __str__(self):
        truth = [
            self.quantity,
            self.add_each,
            True,
            self.high,
            self.add_each,
            self.add_each,
            self.add_each,
            self.add_sum,
            self.add_sum,
        ]
        parts = [
            self.quantity,
            "(",
            "d",
            self.high,
            "+",
            self.add_each,
            ")",
            "+",
            self.add_sum,
        ]

        out = "".join([str(parts[i]) for i in range(len(parts)) if truth[i]])
        return out


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
    if not expr:
        return

    dice, *addends = expr.split("+")

    if len(dice) > 1:
        [q, s] = dice.split("d")
    else:
        q, s = 1, dice[0]

    addends = [int(n) for n in addends]
    q = int(q)
    s = int(s)

    dout = Dice(s, q, add_sum=sum(addends))

    return dout


def roll(istr):
    global Last

    if not istr:
        dice = Last
    else:
        expressions = list(DicePattern.finditer(istr.lower()))
        dice = [str(parse_dice(expr.group(0))) for expr in expressions]
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
