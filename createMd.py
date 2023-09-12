import os
import re
number = 'd049'

# 擺放順序
texs = ['problem.tex','statement.tex','input.tex','output.tex','spec.tex','hint.tex']

md_file = ""
def make_md(number,md_file):
    tex_call = {"problem":problem_tex,
            "statement":statement_tex,
            "input":input_tex,
            "output":output_tex,
            "spec":spec_tex,
            "hint":hint_tex}

    if os.path.isdir(f'zj-{number}'):
        for tex in texs:
            md_file += f'{tex_call.get(tex[:-4],lambda:print("error"))()}\n'
        with open(f'zj-{number}/{number}.md','w') as f:
            f.write(md_file)
    print(md_file)

def problem_tex():
    with open(f'zj-{number}/problem.tex','r') as f:
        text = f.read()
        start_index = text.find('{', text.find('{') + 1) + 1
        end_index = text.find('}', text.find('}') + 1)
        result = '# ' +text[start_index:end_index]
        return result


def statement_tex():
    with open(f'zj-{number}/statement.tex','r') as f:
        textlist = f.readlines()
        print(textlist)
        text = '## 題目敘述\n'
        text += f"<!--{textlist[0][:-2]}-->\n"
        text += ''.join(textlist[1:])
        print(text)
        return text.replace('\\\\\n','\n')

def input_tex():
    with open(f'zj-{number}/input.tex','r') as f:
        return f.read().replace('\\\\\n','')

def output_tex():
    with open(f'zj-{number}/output.tex','r') as f:
        return f.read().replace('\\\\\n','')

def spec_tex():
    pass

def hint_tex():
    pass

make_md(number,md_file)
