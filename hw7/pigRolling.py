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
def prob3():
    for x in range(10):
        diff = abs(x*0.858215883 + 6.1894201219 - sum([score_roll(roll1, roll2, x) for (roll1, roll2) in k_rolls(10**5)])/10**5)
        print(f"relative difference for x = {x}: {round(diff/(x*0.858215883 + 6.1894201219), 3)}")
# prob3()

# problem 4

def prob4():
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    matplotlib.use('TKAgg')
    from scipy.stats import norm
    import matplotlib.pyplot as plt

    results = [0]*1000
    for j in range(1000):
        rolls = k_rolls(30)
        results[j] = sum([score_roll(rolls[i][0],rolls[i][1]) for i in range(30)])/30

    plt.hist(results, bins = 20)
    mean,std=norm.fit(results)
    print(f"mean: {mean}, std: {std}")
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 200)
    y = norm.pdf(x, mean, std)
    plt.plot(x, 10000/sum(y)*y)
    plt.show()

# prob4()

# problem 5
def make_turn(stop_condition):
    x = 0
    while not stop_condition(x):
        roll1, roll2 = one_roll()
        roll_score = score_roll(roll1, roll2, x=x)
        if roll_score == 0:
            x = 0
            break
        else:
            x += roll_score
    return x

def compare_strategies(N = 10**4):
    wins1 = 0
    wins2 = 0
    for _ in range(N): # strategy 1 goes first
        score1 = 0
        score2 = 0
        while True:
            score1 += make_turn(lambda x: x > x*0.858215883 + 6.1894201219)
            if score1 >= 100:
                wins1 += 1
                break
            score2 += make_turn(lambda x: x >= 100)
            if score2 >= 100:
                wins2 += 1
                break

    for _ in range(N): # strategy 2 goes first
        score1 = 0
        score2 = 0
        while True:
            score2 += make_turn(lambda x: x > 100)
            if score2 >= 100:
                wins2 += 1
                break
            score1 += make_turn(lambda x: x > x*0.858215883 + 6.1894201219)
            if score1 >= 100:
                wins1 += 1
                break
    return wins1/(2*N), wins2/(2*N)

def avg_num_turns(N = 10**4):
    num_turns1 = 0
    for _ in range(N):
        score = 0
        while True:
            num_turns1 += 1
            score += make_turn(lambda x: x > x*0.858215883 + 6.1894201219)
            # print(score)
            if score >= 100:
                break
        
    num_turns2 = 0
    for _ in range(N):
        score = 0
        while True:
            num_turns2 += 1
            score += make_turn(lambda x: x > 100)
            # print(score)
            if score >= 100:
                break
    return num_turns1/N, num_turns2/N


def prob5():
    t1, t2 = avg_num_turns(10**4)
    print(f"average number of turns to 100 with strategy 1: {t1} \naverage number of turns to 100 with strategy 2: {t2}")

    win_ratio1, win_ratio2 = compare_strategies(N = 10**4)
    if win_ratio1 > win_ratio2:
        print(f"Strategy 1 is better with win ratio {win_ratio1}")
    else:
        print(f"Strategy 2 is better with win ratio {win_ratio2}")

prob5() # STRATEGY 2 IS BETTER