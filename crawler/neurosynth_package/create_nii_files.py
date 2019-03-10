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
def create_nii_files(dataset, target_folder):
    df_keyword = pd.read_csv('./keyword_list.csv')
    for word in df_keyword['keyword'].tolist():
        ids = dataset.get_studies(features=word, frequency_threshold=0.05)
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
    
    
    create_nii_files(load_dataset_instance('dataset_until2015'), 'train')
    create_nii_files(load_dataset_instance('dataset_after2015'), 'test')
    create_nii_files(load_dataset_instance('dataset'), 'test2')
    
    leave_out_uniformity_files('train')
    leave_out_uniformity_files('test')
    leave_out_uniformity_files('test2')
    
    
if __name__ == '__main__':
    main()



