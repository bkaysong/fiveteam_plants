import numpy as np
import cv2
from urllib.request import urlopen
from sklearn.cluster import KMeans
import boto3


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


def rekognition(photo, bucket):
    # Change bucket and photo to your S3 Bucket and image.
    client = boto3.client('rekognition', region_name='ap-northeast-2')

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},MaxLabels=10)


    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        if label['Name']=='Tomato' and label['Confidence'] > 70 :
            return "tomato"


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