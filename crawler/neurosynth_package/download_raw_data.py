# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 23:47:55 2019

@author: Junsol Kim
"""
import neurosynth as ns
from neurosynth.base.dataset import Dataset
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

# crawling 1335 keywords provided in the Neurosynth (behavior, personality, illness, etc)
def download_keywords(driver):
    driver.get('http://neurosynth.org/analyses/terms/')
    df_keyword = pd.DataFrame(columns=['keyword','numstudy','numactivation'])
    
    # expand list (100 rows/page)
    el = driver.find_element_by_name('term-analyses-table_length')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == '100':
            option.click()
            break
    sleep(2)
    
    # get the last page number
    last_page_num = int(driver.find_element_by_id('term-analyses-table_paginate').find_element(By.TAG_NAME, 'span').find_elements(By.TAG_NAME, 'a')[5].text)
    
    #crawl each row for the first page (keyword, number of study, number of activation)
    for row in driver.find_element_by_id('term-analyses-table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr'):
        cols = row.find_elements(By.TAG_NAME, 'td')
        
        keyword = cols[0].find_element(By.TAG_NAME, 'a').text
        numstudy = cols[1].text
        numactivation = cols[2].text
        df_keyword = df_keyword.append({'keyword': keyword, 'numstudy': numstudy, 'numactivation': numactivation}, ignore_index=True)
        print(keyword)
        
    # crawl each row for each page & iterate all the way to the last page
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
        
    df_keyword.to_csv('./keyword_list.csv')


# Download Neurosynth raw data
def download_dataset():
    # Download raw data
    ns.dataset.download(path='./raw_data', unpack=True) #download latest database

# Save dataset instance file (for fast loading of data)
def save_dataset_instance(db_filename, kw_filename, instance_filename):
    # Create a new Dataset instance
    dataset = Dataset('./raw_data/' + db_filename + '.txt')
    # Add some features
    dataset.add_features('./raw_data/' + kw_filename +'.txt')
    # Save new file
    dataset.save('./raw_data/' + instance_filename +'.pkl')
    return dataset



# Split Neurosynth raw data accroding to the designated year
def split_dataset(year):
    raw_data_db = pd.read_csv("./raw_data/database.txt", sep='\t', low_memory=False)
    raw_data_kw = pd.read_csv("./raw_data/features.txt", sep='\t', low_memory=False)
    
    # Dataset until designated year
    until_year_db = raw_data_db.loc[raw_data_db['year'] <= year]
    until_year_kw = raw_data_kw.loc[raw_data_kw['pmid'].isin(until_year_db['id'])]
    
    # Dataset after designated year
    after_year_db = raw_data_db.loc[raw_data_db['year'] > year]
    after_year_kw = raw_data_kw.loc[raw_data_kw['pmid'].isin(after_year_db['id'])]
    
    until_year_db.to_csv("./raw_data/database_until"+str(year)+".txt", header=True, index=False, sep='\t')
    until_year_kw.to_csv("./raw_data/features_until"+str(year)+".txt", header=True, index=False, sep='\t')
    after_year_db.to_csv("./raw_data/database_after"+str(year)+".txt", header=True, index=False, sep='\t')
    after_year_kw.to_csv("./raw_data/features_after"+str(year)+".txt", header=True, index=False, sep='\t')
    




def main():
    driver = webdriver.Chrome('chromedriver.exe')
    # set up basic path
    os.chdir('../../data')
    d = './raw_data'
    if not os.path.exists(d):
        # If there is no raw data, download raw data
        os.mkdir(d)
        download_keywords(driver)
        download_dataset()
        
    save_dataset_instance('database', 'features', 'dataset')        

    # If you need to split your raw data        
    year = 2015
    split_dataset(year)
    save_dataset_instance('database_until'+str(year), 'features_until'+str(year), 'dataset_until'+str(year))
    save_dataset_instance('database_after'+str(year), 'features_after'+str(year), 'dataset_after'+str(year))


if __name__ == '__main__':
    # Set the border year to divide training data and testing data (e.g. 2015)
    main()

