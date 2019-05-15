from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
import time
from random import randint
import pandas as pd
import re
import math

resturant_region = '이태원'
resturant_name = '우육미엔'
query = resturant_region + " " + resturant_name

Naverblog_url_Beforequery = 'https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query='
Naverblog_url_Afterquery = '&sm=tab_pge&srchby=all&st=sim&where=post&start='

delete_url = 'https://help.naver.com/support/alias/search/word/word_1.naver'


def Naverblog_query_Fetch(query):
    print('Query:', query)
    Naverblog_url = Naverblog_url_Beforequery + query + Naverblog_url_Afterquery + str(1)
    print(Naverblog_url)
    browser.get(Naverblog_url)

    blog_total_amount = browser.find_element_by_css_selector(
        '#main_pack > div.blog.section._blogBase._prs_blg > div > span').text
    blog_total_amount = re.split('[:. ]+', blog_total_amount)
    blog_total_amount = blog_total_amount[2]
    blog_total_amount = blog_total_amount.replace(',', '')
    blog_total_amount = blog_total_amount[:-1]
    print('Total amount of news:', blog_total_amount)
    blog_total_amount = math.ceil(int(blog_total_amount) / 10)

    blog_href_list = []

    #     for i in range(0, blog_total_amount):
    for i in range(0, 4):
        navernews_url = Naverblog_url_Beforequery + query + Naverblog_url_Afterquery + str(10 * i + 1)
        browser.get(navernews_url)
        print(
            browser.find_element_by_css_selector('#main_pack > div.blog.section._blogBase._prs_blg > div > span').text)
        page_blog_href = browser.find_elements_by_css_selector('dl > dt > a')
        page_blog_href_list = [link.get_attribute('href') for link in page_blog_href]
        blog_href_list.append(page_blog_href_list)
        sleep(randint(1, 5))

    Naverblog_list = []
    for list_element in blog_href_list:
        for element in list_element:
            Naverblog_list.append(element)

    Naverblog_list = list(set(Naverblog_list))
    Naverblog_list = [link.replace(delete_url, '') for link in Naverblog_list]
    Naverblog_list = [link for link in Naverblog_list if len(link) != 0]

    print('The amount of total news: ', len(Naverblog_list))
    print(Naverblog_list)

    return Naverblog_list


browser = webdriver.Chrome('/Users/jiwonjang/python/chromedriver')
Naverblog_query_Fetch(query)
