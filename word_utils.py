from collections import Counter
import json
import os
from tqdm import tqdm

def find_words(input_string, vocab, case_sensitive = 'False'):
    # 过滤掉非字母字符
    clean_string = ''.join(filter(str.isalpha, input_string))
    dp = [None] * (len(clean_string) + 1)  # 初始化动态规划表
    dp[len(clean_string)] = []
    if case_sensitive == 'True':
        # 动态规划从后向前构建最长单词组合
        for i in range(len(clean_string) - 1, -1, -1):
            max_word = ""
            max_combo = None
            for j in range(i + 1, len(clean_string) + 1):
                word = clean_string[i:j]
                if word.lower() in vocab and dp[j] is not None:
                    if len(word) > len(max_word):  # 优先选择最长的单词
                        max_word = word
                        max_combo = [word] + dp[j]
            dp[i] = max_combo

        # 如果在开头位置找到了单词组合，返回该组合
        result = dp[0] if dp[0] is not None else []

        # 过滤掉长度为1的单词
        result = [word for word in result if len(word) > 1]
        return result
    else:
        # 动态规划从后向前构建最长单词组合
        for i in range(len(clean_string) - 1, -1, -1):
            max_word = ""
            max_combo = None
            for j in range(i + 1, len(clean_string) + 1):
                word = clean_string[i:j].lower()
                if word in vocab and dp[j] is not None:
                    if len(word) > len(max_word):  # 优先选择最长的单词
                        max_word = word
                        max_combo = [word] + dp[j]
            dp[i] = max_combo

        # 如果在开头位置找到了单词组合，返回该组合
        result = dp[0] if dp[0] is not None else []

        # 过滤掉长度为1的单词
        result = [word for word in result if len(word) > 1]
        return result


def analyze_passwords(args):
    # 读取主要的英语单词文件
    with open(args.word_dic, 'r', encoding='utf-8') as word_file:
        # 逐行读取文件内容，并将单词添加到 english_vocab 中
        english_vocab = set(word.strip().lower() for word in word_file)

    passwords = args.data

    # 分析每个密码
    all_words = []
    with tqdm(total=len(passwords), desc="Analyzing Words in Passwords", unit="password") as pbar:
        for password in passwords:
            # 使用 find_words 分词解析密码
            segmented_password = find_words(password, english_vocab, args.cs)
            # 将分词结果添加到所有单词列表中，保留原始大小写
            if not args.cs:
                segmented_password = [word.lower() for word in segmented_password]
            all_words.extend(segmented_password)

            # 更新进度条
            pbar.update(1)

    # 使用 Counter 统计单词出现的数量
    word_count = Counter(all_words)

    # 创建文件夹如果不存在
    output_directory = os.path.dirname(args.output)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    # 排序并输出结果到文件
    with open(args.output, 'w', encoding='utf-8') as output_file:
        for word, count in sorted(word_count.items(), key=lambda item: item[1], reverse=True):
            output_file.write(f"{word}: {count}\n")
