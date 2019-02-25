# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 01:29:38 2017

@author: Junsol Kim
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import glob


driver = webdriver.Chrome('chromedriver.exe')


''' crawling 1335 keywords provided in the Neurosynth (behavior, personality, illness, etc) '''
driver.get('http://neurosynth.org/analyses/terms/')
df_keyword = pd.DataFrame(columns=['keyword','numstudy','numactivation'])

#expand list (100 rows/page)
el = driver.find_element_by_name('term-analyses-table_length')
for option in el.find_elements_by_tag_name('option'):
    if option.text == '100':
        option.click()
        break
sleep(2)

#get the last page number
last_page_num = int(driver.find_element_by_id('term-analyses-table_paginate').find_element(By.TAG_NAME, 'span').find_elements(By.TAG_NAME, 'a')[5].text)

#crawl each row for the first page (keyword, number of study, number of activation)
for row in driver.find_element_by_id('term-analyses-table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr'):
    cols = row.find_elements(By.TAG_NAME, 'td')
    
    keyword = cols[0].find_element(By.TAG_NAME, 'a').text
    numstudy = cols[1].text
    numactivation = cols[2].text
    df_keyword = df_keyword.append({'keyword': keyword, 'numstudy': numstudy, 'numactivation': numactivation}, ignore_index=True)
    print(keyword)
    
#crawl each row for each page & iterate all the way to the last page
for i in range(last_page_num-1):
    driver.find_element_by_id('term-analyses-table_next').click()
    sleep(2)
    for row in driver.find_element_by_id('term-analyses-table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr'):
        cols = row.find_elements(By.TAG_NAME, 'td')
        keyword = cols[0].find_element(By.TAG_NAME, 'a').text
        numstudy = cols[1].text
        numactivation = cols[2].text
        df_keyword = df_keyword.append({'keyword': keyword, 'numstudy': numstudy, 'numactivation': numactivation}, ignore_index=True)
        print(keyword)
    
    sleep(0.5)
    
df_keyword.to_csv('C:/Users/qmpir/OneDrive - 연세대학교 (Yonsei University)/진행 중인 연구/keyword_list.csv')
    
    
'''Download .nii files from Neurosynth for each keyword'''    

for word in df_keyword['keyword']:
    driver.get('http://neurosynth.org/analyses/terms/'+word)
    sleep(5)
    download_buttons = driver.find_elements_by_class_name('download_icon')
    for button in download_buttons[0:2]:
        button.click()
        sleep(1)
        


'''Download missing .nii files'''

'''
for word in df_keyword['keyword']:
    if len(glob.glob("C:/Users/qmpir/OneDrive - 연세대학교 (Yonsei University)/진행 중인 연구/neurosynth 연구/crawled data/"+word+"_association-test_z_FDR_0.01.nii.gz")) < 1:
        driver.get('http://neurosynth.org/analyses/terms/'+word)
        sleep(5)
        download_buttons = driver.find_elements_by_class_name('download_icon')
        for button in download_buttons[0:2]:
            button.click()
            sleep(1)
        print(word, len(glob.glob("C:/Users/qmpir/OneDrive - 연세대학교 (Yonsei University)/진행 중인 연구/neurosynth 연구/crawled data/"+word+"_association-test_z_FDR_0.01.nii.gz")))
'''