
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

# Create the model
model = LpProblem(name="model-11_maximize-profit", sense=LpMaximize)

# Initialize the decision variables
x_1f = LpVariable(name="x_1f", lowBound=0)
x_1c = LpVariable(name="x_1c", lowBound=0)
x_1b = LpVariable(name="x_1b", lowBound=0)
x_2f = LpVariable(name="x_2f", lowBound=0)
x_2c = LpVariable(name="x_2c", lowBound=0)
x_2b = LpVariable(name="x_2b", lowBound=0)
x_3f = LpVariable(name="x_3f", lowBound=0)
x_3c = LpVariable(name="x_3c", lowBound=0)
x_3b = LpVariable(name="x_3b", lowBound=0)
x_4f = LpVariable(name="x_4f", lowBound=0)
x_4c = LpVariable(name="x_4c", lowBound=0)
x_4b = LpVariable(name="x_4b", lowBound=0)

# Add the constraints to the model
model += (x_1f + x_1c + x_1b <= 20, "amount cargo 1")
model += (x_2f + x_2c + x_2b <= 16, "amount cargo 2")
model += (x_3f + x_3c + x_3b <= 25, "amount cargo 3")
model += (x_4f + x_4c + x_4b <= 13, "amount cargo 4")

model += (x_1f + x_2f + x_3f + x_4f <= 12, "weight front")
model += (x_1c + x_2c + x_3c + x_4c <= 18, "weight center")
model += (x_1b + x_2b + x_3b + x_4b <= 10, "weight back")

model += ((1/12)*(x_1f + x_2f + x_3f + x_4f) == (1/18)*(x_1c + x_2c + x_3c + x_4c), "proportionality 1")
model += ((1/12)*(x_1f + x_2f + x_3f + x_4f) == (1/10)*(x_1b + x_2b + x_3b + x_4b), "proportionality 2")

model += (500*x_1f + 700*x_2f + 600*x_3f + 400*x_4f <= 7000, "volume front")
model += (500*x_1c + 700*x_2c + 600*x_3c + 400*x_4c <= 9000, "volume center")
model += (500*x_1b + 700*x_2b + 600*x_3b + 400*x_4b <= 5000, "volume back")

# Add the objective function to the model
obj_func = 280*(x_1f + x_1c + x_1b) + 360*(x_2f + x_2c + x_2b) + 320*(x_3f + x_3c + x_3b) + 250*(x_4f + x_4c + x_4b)
model += obj_func

# Solve the problem
status = model.solve()

# Print results. Round to get rid of floating point error
print(f"status: {model.status}, {LpStatus[model.status]}")
print(f"objective: {round(model.objective.value())}")
print(f"variables: ")
for var in model.variables():
    print(f"  {var.name}: {round(var.value(),1)}")
print(f"constraints: ")
for name, constraint in model.constraints.items():
    print(f"  {name}: {round(constraint.value(),1)}")

# Solution:
# objective: 11730 -- means the maximum profit is 11730
# x_1b: 0.0 -- means take 0 tons of cargo 1 in the back compartment
# x_1c: 15.5 -- means take 15.5 tons of cargo 1 in the center compartment
# x_1f: 0.0 -- means take 0 tons of cargo 1 in the front compartment
# x_2b: 3.3
# x_2c: 0.8
# x_2f: 7.3
# x_3b: 0.0
# x_3c: 0.0
# x_3f: 0.0
# x_4b: 6.7
# x_4c: 1.7
# x_4f: 4.7







