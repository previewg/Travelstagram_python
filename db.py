import pandas as pd
import numpy as np

def insta_db_tot():
    # 인스타 db
    df = pd.read_excel('static/insta_db.xlsx')
    tot = df.sort_values(by=df.columns[-1], ascending=False)
    tot = tot.reset_index()
    return tot

def insta_db_hot():
    # 인스타 db
    df = pd.read_excel('static/insta_db.xlsx')
    gap = pd.DataFrame()
    gap['국가'] = df['국가']

    gap['차이'] = df[df.columns[-1]]-df[df.columns[-2]]
    gtop = gap.sort_values(by='차이', ascending=False)[:20]
    gtop = gtop.reset_index()

    return gtop

def restrict_db(country):
    # 통관 규정
    rdic=dict()

    restrict = pd.read_excel('static/traveler_restrict_2015.xlsx', index_col=[0,1])
    restrict = restrict.reset_index()

    ctmp=restrict[ restrict['국가']== country]
    ctmp=ctmp[['휴대품', '통관기준']]

    ctmp2 = ctmp.groupby('휴대품')
    for idx, value in ctmp2:
        rdic[idx] = value['통관기준'].values
    
    return rdic
