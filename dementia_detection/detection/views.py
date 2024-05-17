import os
import tensorflow as tf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .models import DementiaImage
from .serializers import DementiaImageSerializer
import cv2
import numpy as np
from django.shortcuts import render, redirect
from .forms import DementiaImageForm
from django.conf import settings

# Đăng ký hàm swish
@tf.keras.utils.register_keras_serializable()
def swish(x):
    return tf.nn.swish(x)

# Load model
model_path = os.path.join(settings.BASE_DIR, 'dementia_detection_model.h5')
model = tf.keras.models.load_model(model_path, custom_objects={'swish': swish})

def upload_image(request):
    prediction = None
    if request.method == 'POST':
        form = DementiaImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            # Perform prediction
            image_path = default_storage.path(instance.image.name)
            image = cv2.imread(image_path)
            image = cv2.resize(image, (28, 28))
            image = image.astype('float32') / 255.0
            image = np.expand_dims(image, axis=0)
            prediction = model.predict(image)
            predicted_class = np.argmax(prediction, axis=1)[0]
            labels = ['Mild_Demented', 'Moderate_Demented', 'Non_Demented', 'Very_Mild_Demented']
            instance.prediction = labels[predicted_class]
            instance.save()
            return render(request, 'upload.html', {'form': form, 'prediction': instance.prediction})
    else:
        form = DementiaImageForm()
    return render(request, 'upload.html', {'form': form, 'prediction': prediction})
