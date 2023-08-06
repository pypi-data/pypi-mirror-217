import pandas   as pd
import datetime as dt
from   ..common import code
from   ..innerIO import stockInfo  as sd

def _GetMovingAverage(shCode, averageCnt = 1200, afterNDays  = 20):
    # averageCnt : 이평선 기준일수
    # afterNDays : 주식매수 이후 평균 등락율을 구하기 위한 분석대상 일수

    dListRes = []
    
    df = sd.ReadStockTrade(shCode)

    if len(df) > averageCnt:
        dList = []
        data = [ [x[0], int(x[1]), int(x[2]), int(x[3])] for x in  df[['일자','종가','거래량','거래대금']].values.tolist() ]

        ePriceAccum = 0    # 이동평균기간 평균을 구하기 위한 종가 누적
        exchngVolAccum = 0 # 이동평균기간 평균을 구하기 위한 거래량 누적
        exchngAmtAccum = 0 # 이동평균기간 평균을 구하기 위한 거래대금 누적

        for i, val in enumerate(data):
            if i == 0:
                ePriceAccum     = val[1]
                exchngVolAccum  = val[2]
                exchngAmtAccum  = val[3]
            elif i < averageCnt:
                ePriceAccum    += val[1]
                exchngVolAccum += val[2]
                exchngAmtAccum += val[3]
            else:
                ePriceAccum    += ( val[1] - data[i - averageCnt][1] )
                exchngVolAccum += ( val[2] - data[i - averageCnt][2] )
                exchngAmtAccum += ( val[3] - data[i - averageCnt][3] )          

            if i < (averageCnt - 1):
                dList.append(val + [None, None, None])
            else:
                dList.append(val + [int(ePriceAccum/averageCnt), int(exchngVolAccum/averageCnt), int(exchngAmtAccum/averageCnt)] )

        ePriceAccumAfterNdays = 0    # 주식매수 이후 평균 등락율을 구하기 위한 종가 누적    

        rLen = len(dList)
        for i in range(rLen):
            if i < afterNDays:
                ePriceAccumAfterNdays += dList[i][1]
            else:
                ePriceAccumAfterNdays += ( dList[i][1] - dList[i - afterNDays][1] )            
#                 print(i, afterNDays, flush=True)
                dListRes.append( dList[i - afterNDays] + [ (ePriceAccumAfterNdays/afterNDays -  dList[i - afterNDays][1]) / dList[i - afterNDays][1] * 100  ])

        for i in range(rLen - afterNDays, rLen):
            dListRes.append( dList[i] + [ None ])
    
    return pd.DataFrame( dListRes, columns=['일자','종가','거래량','거래대금','이평종가','이평거래량','이평거래대금', '기간수익률(%)'] )        


def SimulateMovingAverage(shCode='', averageCnt = 1200, afterNDays  = 20, frPriceRatio = 0.9, toPriceRatio = 1.0, tradeVolRatio = 1.0, tradeAmtRatio = 3.0, form = 'S'):
    
    resList = []
   
    if shCode == '':
        shCode = code.GetStockItemListAll()['종목코드'].tolist()
    elif type(shCode) == str:
        shCode = [shCode]
    elif type(shCode) == list:
        pass
    else:
        print('입력 데이터 오류!!!')
        return None
        
    dfRes = pd.DataFrame([])
    
    objCnt = len(shCode)
    if objCnt >= 10:
        print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '분석대상 : ', objCnt)
    
    for idx, sCode in enumerate(shCode):
        df = _GetMovingAverage(sCode, averageCnt = averageCnt, afterNDays  = afterNDays)

        if len(df) > 0:
            cond = ( df['종가'] >= df['이평종가']*frPriceRatio ) & ( df['종가'] <= df['이평종가']*toPriceRatio ) 
            cond = cond & (df['거래량'] >= df['이평거래량']*tradeVolRatio ) 
            cond = cond & (df['거래대금'] >= df['이평거래대금']*tradeAmtRatio ) 
            
            if form == 'S':
                earnRatioTot = df['기간수익률(%)'].mean()
                tradeCntTot = df['기간수익률(%)'].count()

                earnRatioSelected = df[cond]['기간수익률(%)'].mean()
                tradeCntSelected = df[cond]['기간수익률(%)'].count()

                cName = code.GetStockItem(sCode)['종목명']
                cName = cName.iloc[0] if len(cName) > 0 else ''    
                resList.append([sCode, cName, tradeCntTot, earnRatioTot, tradeCntSelected, earnRatioSelected])

            else:                
                df['종목코드'] = sCode
                cName  = code.GetStockItem(sCode)['종목명']
                df['종목명'] = cName.iloc[0] if len(cName) > 0 else ''                

                dfRes = pd.concat([dfRes, df[cond] ])           
                
        if objCnt >= 10:
            print('\r' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '처리건수 : ', idx + 1, end='')
        
                        
    if form == 'S':
        dfRes = pd.DataFrame(resList, columns=['종목코드','종목명','전체건수', '전체기간수익률','분석대상건수','분석대상거래수익률'])
    else:                    
        dfRes = dfRes[['종목코드','종목명','일자','종가','거래량','거래대금','이평종가','이평거래량','이평거래대금','기간수익률(%)']]
        
    return dfRes