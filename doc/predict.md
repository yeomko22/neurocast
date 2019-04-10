## Predict 사용법
### 0. 환경변수에 "BRAIN_FAC" 이라는 변수를 추가해주고 값은 이 코드의 루트 디렉터리로 잡아줄 것
- ex. /usr/junny/brain_factorization

### 1. feature/als_test_notebook 브랜치 pull
- /experiment/predict.py 파일이 있음
- 여기서 원하는 키워드를 넣으면 원본 예측값 배열 (float)
- 기존에 발견되었었던 포인트 들에 대한 예측값 배열 (float)
- 기존에 발견되지 않았던 영역들애 대한 예측값 배열 (float)
- 이렇게 세 종류를 리턴함

### 2. 학습 모델 웨이트 다운로드
- /data/checkpoint 디렉터리를 만들고, 구글 드라이브 상의 checkpoint 폴더 접속
- als_atlas_kfold_0_5_item.npy 이런식으로 되어 있을텐데 이는
- als 알고리즘 atlas 복셀 클러스터 kfold 벨리데이션 0번째 fold, 5 에포크, item 레이텐트 행렬을 의미한다. (다 몰라도 된다.)
- 주의할 점은 atlas kfold 요 변수에 따라서 다운로드 해야할 원본 데이터가 달라진다는 것이다.
- 또한 item과 user를 항상 쌍으로 다운받아야 한다.
- 그러면 예시로 als_atlas_kfold_0_5_item.npy, als_atlas_kfold_0_5_user.npy 두 파일을 다운받는다.
- 그리고 brain_factorization/data/checkpoint 아래에 넣는다.

### 3. 예측 결과와 비교할 원본 데이터 다운로드
- /data/binary_kfold/atlas 라는 폴더를 만든다.
- 복셀 클러스터링을 적용한 다음, 0과 1로 바꾸어 행렬 형태로 만든 원본 데이터라는 의미이다.
- 구글 드라이브 상에 /binary_kfold 폴더에 접속
- 여기서 앞서 다운로드 받았던 학습 모델 웨이트와 동일한 네이밍 형태의 원본 데이터를 다운받는다.
- 이 경우에는 atlas/train_kfold_atlas_0.npy 를 다운받으면 된다. (나중에 고칠께.. 넘 복잡하다)
- 다운받은 파일은 로컬에 /data/binary_kfold/atlas 폴더안에 얌전히 모셔놓는다.

### 4. 키워드 파일 다운로드
- 행렬만 봐서는 어느 키워드가 몇번째이닞 알 수 없다.
- 그러므로 구글 드라이브 상의 org_nii_files 아래의 keyword_list.csv를 다운로드 받는다.
- 다운로드 받은 파일은 /data/keyword 폴더 아래에 모셔놓는다.
- 이 때 파일 이름만 keyword_origin.csv로 변경해준다. (이 것도 나중에 바꿀 것)

### 5. 키워드 입력 및 실행
- 드디어 준비가 끝났다. 기타 라이브러리 설치 등은 컴과 짬밥 3년차 정도면 해내리라 믿는다.
- predict.py 파일에 input_keyword 에다가 원하는 키워드를 넣고 돌리면 결과 행렬이 출력된다.
- 행운을 빈다. 나는 귀가한다.
