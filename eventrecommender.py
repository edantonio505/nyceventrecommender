import os
import argparse
from recommender import Recommender

def main():
    parser = argparse.ArgumentParser(description='Nyc Event Recommender')

    parser = argparse.ArgumentParser()
    parser.add_argument('-t',  '--today' ,action='store_true', help='Show today\'s events')
    parser.add_argument('-a',  '--all' ,action='store_true', help='Show events all week')
    parser.add_argument('-j',  '--json' ,action='store_true', help='Show events in json format')
    args = parser.parse_args()

    if args.today or args.all:
        # os.system('cls' if os.name == 'nt' else 'clear')
        today = args.today
        json = args.json
        recommender = Recommender(today, json)
        events = recommender.get_recommendation()
        print(events)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()




