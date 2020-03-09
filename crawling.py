#!/usr/bin/env python
# coding: utf-8
"""
# 네이버 영화에서 크롤링
# 문제점: 영화 갯수가 몇개 되지 않는다


import requests
from bs4 import BeautifulSoup as bs
import openpyxl
from urllib.request import urlretrieve
import ssl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["영화제목", "영화장르"])

raw = requests.get("https://movie.naver.com/movie/running/current.nhn",
                  headers={'User-Agent':'Mozilla/5.0'})
html = bs(raw.text, 'html.parser')

movie = html.select("div.lst_wrap li")

for i, m in enumerate(movie):
    # 영화제목 수집
    title = m.select_one("dt.tit a")
    
    # 영화장르 수집
    genre = m.select("dl.info_txt1 dd:nth-of-type(1) a")
    
    genre_list = [g.text for g in genre]
    genre_str = ','.join(genre_list)
    sheet.append([title.text, genre_str])

    title_rename = title.text.replace(" ", "").replace(":", "_")

wb.save("navermovie.xlsx")
"""

# 참고사이트: 네이버 영화 데이터 크롤링하기(https://somjang.tistory.com/entry/Python%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%98%81%ED%99%94-%EB%8D%B0%EC%9D%B4%ED%84%B0-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%98%EA%B8%B0)
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests
import time
import re
import pandas as pd


links = []
# 영화 링크 크롤링
for page in range(10):
    url = "https://series.naver.com/movie/recentList.nhn?orderType=sale&sortingType=&tagCode=&page=" + str(page + 1)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    movielinks = soup.select('div.lst_thum_wrap ul li a[href]')

    for movielink in movielinks:
        link = str(movielink.get('href'))
        links.append("https://series.naver.com"+link)



genre_list = []
title_list = []

# 크롬드라이버 창 안열리고 실행
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)

for link in links:
    driver.switch_to.window(driver.window_handles[-1]) 
    time.sleep(0.1)
    driver.get(link)
    time.sleep(0.1)
    driver.switch_to.window(driver.window_handles[0]) 
    time.sleep(0.3)
    
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    
    flag = soup.text[0:10]
    flag = "".join(flag) 
    flag = flag.replace('\n', '')


    if flag == '네이버':
        time.sleep(1)
        
        genre = driver.find_element_by_css_selector('li.info_lst > ul > li:nth-child(4)').get_attribute('textContent')
        genre = genre.replace('장르','') 
        #genre = genre.split('/') 
        genre_list.append(genre)
        
        movieurl = driver.find_element_by_css_selector('span.al_r > a').get_attribute('href')
        movie_req = requests.get(movieurl) 
        movie_soup = BeautifulSoup(movie_req.text, 'lxml') 
        titles = movie_soup.select('div.mv_info > h3.h_movie > a')
        title = titles[0].text
        title = title.replace('.', '')
        title_list.append(title)


wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["titles", "genres"])

for i in range(len(title_list)):
    sheet.append([title_list[i], genre_list[i]])

    wb.save("movie.xlsx")





