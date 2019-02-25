# brain_factorization
Predicting behaviors based on brain data using collaborative filtering

# 코딩된 내용
## 1. 데이터 크롤링
* crawler/selenium/download_nii_files.py
 * Selenium으로 neurosynth.org를 통해서, 각 keyword(behavior)와 관련된 brain activation 정보가 들어있는 .nii 파일들 다운로드
* crawler/\neurosynth_package/download_raw_data.py
 * Neurosynth에서 제공하는 package로 데이터 다운로드
 
## 2. 크롤링된 데이터
* data/keyword_list: Neurosynth의 1335개 keyword(behavior) 리스트
* data/keyword_uniformity_test: Selenium으로 다운로드. keyword-brainActivation 간 상관관계가 저장된 nii 파일 모음 (uniformity test)
* data/keyword_association_test: Selenium으로 다운로드. keyword-brainActivation 간 상관관계가 저장된 nii 파일 모음 (association test)
* data/raw_data: Neurosynth package로 다운로드된 raw data. 논문 별 activation 데이터.
* data/anatomical.nii: Brain anatomical structure 파일.

# 해결해야 할 문제

## 3. 크롤링된 데이터 => (Brain Voxel X Keyword) 매트릭스 변환 (메모리 부족 때문에 안돌아감 ㅠㅠ)
* create_brain_behav_matrix.py: 매트릭스 변환해서 results 폴더에 저장

# 앞으로 코딩해야 할 내용
## 4. (Brain Voxel X Keyword) 매트릭스를 이용한 collaborative filtering
## 5. Cross-validation
