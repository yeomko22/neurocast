# Brain Factorization
Predicting unknown correlation between behavior and brain using matrix factorization methods.

## Download references
download papers from following link
* https://drive.google.com/open?id=1WKoOp81hdGEnYmqAwpr4b5rURrjCK6YA

## Download data
download data from following link under /data and unzip
* https://drive.google.com/drive/folders/1UMAyO-aLaWzrGxJujKQgxAk94hJYe7j9?usp=sharing
* move unziped file into /data directory

## Data Crawler
### How to use
(currently only available in windows)

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
* data/train
* data/test
* data/test2
  * train: dataset until 2015, test: dataset after 2015, test2: overall dataset (1997~2019)
  * data/uniformity_train, data/uniformity_test, data/uniformity_test2: extracted only uniformity test results
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
* results/coordinates_table.csv
  * represent MNI coordinates and Shen's category (268) for each voxel
* For more detail, see our wiki [link]


## Todo list
- Applying collaborative filtering
- Cross validation
