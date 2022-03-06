import os
import argparse
from recommender import Recommender

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',  '--today' ,action='store_true', help='Show today\'s events ')
    args = parser.parse_args()

    if args.today:
        today = args.today
        os.system('cls' if os.name == 'nt' else 'clear')
        print("just choose this!")
        print("==================")
        recommender = Recommender(today)    
        message = recommender.get_recommendation()
        print(message)
    else:
        # print help
        parser.print_help()
        

if __name__ == "__main__":
    main()




