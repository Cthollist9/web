import json
from progress.bar import Bar

JSON_FILES = ['csdn', 'yahoo']
DICT_FILES = ['dict-10000', 'dict-50000', 'dict-100000', 'dict-200000', 'dict-500000', 'dict-1000000']

def collision_test(json_file, dict_file):

  with open(f'./{json_file}.json') as f:
    test_data = json.load(f)

  with open(f'./dict/{dict_file}.txt') as f:
    lines = f.readlines()
  pwd_dic = [line.split(' ')[0] for line in lines]

  total_cnt = len(test_data)
  match_cnt = 0

  bar = Bar(max=total_cnt)

  hash_table = set(pwd_dic)

  for pwd in test_data:
    if pwd in hash_table:
      match_cnt += 1

    bar.next()
  bar.finish()

  hash_table.clear()
  del hash_table

  acc = float(match_cnt) / total_cnt
  print(f"Accuracy for {json_file} on {dict_file}: {acc}")
  print(f"matched_pwd {match_cnt} in {total_cnt}")

  with open('res.txt', 'a') as f:
    f.write(f"Accuracy for {json_file} on {dict_file}: {acc}\n")
    f.write(f"matched_pwd {match_cnt} in {total_cnt}\n\n")


if __name__ == '__main__':
  for json_file in JSON_FILES:
    for dict_file in DICT_FILES:
      collision_test(json_file, dict_file)