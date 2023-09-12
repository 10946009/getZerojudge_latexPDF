import requests
import os
from bs4 import BeautifulSoup
import shutil
import re
from time import sleep
from hanziconv import HanziConv

# 1.事前準備
#  安裝套件
#  pip install requests
#  pip install bs4
#  pip install hanziconv==0.2.1
#  資料夾底下要準備generator.py、main.tex檔案

# 2.在這裡放入想要抓的zerojudge題目編號
numberlist = ['d049']

# 3.取得順序:品>github的python的ans檔案，輸入1
#   只取得github不取得品上的ans檔案，輸入2
#   不取得答案輸入0
#   沒有此題的答案會顯示沒有答案
get_ans = 1
# 是否要讓main_題號.tex生成main_題號.pdf 要=1 不要=0
run_pdf = 1
#設定時間
timelimit=1

# 爬蟲間格時間
sleep_time = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
problem_from = ''
# 4. 至generator.py寫隱藏測資邏輯
# 5. 如沒有problem.PDF，使用main_題號.tex產pdf放入./題號/dom資料夾

# --------------爬蟲常用的變數-----------------
def get_crowd(url):
    html = requests.get(url,headers=headers)
    html.encoding = 'UTF-8'
    htmltext = BeautifulSoup(html.text, 'html.parser')
    return htmltext
# -----------------------程式碼的部分-------------------------------
#爬取品茹在hackmd的python答案
def get_hackmd_ans(path,number):
    global problem_from
    try:
        htmltext = get_crowd(f'https://hackmd.io/@10946009/zj-{number}')
        title = htmltext.find('div', class_='container-fluid markdown-body').text
        splitlst = '#!/usr/bin/env python '+'\n# '+list(title.split('```'))[1]
        a = open(f'{path}/dom/ans.py','w')
        a.write(splitlst)
        a.close()
        print('取得品茹的答案')
        problem_from = problem_from + f'% 品python:https://hackmd.io/@10946009/zj-{number} \n'
    except :
        print(f'品茹無答案!')
        get_git_other_ans(path,number)

#爬取別人github上的答案
def get_git_other_ans(path,number):
    global problem_from
    # 放入別人的帳號/title即可
    # 對方的答案檔名需要符合格式 例如:a001.py a002.py
    other_giturl=['10946009/pyanszj']
    for i in other_giturl:
        htmltext = get_crowd(f'https://raw.githubusercontent.com/{i}/master/{number}.py')
        #如果沒有404就抓答案
        if '404: Not Found' not in htmltext.text:
            a = open(f'{path}/dom/ans.py','w', encoding='UTF-8')
            a.write(htmltext.text)
            a.close()
            print(f'取得了{i}的答案')
            problem_from = problem_from + f'% {i}:https://github.com/{i}/blob/master/{number}.py \n'
            break
        else:
            print(f'{i}無答案!')

def check_yuihuang(number):
    global problem_from
    try:
        htmltext = get_crowd('https://yuihuang.com/zj-'+number)
        #判斷404
        if 'Error 404' not in htmltext.text:
            problem_from = problem_from + f'% 黃惟:https://yuihuang.com/zj-{number} \n'
    except:
        problem_from = problem_from + f'% 黃惟:https://yuihuang.com/zj-{number} \n'
        print('黃惟網站timeout!')

# 取代常用的特殊字元轉為latex格式
def replace_special_characters(st):
    st = st.replace('\xa0', '\\\\')
    st = st.replace('\n', '\\\\')
    st = st.replace('。', '。\\\\')
    while 1:
        if '\\\\\\\\' in st:
            st = st.replace('\\\\\\\\', '\\\\')
        else:
            break
    st = st.replace('\\\\', '\\\\\n')
    st = st.replace('\t', '')

    #特殊符號
    st = st.replace('≤', '$\leq$')
    st = st.replace('<=', '$\leq$')
    st = st.replace('≥', '$\geq$')
    st = st.replace('>=', '$\geq$')
    st = st.replace('!=', '$\neq$')
    st = st.replace('<', '$<$')
    st = st.replace('>', '$>$')
    st = st.replace('%', '\%')
    return st

#新增&寫入檔案，放入路徑、檔名、要寫入的字
def output_file(path,name,lststring):
    f = open(f'{path}/{name}','w',encoding='UTF-8')
    f.write(lststring)
    f.close()

#針對sample的in,ans檔轉LF
def sample_file(path,name,lststring):
    f = open(f'{path}/{name}','wb')
    f.write((str(lststring)+'\n').encode())
    f.close()

# 爬zerojudge題目
def get_zerojudge_problem(number,path):
    print("正在爬取題目",number)
    try:
        htmltext = get_crowd('https://zerojudge.tw/ShowProblem?problemid='+number)
        problem_all_text = []
        title = htmltext.find('span', id='problem_title').text
        problem = htmltext.find_all('div', class_='panel-body')
        lst = []

        for i in problem:
            if "記憶體限制" in i.text:
                break
            st = i.text.strip()
            problem_all_text.append(st)
            # 取代常用特殊字元
            st = HanziConv.toTraditional(replace_special_characters(st))
            lst.append(st)
        input_output = lst[3:]
        
        for index,io in enumerate(input_output):
            io = io.replace('\r', '\n')
            io = io.replace('\\\\\n', '')
            if index % 2 == 0:
                sample_file(f'{path}/dom/data/sample',f'{(index+2)//2}.in',io)
            else:
                sample_file(f'{path}/dom/data/sample',f'{(index+2)//2}.ans',io)
        
        #題目來源變數
        problem_from = f'% 題目來源:https://zerojudge.tw/ShowProblem?problemid={number} \n'

        #建立檔案&傳放入的文字
        output_file(path,'statement.tex',problem_from+lst[0])
        output_file(path,'input.tex',lst[1])
        output_file(path,'output.tex',lst[2])
        output_file(path,'problem.tex','\problem{zj-'+number+'}{'+title+'}{1}{100}')
        output_file(path,'spec.tex','')
        output_file(path,'hint.tex','')
        output_file(f'{path}/dom','problem.yaml',f'name: {title}')
        output_file(f'{path}/dom','domjudge-problem.ini',f"timelimit='{timelimit}'")

        #複製generator.py到資料夾
        f1 = f'{os.getcwd()}/generator.py'
        f2 = f'{path}/dom/generator.py'
        if not os.path.isfile(f'{path}/dom/generator.py'):
            shutil.copyfile(f1,f2)
        
        # 執行main.tex
        if os.path.isfile(os.getcwd()+'/main.tex'):
            with open(os.getcwd()+'/main.tex', 'r') as f:
                with open(os.getcwd()+f'/main_{number}.tex', 'a') as f_temp:
                    for line in f.readlines():
                        if 'problem.tex' in line:
                            f_temp.write(re.sub('\{.*?\}','{'+f'zj-{number}/problem.tex'+'}',line))
                            continue
                        f_temp.write(line)
            if run_pdf:
                os.system(f'pdflatex main_{number}.tex')
                #如果成功產出來了就放進去並改檔名
                new_pdf = os.getcwd()+f'/main_{number}.pdf'
                path_dom = os.getcwd()+f'/zj-{number}/dom/'
                if os.path.isfile(new_pdf):
                    print('pdf產生ok')
                    shutil.move(new_pdf,path_dom)
                    os.rename(f'{path_dom}main_{number}.pdf',f'{path_dom}problem.pdf')
            
                #刪除暫存
                remove_tamp=[f'main_{number}.aux',f'main_{number}.log',f'main_{number}.out']
                for r in remove_tamp:
                    os.remove(r)
        else:
            print('pdf產生失敗')

    except Exception as err:
        print(err)
        print(number,"無此題目")

def make_dir(number,path):
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
# 爬取zerojudge題目的部分

for number in numberlist:
    path = f'{os.getcwd()}/zj-{number}'
    make_dir(number,path) #建立資料夾
    get_zerojudge_problem(number.lower(),path) #爬取zerojudge題目
    #判斷有沒有黃惟的連結
    check_yuihuang(number)

    #要不要抓取python ans的開關
    if get_ans == 1:
        get_hackmd_ans(path,number)
    elif get_ans == 2:
        get_git_other_ans(path,number)
        
    sleep(sleep_time)