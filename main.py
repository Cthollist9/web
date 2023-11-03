from date_utils import *
def getargs():
    parser = argparse.ArgumentParser(description='date pattern matcher')
    parser.add_argument('--datafile', type=str, default='yahoo')
    parser.add_argument('--end_year', type=int, default=-1)
    parser.add_argument('--start_year', type=int, default=1900)
    parser.add_argument('--start_year2', type=int, default=1940)
    parser.add_argument('--mode', type=str, default='date', help='which analysis to do')

    args = parser.parse_args()

    # process args before starting main procedure
    if args.end_year==-1:
        args.end_year= 2012 if args.datafile=='csdn' else 2014

    return args


if __name__ == '__main__':
    args=getargs()

    args.data = get_data(f'{args.datafile}.json') # password dataset

    if args.mode=='date':
        date_match = find_date_patterns(args)
        tocsv(date_match)
    elif args.mode=='token':
        get_vocab_freq(args)