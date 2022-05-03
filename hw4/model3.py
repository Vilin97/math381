import pulp as p

# return the collectors (LpVariable's) that work at hour x
def collectors(x, xs):
    result = []
    for i in range(24):
        if x in [j%24 for j in [i, i+1, i+2, i+3, i+5, i+6, i+7, i+8]]:
            result.append(xs[i])
    return result

prob = p.LpProblem('Collector', p.LpMinimize)
indices = range(24)
demand = [2, 2, 2, 2, 2, 2, 8, 8, 8, 8, 4, 4,
          3, 3, 3, 3, 6, 6, 5, 5, 5, 5, 3, 3]

xs = p.LpVariable.dicts('x', indices, lowBound=0, cat=p.LpInteger)

prob += p.lpSum([xs[i] for i in indices])
for i in indices:
    prob += p.lpSum(collectors(i, xs)) >= demand[i]

prob.solve()

print("Status:", p.LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", round(v.varValue))
print("Minimum Number of Collectors = ", round(p.value(prob.objective)))

# Solution:
# Minimum Number of Collectors = 16  -- means 16 collectors must be hired
# x_0 = 0 -- means hire 0 collectors to start at hour 0 (midnight)
# x_1 = 4 -- means hire 4 collectors to start at hour 1 (1 AM)
# x_10 = 0 -- etc
# x_11 = 0
# x_12 = 0
# x_13 = 1
# x_14 = 2
# x_15 = 2
# x_16 = 2
# x_17 = 0
# x_18 = 0
# x_19 = 0
# x_2 = 0
# x_20 = 0
# x_21 = 0
# x_22 = 0
# x_23 = 0
# x_3 = 1
# x_4 = 1
# x_5 = 1
# x_6 = 1
# x_7 = 1
# x_8 = 0
# x_9 = 0