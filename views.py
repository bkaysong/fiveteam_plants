from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
import tensorflow as tf
from PIL import Image


fruveg_model = tf.keras.models.load_model('saved_model/fruveg')
# Create your views here.
def func1(request):
    return HttpResponse('hello im bong')

def upload_get(request):
    return render(request, "upload.html")

def upload_post(request):
    if request.method == "POST":
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage(location='media', base_url='media')

        filename = fs.save(upload_file.name, upload_file)


        image = Image.open('media/'+upload_file.name)
        resized_image = image.resize((224,224))
        image_arr = np.array(resized_image)
        predictions = fruveg_model.predict(image_arr.reshape(1,224,224,3))
        print(predictions)
        # 예측값이 가장 높은 과일,야채의 인덱스를 찾아옴
        idx = predictions[0].argmax()

        # 인덱스 번호를 과일,야채 이름으로 바꿈.
        lables = ['beetroot', 'watermelon', 'ginger', 'kiwi', 'lemon', 'soy beans',
                  'carrot', 'jalepeno', 'pear', 'cabbage', 'raddish', 'corn', 'mango',
                  'peas', 'cauliflower', 'pomegranate', 'eggplant', 'orange', 'spinach',
                  'onion', 'tomato', 'cucumber', 'sweetpotato', 'potato', 'garlic',
                  'paprika', 'sweetcorn', 'grapes', 'bell pepper', 'chilli pepper',
                  'pineapple', 'banana', 'apple', 'lettuce', 'turnip', 'capsicum']
        result = lables[idx]

    return render(request, 'result.html', {'result': result})
