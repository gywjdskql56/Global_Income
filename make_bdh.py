import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def filter_universe(df, type):
    df['NATION'] = df['ETF'].apply(lambda x:x.split(' ')[1])
    df = df[df['NATION']=='US']
    df['자산군'] = type
    return df
def make_universe():
    universe_sl = pd.read_excel('data/universe/시니어론,우선주,이머징채권 유니버스.xlsx',sheet_name='Senior Loan')[['ETF']]
    universe_eb = pd.read_excel('data/universe/시니어론,우선주,이머징채권 유니버스.xlsx',sheet_name='Emerging Bond')[['ETF']]
    universe_pr = pd.read_excel('data/universe/시니어론,우선주,이머징채권 유니버스.xlsx',sheet_name='Preferred')[['ETF']]
    universe_sl = filter_universe(universe_sl, '시니어론')
    universe_eb = filter_universe(universe_eb, '이머징채권')
    universe_pr = filter_universe(universe_pr, '우선주')
    universe = universe_sl.append(universe_eb).append(universe_pr)
    return universe

def make_bdp(universe, factor_list, fed_list):

    vol_df = universe[['ETF','자산군']]
    vol_df['PX_VOLUME'] = vol_df['ETF'].apply(lambda x: '=BDP("{}"&" EQUITY","PX_VOLUME")'.format(x))
    vol_df['VOLUME_AVG_30D'] = vol_df['ETF'].apply(lambda x: '=BDP("{}"&" EQUITY","VOLUME_AVG_30D")'.format(x))
    vol_df['FUND_EXPENSE_RATIO'] = vol_df['ETF'].apply(lambda x: '=BDP("{}"&" EQUITY","FUND_EXPENSE_RATIO")'.format(x))
    vol_df['DVD_YIELD'] = vol_df['ETF'].apply(lambda x: '=BDP("{}"&" EQUITY","DIVIDEND_12_MONTH_YIELD")'.format(x))
    fed_df = pd.DataFrame(index=[0])
    pd_df = pd.DataFrame(index=[0])
    prdvd_df = pd.DataFrame(index=[0])
    st_df = pd.DataFrame(index=[0])
    stc_df = pd.DataFrame(index=[0])
    ctr_df = pd.DataFrame(index=[0])
    ctrh_df = pd.DataFrame(index=[0])
    wgt_df = pd.DataFrame(index=[0])
    rcl_df = pd.DataFrame(index=[0])
    acl_df = pd.DataFrame(index=[0])
    aclc_df = pd.DataFrame(index=[0])
    factor_df = pd.DataFrame(index=[0])
    st_date = "1900-01-01"
    ed_date = "2022-11-30"

    # factor_list = ["PVALUEUS INDEX", "PGRWTHUS INDEX", "PMOMENUS INDEX", "PDIVYUS INDEX", "PEARNVUS INDEX", "PVOLAUS INDEX", "PPROFTUS INDEX", "PTRADEUS INDEX", "PSIZEUS INDEX", "PLEVERUS INDEX"]
    for index in factor_list:
        factor_df.loc[0, index + '_date'] = '=BDH("{}","PX_LAST","{}","{}")'.format(index, st_date, ed_date)
        factor_df.loc[0, index] = ''

    # fed_list = ["FEDL01 INDEX", "LUATTRUU INDEX", "SPX INDEX", "INDU INDEX", "CCMP INDEX"]
    for index in fed_list:
        fed_df.loc[0, index + '_date'] = '=BDH("{}","PX_LAST","{}","{}")'.format(index, st_date, ed_date)
        fed_df.loc[0, index] = ''

    for etf in universe['ETF'].tolist():
        pd_df.loc[0, etf+'_date'] = '=BDH("{}"&" EQUITY","PX_LAST","{}","{}")'.format(etf,st_date,ed_date)
        pd_df.loc[0, etf] = ''

        wgt_df.loc[0, etf+'_date'] = "=BQL(\"members(\'"+etf+" EQUITY"+"\',type=Holdings)\",\"ID().weights\",\"Showids=true\",\"date=({})\")".format(ed_date)
        wgt_df.loc[0, etf] = ''

        st_df.loc[0, etf+'_date'] = '=BDS("{}","hb_industry_sector_allocation")'.format(etf+" EQUITY")
        st_df.loc[0, etf] = ''

        stc_df.loc[0, etf+'_date'] = '=BDS("{}","hb_industry_group_alloc")'.format(etf+" EQUITY")
        stc_df.loc[0, etf] = ''

        ctr_df.loc[0, etf+'_date'] = '=BDS("{}","hb_geo_country_region_allocation")'.format(etf+" EQUITY")
        ctr_df.loc[0, etf] = ''

        ctrh_df.loc[0, etf+'_date'] = '=BDS("{}","hb_geo_cntry_alloc")'.format(etf+" EQUITY")
        ctrh_df.loc[0, etf] = ''

        rcl_df.loc[0, etf+'_date'] = '=BDS("{}","hb_rating_class_allocation")'.format(etf+" EQUITY")
        rcl_df.loc[0, etf] = ''

        acl_df.loc[0, etf+'_date'] = '=BDS("{}","hb_asset_class_allocation")'.format(etf+" EQUITY")
        acl_df.loc[0, etf] = ''

        aclc_df.loc[0, etf+'_date'] = '=BDS("{}","fund_asset_alloc_calc")'.format(etf+" EQUITY")
        aclc_df.loc[0, etf] = ''

        prdvd_df.loc[0, etf + '_date'] = '=BDH("{}"&" EQUITY","TOT_RETURN_INDEX_GROSS_DVDS","{}","{}")'.format(etf,st_date,ed_date)
        prdvd_df.loc[0, etf] = ''



    writer = pd.ExcelWriter('//172.16.130.210/금융공학운용부문/J/김효정/Bloomberg/글로벌인컴/bdp.xlsx', engine='openpyxl')
    universe.to_excel(writer, sheet_name='universe')
    pd_df.to_excel(writer, sheet_name='price')
    prdvd_df.to_excel(writer, sheet_name='price_d')
    vol_df.to_excel(writer, sheet_name='volume')
    wgt_df.to_excel(writer, sheet_name='weight')
    st_df.to_excel(writer, sheet_name='style')
    stc_df.to_excel(writer, sheet_name='style_c')
    ctr_df.to_excel(writer, sheet_name='country')
    ctrh_df.to_excel(writer, sheet_name='country_h')
    rcl_df.to_excel(writer, sheet_name='rating')
    acl_df.to_excel(writer, sheet_name='asset')
    aclc_df.to_excel(writer, sheet_name='asset_c')
    fed_df.to_excel(writer, sheet_name='fed')
    factor_df.to_excel(writer, sheet_name='factor')

    writer.save()


def reform_df(df, ticker_list):

    ticker_list = list(set(ticker_list)&set(df.columns))
    pivot = df[ticker_list].columns[list(df[ticker_list].count()).index(max(df[ticker_list].count()))]
    rf_df = df[[pivot+"_date"]].rename(columns={pivot+"_date":"Index"})
    for ticker in ticker_list:
        part_df = df[[ticker+"_date", ticker]].rename(columns={ticker+"_date":"Index"}).dropna()
        if len(part_df)>0:
            rf_df = pd.merge(rf_df, part_df, left_on='Index', right_on='Index', how='outer')
    return rf_df.sort_values(by='Index').set_index('Index')

def draw_eco(up, down, bb_rf_dict, nm, file_nm, col):

    plt.figure(figsize=(18, 10))
    if nm=='before':
        plt.plot(bb_rf_dict['fed'][col].loc[:'2000-01-01'], color='black')
    elif nm=='after':
        plt.plot(bb_rf_dict['fed'][col].loc['2000-01-01':], color='black')
    else:
        plt.plot(bb_rf_dict['fed'][col], color='black')

    for up_tick in up:
        plt.axvspan(up_tick[0],up_tick[1], color='red',alpha=0.5)
    for down_tick in down:
        plt.axvspan(down_tick[0],down_tick[1], color='blue',alpha=0.5)
    plt.savefig('output/plot/eco_{}_{}.png'.format(file_nm, nm))
    plt.clf()
    return 0

def draw_interst_rate_index(up, down, nm, bb_rf_dict):
    plt.figure(figsize=(20, 10))
    idx_list = ["LUATTRUU INDEX", "SPX INDEX", "INDU INDEX", "CCMP INDEX"]
    for idx in idx_list:
        if nm=='before':
            bb_rf_dict['fed'][idx+"(acc)"] = (bb_rf_dict['fed'][idx].loc["1954-07-01":"2000-01-01"].pct_change() + 1).fillna(1).cumprod()
            fed = bb_rf_dict['fed']['FEDL01 INDEX'].loc["1954-07-01":"2000-01-01"]
        elif nm == 'after':
            bb_rf_dict['fed'][idx+"(acc)"] = (bb_rf_dict['fed'][idx].loc["2000-01-01":].pct_change() + 1).fillna(1).cumprod()
            fed = bb_rf_dict['fed']['FEDL01 INDEX'].loc["2000-01-01":]
        else:
            bb_rf_dict['fed'][idx + "(acc)"] = (bb_rf_dict['fed'][idx].pct_change() + 1).fillna(
                1).cumprod()
            fed = bb_rf_dict['fed']['FEDL01 INDEX']
    bb_rf_dict['fed'][list(map(lambda x:x+"(acc)", idx_list))].dropna().plot.line()

    # (bb_rf_dict['fed']["FEDL01 INDEX"].pct_change() + 1).fillna(1).cumprod()
    # plt.plot(bb_rf_dict['fed']['FEDL01 INDEX'], color='black')
    for up_tick in up:
        plt.axvspan(up_tick[0],up_tick[1], color='red',alpha=0.5)
    for down_tick in down:
        plt.axvspan(down_tick[0],down_tick[1], color='blue',alpha=0.5)

    plt.legend()
    plt.savefig('output/plot/eco_지수+금리_{}.png'.format(nm))
    plt.plot(fed, color='black')
    plt.savefig('output/plot/eco_지수+금리o_{}.png'.format(nm))
    plt.clf()

def draw_etf_comp(sheet, pref_df, bb_rf_dict):
    pref_etf = list(set(pref_df['ETF']) & set(bb_rf_dict[sheet].columns))
    pref_bb = bb_rf_dict[sheet][pref_etf]
    pref_bb['TF'] = pref_bb.apply(lambda row: row.fillna(0).sum() > 0.1, axis=1)
    pref_bb = pref_bb[pref_bb['TF']==True]
    del pref_bb['TF']
    if sheet not in ['price', 'fed', 'weight', 'factor', 'price_d']:
        # figsize = (18, 10)
        plt.figure(figsize=(18, 10))
        sns.set(font_scale=1.3)
        sns.heatmap(pref_bb.fillna(0), cmap='Greens', linewidths=1, linecolor='black')
        plt.savefig('output/plot/pref_{}.png'.format(sheet), pad_inches=2)
        plt.clf()
        pref_bb.fillna(0).to_excel('output/xlsx/pref_{}.xlsx'.format(sheet))
    pass

def reform_df_all(pref_df, plot=False):
    bb_dict = dict()
    bb_rf_dict = dict()
    sheet_list = ['price', 'weight', 'style', 'style_c', 'country', 'country_h', 'rating', 'asset', 'asset_c', 'fed', 'price_d', 'factor']
    for sheet in sheet_list:
        print(sheet)
        bb_dict[sheet] = pd.read_excel('data/bdp_updated.xlsx', sheet_name=sheet)
        if sheet=='weight':
            bb_dict[sheet] = bb_dict[sheet].iloc[1:]

        if sheet=='fed':
            bb_rf_dict[sheet] = reform_df(bb_dict[sheet], fed_list).ffill()
        elif sheet=='factor':
            bb_rf_dict[sheet] = reform_df(bb_dict[sheet], factor_list)
        else:
            bb_rf_dict[sheet] = reform_df(bb_dict[sheet], universe['ETF'].tolist())
        pref_etf = list(set(pref_df['ETF']) & set(bb_rf_dict[sheet].columns))
        pref_bb = bb_rf_dict[sheet][pref_etf]
        pref_bb['TF'] = pref_bb.apply(lambda row: row.fillna(0).sum() > 0.1, axis=1)
        pref_bb = pref_bb[pref_bb['TF']==True]
        del pref_bb['TF']
        if plot:
            draw_etf_comp(sheet, pref_df, bb_rf_dict)
    return bb_dict, bb_rf_dict

def make_profit(col_list, assset_class_rf, file_nm, assset_dict=None):
    assset_class_rf = assset_class_rf.ffill()

    period_profit = pd.DataFrame(index=col_list)

    period_profit['금리인상기(22.03 이후)'] = (assset_class_rf.iloc[-1] / assset_class_rf.loc['2022-03-01'] - 1)*100
    period_profit['6M'] = (assset_class_rf.iloc[-1] / assset_class_rf.loc['2022-05-31'] - 1)*100
    period_profit['3M'] = (assset_class_rf.iloc[-1] / assset_class_rf.loc['2022-08-31'] - 1)*100
    period_profit['1M'] = (assset_class_rf.iloc[-1] / assset_class_rf.loc['2022-10-31'] - 1)*100
    if assset_dict is not None:
        period_profit.index = list(map(lambda x:assset_dict[x], period_profit.index))
    for col in period_profit.columns:
        period_profit[col] = period_profit[col].apply(lambda x: str(round(x, 2)) + "%")
    # period_profit.values = [list(map(lambda x:str(round(x,2))+"%", row)) for row in period_profit.values]
    period_profit.to_excel('output/xlsx/{}.xlsx'.format(file_nm))


    s_period_profit = pd.DataFrame(index=col_list)
    date_list = assset_class_rf.index
    month_list = ['2022-03','2022-04','2022-05','2022-06','2022-07','2022-08','2022-09','2022-10','2022-11',]
    for month in month_list:
        print(month)
        dates = list(filter(lambda x: str(x)[:7]==month, date_list))
        min_dt = min(dates)
        max_dt = max(dates)
        s_period_profit[month] = (assset_class_rf.loc[max_dt]/assset_class_rf.loc[min_dt] -1)*100
        s_period_profit[month] = s_period_profit[month].apply(lambda x:str(round(x,2))+"%")
    if assset_dict is not None:
        s_period_profit.index = list(map(lambda x:assset_dict[x], s_period_profit.index))
    s_period_profit.to_excel('output/xlsx/{}_s.xlsx'.format(file_nm))

if __name__=="__main__":
    factor_list = ["PVALUEUS INDEX", "PGRWTHUS INDEX", "PMOMENUS INDEX", "PDIVYUS INDEX", "PEARNVUS INDEX",
                   "PVOLAUS INDEX", "PPROFTUS INDEX", "PTRADEUS INDEX", "PSIZEUS INDEX", "PLEVERUS INDEX"]
    fed_list = ["FEDL01 INDEX", "BBDXY INDEX", "DXY INDEX", "LUATTRUU INDEX", "SPX INDEX", "INDU INDEX", "CCMP INDEX"]
    universe = make_universe()
    #################################
    # make_bdp(universe,factor_list, fed_list)
    plot = False
    #################################
    fed_df = pd.read_excel('data/bdp_updated.xlsx', sheet_name='fed')
    vol_df = pd.read_excel('data/bdp_updated.xlsx', sheet_name='volume')
    vol_df['TF'] = vol_df.apply(lambda row: row.loc['PX_VOLUME']>10000 and row.loc['VOLUME_AVG_30D']>10000, axis=1)
    filtered_vol_df = vol_df[vol_df['TF']==True]
    pref_df = filtered_vol_df[filtered_vol_df['자산군']=='우선주']
    bb_dict, bb_rf_dict = reform_df_all(pref_df, plot=True)

    assset_dict = { 'SPX INDEX' : "미국 주식",
    'LF98TRUU INDEX':"하이일드",    'LD08TRUU INDEX':"국채", 'LUACTRUU INDEX':"회사채",
    'EMUSTRUU INDEX':"신흥국 채권",  'FNPSI INDEX':"우선주",   'FNRE INDEX':"리츠"}
    assset_class = pd.read_excel('data/자산군별 수익률.xlsx')
    assset_class_rf = reform_df(assset_class, list(assset_dict.keys()))

    # period_profit = pd.DataFrame(index=list(assset_dict.keys()))
    #
    # period_profit['금리인상기(22.03 이후)'] = (assset_class_rf.iloc[-1] / assset_class_rf.iloc[0] - 1)*100
    # period_profit['6M'] = (assset_class_rf.iloc[-1] / assset_class_rf.loc['2022-05-31'] - 1)*100
    # period_profit['3M'] = (assset_class_rf.iloc[-1] / assset_class_rf.loc['2022-08-31'] - 1)*100
    # period_profit['1M'] = (assset_class_rf.iloc[-1] / assset_class_rf.loc['2022-10-31'] - 1)*100
    # period_profit.index = list(map(lambda x:assset_dict[x], period_profit.index))
    # for col in period_profit.columns:
    #     period_profit[col] = period_profit[col].apply(lambda x: str(round(x, 2)) + "%")
    # # period_profit.values = [list(map(lambda x:str(round(x,2))+"%", row)) for row in period_profit.values]
    # period_profit.to_excel('output/xlsx/자산군별 수익률.xlsx')
    #
    # s_period_profit = pd.DataFrame(index=list(assset_dict.keys()))
    # date_list = assset_class_rf.index
    # month_list = ['2022-03','2022-04','2022-05','2022-06','2022-07','2022-08','2022-09','2022-10','2022-11',]
    # for month in month_list:
    #     print(month)
    #     dates = list(filter(lambda x: str(x)[:7]==month, date_list))
    #     min_dt = min(dates)
    #     max_dt = max(dates)
    #     s_period_profit[month] = (assset_class_rf.loc[max_dt]/assset_class_rf.loc[min_dt] -1)*100
    #     s_period_profit[month] = s_period_profit[month].apply(lambda x:str(round(x,2))+"%")
    # s_period_profit.index = list(map(lambda x:assset_dict[x], s_period_profit.index))
    # s_period_profit.to_excel('output/xlsx/자산군별 수익률_s.xlsx')
    make_profit(list(assset_dict.keys()), assset_class_rf, "자산군별 수익률", assset_dict)

    make_profit(pref_df['ETF'].to_list(), bb_rf_dict['price'][pref_df['ETF'].to_list()].ffill(), "우선주 ETF 수익률")



    # todo: 금리
    up1 = [('1954-07-01','1957-08-23'),('1958-07-30','1959-09-11'),('1963-07-16','1969-07-17'), ('1971-02-24','1974-07-24'), ('1977-01-12','1980-04-18'), ('1986-12-12', '1989-05-31'), ('1994-01-20','1995-10-25')]
    down1 = [('1957-11-15','1958-02-26'),('1960-06-09','1961-06-13'),('1969-08-06','1970-12-29'),('1974-07-24','1975-03-12'),('1981-01-01','1983-05-25'),('1984-08-27','1985-03-27'), ('1989-05-31', '1992-01-07')]
    up2 = [('2000-01-01','2000-07-03'),('2004-06-10','2006-07-03'),('2016-12-15','2019-07-01'), ('2022-03-16','2022-11-30')]
    down2 = [('2000-12-18','2003-06-25'),('2007-08-09','2008-02-05'),('2008-09-15','2008-12-18'),('2019-07-01','2020-03-16')]

    if plot:
        draw_eco(up=up1, down=down1, bb_rf_dict=bb_rf_dict, nm='before',file_nm='금리', col='FEDL01 INDEX')
        draw_eco(up2, down2, bb_rf_dict, nm='after',file_nm='금리', col='FEDL01 INDEX')
        draw_eco(up1+up2, down1+down2, bb_rf_dict, nm='all',file_nm='금리', col='FEDL01 INDEX')


        draw_eco(up=up1, down=down1, bb_rf_dict=bb_rf_dict, nm='before',file_nm='달러', col='DXY INDEX')
        draw_eco(up2, down2, bb_rf_dict, nm='after',file_nm='달러', col='DXY INDEX')
        draw_eco(up1+up2, down1+down2, bb_rf_dict, nm='all',file_nm='달러', col='DXY INDEX')

        bb_rf_dict['fed']["DXY INDEX(acc)"] = (bb_rf_dict['fed']["DXY INDEX"].dropna().pct_change() + 1).fillna(
            1).cumprod()
        bb_rf_dict['fed']["FEDL01 INDEX(acc)"] = (bb_rf_dict['fed']["FEDL01 INDEX"].dropna().pct_change() + 1).fillna(
            1).cumprod()
        draw_eco(up=up1, down=down1, bb_rf_dict=bb_rf_dict, nm='before',file_nm='금리+달러', col=['DXY INDEX(acc)','FEDL01 INDEX(acc)'])
        draw_eco(up2, down2, bb_rf_dict, nm='after',file_nm='금리+달러', col=['DXY INDEX(acc)','FEDL01 INDEX(acc)'])
        draw_eco(up1+up2, down1+down2, bb_rf_dict, nm='all',file_nm='금리+달러', col=['DXY INDEX(acc)','FEDL01 INDEX(acc)'])


        draw_interst_rate_index(up1, down1, nm='before', bb_rf_dict=bb_rf_dict)
        draw_interst_rate_index(up2, down2, nm='after', bb_rf_dict=bb_rf_dict)



    # todo: 팩터
    plt.figure(figsize=(18, 10))
    for idx in factor_list:
        bb_rf_dict['factor'][idx+"(acc)"] = (bb_rf_dict['factor'][idx].pct_change() + 1).fillna(1).cumprod()
    bb_rf_dict['factor'][list(map(lambda x:x+"(acc)", factor_list))].plot.line()

    # (bb_rf_dict['fed']["FEDL01 INDEX"].pct_change() + 1).fillna(1).cumprod()
    # bb_rf_dict['fed']['FEDL01 INDEX']
    # plt.plot((bb_rf_dict['fed']["FEDL01 INDEX"].pct_change() + 1).fillna(1).cumprod(), color='black')
    for up_tick in up2:
        plt.axvspan(up_tick[0],up_tick[1], color='red',alpha=0.5)
    for down_tick in down2:
        plt.axvspan(down_tick[0],down_tick[1], color='blue',alpha=0.5)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig('output/plot/eco_팩터+금리.png')
    plt.clf()

    # todo: 팩터
    plt.figure(figsize=(25, 10))
    for idx in list(set(factor_list)-{"PVALUEUS INDEX"}):
        bb_rf_dict['factor'][idx.replace("US INDEX","")] = (bb_rf_dict['factor'][idx].pct_change() + 1).fillna(1).cumprod()
    bb_rf_dict['factor'][list(map(lambda x:x.replace("US INDEX",""), list(set(factor_list)-{"PVALUEUS INDEX"})))].plot.line()

    # (bb_rf_dict['fed']["FEDL01 INDEX"].pct_change() + 1).fillna(1).cumprod()
    # bb_rf_dict['fed']['FEDL01 INDEX']
    # plt.plot((bb_rf_dict['fed']["FEDL01 INDEX"].pct_change() + 1).fillna(1).cumprod(), color='black')
    for up_tick in up2:
        plt.axvspan(up_tick[0],up_tick[1], color='red',alpha=0.5)
    for down_tick in down2:
        plt.axvspan(down_tick[0],down_tick[1], color='blue',alpha=0.5)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 5})
    plt.savefig('output/plot/eco_팩터+금리exVALUE.png')

    # todo: 팩터_기간
    plt.figure(figsize=(25, 10))
    for idx in list(set(factor_list)-{"PVALUEUS INDEX"}):
        bb_rf_dict['factor'][idx.replace("US INDEX","")] = (bb_rf_dict['factor'][idx].pct_change() + 1).fillna(1).cumprod()
    bb_rf_dict['factor'][list(map(lambda x:x.replace("US INDEX",""), list(set(factor_list)-{"PVALUEUS INDEX"})))].plot.line()

    # (bb_rf_dict['fed']["FEDL01 INDEX"].pct_change() + 1).fillna(1).cumprod()
    # bb_rf_dict['fed']['FEDL01 INDEX']
    # plt.plot((bb_rf_dict['fed']["FEDL01 INDEX"].pct_change() + 1).fillna(1).cumprod(), color='black')
    for up_tick in up2:
        plt.axvspan(up_tick[0],up_tick[1], color='red',alpha=0.5)
    for down_tick in down2:
        plt.axvspan(down_tick[0],down_tick[1], color='blue',alpha=0.5)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 5})
    plt.savefig('output/plot/eco_팩터+금리exVALUE.png')
    print(1)









    # pd_df = pd.read_excel('data/bdp_updated.xlsx', sheet_name='price')
    # wgt_df = pd.read_excel('data/bdp_updated.xlsx', sheet_name='weight')
    # st_df = pd.read_excel('data/bdp_updated.xlsx', sheet_name='style')
    # stc_df = pd.read_excel('data/bdp_updated.xlsx', sheet_name='style_c')
    # ctr_df = pd.read_excel('data/bdp_updated.xlsx', sheet_name='country')
    # ctrh_df = pd.read_excel('data/bdp_updated.xlsx', sheet_name='country_h')
    # rcl_df = pd.read_excel('data/bdp_updated.xlsx', sheet_name='rating')
    # acl_df = pd.read_excel('data/bdp_updated.xlsx', sheet_name='asset')
    # aclc_df = pd.read_excel('data/bdp_updated.xlsx', sheet_name='asset_c')

    # eft_list = pd_df.loc[0, list(map(lambda x: x+'_date', universe['ETF'].tolist()))]
    # min_idx = (eft_list.tolist()).index(min(eft_list))
    # long_etf = eft_list.index[min_idx].replace('_date','')
    #
    # pd_df_rf = pd_df[[long_etf+'_date', long_etf]].rename(columns={long_etf+'_date':'Date'})
    # for col in universe['ETF'].tolist():
    #     if col != long_etf:
    #         pd_df_rf = pd.merge(pd_df[[col+'_date', col]], pd_df_rf, left_on=[col+'_date'], right_on=['Date'], how='right')
    #         del pd_df_rf[col+'_date']
    # pd_df_rf = pd_df_rf.set_index('Date')
    # pd_df_rf = pd_df_rf.ffill()
    #
    #
    # vol_df['TF'] = vol_df.apply(lambda row: row.loc['PX_VOLUME']>10000 and row.loc['VOLUME_AVG_30D']>10000, axis=1)
    # filtered_vol_df = vol_df[vol_df['TF']==True]
    # pref_df = filtered_vol_df[filtered_vol_df['자산군']=='우선주']
    # pref_ticker = list()
    # for pref in list(map(lambda x: x+"_date",pref_df['ETF'])):
    #     pref_ticker += wgt_df[pref].values.tolist()
    # pref_ticker = list(set(pref_ticker))

    print(1)

    # index = [0.01, 0.02, 0.03, 0.05]
    # idx = [i for i in range(len(index))]
    # index2idx = dict(zip(index,idx))
    # d2_list = np.array([[0.05, 0.02, 0.03],
    #  [0.02, 0.03, 0.05],
    #  [0.05, 0.01, 0.02]])
    # d2_shape = d2_list.shape
    # d2_list = np.array(list(map(lambda x:index2idx[x],d2_list.flatten()))).reshape(d2_shape)


