from date_utils import *
from word_utils import *

def getargs():
    parser = argparse.ArgumentParser(description='date pattern matcher and password word analyzer')
    parser.add_argument('--datafile', type=str, default='a')
    parser.add_argument('--end_year', type=int, default=-1)
    parser.add_argument('--start_year', type=int, default=1900)
    parser.add_argument('--start_year2', type=int, default=1940)
    parser.add_argument('--mode', type=str, default='date', help='which analysis to do')
    parser.add_argument('--word_dic', type=str,default='./data/words.txt', help='Path to the word dictionary file.')
    parser.add_argument('--output', type=str,default='./output/result.txt', help='Path to the output file.')
    parser.add_argument('--cs', type=str, default='False', help='Flag to enable case-sensitive matching.')

    args = parser.parse_args()

    # process args before starting main procedure
    if args.end_year==-1:
        args.end_year= 2012 if args.datafile=='csdn' else 2014

    return args


if __name__ == '__main__':
    args = getargs()
    args.data = get_data(f'./data/{args.datafile}.json') # password dataset

    # if args.mode=='date':
    #     date_match = find_date_patterns(args)
    #     tocsv(date_match)
    # elif args.mode=='token':
    #     get_vocab_freq(args)
        
    analyze_passwords(args)