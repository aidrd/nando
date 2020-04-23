
import docx
import sys
import re

args = sys.argv
doc= docx.Document(args[1])
txt = []
flg = 0
count_summary = 0

for par in doc.paragraphs:

    if re.match(r'[１|1][．|.]\s?概要|総論', par.text) is not None:
        flg = 1
    elif re.match(r'[２|2][．|.]\s?原因|^原因\s|^原因|＜疾患分類＞', par.text) is not None:
        break

    if re.match(r'○\u3000概要|概要', par.text) is not None:
        count_summary = count_summary + 1

    if (flg==1 or count_summary>1) and re.match(r'[１|1][．|.]\s?概要|総論|概念', par.text) is None:
        txt.append((par.text).replace('\n',''))

print(re.sub('^概要　|^概要|^\s*|\s*$|　$|\s*[２|2][．|.]原因.*', '', "".join(txt)), end="")


