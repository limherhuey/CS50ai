from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # puzzle structure - a character is either a knight or a knave, not both
    # a knight always tells the truth while a knave always lies
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # character's testimony (conditions for them to be true or false)
    Biconditional(AKnight, And(AKnight, AKnave)),       # only need either one of the biconditionals but
    Biconditional(AKnave, Not(And(AKnight, AKnave)))    # this is one eg to show the entirety of the puzzle
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # puzzle structure
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # characters' testimonies (assume they are knights and must be truthful)
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # puzzle structure
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # characters' testimonies (assume they are knights and must be truthful)
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),

    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # puzzle structure
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # characters' testimonies (assume they are knights and must be truthful)
    Biconditional(AKnight, Or(AKnight, AKnave)),

    Biconditional(BKnight, Or(Biconditional(AKnight, AKnave), Biconditional(AKnave, Not(AKnave)))),

    Biconditional(BKnight, CKnave),

    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
