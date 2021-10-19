from django.core.files import File
from pathlib import Path
from PIL import Image
from io import BytesIO
from django.core.files.storage import default_storage



def image_resize(image, width, height,*args,**kwargs):
    image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
    }

    # Open the image using Pillow
    try:
        img = Image.open(image)
    except:
        return
    # check if either the width or height is greater than the max
    if img.width > width or img.height > height:
        fullpath = image.file.name
        output_size = (width, height)
        # Create a new resized “thumbnail” version of the image with Pillow
        img.thumbnail(output_size)
        # Find the file name of the image
        img_filename = Path(fullpath).name
        # Spilt the filename on “.” to get the file extension only
        img_suffix = Path(fullpath).name.split(".")[-1].lower()
        # Use the file extension to determine the file type from the image_types dictionary
        img_format = image_types[img_suffix]
        # Save the resized image into the buffer, noting the correct file type
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        # Wrap the buffer in File object
        file_object = File(buffer)
        try:
            if fullpath != 'default.jpg':
                default_storage.delete(fullpath)
        except:
            pass
        # Save the new resized file as usual, which will save to S3 using django-storages
        image.save(img_filename, file_object)