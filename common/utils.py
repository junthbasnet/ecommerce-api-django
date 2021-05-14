
from io import BytesIO

from PIL import Image
from django.core.files import File


def compress(image):
    im = Image.open(image)
    name = image.name.split(".")[0]
    # create a BytesIO object
    im_io = BytesIO()
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    im = im.convert("RGB")
    # save image to BytesIO object
    im.save(im_io, 'webp', quality=100)
    # create a django-friendly Files object
    new_image = File(im_io, name=f"{name}.webp")
    return new_image


def resize_image(image_file):
    image = Image.open(image_file)
    name = image_file.name.split(".")[0]
    image_file = BytesIO()
    w, h = image.size
    image = image.resize((w // 10, h // 10), Image.ANTIALIAS)
    image.save(image_file, 'webp', quality=100)
    new_image = File(image_file, name=f"{name}.webp")
    return new_image


