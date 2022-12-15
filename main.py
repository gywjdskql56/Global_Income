import pandas as pd
import os
import re


file_list = os.listdir('universe_data/')
file_list.remove('신규포트 정리_201910.xlsx')
file_list.remove('신규포트정리_2022.xlsx')
sheet_name_list = ['배당주', '리츠', 'HYPFCB','PEF','인프라']

total_data= pd.DataFrame()
data = dict()
for file in file_list:
    for sheet in sheet_name_list:
        if sheet == '배당주':
            if file == '신규포트 정리.xlsx':
                continue
            df = pd.DataFrame()
            df['Security ID'] = pd.read_excel('universe_data/' + file, sheet_name=sheet)['Ticker']
            df['Portfolio Name'] = '배당주'
        else:
            print('**', file, '----', sheet)
            df = pd.read_excel('universe_data/'+file, sheet_name=sheet)[['Portfolio Name','Security ID']]
            # data[sheet] = list(set(df.dropna().tolist()))
            # print('Security ID' in list(data[sheet].columns))
        total_data = total_data.append(df)
recent_df_1 = pd.read_excel('universe_data/신규포트 정리_201910.xlsx', sheet_name='Sheet2')[['Portfolio Name','Security ID']]
recent_df_2 = pd.read_excel('universe_data/신규포트정리_2022.xlsx')
recent_df_2 = recent_df_2[['Portfolio Name1', 'Security ID1']].rename(columns={'Portfolio Name1':'Portfolio Name','Security ID1':'Security ID'}).append(recent_df_2[['Portfolio Name2','Security ID2']].rename(columns={'Portfolio Name2':'Portfolio Name','Security ID2':'Security ID'})).append(recent_df_2[['Portfolio Name3','Security ID3']].rename(columns={'Portfolio Name3':'Portfolio Name','Security ID3':'Security ID'}))
total_data = total_data.append(recent_df_1)
total_data = total_data.append(recent_df_2)
total_data = total_data.dropna()
total_data['Security ID'] = total_data['Security ID'].apply(lambda x: str(x).upper())
############################################
# recent_df['Security ID'] = recent_df['Security ID'].apply(lambda x: str(x).upper())
############################################
total_data['Portfolio Name'] = total_data['Portfolio Name'].apply(lambda x: str(x).replace('533700_',''))
total_data = total_data.dropna(subset=['Portfolio Name','Security ID']).drop_duplicates(subset=['Security ID'], keep='last')
########################################
# recent_df = recent_df.dropna(subset=['Portfolio Name','Security ID']).drop_duplicates(subset=['Security ID'])
# recent_df['Portfolio Name'] = recent_df['Portfolio Name'].apply(lambda x: str(x).replace('533700_',''))
#######################################

type_list = ['10: 주식', '40: 파생', '70: 수익증권', '80: ETF']
bond_type_list = ['20: 채권', '30: 유동']

fund_df = pd.read_excel('fund_data/펀드명세부_2301_221130.xlsx')
fund_df = fund_df.drop_duplicates(subset=['Ticker'])

fund_df['type'] = fund_df['자산구분'].apply(lambda x: x in type_list)
fund_df_eq = fund_df[fund_df['type']==True]
fund_df_bd = fund_df[fund_df['type']==False]
fund_df_bd[['Security ID']] = fund_df_bd[['Ticker']]
fund_df_bd[['Portfolio Name']] = 'BOND'
fund_df_bd.loc[fund_df_bd['자산구분']=='30: 유동', 'Portfolio Name'] = 'Cash'

except_list = list(set(fund_df_eq.Ticker.dropna()) - set(total_data['Security ID']))
fund_df_eq['Ticker']  = fund_df_eq['Ticker'].apply(lambda x: str(x).upper())


except_list = list(set(fund_df_eq.Ticker.dropna()) - set(total_data['Security ID']))
print(except_list)
# fund_df_added_recent = pd.merge(fund_df_eq, recent_df)
fund_df_added = pd.merge(fund_df_eq, total_data, left_on='Ticker', right_on='Security ID', how='left')
fund_df_added['Portfolio Name'] = fund_df_added['Portfolio Name'].apply(lambda x : 'REIT' if x=='리츠' else x)
fund_df_added['Portfolio Name'] = fund_df_added['Portfolio Name'].apply(lambda x : 'DIV' if x=='배당주' else x)
fund_df_added['Portfolio Name'] = fund_df_added['Portfolio Name'].apply(lambda x : 'INFRA' if x=='인프라' else x)
fund_df_added['Portfolio Name'] = fund_df_added['Portfolio Name'].apply(lambda x : 'PREF' if x=='우선주' else x)
fund_df_added['Portfolio Name'] = fund_df_added['Portfolio Name'].apply(lambda x : 'PREF' if x=='우선주' else x)
# fund_df_added['Security ID'] = fund_df_added['Ticker']

fund_df_eq['in'] = fund_df_eq['Ticker'].apply(lambda x: x in except_list)
temp2 = fund_df_eq[fund_df_eq['in']==True]
temp2[['Ticker','종목명','자산구분','업종','거래국가']].to_excel('except_df.xlsx')
temp2[['Ticker','종목명','자산구분','업종','거래국가']].drop_duplicates(subset=['Ticker']).to_excel('except_df.xlsx',index=False)

del fund_df_eq['in']

fund_df_added = fund_df_added.set_index('Ticker')
fund_df_added.loc[['395400A KS EQUITY', '396690A KS EQUITY', '348950A KS EQUITY', 'J3954001C KS EQUITY', 'J3489501C KS EQUITY'], 'Portfolio Name'] = 'REIT'
fund_df_added.loc['IBE/D SM EQUITY', 'Portfolio Name'] = 'INFRA'
fund_df_added = fund_df_added.reset_index().set_index('종목명')
fund_df_added.loc['미래에셋배당프리미엄증권자(주식혼합)C-F', 'Ticker'] = '1BN4315 KS Equity'
fund_df_added.loc['미래에셋배당프리미엄증권자(주식혼합)C-F', 'Security ID'] = '1BN4315 KS Equity'
fund_df_added.loc['미래에셋차이나배당프리미엄증권자투자신탁1호(주식혼합)종류F', 'Ticker'] = '1AW3954 KS Equity'
fund_df_added.loc['미래에셋차이나배당프리미엄증권자투자신탁1호(주식혼합)종류F', 'Security ID'] = '1AW3954 KS Equity'
fund_df_added = fund_df_added.reset_index()

fund_df_added = fund_df_added.append(fund_df_bd).sort_values('일자')

fund_df_added = fund_df_added.set_index('일자')
# fund_df_added.loc[list(set(fund_df_added.index))[2]]['순자산비'].sum()
# fund_df_added[fund_df_added['Portfolio Name']=='PREF'].loc['2022-05-31'][['Security ID','자산구분','Portfolio Name','순자산비']] /= fund_df_added[fund_df_added['Portfolio Name']=='PREF'].loc['2022-05-31'][['순자산비']].sum()
fund_df_added = fund_df_added.reset_index('일자').dropna(subset=['일자'])
fund_df_added['일자'] = fund_df_added['일자'].apply(lambda x:x.strftime('%Y-%m-%d'))
fund_df_added = fund_df_added.set_index('일자')
writer = pd.ExcelWriter('result/weight.xlsx', engine='xlsxwriter')

# fund_df_added_all = fund_df_added.dropna(subset = ['Security ID'])
# fund_df_added_all['Fixed Weight'] = fund_df_added_all['순자산비'] * 100
fund_df_added.loc[fund_df_added['자산구분']=='30: 유동','Security ID'] = fund_df_added.loc[fund_df_added['자산구분']=='30: 유동','종목명'].apply(lambda x: re.findall('\[(.*?)\]',x)[0]+' Curncy' if '[' in x else '')
df1 = fund_df_added.reset_index().rename(columns={'일자':'Date','순자산비':'Fixed Weight'})[['Date','Portfolio Name','Security ID','Fixed Weight', '종목명' ,'자산구분']]
df1['Portfolio Name'] = '533700_ALL'
df1.to_excel(writer, sheet_name='전체')
fund_df_added_bd = fund_df_added[fund_df_added['type']==True]
for date in list(set(fund_df_added_bd.index)):
    fund_df_added_bd.loc[date,'Fixed Weight'] = fund_df_added_bd.loc[date,'순자산비'] / fund_df_added_bd.loc[date,'순자산비'].sum() * 100
fund_df_added_bd = fund_df_added_bd.reset_index()
df2 = fund_df_added_bd.rename(columns={'일자':'Date'})[['Date','Portfolio Name','Security ID','Fixed Weight', '종목명' ,'자산구분']]
df2['Portfolio Name'] = '533700_ALL_exB'
df2.to_excel(writer, sheet_name='채권제외')
total_asset_df = pd.DataFrame()
for asset in ['LOAN', 'HY', 'CB', 'PREF', 'DIV', 'INFRA', 'UST', 'PEF', 'BDC', 'REIT']:
    asset_df = fund_df_added[fund_df_added['Portfolio Name']==asset]
    asset_df['조정비율'] = 0
    for date in list(set(asset_df.index)):
        asset_df.loc[date, 'Fixed Weight'] = asset_df.loc[date, '순자산비'] / asset_df.loc[date, '순자산비'].sum()  * 100


    asset_df = asset_df.reset_index()
    # asset_df['Fixed Weight'] = asset_df['조정비율'] * 100
    asset_df['Portfolio Name'] = asset_df['Portfolio Name'].apply(lambda x: '533700_'+x)
    asset_df = asset_df.rename(columns={'일자':'Date'})[['Date','Portfolio Name','Security ID','Fixed Weight', '종목명' ,'자산구분']]
    total_asset_df = total_asset_df.append(asset_df)
    asset_df.to_excel(writer, sheet_name=asset)

writer.save()
total_asset_df = total_asset_df.append(df1).append(df2)
total_asset_df = total_asset_df[total_asset_df['자산구분']!='40: 파생']
total_asset_df.to_excel('result/BBU_upload.xlsx')

fund_df_added.to_excel('fund_df.xlsx')

print(1)