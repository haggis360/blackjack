import random
from handscore import HandScore

# this is the persisted strategy preserved in a state
# the state forms a memory of what has happened when we have faced
# previous decisions and selects a prefered strategy based on the memory
# here we store all the handscores for every permutation of starting hand and dealer card


class HandScoreState:
    def __init__(self, dealer_cards: list[int], player_hand_totals: list[int]):
        initialdealerscores = dict.fromkeys(dealer_cards, None)
        self.result_dict = dict.fromkeys(
            player_hand_totals, initialdealerscores)
        dic = []
        for i in player_hand_totals:
            col = []
            for j in dealer_cards:
                col.append(HandScore(0, 0, 0))
            hands = dict(zip(dealer_cards, col))
            dic.append(hands)
        playerhands = dict(zip(player_hand_totals, dic))
        self.result_dict = playerhands

    def update_strategy(self, dealer_score, playertotal, play_option, payout):
        if dealer_score == 0 or playertotal < 2 or playertotal > 21:
            return
        score = self.result_dict[playertotal].get(dealer_score)
        if score is None:
            score = HandScore(0, 0, 0)
            self.result_dict[playertotal][dealer_score] = score
        self.result_dict[playertotal][dealer_score].update_payout(
            play_option, payout)

    def get_results(self):
        return self.result_dict

    def select_strategy(self, dealerfaceupcard: int, playertotal: int, mutate: bool):
        hs = self.result_dict[playertotal].get(dealerfaceupcard)
        if mutate or hs is None:
            return random.choice('HSD')
        return hs.favoured_strategy()


# tests a small matrix
def main():
    print("go")
    hsm = HandScoreState([2, 3], [19, 20])
    print("result")
    print(hsm.result_dict)
    print(hsm.result_dict[19][2])
    hsm.update_strategy(2, 19, "S", -2)
    print(hsm.result_dict)
    print(hsm.result_dict[19][2])
    print(hsm.result_dict[20][2])


if __name__ == "__main__":
    main()
