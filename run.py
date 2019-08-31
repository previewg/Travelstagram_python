from flask import Flask, render_template, url_for, request, redirect, session, jsonify
import pandas as pd
import numpy as np
from crawling import youtube_crawling, basic_content, tripadviser_crawling
from db import insta_db_tot, restrict_db, insta_db_hot

# 여행지 추천
import random

# import os

# 인스타db
tot = insta_db_tot()
hot = insta_db_hot()

app = Flask(__name__)


@app.route('/')
def home():
    # 중복되지 않는 3개의 랜덤 숫자를 뽑아냄(0~19)
    rands = set()
    while len(rands) < 3:
        rands.add(random.randint(0,19))
    rands = list(rands)
    return render_template('index.html', tot=tot, hot=hot, rands=rands)

@app.route('/search')
def search():
    cname = request.args.get('country')
    
    # 입력 오류 처리
    crow = tot[tot['국가']==cname]
    if not list(crow.index):
        return render_template('error.html', msg='나라 이름을 다시 확인해주세요')
    
    # 랭크 정보
    rank = [ crow.index[0]+1, crow[tot.columns[-1]].values[0] ]

    addr = 'static/img/countries/%s1.jpg' %cname
    
    imgflag=True

    try:
        with open(addr, 'r', encoding = 'utf-8') as f:
            print('open img')
    except Exception as e:
        imgflag = False
        print('no img')
    else:
        pass

    # 네이버 나라 정보 크롤링(bs4)
    basic_src = basic_content(cname)
    with open('templates/basic_src.html', 'w', encoding = 'utf-8') as f:
        f.write('%s' % basic_src)
    print('naver 크롤링 완료')

    # 트립어드바이저 크롤링
    trip=tripadviser_crawling(cname)
    trip = pd.DataFrame( trip )
    trip.transpose()
    print('트립어드바이저 크롤링 완료')

    # 통관 규정(db)
    rdic = restrict_db(cname)

    # print(rdic)

    # 유튜브 크롤링
    yout = youtube_crawling(cname)
    yout = pd.DataFrame( yout )
    yout.transpose()
    print('유튜브 크롤링 완료')

    return render_template('index2.html', cname=cname, rank=rank, searchdic=yout, rdic=rdic, trip=trip, imgflag=imgflag)
    


if __name__=='__main__':# 이코드를 메인으로 구동시 서버가동
    app.config['TEMPLATES_AUTO_RELOAD'] = True # 검색마다 include된 웹 페이지를 업데이트(debug true를 사용하지 않고)
    app.run()
