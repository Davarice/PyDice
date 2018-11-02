import re
from numpy import random as npr


DicePattern = re.compile(r"(\b\d+d\d+([-+*/]\d+)?\b)")
Last = []
I = 0


def get_number(nmin, nmax):
    """Return a number between nmin and nmax, inclusive"""
    return npr.randint(nmin, nmax + 1)


class DieRoll:
    def __init__(self, results, add_each=0, add_sum=0, src=None):
        self.res = results
        self.add_each = add_each
        self.add_sum = add_sum
        self.src = src or "Dice"

    @property
    def results(self):
        return [int(n) + self.add_each for n in self.res]

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
        return DieRoll(
            results=[get_number(self.low, self.high) for _ in range(self.quantity)],
            add_each=self.add_each,
            add_sum=self.add_sum,
            src=self,
        )

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

    return Dice(s, q, add_sum=sum(addends))


def roll(istr):
    global Last

    if not istr:
        dice = Last
    else:
        expressions = list(DicePattern.finditer(istr.lower()))
        dice = [parse_dice(expr.group(0)) for expr in expressions]
        Last = dice

    results = [die.roll() for die in dice]
    return results


def roll_and_print(istr):
    results = roll(istr)
    for i in range(len(results)):
        for number in results[i].results:
            print(f"d{results[i].src.high}: {number}")
        print(f"{results[i].src} TOTAL: {results[i].total}")


if __name__ == "__main__":
    while 1:
        roll_and_print(input("Roll dice: "))
