# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 23:47:55 2019

@author: Junsol Kim
"""
from neurosynth.base.dataset import Dataset
from neurosynth.analysis import meta
import os

#download raw data
ns.dataset.download(path='data', unpack=False) #download latest database


'''
#export .nii file for each keyword
dataset = Dataset('data/database.txt')
dataset.add_features('data/features.txt')

keywords = dataset.get_feature_names()
for word in keywords:
    ids = dataset.get_studies(features=word, frequency_threshold=0.001)
    ma = meta.MetaAnalysis(dataset, ids)
    
    if not os.path.exists('data/'+word):
        os.makedirs('data/'+word)
'''