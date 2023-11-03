import os
import json
import numpy as np
from tqdm import tqdm
import argparse

def get_data(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

def savejson(data, filename, indent=None):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=indent)

def is_year(text):
    year = int(text)
    if year > 1950 and year < 2015:
        return True
    else:
        return False

def is_year2(text):
    return is_year('20'+text) or is_year('19'+text)

daylist = [f'{i:02d}' for i in range(1,32)]
months_name={
    "january":daylist,
    "february":daylist[:29],
    "march":daylist,
    "april":daylist[:30],
    "may":daylist,
    "june":daylist[:30],
    "july":daylist,
    "august":daylist,
    "september":daylist[:30],
    "october":daylist,
    "november":daylist[:30],
    "december":daylist,
}

months_short = {
    "jan":daylist,
    "feb":daylist[:29],
    "mar":daylist,
    "apr":daylist[:30],
    "may":daylist,
    "jun":daylist[:30],
    "jul":daylist,
    "aug":daylist,
    "sep":daylist[:30],
    "oct":daylist,
    "nov":daylist[:30],
    "dec":daylist,
}

monthday_mapping = {
    '01':daylist,
    '02':daylist[:29],
    '03':daylist,
    '04':daylist[:30],
    '05':daylist,
    '06':daylist[:30],
    '07':daylist,
    '08':daylist,
    '09':daylist[:30],
    '10':daylist,
    '11':daylist[:30],
    '12':daylist,
}

daylist1 = [f'{i:d}' for i in range(1,10)]
monthday_mapping1 = {
    '01':daylist1,
    '02':daylist1,
    '03':daylist1,
    '04':daylist1,
    '05':daylist1,
    '06':daylist1,
    '07':daylist1,
    '08':daylist1,
    '09':daylist1,
    '10':daylist1,
    '11':daylist1,
    '12':daylist1,
}

concator = ['--','-','/','\\','.']
def gen_month_day_patt():
    month_day_mmdd = []
    month_day_ddmm = []
    month_day_mm_dd, month_day_dd_mm = [],[]
    for i in range(1, 13):
        for j in range(1, 32):
            if i in [4, 6, 9, 11]:
                if j>=31:
                    continue
            if i==2 and j>=30:
                continue
            month_day_mmdd.append(f'{i:02d}{j:02d}')
            month_day_ddmm.append(f'{j:02d}{i:02d}')
            
            for con in concator:
                month_day_mm_dd.append(f'{i:02d}{con}{j:02d}')
                month_day_mm_dd.append(f'{i:d}{con}{j:02d}')
                month_day_mm_dd.append(f'{i:02d}{con}{j:d}')

                month_day_dd_mm.append(f'{j:02d}{con}{i:02d}')
                month_day_dd_mm.append(f'{j:d}{con}{i:02d}')
                month_day_dd_mm.append(f'{j:02d}{con}{i:d}')

    return [list(set(pattern)) for pattern in [month_day_mmdd,month_day_ddmm,month_day_mm_dd, month_day_dd_mm]]

def wordfreqs(corpus):
    freqs     = {}
    for word in corpus:
        if word not in freqs:
            freqs[word] = 1
        else:
            freqs[word] += 1
    # sort keys of freqs by its values in descending order
    freqs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
    return freqs

def topn_words(freqs, n):
    top_res = freqs[:n]
    top_cnt = np.sum([item[1] for item in top_res])
    return top_res, top_cnt

def downn_words(freqs, n):
    top_res = freqs[-n:]
    top_cnt = np.sum([item[1] for item in top_res])
    return top_res, top_cnt

def isdigit(c):
    return c>='0' and c<='9'

def validate_date(p, d, pos): # return true when there are no digits before and after d
    l = len(d)
    for i in range(p.find(d), len(p)): # check all matches of 'd', if one match satisfy the condition, return True
        if d in p[i:]:
            if (i==0 or not isdigit(p[i-1])) and (i==len(p)-l or not isdigit(p[i+l])):
                if pos==0 and (i==len(p)-l or not isdigit(p[-1])): # do not allow non-date adjacent digit before 'm', unless the digits are 'd'
                    return True
                if pos==1 and (i==0 or not isdigit(p[0])): # do not allow non-date adjacent digit right after 'm', unless the digits are 'd'
                    return True
    return False

delimeter = '<d>'
def match_mmdd(p): # match month and (month and day)
    month_flag=False
    day_flag=False
    pattern = ''
    locs = [0,0] # position of year, month and day
    pos_deli = p.find(delimeter)
    for m in monthday_mapping:
        if m in p: # match month
            # get all possible match positions
            for pos in range(p.find(m), len(p)-len(m)+1):
                if m in p[pos:]: # month matched
                    locs[0] = -1 if pos<pos_deli else 1
                    pattern = 'my' if pos<pos_deli else 'ym'
                    month_flag=True
                    p1 = p[:pos]
                    p2 = p[pos+2:]
                    for d in monthday_mapping[m]:
                        if (d in p1 and validate_date(p1, d, 0)): # match month and day
                            locs[1] = -1 if p1.find(d)<pos_deli else 1
                            if locs[0]==locs[1]:
                                if locs[0]==-1: # both before y
                                    pattern = 'dmy'
                                else: # both after y
                                    pattern = 'ydm'
                            else:
                                pattern = 'dym'
                            day_flag=True
                        elif (d in p2 and validate_date(p2, d, 1)): # match month and day
                            locs[1] = 1 if p2.find(d)+pos+2>=pos_deli+3 else -1
                            if locs[0]==locs[1]:
                                if locs[0]==-1: # both before y
                                    pattern = 'mdy'
                                else: # both after y
                                    pattern = 'ymd'
                            else:
                                pattern = 'myd'
                            day_flag=True
                        if day_flag:
                            return month_flag, day_flag, pattern, [m, d]
                    if len(p1)>0 and isdigit(p1[-1]): # non-date digit before matched 'month'
                        month_flag=False
                    if len(p2)>0 and isdigit(p2[0]): # non-date digit after matched 'month'
                        month_flag=False
    return month_flag, day_flag, pattern, [m, None]


lists = {'month_full':[], 'month_full_d':[], 'month_full_dd':[], 'month_full_yy':[], 'month_full_yyyy':[], 
        'month_short':[], 'month_short_d':[], 'month_short_dd':[], 'month_short_yy':[], 'month_short_yyyy':[], 
        'yyyy':[], 'yyyymm':[], 'yyyymmdd':[], 'yymm':[], 'yymmdd':[], 'md':[], 'md_rest':[]}

month_day_mmdd,month_day_ddmm,month_day_mm_dd, month_day_dd_mm = gen_month_day_patt()
monthday_patterns = list(set(month_day_mmdd+month_day_mm_dd))
daymonth_patterns = list(set(month_day_ddmm+month_day_dd_mm)-set(monthday_patterns))

monthday_patterns_map = {}
for i in monthday_patterns:
    for con in concator:
        if con in i:
            monthday_patterns_map[i] = con
            break
    if i not in monthday_patterns_map:
        monthday_patterns_map[i] = ''

for i in daymonth_patterns:
    for con in concator:
        if con in i:
            monthday_patterns_map[i] = con
            break
    if i not in monthday_patterns_map:
        monthday_patterns_map[i] = ''

def tocsv(match):
    if type(match)==str:
        match = get_data(f'{match}_match.json')
    rowh = ['yyyy','yyyy&mm','yyyy&mm&dd','yy&mm','yy&mm&dd','mm&dd','m&--&d','m&-&d','m&/&d','m&\\&d','m&.&d',
            '月份全称','月份全称&d','月份全称&dd','月份全称&yy','月份全称&yyyy','月份缩写','月份缩写&d','月份缩写&dd','月份缩写&yy','月份缩写&yyyy']
    info = '构成成分\顺序, 总计, 年月, 月年, 月日, 日月, 年月日, 月日年, 日月年, 年日月, 月年日, 日年月\n'
    keys = list(lists.keys())
    default_line = ['\\' for i in range(info.count(','))]
    lines = []
    for i in range(16):
        entry = match[keys[i]]
        if i==15:
            entry = [[t[0],t[1].replace('y','') if 'y' in t[1] else t[1],t[2]] for t in entry]
            totals = [len([t for t in entry if monthday_patterns_map[t[2]]==deli]) for deli in ['','--','-','/','\\','.']]
            orders = [[len([t for t in entry if monthday_patterns_map[t[2]]==deli and t[1]==od]) for od in ['md', 'dm']] for deli in ['','--','-','/','\\','.']]
            new_lines = [[rowh[5+j]]+default_line for j in range(len(totals))]
            for j,t in enumerate(totals):
                new_lines[j][1]=t
                new_lines[j][4]=orders[j][0]
                new_lines[j][5]=orders[j][1]
            lines += new_lines
        else:
            new_line = [rowh[i-10]]+default_line if i>=10 else [rowh[i+11]]+default_line
            total = len(entry)
            new_line[1]=total
            if i not in [0,5,10]:
                for j, od in enumerate(['ym', 'my', 'md', 'dm', 'ymd', 'mdy', 'dmy', 'ydm', 'myd', 'dym']):
                    new_line[j+2] = len([t for t in entry if t[1]==od])
            if i < 10 or i in [10,11,13]:
                for j in range(4, 10):
                    new_line[j+2] = '\\'

            if i in [1,2,6,7,12,14]:
                for j in range(2):
                    new_line[j+2] = '\\'

            if i in [3,4,8,9,12,14,11,13]:
                for j in range(2,4):
                    new_line[j+2] = '\\'

            lines.append(new_line)

    for new_line in lines:
        info += new_line[0]
        for item in new_line[1:]:
            info += f', {item}'
        info += '\n'

    print(info)

def train_tokenizer(args):
    from tokenizers import ByteLevelBPETokenizer
    import torch

    lc_file = f'{args.datafile}_l.json'
    # predef_tokens = list(set(list(months_name.keys())+list(months_short.keys())+monthday_mmdd+monthday_ddmm+[f'{y}' for y in range(1940,2013)]+[f'{d:02d}' for d in range(1,32)]))
    predef_tokens = []
    # Initialize tokenizer
    tokenizer = ByteLevelBPETokenizer() 
    # prepare data (lower case)
    data = []
    if not os.path.exists(lc_file):
        for e in args.data:
            data.append(e.lower())
        savejson(data, lc_file)

    tokenizer.train(files=[lc_file], vocab_size=50000, min_frequency=2, special_tokens=predef_tokens)

    # Save files to disk
    torch.save(tokenizer, f"{args.datafile}_bpe_tokenizer.pt")

def get_vocab_freq(args):
    from tokenizers import ByteLevelBPETokenizer
    import torch
    # Load tokenizer 
    tokenizer_path = f"{args.datafile}_bpe_tokenizer.pt"
    if not os.path.exists(tokenizer_path):
        train_tokenizer(args)
    tokenizer = torch.load(tokenizer_path)
    # Encode data
    encoded = tokenizer.encode_batch(args.data)

    frequencies = {}
    for e in encoded:
        e = e.tokens
        for t in e:
            if t in frequencies:
                frequencies[t] += 1
            else:
                frequencies[t] = 1

    frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    res = [{},{}]
    for item in frequencies:
        if len(item[0])>=3:
            res[0][item[0]]=item[1]
        else:
            res[1][item[0]]=item[1]

    savejson(res, f'{args.datafile}_bpe_tokens.json', indent=4)

def find_date_patterns(args):
    data = args.data
    date_match = lists.copy()
    years = [f'{d}' for d in range(args.start_year, args.end_year)]
    years2 = list(set([f'{y}'[2:] for y in range(args.start_year2, args.end_year)]))

    for i in tqdm(range(len(data))):
    # for i in tqdm(range(100000)):
        p=data[i].lower()
        p0 = data[i]
        flag=True
        for m in months_name:
            if m in p:
                date_match['month_full'].append(p0)
                year_flag=True
                for y in years:
                    if y in p:
                        date_match['month_full_yyyy'].append([p0, 'ym' if p.find(y)<p.find(m) else 'my', [y, m]])
                        year_flag=False
                        break
                if year_flag:
                    for y in years2:
                        if y in p:
                            date_match['month_full_yy'].append([p0, 'ym' if p.find(y)<p.find(m) else 'my', [y, m]])
                            break
                day_flag=True
                for d in months_name[m]:
                    if d in p:
                        date_match['month_full_dd'].append([p0, 'dm' if p.find(d)<p.find(m) else 'md', [m,d]])
                        day_flag=False
                        break
                if day_flag:
                    for d in daylist1:
                        if d in p:
                            date_match['month_full_d'].append([p0, 'dm' if p.find(d)<p.find(m) else 'md', [m,d]])
                            break
                flag=False
                break
        
        if flag:
            for m in months_short:
                if m in p:
                    date_match['month_short'].append(p0)
                    year_flag=True
                    for y in years:
                        if y in p:
                            date_match['month_short_yyyy'].append([p0, 'ym' if p.find(y)<p.find(m) else 'my', [y, m]])
                            year_flag=False
                            break
                    if year_flag:
                        for y in years2:
                            if y in p:
                                date_match['month_short_yy'].append([p0, 'ym' if p.find(y)<p.find(m) else 'my', [y, m]])
                                break

                    day_flag=True
                    for d in months_short[m]:
                        if d in p:
                            date_match['month_short_dd'].append([p0, 'dm' if p.find(d)<p.find(m) else 'md', [m,d]])
                            day_flag=False
                            break
                    if day_flag:
                        for d in daylist1:
                            if d in p:
                                date_match['month_short_d'].append([p0, 'dm' if p.find(d)<p.find(m) else 'md', [m,d]])
                                break

                    break
        
        flag=True # month_full or month_short may catch samples that do not actually have a month name, so we need to catch with other patterns
        if flag:
            candidate = [False, False,'', None]
            for y in years:
                if y in p:
                    candidate = [False, False, '', None]
                    for pos in range(p.find(y), len(p)-len(y)+1): # check all possible position for y
                        if y in p:
                            p1 = p[:p.find(y)]+delimeter+p[p.find(y)+4:] # remove year from password
                            month_flag, day_flag, pattern, md = match_mmdd(p1)
                            if day_flag:
                                candidate = [day_flag, month_flag, pattern, [y]+md]
                                break
                            elif month_flag:
                                if not candidate[0]:
                                    candidate = [day_flag, month_flag, pattern, [y, md[0]]]
                            else:
                                candidate = [day_flag, month_flag, 'y', [y]]
                    if candidate[0]:
                        break # do not stop unless find yymmdd
            
            res = [p0, candidate[-2], candidate[-1]]
            if candidate[0]:
                date_match['yyyymmdd'].append(res)
                flag = False
            elif candidate[1]:
                date_match['yyyymm'].append(res)
                flag = False
            elif candidate[-1] is not None:
                date_match['yyyy'].append(res)

        if flag:
            candidate = [False, False, '', None]
            for y in years2:
                if y in p:
                    candidate = [False, False, '', None]
                    for pos in range(p.find(y), len(p)-len(y)+1): # check all possible position for y
                        if y in p:
                            p1 = p[:p.find(y)]+delimeter+p[p.find(y)+2:] # remove year from password
                            month_flag, day_flag, pattern, md = match_mmdd(p1)
                            if day_flag:
                                candidate = [day_flag, month_flag, pattern, [y]+md]
                                break
                            elif month_flag:
                                if not candidate[0]:
                                    candidate = [day_flag, month_flag, pattern, [y, md[0]]]
                    if candidate[0]:
                        break # do not stop unless find yymmdd
            
            res = [p0, candidate[-2], candidate[-1]]
            if candidate[0]:
                date_match['yymmdd'].append(res)
                flag = False
            elif candidate[1]:
                date_match['yymm'].append(res)
                flag = False

        if flag: # month{}day or day{}month pattern
            for pattern in monthday_patterns:
                if pattern in p:
                    date_match['md'].append([p0, 'md', pattern])
                    flag=False
                    break
            if flag:
                for pattern in daymonth_patterns:
                    if pattern in p:
                        date_match['md'].append([p0, 'dm', pattern])
                        flag=False
                        break

        if flag: # other suspicious month day pattern
            month_flag, day_flag, pattern, md = match_mmdd(p)
            if day_flag:
                date_match['md_rest'].append([p0, pattern, md])

    savejson(date_match, f'{args.datafile}_match.json')
    return date_match
