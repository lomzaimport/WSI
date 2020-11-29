import random
import math

def Jx(x):
    p = [9, 6, 0, 4, 0]
    return 0.05*p[0]*x[0]**2 + 0.04*p[1]*x[1]**2 + 0.03*p[2]*x[2]**2 + 0.02*p[3]*x[3]**2 + 0.01*p[4]*x[4]**2 + math.sin((p[4]+1)*x[0])*math.sin((p[3]+1)*x[1])*math.sin((p[2]+1)*x[2])*math.sin((p[1]+1)*x[3])*math.sin((p[0]+1)*x[4])

def evolutionAlgorithm(population_number, iterations):

    # Tworzenie populacji o zadanej liczebności
    population = []
    for _i in range(population_number):
        x = []
        for _j in range(5):
            x.append(random.uniform(-5.0,5.0))
            population.append(x)

    while iterations > 0:

        # Selekcja turniejowa
        parents_population = []
        while len(parents_population) != len(population):
            subject1 = random.choice(population)
            subject2 = random.choice(population)
            if Jx(subject1) < Jx(subject2):
                parents_population.append(subject1[:])
            else:
                parents_population.append(subject2[:])

        # Mutacja gaussowska
        for x in parents_population:
            a = random.randint(0,1)
            if a == 0:
                while True:
                    mutation = []
                    for _i in range(len(x)):
                        mutation.append(random.gauss(0, 0.1))
                    if (x[0] + mutation[0] <= 5 and x[0] + mutation[0] >= -5 and x[1] + mutation[1] <= 5 and x[1] + mutation[1] >= -5 and x[2] + mutation[2] <= 5 and 
                        x[2] + mutation[2] >= -5 and x[3] + mutation[3] <= 5 and x[3] + mutation[3] >= -5 and x[4] + mutation[4] <= 5 and x[4] + mutation[4] >= -5):
                        for j in range(len(x)):
                            x[j] = x[j] + mutation[j]
                        break

        population = parents_population.copy()
        iterations -= 1
    
    minimum = population[0]
    for x in population:
        if Jx(x) < Jx(minimum):
            minimum = x
    return minimum


for i in range(5):
    minimum = evolutionAlgorithm(500,200)
    print(f'J({minimum[0]:.2f}, {minimum[1]:.2f},{minimum[2]:.2f},{minimum[3]:.2f},{minimum[4]:.2f}) = {Jx(minimum):.2f}')

