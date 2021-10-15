"""Survival bag.

Usage: main.py [-h | --help] [-v | --verbose] [options]

Options:
    -f FILENAME --filename=FILENAME                         Items Filename (.YML) [default: items.yml]

    -w WEIGHT --max-weight=WEIGHT                           Max weight capacity for the surival bag [default: 20]
    -n NB_INDIVIDUALS --nb-individuals=NB_INDIVIDUALS       Number of individuals [default: 1]
    -g NB_GENERATIONS --nb-generations=NB_GENERATIONS       Number of generations [default: 1]
    -m MUTATION_RATE --mutation-rate=MUTATION_RATE          Mutation rate (between 0 and 1) [default: 0.05]
    -e ELITE_RATE --elite-rate=ELITE_RATE                   Elite rate (between 0 and 1) [default: 0.1]
    -p PICK_RATE --pick-rate=PICK_RATE                      Pick rate (between 0 and 1) [default: 0.5]

    --mode=MODE                                             Mode (only genetic_algorithm, for the moment) [default: genetic_algorithm]

    --graph                                                 Display best fitness per generations curve

    -v --verbose                                            Activate verbose

    -h --help                                               Print this help
"""

import yaml
import survival_bag_optimizer
from docopt import docopt


def main_genetic_algo(items, args):
    parameters = {
        "nb_individuals": int(args["--nb-individuals"]),
        "nb_generations": int(args["--nb-generations"]),
        "mutation_rate": float(args["--mutation-rate"]),
        "pick_percentage": float(args["--pick-rate"]),
        "elite_percentage": float(args["--elite-rate"]),
    }
    optimizer = survival_bag_optimizer.SurvivalBagOptimizer(items=items, max_weight=int(args["--max-weight"]), parameters=parameters, verbose=args["--verbose"])
    optimizer.run()
    if args["--graph"]:
        optimizer.display_graph()

if __name__ == '__main__':
    args = docopt(__doc__, version="Genetic Algorithm")
    try:
        with open(args["--filename"]) as items_file:
            items = yaml.safe_load(items_file)
        if args["--mode"] == "genetic_algorithm":
            main_genetic_algo(items, args)
    except FileNotFoundError as e:
        print(f"Error: '{args['--filename']}' file does not exist.")
    except yaml.parser.ParserError as e:
        print(f"Error: Can't parse '{args['--filename']}' file, {e.problem}.")
