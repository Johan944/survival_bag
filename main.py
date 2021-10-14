"""Survival bag.

Usage: main.py [-h | --help] [-v | --verbose] [options]

Options:

    -w WEIGHT --max-weight=WEIGHT                           Max weight capacity for the surival bag [default: 20]
    -n NB_INDIVIDUALS --nb-individuals=NB_INDIVIDUALS       Number of individuals [default: 1]
    -g NB_GENERATIONS --nb-generations=NB_GENERATIONS       Number of generations [default: 1]
    -m MUTATION_RATE --mutation-rate=MUTATION_RATE          Mutation rate (between 0 and 1) [default: 0.05]
    -e ELITE_RATE --elite-rate=ELITE_RATE                   Elite rate (between 0 and 1) [default: 0.3]
    -p PICK_RATE --pick-rate=PICK_RATE                      Pick rate (between 0 and 1) [default: 0.5]

    --mode=MODE                                             Choose a mode (genetic_algorithm is the only option, for the moment...) [default: genetic_algorithm]

    -v --verbose                                            Activate verbose

    -h --help                                               Print this help
"""

import survival_bag_optimizer
from docopt import docopt

items = {
    "raincoat": {"value": 5, "weight": 2},
    "pocket knife": {"value": 3, "weight": 1},
    "mineral water": {"value": 15, "weight": 5},
    "gloves": {"value": 5, "weight": 1},
    "sleeping bag": {"value": 6, "weight": 4},
    "tent": {"value": 18, "weight": 9},
    "portable stove": {"value": 8, "weight": 5},
    "canned food": {"value": 20, "weight": 4},
    "tekyn dev laws": {"value": 30, "weight": 5},
    "snacks": {"value": 8, "weight": 3},
    "compass": {"value": 5, "weight": 2},
    "lighter": {"value": 10, "weight" : 1},
    "rope": {"value": 4, "weight": 4},
    "flash light": {"value": 7, "weight": 3},

}

def main_genetic_algo(args):
    parameters = {
        "nb_individuals": int(args["--nb-individuals"]),
        "nb_generations": int(args["--nb-generations"]),
        "mutation_rate": float(args["--mutation-rate"]),
        "pick_percentage": float(args["--pick-rate"]),
        "elite_percentage": float(args["--elite-rate"]),
    }
    optimizer = survival_bag_optimizer.SurvivalBagOptimizer(items=items, max_weight=int(args["--max-weight"]), parameters=parameters, verbose=args["--verbose"])
    optimizer.run()

if __name__ == '__main__':
    args = docopt(__doc__, version="Genetic Algorithm")
    if args["--mode"] == "genetic_algorithm":
        main_genetic_algo(args)