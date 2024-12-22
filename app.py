#Proxytechtor 2.0.0
from argparse import ArgumentParser
from time import time
from varifier import Varifier

def parse_arguments():
    parser = ArgumentParser(prog="Proxytechtor v2",description="Tool for public proxies varification.")
    parser.add_argument("-p", "--proxies", default="data/proxies.txt", help="Path to the file with proxy servers or files.")
    parser.add_argument("-j", "--judge", default="data/judge.txt" , help="Path to the file with judges.")
    parser.add_argument("-e", "--exclude", default="data/exclude.txt", help="Path to the file with exclude ranges.")
    parser.add_argument("-o", "--output",default=f"checked_proxies_{(int)(time())}.txt", help="Path to the output file.")
    parser.add_argument("-t", "--threads",default=300, type=int, help="Number of threads (numeric value).")
    parser.add_argument("-r", "--reload",default=0, type=int, help="Timeout untill next proxy loading from source (numeric value in seconds). Single run, if set 0.")
    parser.add_argument("-w", "--werbouse", action="store_true", help="Enable additional console logging.")

    args = parser.parse_args()

    return args

def main():
    args = parse_arguments()

    v = Varifier(args.proxies,args.judge,threads=args.threads)
    v.check_proxies()

if __name__ == "__main__":
    main()
