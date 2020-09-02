from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from seller.models import Seller
from .forms import SellerForm
from PIL import Image, ExifTags
# Create your views here.

from base64 import b64encode, b64decode
import hashlib
from Cryptodome.Cipher import AES

from Cryptodome.Random import get_random_bytes
def encrypt(plain_text, password):
    # generate a random salt
    salt = get_random_bytes(AES.block_size)
    # use the Scrypt KDF to get a private key from the password
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    # create cipher config
    cipher_config = AES.new(private_key, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    return {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }


def decrypt(enc_dict, password):
    # decode the dictionary entries from base64
    salt = b64decode(enc_dict['salt'])
    cipher_text = b64decode(enc_dict['cipher_text'])
    nonce = b64decode(enc_dict['nonce'])
    tag = b64decode(enc_dict['tag'])

    # generate the private key from the password and salt
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    # create the cipher config
    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    # decrypt the cipher text
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted

import ast

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
def handle_uploaded_file_profile(f,image_name):
    format = "jpg"
    with open("seller/static/images/seller/"+image_name+"."+format, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def handle_uploaded_file_loose(f,image_name):
    format = "jpg"
    with open("seller/static/images/seller/"+image_name+"."+format, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
import hashlib
def en_mode(request):
    if request.method == "POST":
        data = request.POST
        hashed_password = hashlib.sha256(data['admin_password'].encode())
        hexdigest_password = hashed_password.hexdigest()
        if hexdigest_password == "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9":
            encrypted_list = Seller.objects.all()
            for list in encrypted_list:
                list.seller_name = encrypt(list.seller_name, hexdigest_password)
                list.location = encrypt(list.location,hexdigest_password)
                list.price = encrypt(list.price,hexdigest_password)
                list.token = encrypt(list.token,hexdigest_password)
                list.status = encrypt(list.status,hexdigest_password)
                list.product_name = encrypt(list.product_name,hexdigest_password)
                list.save()
            return redirect('seller')
        else:
            return HttpResponse("You aren't supposed to be here")
    return render(request,'encode_mode.html')
def de_mode(request):
    if request.method == "POST":
        data = request.POST
        hashed_password = hashlib.sha256(data['admin_password'].encode())
        hexdigest_password = hashed_password.hexdigest()
        if hexdigest_password == "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9":
            decrypted_list = Seller.objects.all()
            for list in decrypted_list:
                list.seller_name = ast.literal_eval(list.seller_name)
                list.seller_name = decrypt(list.seller_name, hexdigest_password)
                list.seller_name = bytes.decode(list.seller_name)
                list.location = ast.literal_eval(list.location)
                list.location = decrypt(list.location, hexdigest_password)
                list.location = bytes.decode(list.location)
                list.price = ast.literal_eval(list.price)
                list.price = decrypt(list.price, hexdigest_password)
                list.price = bytes.decode(list.price)
                list.token = ast.literal_eval(list.token)
                list.token = decrypt(list.token, hexdigest_password)
                list.token = bytes.decode(list.token)
                list.status = ast.literal_eval(list.status)
                list.status = decrypt(list.status, hexdigest_password)
                list.status = bytes.decode(list.status)
                list.product_name = ast.literal_eval(list.product_name)
                list.product_name = decrypt(list.product_name, hexdigest_password)
                list.product_name = bytes.decode(list.product_name)
                list.save()
            return redirect('seller')
        else:
            return HttpResponse("You aren't supposed to be here")
    return render(request,'decode_mode.html')
def add_seller(request):
    sform = SellerForm()
    if request.method == "POST":
        data = request.POST
        hashed_password = hashlib.sha256(data['admin_password'].encode())
        hexdigest_password = hashed_password.hexdigest()
        if hexdigest_password == "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9":
            handle_uploaded_file_loose(request.FILES['loose'], data['token'])
            handle_uploaded_file_profile(request.FILES['profile'], data['seller_name'])
            format = "jpg"
            path_loose = "seller/static/images/seller/" + data['token'] + "." + format
            rotate_image(path_loose)
            path_profile = "seller/static/images/seller/" + data['seller_name'] + "." + format
            rotate_image(path_profile)
            update_seller = Seller.objects.create(profile=convertToBinaryData(path_profile),
                                                         seller_name=data['seller_name'],
                                                         location=data['location'],
                                                         price=data['price'],
                                                         token=data['token'],
                                                         status=data['status'],
                                                        product_name=data['product_name'],
                                                         image=convertToBinaryData(path_loose))
            if update_seller:
                return redirect('seller')
        else:
            return HttpResponse("You aren't supposed to be here")
    return render(request,'add_seller.html',{'sform':sform})
import random
def seller_page(request):
    seller_list = Seller.objects.all()
    return render(request,"seller_page.html",{"seller_list":seller_list})
