import k_means
import random

#####################
#Basic Test
#####################

#dataset = [(10, 15), (15, 15), (15, 10), (30, 35), (35, 35), (35, 30)]
#cluster count
#k = 2
#k_means.calculate(dataset, k)

#####################
#Random Test
#####################

pointCount = 50
#cluster count
k = 5

x = random.sample(range(0, 1000), pointCount)
y = random.sample(range(0, 1000), pointCount)
dataset = list(zip(x, y))

k_means.calculate(dataset, k)