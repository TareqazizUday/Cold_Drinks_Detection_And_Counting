import os
import cv2
from PIL import Image
import numpy as np

import tensorflow as tf
from django.conf import settings
from django.template.response import TemplateResponse
from django.utils.datastructures import MultiValueDictKeyError

from django.core.files.storage import FileSystemStorage
from .DrinksApi import drinksdetection


class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


def index(request):
    message = ""
    prediction = ""
    fss = CustomFileSystemStorage()
    try:
        image = request.FILES["image"]
        print("Name", image.file)
        _image = fss.save(image.name, image)
        path = str(settings.MEDIA_ROOT) + "/" + image.name
        # image details
        image_url = fss.url(_image)
        print(path)
        # Read the image
        products , total_product_count = drinksdetection(path)
        print(total_product_count)
        print(products)
        
        return TemplateResponse(
            request,
            "index.html",
            {
                "message": message,
                "total_product_count": total_product_count,
                "image_url": image_url,
                "prediction": products,
            },
        )
    except MultiValueDictKeyError:

        return TemplateResponse(
            request,
            "index.html",
            {"message": "No Image Selected"},
        )

