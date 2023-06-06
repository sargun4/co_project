
def initialize():
    with open('input.txt') as f:
       instrunctns = f.read().splitlines()
    lst = "0"*16
    memory = [lst]*128

    i = 0
    for line in instrunctns:
        memory[i] = line
        i += 1
    return [memory,instrunctns]

def dump(memory):
    ctr = 0
    # print \ memory dump
    for i in memory:
        print(i)
        ctr += 1
