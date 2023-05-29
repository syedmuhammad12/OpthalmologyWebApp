from django.shortcuts import render,HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import connection
from datetime import datetime
import base64
from PIL import Image
import numpy as np
import cv2
from io import BytesIO
from keras.models import load_model
from keras.utils import load_img
import os
from random import randint
# from dicom import dcmread  

model = load_model("H_mobilenetv2.h5")

# Create your views here.
def index(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'index.html')

def models_page_redirect(request):
    return render(request, "./models-page.html")


def logout(request):
    return redirect("index")

def models_page(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print(password)
    if username == "doctor" and password == "54321":
        return render(request, "./models-page.html")
    else:
        messages.error(request, 'Username OR password is incorrect')
    return redirect("index")

def model1_page(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, "./model1.html")

def model2_page(request):
    return render(request, "model2.html")

def model3_page(request):
    return render(request, "model3.html")

def model_eval(request):
    global model
    offset_1 = request.POST.get('right_eye').index(',') + 1
    offset_2 = request.POST.get('left_eye').index(',') + 1
    # left_image_name = request.POST.get('left_image_name')
    # right_image_name = request.POST.get('right_image_name')
    img_bytes_1 = base64.b64decode(request.POST.get('right_eye')[offset_1:])
    img_bytes_2 = base64.b64decode(request.POST.get('left_eye')[offset_2:])
    # if left_image_name.endswith(".dcm"):
    #    img_1 = dcmread(BytesIO(img_bytes_1), force=True)
    #    img_1 = img_1.pixel_array
    # else:
    #     img_1 = Image.open(BytesIO(img_bytes_1))
    #     img_1  = np.array(img_1)
    #     img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)
    # if right_image_name.endswith(".dcm"):
    #     img_2 = dcmread(BytesIO(img_bytes_2), force=True)
    #     img_2 = img_2.pixel_array
    # else:
    #     img_2 = Image.open(BytesIO(img_bytes_2))
    #     img_2  = np.array(img_2)
    #     img_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2RGB)
    
    # file_name_1 = request.POST.get('file_name_1')  
    # file_name_2 = request.POST.get('file_name_2')
    
    # if os.path.exists("./images/"+file_name_1+".jpg"):
    #     file_name_1 += str(random(999999, 999999999))
    # if os.path.exists("./images/"+file_name_2+".jpg"):
    #     file_name_2 += str(random(999999, 999999999))

    # cv2.imwrite(f"./images/{file_name_1}.jpg", img_1)
    # cv2.imwrite(f"./images/{file_name_2}.jpg", img_2)
    
    img_1= load_img(BytesIO(img_bytes_1), target_size=(224,224))
    img_2= load_img(BytesIO(img_bytes_2), target_size=(224,224))

    img_1 = np.array(img_1)
    img_1 = img_1 / 255.0
    img_1 = img_1.reshape(1,224,224,3)
    
    img_2 = np.array(img_2)
    img_2 = img_2 / 255.0
    img_2 = img_2.reshape(1,224,224,3)

    label_1 = model.predict(img_1)
    label_2 = model.predict(img_2)

    result_right_eye= ""
    result_left_eye = ""

    if label_1[0][0]>0.5:
        result_right_eye = "Referable Diabetic Retinopathy"
    else:
        result_right_eye = "Non Referable Diabetic Retinopathy"
    
    if label_2[0][0]>0.5:
        result_left_eye = "Referable Diabetic Retinopathy"
    else:
        result_left_eye = "Non Referable Diabetic Retinopathy"
    
    if result_right_eye == "Referable Diabetic Retinopathy" or result_left_eye == "Referable Diabetic Retinopathy":
        request.session["result_summary"] = "Referable Diabetic Retinopathy"
    else:
        request.session["result_summary"] = "Non Referable Diabetic Retinopathy"
        
    
    request.session["right_eye_result"] = result_right_eye
    request.session["left_eye_result"] = result_left_eye
    request.session["right_eye_image"] = request.POST.get('right_eye')
    request.session["left_eye_image"] = request.POST.get('left_eye')
    # request.session["right_eye_image_name"] = file_name_1
    # request.session["left_eye_image_name"] = file_name_2
    return JsonResponse({"done": 200})

def registration_page(request):
    return render(request, "./registration.html")


def report_page(request):
    full_name = request.POST.get('full_name')
    dob = request.POST.get('dob')
    gender = request.POST.get('gender')

    patient_id = request.POST.get('patient_id')
    encounter_id = request.POST.get('encounter_id')
    dialtion_status = request.POST.get('dialtion_status')
    referring_location = request.POST.get('referring_location')
    referring_provider = request.POST.get('referring_provider')
    eye_control_id = request.POST.get('eye_control_id')
    print(patient_id, encounter_id)

    examine_date = datetime.now().strftime("%Y-%b-%d %H:%M")
    
    # right_eye_image_name = request.session.get('right_eye_image_name')
    # left_eye_image_name = request.session.get('left_eye_image_name')
    right_eye_image_name = f"{patient_id}_right_eye"
    left_eye_image_name = f"{patient_id}_left_eye"
    temp_right_eye_image_name = right_eye_image_name
    temp_left_eye_image_name = left_eye_image_name
    right_eye_image = request.session.get('right_eye_image')
    left_eye_image = request.session.get('left_eye_image')

    while os.path.exists("./images/"+temp_right_eye_image_name+".jpg"):
        temp_right_eye_image_name = right_eye_image_name
        temp_right_eye_image_name += f"_{str(randint(999999, 999999999))}" 
    while os.path.exists("./images/"+temp_left_eye_image_name+".jpg"):
        temp_left_eye_image_name = left_eye_image_name
        temp_left_eye_image_name += f"_{str(randint(999999, 999999999))}" 

    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS patient_info (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id VARCHAR, encounter_id VARCHAR, full_name VARCHAR, dob VARCHAR,
                       gender VARCHAR, dilation_status VARCHAR, ref_location VARCHAR, referring_provider VARCHAR, eye_control_id VARCHAR, examine_date VARCHAR,
                       right_eye_result VARCHAR, left_eye_result VARCHAR, result_summary VARCHAR, right_eye_image VARCHAR, left_eye_image VARCHAR)
                       """)
        cursor.execute(f"""
        INSERT INTO patient_info(patient_id, encounter_id, full_name, dob, gender, dilation_status, ref_location, referring_provider, eye_control_id, examine_date,
                       right_eye_result, left_eye_result, result_summary, right_eye_image, left_eye_image) VALUES ('{patient_id}', '{encounter_id}', '{full_name}', '{dob}', '{gender}', '{dialtion_status}', '{referring_location}', '{referring_provider}', 
        '{eye_control_id}', '{examine_date}', '{request.session.get('right_eye_result')}', '{ request.session.get('left_eye_result')}', '{request.session.get('result_summary')}',
        '{temp_right_eye_image_name + ".jpg"}', '{temp_left_eye_image_name + ".jpg"}')
        """)
    

    offset_1 = right_eye_image.index(',') + 1
    offset_2 = left_eye_image.index(',') + 1
    img_bytes_1 = base64.b64decode(right_eye_image[offset_1:])
    img_bytes_2 = base64.b64decode(left_eye_image[offset_2:])
    img_1 = Image.open(BytesIO(img_bytes_1))
    img_2 = Image.open(BytesIO(img_bytes_2))
    img_1  = np.array(img_1)
    img_2  = np.array(img_2)
    img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)
    img_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2RGB)
    
    cv2.imwrite(f"./images/{temp_right_eye_image_name}.jpg", img_1)
    cv2.imwrite(f"./images/{temp_left_eye_image_name}.jpg", img_2)

    params = {"name": full_name, "gender": gender, "dob": dob,  "patient_id": patient_id,  "encounter_id": encounter_id, "dialtion_status": dialtion_status, 
              "referring_location": referring_location, "referring_provider": referring_provider, "eye_control_id": eye_control_id, "current_examine_date": examine_date,
              "result_right_eye": request.session.get('right_eye_result'), "result_left_eye": request.session.get('left_eye_result'), 
              "result_summary": request.session.get('result_summary'), 
              "right_eye_image": request.session.get('right_eye_image'), "left_eye_image": request.session.get('left_eye_image'), 
              'right_eye_image_name': temp_right_eye_image_name, 'left_eye_image_name': temp_left_eye_image_name}
    return render(request, "./report.html", params)


