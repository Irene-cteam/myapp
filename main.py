from fastapi import FastAPI, Request, Response
import json
import yfinance as yf
import yfinance.shared as shared
from enum import Enum
import numpy as np
import pandas as pd

app = FastAPI()


class ColumnEnum(Enum):
    Open = 0
    High = 1
    Low = 2
    Close = 3
    Volume = 4


class StockPrice:
    def __init__(self, request_data) -> None:
        self.start_date = request_data["timeframe"]["start_date"]
        self.end_date = request_data["timeframe"]["end_date"]
        self.symbol_list = request_data['symbol_list']
        self.column = request_data['column']
        self._get_stock_price()
        self._prepare_data()

    def _get_stock_price(self):
        stocks = yf.download(
            self.symbol_list, start=self.start_date, end=self.end_date)
        if shared._ERRORS:
            raise Exception(shared._ERRORS)
        df = stocks[ColumnEnum(self.column).name].iloc[::-1]  # iloc[::-1]將順序翻轉
        df = df.replace(np.nan, None, regex=True)

        if isinstance(df, pd.Series):  # 檢查 df 是否為 Series
            df = df.to_frame(name=self.symbol_list[0])
        self.df = df.to_dict(orient="index")  # 轉換成 dict 格式

    def _prepare_data(self):
        self.result_list = []  # 建立空的結果列表
        for i in self.df:
            self.result_list.append({
                "time": i.strftime("%Y-%m-%d"),  # 轉換成可讀字符串表示的時間
                "data": [{"symbol": symbol, "value": value}
                         for symbol, value in self.df[i].items()]  # 將該時間的每筆資料抽出轉換成字典格式
            })

    def get_result(self):
        self.result_list = {
            "status": 1, "result": self.result_list
        }
        return self.result_list


@app.post('/stock')
async def stock(request: Request):
    try:
        request_data = await request.json()
        result = StockPrice(request_data).get_result()
        return Response(content=json.dumps(result), media_type="application/json")
    except Exception as e:
        return Response(content=json.dumps({"status": 0, "error_msg": str(e)}), media_type='application/json')
