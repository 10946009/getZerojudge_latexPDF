import requests
import os
from bs4 import BeautifulSoup
import shutil

# 1.事前準備
#  安裝套件
#  pip install requests
#  pip install bs4
#  資料夾底下要準備generator.py檔案

# 2.在這裡放入想要抓的zerojudge題目，英文要小寫
numberlist = ['d074']

# 3.如果需要取得python的ans檔案，輸入1，否則輸入0
#   沒有此題的答案會顯示沒有答案
get_ans = 1

#設定時間
timelimit=1

# 4. 至generator.py寫隱藏測資邏輯
# 5. 使用main.tex把路徑修改，\includes{zj-xxxx要改的題號/problem.tex}，把產好的pdf放入題號/dom資料夾

# -----------------------程式碼的部分-------------------------------
#爬取品茹在hackmd的python答案
def get_hackmd_ans(path,number):
    url = f'https://hackmd.io/@10946009/zj-{number}'
    html = requests.get(url)
    html.encoding = 'UTF-8'
    sp = BeautifulSoup(html.text, 'html.parser')
    # print(sp)
    try:
        title = sp.find('div', class_='container-fluid markdown-body').text
        splitlst = '#!/usr/bin/env python '+'\n# '+list(title.split('```'))[1]
        a = open(f'{path}/dom/ans.py','w')
        a.write(splitlst)
        a.close
    except Exception as err:
        print(err)
        print(number,'沒有答案')

# 取代常用的特殊字元轉為latex格式
def replace_special_characters(st):
    st = st.replace('\xa0', '\\\\')
    st = st.replace('\n', '\\\\')
    st = st.replace('。', '。\\\\')
    st = st.replace('\t', '')
    st = st.replace('≤', '$\leq$')
    st = st.replace('<=', '$\leq$')
    st = st.replace('≥', '$\geq$')
    st = st.replace('>=', '$\geq$')
    st = st.replace('!=', '$\neq$')
    st = st.replace('\\\\', '\\\\\n')
    st = st.replace('<', '$<$')
    st = st.replace('>', '$>$')
    return st

#新增&寫入檔案，放入路徑、檔名、要寫入的字
def output_file(path,name,lststring):
    f = open(f'{path}/{name}','w',encoding='UTF-8')
    f.write(lststring)
    f.close

#針對sample的in,ans檔轉LF
def sample_file(path,name,lststring):
    f = open(f'{path}/{name}','wb')
    f.write((str(lststring)+'\n').encode())
    f.close

# 爬取zerojudge題目的部分
for number in numberlist:
    try:
        url = 'https://zerojudge.tw/ShowProblem?problemid='+number
        html = requests.get(url)
        html.encoding = 'UTF-8'
        sp = BeautifulSoup(html.text, 'html.parser')
        testlst = []
        title = sp.find('span', id='problem_title').text
        problem = sp.find_all('div', class_='panel-body')
        lst = []
        newlst = []
        for i in problem:
            if "記憶體限制" in i.text:
                break
            st = i.text.strip()
            testlst.append(st)
            # 取代常用特殊字元
            st = replace_special_characters(st)
            lst.append(st)
        

        input_output = lst[3:]
        
        path = f'{os.getcwd()}/zj-{number}'
        #建立題目資料夾
        if not os.path.isdir(path):
            os.mkdir(path)
        #建立題目裡的code資料夾
        if not os.path.isdir(f'{path}/dom'):
            os.mkdir(f'{path}/dom')  
        if not os.path.isdir(f'{path}/dom/data'):
            os.mkdir(f'{path}/dom/data')
        if not os.path.isdir(f'{path}/dom/data/sample'):
            os.mkdir(f'{path}/dom/data/sample')
        for index,io in enumerate(input_output):
            io = io.replace('\\\\\n', '')
            if index % 2 == 0:
                sample_file(f'{path}/dom/data/sample',f'{(index+2)//2}.in',io)
            else:
                sample_file(f'{path}/dom/data/sample',f'{(index+2)//2}.ans',io)
        

        problem_from = '% 題目來源:https://zerojudge.tw/ShowProblem?problemid='+number+'\n% 黃惟:https://yuihuang.com/zj-'+number+'\n% 品python:https://hackmd.io/@10946009/zj-'+number+'\n'

        #建立檔案&傳放入的文字
        output_file(path,'statement.tex',problem_from+lst[0])
        output_file(path,'input.tex',lst[1])
        output_file(path,'output.tex',lst[2])
        output_file(path,'problem.tex','\problem{zj-'+number+'}{'+title+'}{1}{100}')
        output_file(path,'spec.tex','')
        output_file(path,'hint.tex','')
        output_file(f'{path}/dom','problem.yaml',f'name: {title}')
        output_file(f'{path}/dom','domjudge-problem.ini',f"timelimit='{timelimit}'")

        #複製generator.py到各個資料夾
        f1 = f'{os.getcwd()}/generator.py'
        f2 = f'{path}/dom/generator.py'
        if not os.path.isfile(f'{path}/dom/generator.py'):
            shutil.copyfile(f1,f2)

        #要不要抓取python ans的開關
        if get_ans:
            get_hackmd_ans(path,number)
    except Exception as err:
        print(err)
        print(number,"無此題目")