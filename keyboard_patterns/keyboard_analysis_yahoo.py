import re
key_patterns = ['asdfghjkl;\'',
'qwertyuiop',
'zxcvbnm,./',
'qazsedcftgbhujmkol.;',
'wsxdrfvgyhnjik,lp;/'
]
f = open(r'plaintxt_yahoo.txt',errors = 'ignore')
if(f):
    print('open')
plaintxt = f.read()
f.close()
plaintxt_lines = plaintxt.split('\n')    #这里切割会把邮箱和用户名切一起，但我们只用密码，所以并不重要
num_txt = len(plaintxt_lines)
count = 0
pwds = []
int = 0
pattern_pwds = []
stats = {'asdfghjkl;\'':0,'qwertyuiop':0,'zxcvbnm,./':0,'qazsedcftgbhujmkol.;':0,'wsxdrfvgyhnjik,lp;/':0}
for plaintxt_line in plaintxt_lines:
    # if int > 10000:
        # break
    match = 0
    # pattern_count = 0
    pwd = plaintxt_line.split(':')[2]
    for key_pattern in key_patterns:
        len_pattern = len(key_pattern)
        # print(len_pattern)
        for i in range(len_pattern-4):
            pattern_seg = key_pattern[i:i+5]
            if re.search(pattern_seg,pwd,re.I):
                match = 1
                pwd = pwd+'\n'
                pattern_pwds.append(pwd)
                print('finish:',int/num_txt)
                break
        if match:
            stats[key_pattern] += 1
            break
        # pattern_count += 1
    int += 1
stats_outs = []
int = 0
for key_pattern in key_patterns:
    stats_outs.append(key_pattern)
    stats_outs[int] = stats_outs[int]+' : '+str(stats[key_pattern])+'\n'
    int += 1

print(pattern_pwds)
print(stats_outs)
with open('yahoo_keyboard_pattern.txt','w') as f:
    f.writelines(pattern_pwds)
with open('yahoo_keyboard_stats.txt','w') as f:
    f.writelines(stats_outs)



