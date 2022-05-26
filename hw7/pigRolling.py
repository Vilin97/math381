import random

roll_probabilities = [0.20086083213773315, 0.35294117647058826, 0.3328550932568149, 0.08034433285509325, 0.028694404591104734, 0.00430416068866571]
scores = [0,1,5,10,15,20,25,40,60]

def prob(list_of_rolls):
    result = 0.0
    for (a,b) in list_of_rolls:
        result += roll_probabilities[a]*roll_probabilities[b]
    return result

# x is the current score
def prob_of_score(score, x=0):
    if score == 0:
        return prob([(0,1), (1,0)])
    elif score == x+1:
        return prob([(0,0), (1,1)])
    elif score == x+5:
        return prob([(0,2), (1,2), (2,0), (2,1)]) + prob([(0,3), (1,3), (3,0), (3,1)])
    elif score == x+10:
        return prob([(0,4), (1,4), (4,0), (4,1)]) + prob([(2,3), (3,2)])
    elif score == x+15:
        return prob([(0,5), (1,5), (5,0), (5,1)]) + prob([(2,4), (4,2), (3,4), (4,3)])
    elif score == x+20:
        return prob([(2,2)]) + prob([(3,3)]) + prob([(2,5), (5,2), (3,5), (5,3)])
    elif score == x+25:
        return prob([(4,5),(5,4)])
    elif score == x+40:
        return prob([(4,4)])
    elif score == x+60:
        return prob([(5,5)])
    else:
        return 0.0

# x is the current score
def score_roll(roll1, roll2, x=0):
    if (roll1, roll2) in [(0,1), (1,0)]: # prob 0.14178411680310576
        return 0 # Pig Out
    elif (roll1, roll2) in [(0,0), (1,1)]: # prob 0.16491254793550553
        return x+1 # Sider
    elif (roll1, roll2) in [(0,2), (1,2), (2,0), (2,1)]:
        return x+5 # Single Razorback
    elif (roll1, roll2) in [(0,3), (1,3), (3,0), (3,1)]:
        return x+5 # Single Trotter
    elif (roll1, roll2) in [(0,4), (1,4), (4,0), (4,1)]:
        return x+10 # Single Snouter
    elif (roll1, roll2) in [(0,5), (1,5), (5,0), (5,1)]:
        return x+15 # Single Leaning Jowler
    elif (roll1, roll2) == (2,2):
        return x+20 # Double Razorback
    elif (roll1, roll2) == (3,3):
        return x+20 # Double Trotter
    elif (roll1, roll2) == (4,4):
        return x+40 # Double Snouter
    elif (roll1, roll2) == (5,5):
        return x+60 # Double Leaning Jowler
    elif (roll1, roll2) in [(2,3), (3,2)]:
        return x+10
    elif (roll1, roll2) in [(2,4), (4,2), (3,4), (4,3)]:
        return x+15
    elif (roll1, roll2) in [(2,5), (5,2), (3,5), (5,3)]:
        return x+20
    elif (roll1, roll2) in [(4,5),(5,4)]:
        return x+25
    else:
        raise ValueError("Invalid Roll!")
        
# print(sum([prob_of_score(s) for s in scores])) # 1.0
# print(sum([prob_of_score(s) for s in scores[1:]])) # 0.8582158831968942

# problem 2
def one_roll():
    return tuple(random.choices(range(6), weights=roll_probabilities,k=2))
def k_rolls(k):
    return list(zip(random.choices(range(6), weights=roll_probabilities, k = k),random.choices(range(6), weights=roll_probabilities, k = k)))
    

# problem 3
# expected score after 1 more roll is
# x + prob_of_score(1) + 5*prob_of_score(5) + 10*prob_of_score(10) + 15*prob_of_score(15) + 20*prob_of_score(20) + 25*prob_of_score(25) + 40*prob_of_score(40) + 60*prob_of_score(60) 
# = x*0.858215883 + 6.1894201219

# testing that relative difference between the calculated expected value and the observed average is small
for x in range(10):
    diff = abs(x*0.858215883 + 6.1894201219 - sum([score_roll(roll1, roll2, x) for (roll1, roll2) in k_rolls(10**5)])/10**5)
    print(f"relative difference for x = {x}: {round(diff/(x*0.858215883 + 6.1894201219), 3)}")

# problem 4
# TODO

# problem 5
# The first strategy is better because the second strategy will NEVER win. In fact, the score for the second strategy will stay at 0 forever, because the only stop condition is pigout, which resets the entire turn's score back to 0.