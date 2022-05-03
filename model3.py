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
