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


## 코드
- KMeans 알고리즘으로 토마토가 익었는지 익지 않았는지 분류
```
def ripe(url):
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    readFlag = cv2.IMREAD_COLOR
    image = cv2.imdecode(image, readFlag)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))  # height, width 통합

    k = 5
    clt = KMeans(n_clusters=k)
    clt.fit(image)

    for center in clt.cluster_centers_:
        if center[0] > center[1] * 2 and center[0] > center[2] * 2:
            return "good"

if ripe('https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FkRkIk%2FbtrC5K0PSsC%2FwjBKkTqCI8ytVkWRVR7K9K%2Fimg.jpg') == "good":
    print("익었다")
else:
    print("안 익었다")
    ```

- AWS의 Rekognition을 사용하여 토마토 이미지인지 판단
```
def rekognition(photo, bucket):
    # Change bucket and photo to your S3 Bucket and image.
    client = boto3.client('rekognition', region_name='ap-northeast-2')

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},MaxLabels=10)


    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        if label['Name']=='Tomato' and label['Confidence'] > 70 :
            return "tomato"
```

- AWS의 S3에서 저장된 이미지를 로드
- 최종으로 토마토이미지인지 파악 후 토마토 익음 분류.

```
if __name__ == "__main__":
    photo = "tomato_18.jpg"
    bucket = "tftomato1"
    if rekognition(photo, bucket) == "tomato" :
        if ripe("https://"+bucket+".s3.ap-northeast-2.amazonaws.com/"+photo) == "good":
            print("익었다")
        else:
            print("안 익었다")
    else :
        print("토마토 없음")
```
