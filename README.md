# getZerojudge_latexPDF
# 待測試中...
## 步驟
1.開啟getZerojudge.py，修改numberlist變數
  輸入需要爬的zj題號即可，可以多筆，
  
   範例:numberlist = ['a001','a002'] 
  
  
2.執行getZerojudge.py，會在目前目錄底下生成對應的zj-題號資料夾，
以及同getZerojudge.py下的目錄會生成main_題號.tex的對應題目tex檔案，供PDF有誤可進行修改再重新上傳

3.至zj-xxx/dom/generator.py，修改對應題目的邏輯測資，執行後會在zj-xxx/dom/data/secret/這裡產生ans與in檔

## 根據tex檔案產生md格式
  生成完題目資料夾後，開啟createMd.py
  number_list = ['a001','a002'] 輸入要產生md格式的題號
  執行後md格式的文建會出現在zj-a001、zj-a002的底下

  ## docker image
  https://hub.docker.com/repository/docker/sd030/ubuntu-latex/general
