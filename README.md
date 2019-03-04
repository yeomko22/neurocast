# Brain Factorization
Predicting unknown correlation between behavior and brain using matrix factorization methods.

## Download data
down load data from following link under /data and unzip
* https://drive.google.com/drive/folders/1UMAyO-aLaWzrGxJujKQgxAk94hJYe7j9?usp=sharing
* move unziped file into /data directory

## Data Crawler
### How to use
(currently only available in windows)

crawler/selenium/download_nii_files.py
* Download nii files from neurosynth.org using selenium and chrome driver
```
cd crawler/selenium
python download_nii_files.py
```
crawler/neurosynth_package/download_raw_data.py
  * Download data using Neurosynth official package
```
cd crawler/neurosynth_package
python download_raw_data.py
```

### Output
The crawled data can be downloaded from above google drive link.
* data/keyword_list
  * List of 1335 behavior from Neurosynth
* data/keyword_uniformity_test
  * nii file list which represent correlation between keyword - brain activation.  
  (downloaded by selenium crawler)
* data/keyword_association_test
  * nii file list which represent correlation between keyword - brain activation.  
  (downloaded by selenium crawler)
* data/raw_data
  * Raw brain activation data per paper.  
  (downloaded by neurosynth package crawler)
* data/anatomical.nii
  * Brain anatomical structure
* For more detail, see our wiki [link]


## Preprocessing Data
### How to use
```
cd preprocessor
python preprocessor.py
```
### Output
The crawled data can be downloaded from following link.
https://drive.google.com/drive/folders/1NDWWc4bBMuMSRmq8S4q8U2eHVXtPpzH_

* data/result/uniformity_sorted.csv
* data/result/association_sorted.csv
  * represent activation score per brain voxel coordinates and keyword.
* For more detail, see our wiki [link]


## Todo list
- Applying collaborative filtering
- Cross validation
