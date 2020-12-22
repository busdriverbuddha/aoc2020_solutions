def deck2string(deck):
    return "".join("{:02d}".format(v) for v in deck)

def play_game(p1deck, p2deck, return_deck=False):
    p1deck, p2deck = list(p1deck), list(p2deck)
    prev_rounds = []
    while True:
        this_config = (deck2string(p1deck), deck2string(p2deck))
        if this_config in prev_rounds:
            if return_deck:
                return "p1", p1deck
            else:
                return "p1"
        prev_rounds.append(this_config)
        
        p1card, p2card = p1deck.pop(0), p2deck.pop(0)       

        if len(p1deck) >= p1card and len(p2deck) >= p2card:
            round_winner = play_game(p1deck[:p1card], p2deck[:p2card])
        else:
            round_winner = "p1" if p1card > p2card else "p2"

        winnerdeck = p1deck if round_winner == "p1" else p2deck
        winnerdeck += [
            p1card if round_winner == "p1" else p2card,
            p2card if round_winner == "p1" else p1card
        ]
        
        if p1deck and p2deck:
            continue

        return_value = "p1" if not p2deck else "p2"
        if return_deck:
            return_value = (return_value, p1deck if return_value == "p1" else p2deck)
        return return_value
        
    

INPUT_FILE = "input"

player1, player2 = open(INPUT_FILE).read().split("\n\n")

p1deck = list(map(int, player1.split("\n")[1:]))

p2deck = list(map(int, player2.split("\n")[1:]))

_, winning_deck = play_game(p1deck, p2deck, True)

winning_deck.reverse()
final_score = sum(i * v for i, v in enumerate(winning_deck, 1))

print(final_score)