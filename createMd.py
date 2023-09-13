import os
import re
number_list = ['a001','a002']
# 擺放順序
texs = ['problem.tex','statement.tex','input.tex','output.tex']
first_name = "zj-"
md_file = ""

def make_md(number,md_file):
    tex_call = {"problem":problem_tex,
            "statement":statement_tex,
            "input":input_tex,
            "output":output_tex,
            "spec":spec_tex,
            "hint":hint_tex}

    if os.path.isdir(f'{first_name}{number}'):
        for tex in texs:
            md_file += f'{tex_call.get(tex[:-4],lambda:print("error"))(number)}\n'
        with open(f'{first_name}{number}/{number}.md','w') as f:
            f.write(md_file)
    print(md_file)

def problem_tex(number):
    with open(f'{first_name}{number}/problem.tex','r') as f:
        text = f.read()
        start_index = text.find('{', text.find('{') + 1) + 1
        end_index = text.find('}', text.find('}') + 1)
        result = '# ' +text[start_index:end_index]
        return result


def statement_tex(number):
    with open(f'{first_name}{number}/statement.tex','r') as f:
        textlist = f.readlines()
        print(textlist)
        text = '## 題目敘述\n'
        text += f"<!--{textlist[0][:-2]}-->\n"
        text += ''.join(textlist[1:])
        print(text)
        return text.replace('\\\\\n','\n')

def input_tex(number):
    with open(f'{first_name}{number}/input.tex','r') as f:
        text = "## input\n"+f.read().replace('\\\\\n','')+"\n"
        path = f'{os.getcwd()}/{first_name}{number}/dom/data/sample/'
        ans_in_list = os.listdir(path)
        for ans_in in ans_in_list :
            if "ans" in ans_in:continue
            with open(f'{path}/{ans_in}','r') as f_ans:
                text+= "```\n"+f_ans.read()+"```\n"
        return text

def output_tex(number):
    with open(f'{first_name}{number}/output.tex','r') as f:
        text = "## output\n"+f.read().replace('\\\\\n','')+"\n"
        path = f'{os.getcwd()}/{first_name}{number}/dom/data/sample/'
        ans_in_list = os.listdir(path)
        for ans_in in ans_in_list :
            if "in" in ans_in:continue
            with open(f'{path}/{ans_in}','r') as f_ans:
                text+= "```\n"+f_ans.read()+"```\n"
        return text

def spec_tex():
    return ""

def hint_tex():
    return ""

for n in number_list:
    make_md(n,md_file)
