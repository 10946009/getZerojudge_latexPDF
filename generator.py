#!/usr/bin/python
import subprocess
import os
import random
import glob
#############################################################################

# 1. 請先把解答程式放在ans.py
# 2. 確定terminal開在generator.py同一層的資料夾 ex: C:/xxx/xxx/a001
# 3. 設定測資範本
    
###############################################################################


# 在這邊定義secret測資數量!!!
secret_count = 5

secret = []
for i in range(secret_count):
    sample_input = ''
    inputlist = []

    # 在這裡定義隱藏測資邏輯!!!!!!!!!!!!
    # sample_input = 一行文字
    # inputlist.append(sample_input+"\n") 用來存入每一行的測資，結尾\n用來換行

    # 此為zj-a001的範例，直接定義secret即可
    # secret=['python','c++','hello','a123','abcdefg']

    # 此為zj-a002的範例，定義兩個數的亂數
    # a = random.randrange(0,10000)
    # b = random.randrange(0,10000)
    # sample_input = f'{a} {b}\n'
    # inputlist.append(f'sample_input')
    
    # 此為zj-d074的範例，定義亂數
    M = random.randrange(1, 10)
    sample_input = f"{M}"
    inputlist.append(sample_input+"\n")
    mlst=[]
    for r in range(0,M):
        m =random.randrange(10,100)
        mlst.append(str(m))

    inputlist.append(' '.join(mlst))
    #測資邏輯結束

    #輸出secret
    if len(secret) == secret_count:
        break 
    secret.append(''.join(inputlist))


#----------------------------------------------------
# 把測資跟secret放進ans.py並取出output
def generate_in_ans_file(input, path, number):
    p = subprocess.Popen(os.getcwd() + "/ans.py",
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8', shell=True)

    output, error = p.communicate(input=input)
    print(input, output, path, number)
    with open(f"{path}/{number}.in",'w', encoding = 'utf-8') as f:
        f.write(input)
    with open(f"{path}/{number}.ans",'w', encoding = 'utf-8') as f:
        f.write(output)

# 定義路徑
secret_path = os.getcwd() + "/data/secret"
path = [
    os.getcwd() + "/data",
    secret_path
]

# 建立sample跟secret資料夾
for p in path:
    if not os.path.isdir(p):
        os.mkdir(p)

# 產生input跟ans
number = 0
for i, d in enumerate(secret):
    number += 1
    generate_in_ans_file(d, secret_path, number)

