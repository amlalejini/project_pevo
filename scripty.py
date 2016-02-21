import random

'''
This is me working through the DEAP tutorials -- it turns out that 
 I really do not like DEAP.
'''

MUT_RATE = 0.02

# Individuals
class Individual(object):

    def __init__(self, genome = None, glength = 100):
        '''
        Individual constructor
        '''
        self.phenotype = None
        self.fitness = None

        if genome == None:
            self.rand_init(glength)
        else:
            self.genome = genome
            # Run updates
            self.update_phenotype()
            self.update_fitness()

    def rand_init(self, length = 100):
        self.genome = [random.randint(0, 1) for _ in range(0, length)]
        # Run updates
        self.update_phenotype()
        self.update_fitness()

    def update_phenotype(self):
        '''
        '''
        self.phenotype = sum(self.genome)


    def update_fitness(self):
        '''
        '''
        self.fitness = self.phenotype

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __ne__(self, other):
        return self.fitness != other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.figness <= other.fitness



# class Population(object):

#     def __init__(self, size):
#         '''
#         '''
#         self.population = []

#     def initialize_population


# Things I want to do:
#   - Make calculations parallel

def crossover(gen1, gen2):
    xpoint = random.randint(0, len(gen1))
    offspring_gen1 = gen1[:xpoint] + gen2[xpoint:]
    offspring_gen2 = gen2[:xpoint] + gen1[xpoint:]
    return offspring_gen1

def mutate(val):
    return 0 if val == 1 else 1

def sex(indiv1, indiv2):
    '''
    Give two individuals, this function returns an offspring
    '''
    ma_contrib = [val if random.uniform(0, 1.0) <= MUT_RATE else mutate(val) for val in indiv1.genome]
    pa_contrib = [val if random.uniform(0, 1.0) <= MUT_RATE else mutate(val) for val in indiv2.genome]
    offspring = Individual(genome = crossover(ma_contrib, pa_contrib))
    return offspring


def advance_population(population):
    '''
    Given a population, select two individuals for reproduction
    TODO: look up faster calculation for proportional selection
    '''
    new_population = []
    random_offspring_mult = 0.1
    # reserve some random slots
    random_slots = int(random_offspring_mult * len(population))
    # calculate total fitness
    total_fitness = sum(individual.fitness for individual in population)
    for i in range(len(population) - random_slots):
        ma_selector = random.uniform(0, total_fitness)
        pa_selector = random.uniform(0, total_fitness)
        ma = None  # Parent 0
        pa = None  # Parent 1
        tf = 0
        k = 0
        while ma == None or pa == None:
            print(k)
            tf += population[k].fitness
            if ma == None and ma_selector < tf:
                ma = k
            if pa == None and pa_selector < tf:
                pa = k
            k += 1
        offspring = sex(population[ma], population[pa])
        new_population.append(offspring)
    
    for i in range(0, random_slots):
        ma = random.randint(0, len(population))
        pa = random.randint(0, len(population))
        offspring = sex(population[ma], population[pa])
        new_population.append(offspring)

    return new_population


if __name__ == "__main__":
    POP_SIZE = 100
    G_LEN = 100
    MAX_GENERATION = 100

    # Init Population
    pop = [Individual(glength = G_LEN) for _ in range(0, POP_SIZE)]
    # Loop some number of generations
    generation = 0
    while generation < MAX_GENERATION:
        # create new empty population
        tpop = advance_population(pop)
        pop = tpop
        generation += 1
    print("POPULATION")
    for indiv in pop:
        print("========")
        print(indiv.genome)
        print("Fitness: " + str(indiv.fitness))

