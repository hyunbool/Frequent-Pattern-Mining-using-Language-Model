# 네이버 영화 데이터 크롤링하기(https://somjang.tistory.com/entry/Python%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%98%81%ED%99%94-%EB%8D%B0%EC%9D%B4%ED%84%B0-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%98%EA%B8%B0)
from bs4 import BeautifulSoup
import requests
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd

def get