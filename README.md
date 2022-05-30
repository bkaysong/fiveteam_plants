# 토마토 수확 가능여부 식별
이미지 분류 기술을 사용하여 모양, 색상 및 질감 특징을 기반으로 토마토의 수확 여부를 식별합니다.


## 개요
토마토 수확 가능여부 식별은 이미지 처리 기술을 사용하여 토마토의 색상을 기준으로 토마토가 익었는지 안 익었는지 여부를 식별합니다. 

이미지는 먼저 AWS의 Rekognition에서 토마인지 여부를 파악후에 K-means 알고리즘을 통해 토마토의 익음 정도를 식별합니다.

## 사용프로그램
- AWS S3
- AWS Lambda
- AWS Rekognition
- Python
- Numpy
- Scikit learn

## 아키텍쳐
![ar](https://user-images.githubusercontent.com/102707438/170937122-cf18c49a-1d09-428b-a607-cf3d3edf34d2.png)
