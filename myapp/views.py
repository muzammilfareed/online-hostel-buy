import os
from datetime import datetime

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from myapp.models import house_info, house_images, house_video
from django.core.files.storage import FileSystemStorage
from authen_app.models import CustomUser

@csrf_exempt
def index(request):
    if request.user.is_superuser:
        user_id = request.user.id
        print('asd')
        all_obj = CustomUser.objects.all()
        # email = obj.email

        context = {
            'all_obj': all_obj,
        }
        # print(email)
        return render(request, 'auth.html',context)
    else:
        data = house_info.objects.filter(is_available=True)
        data_list = []
        for i in data:
            images_list = []
            images = house_images.objects.filter(house_id=i.pk)
            for image in images:
                images_list.append(image.image_path)
            data_list.append([i.pk, images_list[0], i.address, i.user_id, i.rent, i.no_of_rooms, i.no_of_bath, i.description, i.user.username, i.phone_number,i.name, i.location,i.square_fit])
        print(data_list)
        context = {
            'data_list': data_list
        }
        return render(request, 'index11.html', context)


def get_user_data(request):
    user_id = request.user.id
    data = house_info.objects.filter(user_id=user_id)
    activate_data_list = []
    inactivate_data_list = []
    for i in data:
        if i.is_available:
            images_list = []
            images = house_images.objects.filter(house_id=i.pk)
            for image in images:
                images_list.append(image.image_path)
            activate_data_list.append([i.pk, images_list[0], i.address, i.user_id, i.rent, i.no_of_rooms, i.no_of_bath, i.description, i.user.username, i.phone_number,i.name, i.location,i.square_fit])
        else:
            images_list = []
            images = house_images.objects.filter(house_id=i.pk)
            for image in images:
                images_list.append(image.image_path)
            inactivate_data_list.append([i.pk, images_list[0], i.address, i.user_id, i.rent, i.no_of_rooms, i.no_of_bath, i.description, i.user.username, i.phone_number,i.name, i.location,i.square_fit])
    context = {
        'activate_data_list': activate_data_list,
        'inactivate_data_list': inactivate_data_list
    }
    print(context)
    return render(request, 'index.html', context)


@csrf_exempt
def house_info_save(request):
    if request.method == 'POST':
        user_id = int(request.user.id)
        electricity = int(request.POST.get('electricity'))
        water = int(request.POST.get('water'))
        gas = int(request.POST.get('gas'))
        internet = int(request.POST.get('internet'))
        furnished = int(request.POST.get('furnished'))
        rent = int(request.POST.get('rent'))
        rooms = int(request.POST.get('rooms'))
        is_available = int(request.POST.get('is_available'))

        obj_house_info = house_info(
            user_id=user_id,
            name=request.POST.get('name'),
            address=request.POST.get('address'),
            phone_number=request.POST.get('phone_number'),
            square_fit=request.POST.get('square_fit'),
            # longitude=request.POST.get('longitude'),
            # latitude=request.POST.get('latitude'),
            location=request.POST.get('location'),
            description=request.POST.get('description'),
            additional_info=request.POST.get('additional_info'),
            no_of_rooms=rooms,
            no_of_bath=request.POST.get('bath'),
            no_of_kitchen=request.POST.get('kitchen'),
            is_available=is_available,
            is_electricity=electricity,
            is_water=water,
            is_gas=gas,
            is_internet=internet,
            is_furnished=furnished,

            rent=rent,
            )
        obj_house_info.save()
        images = request.FILES.getlist('images[]')
        house_id = obj_house_info.pk
        for image in images:
            res = save_house_images(image, house_id, user_id)
        videos = request.FILES.getlist('videos')
        for video in videos:
            res = save_house_videos(video, house_id, user_id)
        return redirect('index')
    return render(request, 'add_home.html')


def save_house_images(image, house_id, user_id):
    try:
        file_extension = image.name.split('.')[-1]
        date_time = datetime.now().strftime('%Y%m%d%H%M%S%f')
        folder_path = f'static/user_house_images/{user_id}'
        try:
            os.mkdir(folder_path)
        except:
            pass
        images_save_folder = f'{folder_path}/{house_id}'
        try:
            os.mkdir(images_save_folder)
        except:
            pass
        file_save_name = f'{images_save_folder}/{date_time}.{file_extension}'
        fs = FileSystemStorage()
        fd = fs.save(file_save_name, image)
        file_path = fs.url(fd)
        print(file_path)
        obj_house_images = house_images()
        obj_house_images.house_id = house_id
        obj_house_images.image_path = file_path
        obj_house_images.save()
        return True
    except Exception as e:
        print(e)
        return False


def save_house_videos(video, house_id, user_id):
    file_extension = video.name.split('.')[-1]
    date_time = datetime.now().strftime('%Y%m%d%H%M%S%f')
    folder_path = f'static/user_house_videos/{user_id}'
    try:
        os.mkdir(folder_path)
    except:
        pass
    images_save_folder = f'{folder_path}/{house_id}'
    try:
        os.mkdir(images_save_folder)
    except:
        pass
    file_save_name = f'{images_save_folder}/{date_time}.{file_extension}'
    fs = FileSystemStorage()
    fd = fs.save(file_save_name, video)
    file_path = fs.url(fd)
    print(file_path)
    obj_house_images = house_video()
    obj_house_images.house_id = house_id
    obj_house_images.video_path = file_path
    obj_house_images.save()
    return True


