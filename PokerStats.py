#functions for determining the chances of getting a certain hand
from math import factorial

#Royal Flush


def royal_flush_prob():
    number_outcomes = choose(52, 5)
    number_of_ways = 4
    probability = number_of_ways/number_outcomes
    return probability


def straight_flush_prob():
    number_outcomes = choose(52, 5)
    number_of_ways = 40
    probability = number_of_ways/number_outcomes
    return probability

def four_of_kind_prob():
    number_outcomes = choose(52,5)
    number_of_ways = 13*(52-4)
    probability = number_of_ways/number_outcomes
    return probability

def full_house():
    number_outcomes = choose(52,5)

def flush():
    number_outcomes = choose(52, 5)
    number_of_ways = 4*choose(13,5)
    probability = number_of_ways/number_outcomes
    return probability

def straight():
    number_outcomes = choose(52, 5)
    number_of_ways = 10*pow(4, 5) - 40
    probability = number_of_ways/number_outcomes
    return probability

def three_kind_prob():
    number_outcomes = choose(52, 5)
    number_of_ways = 13*choose(4, 3)*16*choose(12, 2)
    probability = number_of_ways/number_outcomes
    return probability

def 

def choose(n, r):
    numerator = factorial(n)

    denominator = factorial(r)*factorial(n-r)

    return numerator/denominator


print(three_kind_prob()*100)