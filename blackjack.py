import random
from handscorestate import HandScoreState
from mutation import Mutation
from stateplotter import StatePlotter

# take a card from the deck with a no put back policy


def draw_card(deck, cardsdrawn: list[(int, str)]):
    card = deck[random.randint(0, 51)]
    while card in cardsdrawn:
        card = deck[random.randint(0, 51)]
    return card

# return the dealers payout after compariing hands


def calc_payout(dealer_score: int, playertotal: int, play_option: str):
    if playertotal == 21:
        if dealer_score == 21:
            return 0
        return 3 if play_option == "D" else 1.5
    elif playertotal == -1:
        return -2 if play_option == "D" else -1
    if dealer_score == playertotal:
        return 0
    elif playertotal > dealer_score:
        return 2 if play_option == "D" else 1
    else:
        return -2 if play_option == "D" else -1

# draw dealer cards and calculate their score -1 if bust


def calculatedealer_score(dealerfaceupcard, cardsdrawn, deck):
    dealer_score = dealerfaceupcard[1]
    if dealer_score == 1:
        dealer_score = 11
    dealerdrawncards = 1
    #  print(dealer_score)
    while dealer_score < 17:
        # draw a card
        next_dealer_card = random.randint(0, 51)
        dealerdrawncards += 1
        while next_dealer_card in cardsdrawn:
            next_dealer_card = random.randint(0, 51)
        cardsdrawn.append(next_dealer_card)
        card = deck[next_dealer_card]
        cardval = card[1]
        if cardval == 1 and dealerdrawncards < 3 and dealer_score < 11:
            cardval = 11
        dealer_score += cardval
    # if >21 bust dealer loses return -1
    if dealer_score > 21:
        return -1
    return dealer_score


def main():
    hsm = HandScoreState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [
        2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    deck = [(i, card) for i in ['H', 'D', 'S', 'C'] for card in cards]
    num_iterations = 10000
    randon_mutation = Mutation(num_iterations, 0.3)
    for i in range(1, num_iterations):
        cardsdrawn = []
        dealerfaceupcard = draw_card(deck, cardsdrawn)
        cardsdrawn.append(dealerfaceupcard)
        playercard1 = draw_card(deck, cardsdrawn)
        cardsdrawn.append(playercard1)
        playercard2 = draw_card(deck, cardsdrawn)
        playerstart = playercard1[1]+playercard2[1]
        playertotal = playercard1[1]+playercard2[1]

        # use the strategy to retrieve an action to perform passing the player total, the dealer face up card, the iteration number(for random mutation)
        play_option = hsm.select_strategy(
            dealerfaceupcard[1], playertotal, randon_mutation.mutate(i))

        # apply the action and get a return outcome
        if play_option == "H" or play_option == "D":
            next_player_card = draw_card(deck, cardsdrawn)
            next_val = next_player_card[1]
            playertotal += next_val
            playertotal = -1 if playertotal > 21 else playertotal
            cardsdrawn.append(next_player_card)

        dealer_score = calculatedealer_score(
            dealerfaceupcard, cardsdrawn, deck)
        payout = calc_payout(dealer_score, playertotal, play_option)
        # print(str(dealer_score) + "vs "+str(playertotal) + play_option + " pays "+str(payout))
        # update the strategy with the average result for this action and playertotal/dealer card
        hsm.update_strategy(
            dealerfaceupcard[1], playerstart, play_option, payout)
        # every 100 iterations plot the grid with preferred strategy
        if i % 50 == 0 or i < 50:
            print(str(i)+" ITERATIONS: ")
            stateplot = StatePlotter()
            stateplot.print(hsm)


# small test with 3 cards
def test_3_cards():
    cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    deck = [(i, card) for i in ['H', 'D', 'S', 'C'] for card in cards]
    dealerfaceupcard = deck[random.randint(0, 51)]
    cardsdrawn = [dealerfaceupcard]
    dealer_score = calculatedealer_score(
        dealerfaceupcard, cardsdrawn, deck)
    playertotal = deck[random.randint(
        0, 51)][1]+deck[random.randint(0, 51)][1]+deck[random.randint(0, 51)][1]
    print(str(dealerfaceupcard)+" "+str(dealer_score)+" v "+str(playertotal))


if __name__ == "__main__":
    main()
