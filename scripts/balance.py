import matplotlib.pyplot as plt
import numpy as np
import random
from collections import Counter

# data = [[0,1],[2,3]]
# plt.imshow(data, cmap='hot', interpolation='nearest')
# plt.colorbar()
# plt.show()

# generate a completly random weapon, then grade it based on its strength

# attack = random.randint(1, 20)
# required_charge = random.randint(1, 20)


# values = [random.gauss(0, 1) for i in range(5000)]
# min_value = min(values)
# max_value = max(values)
# num_buckets = 30
# range_values = max_value - min_value
# step = range_values / (num_buckets-1)

# x = [min_value + (i+0.5) * step for i in range(num_buckets)]
# y = [0] * num_buckets
# for value in values:
#     for i in range(num_buckets):
#         if value < x[i]+step/2.0:
#             y[i] += 1
#             break

# plt.bar(x, y)
# plt
# #plt.plot(x, y)
# plt.show()

# base_stat = 1

frequency = [
    "Common",
    "Uncommon",
    "Very Uncommon",
    "Rare",
    "Very rare",
    "Artefact",
]

attack_base = 1
charge_base = 5
attack_step = 1
charge_step = -1
cost_base = (0, 3, 0)
cost_step = (0, 0, 7)

import currency, tabulate

items = []
for i in range(4):
    attack = attack_base + i * attack_step
    for j in range(3):
        if i + j >= len(frequency):
            continue
        charge = charge_base + j * charge_step
        rarity = frequency[i + j]
        cost = currency.coins(currency.abs(cost_base) + currency.abs(cost_step) * (i + j))
        items.append((attack, charge, rarity, currency.format(cost)))

print(tabulate.tabulate(items, headers=["Attack", "Charge", "Rarity", "Cost"]))
