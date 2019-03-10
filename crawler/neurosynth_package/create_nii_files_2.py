# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 23:47:55 2019

@author: Junsol Kim
"""


from neurosynth.base.dataset import Dataset
from neurosynth.analysis import meta
import pandas as pd
import os
import shutil


# Load dataset instance (.pkl)
def load_dataset_instance(instance_filename):
    dataset = Dataset.load('./raw_data/' + instance_filename +'.pkl')
    return dataset
    
# Create nii files (association test, uniformity test, and others)
# e.g. if year is 2015 and after is True, it only considers research papers after 2015 when making nii files
def create_nii_files_test(dataset, target_folder, year = None, after = True):
    df_keyword = pd.read_csv('./keyword_list.csv')
    if year is not None:
        raw_data_db = pd.read_csv("./raw_data/database.txt", sep='\t', low_memory=False)
        if after:
            masked_id = set(raw_data_db.loc[raw_data_db['year'] > year]['id'].tolist())
        else:
            masked_id = set(raw_data_db.loc[raw_data_db['year'] <= year]['id'].tolist())
            
        
    for word in df_keyword['keyword'].tolist():
        ids = dataset.get_studies(features=word, frequency_threshold=0.05)
        if year is not None:
            ids = list(set(ids) & masked_id)
        
        
        ma = meta.MetaAnalysis(dataset, ids)
        ma.save_results('./'+target_folder, word)
       
# Leave out uniformity test nii files
def leave_out_uniformity_files(target_folder):
    df_keyword = pd.read_csv('./keyword_list.csv')
    if not os.path.exists('./uniformity_'+target_folder):
        os.mkdir('./uniformity_'+target_folder)
    for word in df_keyword['keyword'].tolist():
        shutil.copy('./'+target_folder + '/' + word + '_uniformity-test_z_FDR_0.01.nii.gz', './uniformity_'+target_folder + '/' + word + '.nii.gz')
    
    

def main():
    # set up basic path
    os.chdir('../../data')
    dirs = ['./raw_data', './train', './test', './test2']
    for d in dirs:
        if not os.path.exists(d):
            os.mkdir(d)
    
    dataset = load_dataset_instance('dataset')
    
    #create_nii_files(dataset, 'train999', year = 2015, after = False)
    create_nii_files(dataset, 'test1999', year = 2015, after = True)
    #create_nii_files(dataset, 'test2999')
    
    #leave_out_uniformity_files('train')
    #leave_out_uniformity_files('test')
    #leave_out_uniformity_files('test2')
    
    
if __name__ == '__main__':
    main()



