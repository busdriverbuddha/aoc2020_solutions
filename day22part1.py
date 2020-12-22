INPUT_FILE = "input"

player1, player2 = open(INPUT_FILE).read().split("\n\n")

p1deck = list(map(int, player1.split("\n")[1:]))
p2deck = list(map(int, player2.split("\n")[1:]))

while p1deck and p2deck:
    p1card, p2card = p1deck.pop(0), p2deck.pop(0)
    
    if p1card > p2card:
        p1deck += [p1card, p2card]
    else:
        p2deck += [p2card, p1card]

winning_deck = p1deck if p1deck else p2deck
winning_deck.reverse()

final_score = sum(i * v for i, v in enumerate(winning_deck, 1))

print(final_score)