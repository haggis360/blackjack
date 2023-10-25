import random


class Mutation:

    # favour random mutations on earlier iterations in the cycle
    # reduce the probability by setting a percent of max limit that mutations are capped at
    def __init__(self, size: int, lower_pct_limit: int):
        self.MAX_RANGE = int(size*(1-lower_pct_limit))  # 90
        self.MAX = size  # 100

    def mutate(self, iteration: int) -> bool:
        prob = int(random.randint(1, self.MAX_RANGE))  # 1, 90
        return self.MAX-iteration > prob  # 99

# to test the true/false probab of mutation


def main():
    m = Mutation(100, 0.3)
    for i in range(1, 100):
        print(m.mutate(i))


if __name__ == "__main__":
    main()
