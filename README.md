# getZerojudge_latexPDF
## 步驟
1.開啟getZerojudge.py，修改numberlist變數
  輸入需要爬的zj題號即可，可以多筆，範例:numberlist = ['d074','a001'] #英文要小寫
2.執行getZerojudge.py，會在目前目錄底下生成對應的zj-題號資料夾
3.至zj-xxx/dom/generator.py，修改對應題目的邏輯測資，執行後會在zj-xxx/dom/data/secret/這裡產生ans與in檔

## 產生題目PDF
 main.tex的第199行， \includes{zj-d074/problem.tex}中修改要看的題號即可產生對應題目的pdf
