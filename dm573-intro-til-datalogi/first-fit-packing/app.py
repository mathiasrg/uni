from random import seed, random
from typing import List

seed(42)

values = [random() for _ in range(50)]
containers:List[List[float]] = []

for input in values:
        x = 0
        while x < len(containers):
            container = containers[x]
            if sum(container) + input <= 1:
                container.append(input)
                break
            x += 1
        else:
            containers.append([input])


print(len(containers))
print("All heights: ")
print([sum(inner) for inner in containers])


