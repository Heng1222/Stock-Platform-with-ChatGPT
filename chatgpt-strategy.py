# -*- coding:utf-8 -*-
import requests
import sys
import json
API_KEY = '' #your Chat GPT api key
# 取得使用者傳入的需求
userRequest = " ".join(sys.argv[1:])
response = requests.post(
    'https://api.openai.com/v1/chat/completions',
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    },
    json={
        'model': 'gpt-3.5-turbo',
        'messages': [
            {   "role":"system", "content":"""請忘掉先前的資料，現在您扮演資深量化分析師""",
                "role": "user", "content": """您現在被要求將投資者入場策略轉為等價股票入場訊號的判斷式，您可以使用所有網路上能找到的資料為輔助。當您的判斷式回傳True表示符合投資者入場策略，可以買進做多，False表示不符合需求。請考慮以下條件：
預計止損和止盈分別為買入價格的8%和20%。
希望在10天內完成股票的買進和賣出。
精準抓到股票起漲點。
講求獲利。
每個資料都代表某天的數據。

您擁有以下有關於股票資料的Python串列（pandas.Series格式）：
c_open：股票的開盤價
c_high：股票的最高價
c_close：股票的收盤價
c_low：股票的最低價
ma5：MACD指標之5日移動平均線
ma10：MACD指標之10日移動平均線
ma20：MACD指標之20日移動平均線
K：KD指標之K線
D：KD指標之D線
volume：當日交易量
舉例：
今天的開盤價表示為c_open[-1]
ma20[-2]為昨天的20均線值
2天前的K線為K[-3]
取得近3天ma10資料 ma10[-3]
近5天最低價為c_close[-5:].min()
您最多可以使用最近30天的資訊（[-30]）

請確保：
只能使用上述提供的資料。
需為合理、有可能達成的條件。
在符合投資者需求的前提下最佳化判斷式。

投資者需求："""+str(userRequest)+"""據上述需求，請回傳一個符合需求的布林表達式。當判斷式回傳True代表明天會買入做多布局，回傳False則不買入。請詳細考慮各種指標的搭配和選擇，以最大化利潤。
只要給我該表達式(不需換行，且and判斷子以&表示，or判斷子以|表示)，其他不用多說。請充分運用您有的資料，講求精確。"""}],
    }
)
jsonr = response.json()
with open("ErrorMessage.txt", "a+") as ErrorMsg:
        ErrorMsg.write("input userRequest：\n")
        ErrorMsg.write("%s\n"% userRequest)
        ErrorMsg.write("chatGPT respon：\n")
        ErrorMsg.write("%s\n"% jsonr["choices"][0]["message"]["content"])
print(jsonr["choices"][0]["message"]["content"])