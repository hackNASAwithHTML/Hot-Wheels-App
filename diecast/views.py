from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .forms import DieCastForm
from PIL import Image, ExifTags
from .models import DieCastModel
# Create your views here.
def rotate_image(filepath):
  try:
    image = Image.open(filepath)
    for orientation in ExifTags.TAGS.keys():
      if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(image._getexif().items())

    if exif[orientation] == 3:
        image = image.rotate(180, expand=True)
    elif exif[orientation] == 6:
        image = image.rotate(270, expand=True)
    elif exif[orientation] == 8:
        image = image.rotate(90, expand=True)
    image.save(filepath)
    image.close()
  except (AttributeError, KeyError, IndexError):
    # cases: image don't have getexif
    pass
def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData
def handle_uploaded_file(f,image_name):
    format = "jpg"
    with open("diecast/static/images/hot_wheels_storage/"+image_name+"."+format, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
import hashlib

def add_diecast(request):
    dform = DieCastForm()
    if request.method == "POST":
        data = request.POST
        hashed_password = hashlib.sha256(data['admin_password'].encode())
        hexdigest_password = hashed_password.hexdigest()
        if hexdigest_password=="240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9":
            handle_uploaded_file(request.FILES['hotwheelsimage'], data['toy_code'])
            format = "jpg"
            path = "diecast/static/images/hot_wheels_storage/" + data['toy_code'] + "." + format
            rotate_image(path)
            update_gallery = DieCastModel.objects.create(toy_code=data['toy_code'],
                                                     casting_name=data['casting_name'],
                                                     series=data['series'],
                                                     year=data['year'],
                                                    choice=data['choice'],
                                                     color=data['color'],
                                                     loose_photo=convertToBinaryData(path))
            if update_gallery:
                return redirect('home')
        else:
            return HttpResponse("You are not admin, aren't you OwO ?")
    return render(request,"add_diecast.html",{"dform":dform})