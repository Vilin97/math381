from calendar import c
import random

values = ["red", "not red"]

def AppTester():
    rolls = random.choices(values, weights=(18, 20), k=100)
    for i in range(93):
        if rolls[i:i+8].count("red") == 6:
            return True
    return False

N = 10**6
counter = 0
for i in range(N):
    counter += AppTester()
print(f"probability of seeing 6 out of 8 rolls in 100 rolls: {counter/N}") # 0.965772