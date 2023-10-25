import random

# this is the memory of what has happened for an individual hand
# it provides a way to aggregate payouts over time and give an average
# payout based on total payout and num occurences for the option


class HandScore:

    def __init__(self, h: int, s: int, d: int):
        self.hit_count = h
        self.stand_count = s
        self.double_down_count = d
        self.hit_total = 0
        self.stand_total = 0
        self.double_down_total = 0

    def favoured_strategy(self):
        try:
            avghit = 0 if self.hit_count == 0 else self.hit_total/self.hit_count
            avgstand = 0 if self.stand_count == 0 else self.stand_total/self.stand_count
            avgd = 0 if self.double_down_count == 0 else self.double_down_total/self.double_down_count
            # remove this test if we always want to H when there is no preferred strtegy otherwise random
            if self.hit_count == 0 and self.double_down_count == 0 and self.stand_count == 0:
                return random.choice('HSD')

            maxval = max(avgstand, avgd, avghit)
            if avghit == maxval:
                return "H"
            elif avgd == maxval:
                return "D"
            else:
                return "S"
        except ZeroDivisionError:
            return "-"

    def update_payout(self, choice: str, payout: int):
        if choice == "S":
            self.stand_total += payout
            self.stand_count += 1
        elif choice == "D":
            self.double_down_count += 1
            self.double_down_total += payout
        else:
            self.hit_count += 1
            self.hit_total += payout

    def __str__(self) -> str:
        return "H:"+str(self.hit_total)+"/"+str(self.hit_count)+", S:"+str(self.stand_total)+"/"+str(self.stand_count)+", D:"+str(self.double_down_total)+"/"+str(self.double_down_count)
