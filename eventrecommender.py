import os
import argparse
from recommender import Recommender

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--today', help='Show today\'s events [True|False]')
    args = parser.parse_args()
    
    if args.today == None:
        parser.parse_args(['-h'])
        quit()
    if args.today != "True" and args.today != "False":
        print("The today arguments should be either 'True' or 'False'")
        parser.parse_args(['-h'])
        quit()
    today = True if args.today == "True" else False
    os.system('cls' if os.name == 'nt' else 'clear')
    print("just choose this!")
    print("==================")
    recommender = Recommender(today)    
    message = recommender.get_recommendation()
    print(message)

if __name__ == "__main__":
    main()




