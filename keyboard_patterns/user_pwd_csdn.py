import re
f = open(r'www.csdn.net.txt',errors = 'ignore')
if f:
    print('have open')
plaintxt = f.read()
f.close()
plain_lines = plaintxt.split('\n')    #每行一个元素
len_plain_lines = len(plain_lines)
len_user_pwd_mails = len(plain_lines)
user_relate_pattern = []
int = 0
for plain_line in plain_lines:
    # if int > 1000:
        # break
    user_name = plain_line.split(' # ')[0]
    pwd = plain_line.split(' # ')[1]
    len_user_name = len(user_name)
    if len_user_name <3 :
        continue
    if len_user_name < 5:
        check_len = 1
    else:
        check_len = len_user_name-4
    for i in range(check_len):
        pattern_seg = user_name[i:i+5]
        if pattern_seg in pwd.upper():
            user_relate_pattern.append(plain_line+'\n')
            print('finish:',int/len_plain_lines)
            break
    int += 1
# print(pattern_pwds)
with open('csdn_user_name_pattern.txt','w') as f:
    f.writelines(user_relate_pattern)



 