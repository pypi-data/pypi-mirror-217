# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:40:32 2023

@author: 2020033001
"""
from zipline.pipeline import Pipeline, CustomFactor
from zipline.pipeline.data import Column, DataSet
from zipline.pipeline.domain import Domain,TW_EQUITIES

class TQDataSet(DataSet): 
    
    #Market=Column(float) #市場別
    Open=Column(float) #開盤價
    High=Column(float) #最高價
    Low=Column(float) #最低價
    Close=Column(float) #收盤價
    Adjust_Factor=Column(float) #調整係數
    Volume_1000_Shares=Column(float) #成交量_千股
    Value_Dollars=Column(float) #成交金額_元
    Transaction=Column(float) #成交筆數
    Last_Bid=Column(float) #最後揭示買價
    Last_Offer=Column(float) #最後揭示賣價
    Average_Trade_Price=Column(float) #當日均價
    ROI=Column(float) #報酬率
    High_Low_Diff=Column(float) #高低價差
    Turnover=Column(float) #周轉率
    Issue_Shares_1000_Shares=Column(float) #流通在外股數_千股
    Market_Cap_Dollars=Column(float) #個股市值_元
    Market_Cap_Percentage=Column(float) #市值比重
    Trade_Value_Percentage=Column(float) #成交金額比重
    PER_TWSE=Column(float) #本益比
    PBR_TWSE=Column(float) #股價淨值比
    Dividend_Yield_TWSE=Column(float) #股利殖利率
    Cash_Dividend_Yield_TEJ=Column(float) #現金股利率
    
    annd_s = Column(float) # 市值比重
    Sales_Monthly = Column(float) # 單月營收_千元
    Sales_Monthly_LastYear = Column(float) # 去年單月營收_千元
    YoY_Monthly_Sales = Column(float) # 單月營收成長率％
    MoM_Monthly_Sales = Column(float) # 單月營收與上月比％
    Sales_Accumulated = Column(float) # 累計營收_千元
    Sales_Accu_LastYear = Column(float) # 去年累計營收_千元
    YoY_Accu_Sales = Column(float) # 累計營收成長率％
    Highest_Monthly_Sales = Column(float) # 歷史最高單月營收_千元
    #Highest_Monthly_Sales_YM = Column(float) # 歷史最高單月營收_年月
    Month_Sales_Compared_To_High_Month_Sales_MoM = Column(float) # 與歷史最高單月營收比%
    Lowest_Monthly_Sales = Column(float) # 歷史最低單月營收_千元
    #Lowest_Monthly_Sales_YM = Column(float) # 歷史最低單月營收_年月
    Month_Sales_Compared_To_Lowest_Month_Sales_MoM = Column(float) # 與歷史最低單月營收比%
    #Highest_Or_Lowest_All_Time = Column(float) # 創新高/低
    #Highest_Or_Lowest_In_12M = Column(float) # 創新高/低_近一年
    #Highest_Or_Lowest_Same_Month = Column(float) # 創新高/低_同月比較
    #Hit_New_High_Or_Low_In_N_Months = Column(float) # 創 N月新高/低
    Sales_Accu_12M = Column(float) # 近12月累計營收_千元
    Sales_Accu_12M_Last_Year = Column(float) # 去年近12月累計營收_千元
    YoY_AccuSales_12M = Column(float) # 近12月累計營收成長率％
    Sales_Accu_3M = Column(float) # 近 3月累計營收_千元
    Sales_Accu_3M_LastYear = Column(float) # 去年近 3月累計營收_千元
    YoY_Accu_Sales_3M = Column(float) # 近3月累計營收成長率％
    MoM_Accu_Sales_3M = Column(float) # 近3月累計營收與上月比％    
    QoQ_Accu_Sales_3M = Column(float) # 近3月累計營收變動率％
    #Outstanding_Shares_1000_Shares = Column(float) # 流通在外股數_千股
    Sales_Per_Share_Single_Month = Column(float) # 單月每股營收_元
    Sales_Per_Share_Accu = Column(float) # 累計每股營收_元
    Sales_Per_Share_Accu_12M = Column(float) # 近12月每股營收_元
    Sales_Per_Share_Accu_3M = Column(float) # 近 3月每股營收_元
        
    
    Qfii_Buy_Vol=Column(float) #外資買進張數
    Qfii_Sell_Vol=Column(float) #外資賣出張數
    Qfii_Diff_Vol=Column(float) #外資買賣超張數
    Qfii_Buy_Amt=Column(float) #外資買進金額_元
    Qfii_Sell_Amt=Column(float) #外資賣出金額_元
    Qfii_Diff_Amt=Column(float) #外資買賣超金額_元
    Qfii_Stock_Holding_Pct=Column(float) #外資持股率
    Fund_Buy_Vol=Column(float) #投信買進張數
    Fund_Sell_Vol=Column(float) #投信賣出張數
    Fund_Diff_Vol=Column(float) #投信買賣超張數
    Fund_Buy_Amt=Column(float) #投信買進金額_元
    Fund_Sell_Amt=Column(float) #投信賣出金額_元
    Fund_Diff_Amt=Column(float) #投信買賣超金額_元
    Fund_Stock_Holding_Pct=Column(float) #投信持股率
    Dealer_Proprietary_Buy_Vol=Column(float) #自營商買進張數_自行
    Dealer_Proprietary_Sell_Vol=Column(float) #自營商賣出張數_自行
    Dealer_Proprietary_Diff_Vol=Column(float) #自營買賣超張數_自行
    Dealer_Proprietary_Buy_Amt=Column(float) #自營商買進金額_自行
    Dealer_Proprietary_Sell_Amt=Column(float) #自營商賣出金額_自行
    Dealer_Proprietary_Diff_Amt=Column(float) #自營買賣超金額_自行
    Dealer_Hedge_Buy_Vol=Column(float) #自營商買進張數_避險
    Dealer_Hedge_Sell_Vol=Column(float) #自營商賣出張數_避險
    Dealer_Hedge_Diff_Vol=Column(float) #自營買賣超張數_避險
    Dealer_Hedge_Buy_Amt=Column(float) #自營商買進金額_避險
    Dealer_Hedge_Sell_Amt=Column(float) #自營商賣出金額_避險
    Dealer_Hedge_Diff_Amt=Column(float) #自營買賣超金額_避險
    Dealer_Stock_Holding_Pct=Column(float) #自營商持股率
    Total_Buy_Vol=Column(float) #合計買進張數
    Total_Sell_Vol=Column(float) #合計賣出張數
    Total_Diff_Vol=Column(float) #合計買賣超張數     
    Total_Buy_Vol=Column(float) #合計買進張數
    Total_Sell_Vol=Column(float) #合計賣出張數
    Total_Diff_Vol=Column(float) #合計買賣超張數
    Total_Buy_Amt=Column(float) #合計買進金額_元
    Total_Sell_Amt=Column(float) #合計賣出金額_元
    Total_Diff_Amt=Column(float) #合計買賣超金額_元   
    
    Margin_Purchase=Column(float) #融資買進
    Margin_Sale=Column(float) #融資賣出
    Margin_Balance_Vol=Column(float) #融資餘額
    Margin_Balance_Amt=Column(float) #融資餘額_元
    Cash_Redemption=Column(float) #現金償還
    Margin_Quota=Column(float) #融資限額
    Margin_Short_Coverting=Column(float) #融券買進
    Margin_Short_Sales=Column(float) #融券賣出
    Margin_Short_Balance_Vol=Column(float) #融券餘額
    Margin_Short_Balance_Amt=Column(float) #融券餘額_元
    Margin_Stock_Redemtion=Column(float) #現券償還
    Margin_Short_Quota=Column(float) #融券限額
    Margin_Balance_Ratio=Column(float) #資券比
    Margin_Day_Trading_Vol=Column(float) #資券互抵
    Margin_Day_Trading_Amt=Column(float) #資券互抵_元
    SBL_Short_Sales_Vol=Column(float) #借券賣出
    SBL_Short_Sales_Amt=Column(float) #借券賣出_元
    SBL_Short_Returns_Vol=Column(float) #當日還券
    SBL_Short_Balance_Vol=Column(float) #借券餘額    
    SBL_Short_Balance_Amt=Column(float) #借券餘額_元
    SBL_Short_Quota=Column(float) #借券可使用額度
    Margin_Maintenance_Ratio=Column(float) #融資維持率
    Margin_Short_Maintenance_Ratio=Column(float) #融券維持率
    Account_Maintenance_Ratio=Column(float) #整戶維持率
    Day_Trading_Volume_1000_Shares=Column(float) #當沖成交股數_千股
    Day_Trading_Pct=Column(float) #當沖買賣占比
       
    
    #edate2 =Column(float) #公告日(集保股權)
    #edate1 =Column(float) #集保發布日
    Total_Custodied_Shares_1000_Lots=Column(float) #集保庫存股數_千股
    Total_Custodied_Shares_1000_Lots=Column(float) #集保庫存股數_千股
    Pledged_Stock_Shares_1000_Lots=Column(float) #設質股數_千股
    Custodied_Under_400_Lots_Total_Holders=Column(float) #未滿400張集保人數
    Custodied_Under_400_Lots_Total_Lots=Column(float) #未滿400張集保張數
    Custodied_Under_400_Lots_Pct=Column(float) #未滿400張集保占比
    Custodied_Larger_Than_400_Lots_Total_Holders=Column(float) #超過400張集保人數
    Custodied_Larger_Than_400_Lots_Total_Lots=Column(float) #超過400張集保張數
    Custodied_Larger_Than_400_Lots_Pct=Column(float) #超過400張集保占比
    Custodied_Lots_Between_400_600_Total_Holders=Column(float) #400-600張集保人數
    Custodied_Lots_Between_400_600_Total_Lots=Column(float) #400-600張集保張數
    Custodied_Lots_Between_400_600_Pct=Column(float) #400-600張集保占比
    Custodied_Lots_Between_600_800_Total_Holders=Column(float) #600-800張集保人數
    Custodied_Lots_Between_600_800_Total_Lots=Column(float) #600-800張集保張數
    Custodied_Lots_Between_600_800_Pct=Column(float) #600-800張集保占比
    Custodied_Lots_Between_800_1000_Total_Holders=Column(float) #800-1000張集保人數
    Custodied_Lots_Between_800_1000_Total_Lots=Column(float) #800-1000張集保張數
    Custodied_Lots_Between_800_1000_Pct=Column(float) #800-1000張集保占比
    Custodied_Greater_Than_1000_Lots_Total_Holders=Column(float) #超過1000張集保人數
    Custodied_Greater_Than_1000_Lots_Total_Lots=Column(float) #超過1000張集保張數
    Custodied_Greater_Than_1000_Lots_Pct=Column(float) #超過1000張集保占比 
   
   
    Cash_and_Cash_equivalent=Column(float) #現金及約當現金
    Deposit_interbank_funds=Column(float) #存放同業
    Accounts_Receivable=Column(float) #應收帳款
    Long_term_Accounts_Receivable=Column(float) #長期應收款
    Inventories=Column(float) #存貨
    Accounts_Payable=Column(float) #應付帳款
    Fixed_Assets=Column(float) #固定資產
    Living_Assets=Column(float) #生物資產
    Intangible_Assets=Column(float) #無形資產
    Oil_and_Gas_Assets=Column(float) #油氣資產
    Prepayments=Column(float) #預付款
    Other_Receivables=Column(float) #其他應收款
    Advances_Receipts_Current=Column(float) #預收款_流動
    Other_Accounts_Payable=Column(float) #其他應付款
    Advances_Receipts_Non_Current=Column(float) #預收款_非流動
    Non_current_Assets_Classified_as_Held_for_Sale=Column(float) #待出售非流動資產
    Liabilities_Included_in_Disposal_Groups_Classified_as_Held_for_Sale=Column(float) #待出售資產相關負債
    Other_Current_Assets=Column(float) #其他營運流動資產
    Other_Non_current_Assets=Column(float) #其他營運非流動資產
    Other_Current_Liabilities=Column(float) #其他營運流動負債
    Other_Non_current_Liabilities=Column(float) #其他營運非流動負債
    Portfolio_of_Assets_Current=Column(float) #金融資產流動
    Portfolio_of_Liabilities_Current=Column(float) #金融負債流動
    Portfolio_of_Assets_Non_current=Column(float) #金融資產非流動
    Portfolio_of_Liabilities_Non_current=Column(float) #金融負債非流動
    Equity_Method_Investment=Column(float) #策略性投資
    Property_Investments=Column(float) #投資性不動產
    Financings_Provided_Current=Column(float) #資金貸與_流動
    Financings_Provided_Non_current=Column(float) #資金貸與_非流動
    Short_term_Borrowings_Financial_Institutions=Column(float) #金融借款_流動
    Long_term_Borrowings_Financial_Institutions=Column(float) #金融借款_非流動
    Short_term_Borrowings_Non_financial_Institutions=Column(float) #非金融借款_流動
    Long_term_Borrowings_Non_financial_Institutions=Column(float) #非金融借款_非流動
    Contingent_Liabilities=Column(float) #或有負債
    Common_Stocks=Column(float) #普通股股本
    Capital_Reserves=Column(float) #資本公積
    Total_Retained_Earnings=Column(float) #保留盈餘
    Preferred_Stocks=Column(float) #特別股股本      
    Non_controlling_Interest=Column(float) #非控制權益
    Total_Other_Equity_Interest=Column(float) #其他權益
    Total_Current_Assets=Column(float) #流動資產合計
    Total_Non_current_Assets=Column(float) #非流動資產合計
    Total_Assets=Column(float) #資產總計
    Total_Current_Liabilities=Column(float) #流動負債合計
    Total_Non_current_Liabilities=Column(float) #非流動負債合計
    Total_Liabilities=Column(float) #負債總額
    Total_Equity=Column(float) #股東權益總計
    Total_Liabilities_and_Equity=Column(float) #負債及股東權益總計
    Borrowings=Column(float) #長短期借款
    Quick_Assets=Column(float) #速動資產
    Total_Fixed_Assets=Column(float) #生財設備
    Accounts_Receivable_Current_and_Non_Current=Column(float) #長短期應收帳款
    Operating_Income=Column(float) #營業收入
    Total_Operating_Income=Column(float) #營業總收入
    Operating_Cost=Column(float) #營業成本
    Total_Operating_Cost=Column(float) #營業總成本
    Total_Operating_Expenses=Column(float) #營業費用
    Gain_or_Loss_from_Disposal_of_Assets=Column(float) #處分資產損益
    Impairment_Loss_Reversal_on_Property_Plant_and_Equipment=Column(float) #固定資產減損
    Impairment_Loss_Reversal_on_Biological_Assets=Column(float) #生物資產減損
    Impairment_Loss_Reversal_on_Oil_and_Gas_Assets=Column(float) #油氣資產減損    
    Impairment_Loss_on_Intangible_Assets=Column(float) #無形資產減損
    Income_Tax_Expense=Column(float) #所得稅
    Other_Gain_or_Loss=Column(float) #其他營運損益
    Other_Adjustment_Items=Column(float) #其他調整項
    Gain_Loss_from_Subsidiary_Profit_before_Consolidated=Column(float) #合併方合併前淨利潤    
    Gain_or_Loss_from_Exchange=Column(float) #匯兌損益
    Gain_or_Loss_on_Valuation_of_Assets=Column(float) #評價損益    
    Gain_or_Loss_from_Futures_and_Options=Column(float) #期權損益
    Gain_or_Loss_on_Disposal_of_Equity_Method_Investments=Column(float)  #策略投資處分損益
    Gain_or_Loss_on_Valuation_of_Equity_Method_Investments=Column(float)  #策略投資評價損益
    Gain_or_Loss_on_Fixed_Interest_Investments=Column(float) #定息投資損益
    Gain_or_Loss_on_other_Investments=Column(float) #其他投資損益
    Investment_Gain_of_Loss_Equity_Method=Column(float) #策略投資權益法損益      
    Total_Interest_Income=Column(float) #利息收入
    Interest_Expense=Column(float) #利息支出
    Capitalized_Interest=Column(float) #資本化利息支出     
    Net_Income_Attributable_to_Non_controlling_Interest=Column(float) #非控制權益損益
    Operating_Profit=Column(float) #營業利潤
    Profit_Before_Tax=Column(float) #利潤總額         
    Net_Income_Loss = Column(float) #淨利潤
    Net_Income_Attributable_to_Parent = Column(float) #母公司淨利
    Basic_Earnings_Per_Share = Column(float) #母公司每股盈餘
    Preferred_Stock_Dividends = Column(float) #特別股股息
    Gross_Profit_Loss_from_Operations = Column(float) #毛利
    Net_Operating_Income_Loss = Column(float) #營業利益
    Non_Recurring_Net_Income = Column(float) #非常續性利益
    Recurring_Net_Income = Column(float) #常續性利益
    Non_Operating_Income = Column(float) #非營業利益
    Earnings_Before_Interest_and_Tax = Column(float) #稅前息前淨利
    Proceeds_from_Disposal_of_Fixed_and_Intangible_Assets = Column(float) #處分生財設備
    Purchase_of_Fixed_and_Intangible_Assets = Column(float) #購買生財設備
    Net_Income_Loss_CF = Column(float) #淨利潤_CF
    Reversal_of_Allowance_for_Doubtful_Debts = Column(float) #提列呆帳
    Reversal_of_Allowance_Inventory_Obsolescence = Column(float) #存貨跌價呆滯損失
    Depreciation_and_Amortisation = Column(float) #折舊及攤提
    Gain_or_Loss_from_Disposal_of_Assets_CF = Column(float) #處分生財設備損益_CF
    Impairment_Loss_Reversal_on_Property_Plant_and_Equipment_CF = Column(float) #生財設備資產減損_CF
    Decrease_Increase_in_Accounrs_Receivable = Column(float) #應收帳款增減
    Decrease_Increase_in_Inventories = Column(float) #存貨增減
    Increase_Decrease_in_Accounts_Payable = Column(float) #應付帳款增減
    Decrease_Increase_in_Prepayments = Column(float) #預付款增減
    Decrease_Increase_in_Other_Receivables = Column(float) #其他應收款增減
    Increase_Decrease_in_Advances_Receipts = Column(float) #預收款增減
    Increase_Decrease_in_Other_Accounts_Payable = Column(float) #其他應付款增減
    Other_Adjustment_from_Operating_Activities = Column(float) #其他營運現金
    Cash_Payment_of_Investment = Column(float) #支付投資現金
    Proceeds_from_Disposal_of_Investment = Column(float) #收回投資現金
    Cash_Flow_from_Acquisition_of_Equity_Method_Investment = Column(float) #新增策略性投資
    Disposal_of_Equity_Method_Investment = Column(float) #處分策略性投資
    Cash_Inflow_from_Financings_Provided = Column(float) #資金貸與現金流入  
       
    Cash_Outflow_from_Financings_Provided = Column(float) #資金貸與現金流出
    Other_Adjustment_from_Investment_Activities = Column(float) #其他投資現金
    Increase_in_Debt = Column(float) #借款現金流入
    Debt_Redeemed = Column(float) #還款現金流出
    Interest_Paid = Column(float) #分配股利或支付利息
    Proceeds_from_Capital_Increase_Decrease = Column(float) #權益現金流入
    Other_Adjustment_from_Financing_Activities = Column(float) #其他融資現金
    Effect_of_Exchange_Rate_Changes_on_Cash_and_Cash_Equivalents = Column(float) #匯率影響數
    Other_Cash_Equivalents_Increase_Decrease = Column(float) #其他影響數
    Increase_Decrease_in_Cash_and_Cash_Equivalents = Column(float) #現金淨增加額
    Cash_and_Cash_Equivalents_Beginning = Column(float) #期初現金及等價物淨額
    Cash_Flow_from_Operating_Activities = Column(float) #營運產生現金流量
    Cash_Flow_from_Investing_Activities = Column(float) #投資產生現金流量
    Cash_Flow_from_Financing_Activities = Column(float) #融資產生現金流量
    Cash_and_Cash_Equivalents_Ending = Column(float) #期末現金及等價物淨額
    Number_of_Employees = Column(float) #員工人數
    Common_Stock_Shares_Issued_Thousand_Shares = Column(float) #期末股數
    Weighted_Average_Outstanding_Shares_Thousand = Column(float) #加權平均股數
    Taxrate = Column(float) #稅率
    Return_Rate_on_Equity_A_percent = Column(float) #常續ROE
    Return_on_Total_Assets_A_percent = Column(float) #常續ROA
    Gross_Margin_Rate_percent = Column(float) #營業毛利率
    Operating_Income_Rate_percent = Column(float) #營業利益率
    Pre_Tax_Income_Rate_percent = Column(float) #稅前淨利率
    Net_Income_Rate_percent = Column(float) #稅後淨利率
    Operating_Expenses_Ratio = Column(float) #營業費用率
    Net_Non_operating_Income_Ratio = Column(float) #業外收支率
    Sales_Growth_Rate = Column(float) #營收成長率
    Gross_Margin_Growth_Rate = Column(float) #營業毛利成長率
    Operating_Income_Growth_Rate = Column(float) #營業利益成長率
    Pre_Tax_Income_Growth_Rate = Column(float) #稅前淨利成長率
    Net_Income_Growth_Rate = Column(float) #稅後淨利成長率
    Total_Assets_Growth_Rate = Column(float) #資產成長率   
       
    Total_Equity_Growth_Rate = Column(float) #淨值成長率
    Depreciable_Fixed_Assets_Growth_Rate = Column(float) #固定資產成長率
    Acid_Test = Column(float) #速動比率
    Current_Ratio = Column(float) #流動比率
    Cash_Flow_from_Operating_Ratio = Column(float) #現金流量比率
    Liabilities_Ratio = Column(float) #負債比率
    Interest_Expense_Rate_percent = Column(float) #利息支出率
    Times_Interest_Earned = Column(float) #利息保障倍數
    Debt_Equity_Ratio = Column(float) #借款依存度
    Accounts_Receivable_Turnover = Column(float) #應收帳款週轉率
    Accounts_Payable_Turnover = Column(float) #應付帳款週轉率
    Inventory_Turnover = Column(float) #存貨週轉率
    Total_Assets_Turnover = Column(float) #總資產週轉率
    Equity_Turnover = Column(float) #淨值週轉率
    Fixed_Asset_Turnover = Column(float) #固定資產週轉率
    Days_Receivables_Outstanding = Column(float) #期末收帳天數
    Days_Payables_Outstanding = Column(float) #期末付帳天數
    Days_Inventory_Outstanding = Column(float) #期末售貨天數
    Net_Operating_Cycle = Column(float) #淨營業週期
    Book_Value_Per_Share_A = Column(float) #每股淨值
    Sales_Per_Share = Column(float) #每股營業收入
    Operating_Income_Per_Share = Column(float) #每股營業利益
    Pre_Tax_Income_Per_Share = Column(float) #每股稅前淨益
    Net_Income_Per_Share = Column(float) #每股稅後淨利
    Sales_Per_Employee = Column(float) #每人營收   

    industry_c = Column(object,missing_value=("")) 
    Security_Type_Chinese = Column(object,missing_value=(""))  # 證券種類(中)
    Security_Type_English = Column(object,missing_value=(""))  # 證券種類(英)
    Market_Board =Column(object,missing_value=("")) # 板塊別
    Industry = Column(object,missing_value=(""))  # 產業別_中文
    Industry_Eng = Column(object,missing_value=(""))  # 產業別_英文
    Attention_Stock_Fg = Column(object,missing_value=(""))  # 是否為注意股票
    Disposition_Stock_Fg = Column(object,missing_value=(""))  # 是否為處置股票
    Matching_Period = Column(object,missing_value=(""))  # 分盤間隔時間
    Suspended_Trading_Stock_Fg = Column(object,missing_value=(""))  # 是否暫停交易
    Full_Delivery_Stock_Fg = Column(object,missing_value=(""))  # 是否全額交割
    Limit_Up_or_Down = Column(object,missing_value=(""))  # 漲跌停註記
    Limit_Up_or_Down_in_Opening_Fg = Column(object,missing_value=(""))  # 是否開盤即漲跌停
    Suspension_of_Buy_After_Day_Trading_Fg = Column(object,missing_value=(""))  # 暫停當沖先賣後買註記
    Component_Stock_of_TWN50_Fg = Column(object,missing_value=(""))  # 是否為臺灣50成分股
    Component_Stock_of_MSCI_TW_Fg = Column(object,missing_value=(""))  # 是否為MSCI成分股
    Component_Stock_of_TPEx50_Fg = Column(object,missing_value=(""))  # 是否為富櫃50成分股
    Component_Stock_of_TPEx200_Fg = Column(object,missing_value=(""))  # 是否為富櫃200成分股
    Component_Stock_of_High_Dividend_Fg = Column(object,missing_value=(""))  # 是否為高股息指數成分
    Component_Stock_of_MidCap100_Fg = Column(object,missing_value=(""))  # 是否為中型100成分股
    PER_TEJ = Column(float) # 本益比_TEJ
    PBR_TEJ = Column(float) # 股價淨值比_TEJ
    PSR_TEJ = Column(float) # 股價營收比_TEJ        
  
    domain = TW_EQUITIES
        
    

   