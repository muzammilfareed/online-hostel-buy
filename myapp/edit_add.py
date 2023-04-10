import os
from datetime import datetime
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from myapp.models import house_info, house_images, house_video
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse


def edit_add(request, pk):
    obj_add = house_info.objects.get(pk=pk)
    name = obj_add.name
    address = obj_add.address
    phone_number = obj_add.phone_number
    location = obj_add.location
    description = obj_add.description
    additional_info = obj_add.additional_info
    booker_name = obj_add.booker_name
    booked_by_user_id = obj_add.booked_by_user_id
    no_of_rooms = obj_add.no_of_rooms
    square_fit = obj_add.square_fit
    no_of_bath = obj_add.no_of_bath
    no_of_kitchen = obj_add.no_of_kitchen
    is_electricity = obj_add.is_electricity
    is_water = obj_add.is_water
    is_gas = obj_add.is_gas
    is_internet = obj_add.is_internet
    is_furnished = obj_add.is_furnished
    is_available = obj_add.is_available
    created_datetime = obj_add.created_datetime
    modified_datetime = obj_add.modified_datetime
    booking_date = obj_add.booking_date
    rent = obj_add.rent
    images_list = []
    images_list2 = []
    for i in house_images.objects.filter(house_id=pk):
        images_list.append([i.pk, i.image_path])
    video = house_video.objects.get(house_id=pk)
    context = {
        'name': name,
        'address':     address,
        'phone_number': phone_number,
        'location': location,
        'description': description,
        'additional_info': additional_info,
        'booker_name': booker_name,
        'booked_by_user_id': booked_by_user_id,
        'no_of_rooms': no_of_rooms,
        'square_fit': square_fit,
        'no_of_bath ': no_of_bath ,
        'no_of_kitchen': no_of_kitchen,
        'is_electricity': is_electricity,
        'is_water': is_water,
        'is_gas ': is_gas ,
        'is_internet': is_internet,
        'is_furnished': is_furnished,
        'is_available': is_available,
        'created_datetime': created_datetime,
        'modified_datetime': modified_datetime,
        'booking_date': booking_date,
        'rent': rent,
        'images_list': images_list,
        'video': video.video_path
    }
    return render(request, 'edit_add.html', context)





def status_change(request, pk):
    obj_add = house_info.objects.get(pk=pk)
    name = obj_add.name
    address = obj_add.address
    phone_number = obj_add.phone_number

    is_available = obj_add.is_available

    context = {
        'name': name,
        'address':     address,
        'phone_number': phone_number,
        'is_available': is_available,
    }
    if request.method == 'POST':
        is_available = int(request.POST.get('is_available'))
        obj_add.is_available= is_available
        obj_add.save()
        return redirect('get_user_data')
    return render(request, 'status_change.html', context)




def bocked_status_change(request, pk):
    obj_add = house_info.objects.get(pk=pk)
    is_available = obj_add.is_available
    context = {
        'is_available': is_available,
    }
    if request.method == 'POST':
        is_available = int(request.POST.get('is_available'))
        obj_add.is_available=is_available
        obj_add.save()
        return redirect('get_user_data')
    return render(request, 'bocked_status_change.html', context)


def delete(request, pk):
    obj_add = house_info.objects.get(pk=pk)
    obj_add.delete()
    return redirect('get_user_data')




def edit_home(request, pk):
    obj_add = house_info.objects.get(pk=pk)
    name = obj_add.name
    address = obj_add.address
    phone_number = obj_add.phone_number
    location = obj_add.location
    description = obj_add.description
    additional_info = obj_add.additional_info
    booker_name = obj_add.booker_name
    booked_by_user_id = obj_add.booked_by_user_id
    no_of_rooms = obj_add.no_of_rooms
    square_fit = obj_add.square_fit
    no_of_bath = obj_add.no_of_bath
    no_of_kitchen = obj_add.no_of_kitchen
    is_electricity = obj_add.is_electricity
    is_water = obj_add.is_water
    is_gas = obj_add.is_gas
    is_internet = obj_add.is_internet
    is_furnished = obj_add.is_furnished
    is_available = obj_add.is_available
    created_datetime = obj_add.created_datetime
    modified_datetime = obj_add.modified_datetime
    booking_date = obj_add.booking_date
    rent = obj_add.rent
    rooms = obj_add.no_of_rooms
    images_list = []
    for i in house_images.objects.filter(house_id=pk):
        images_list.append([i.pk, i.image_path])
    video = None
    try:
        video = house_video.objects.get(house_id=pk)
    except:
        pass
    print(no_of_bath)
    print(additional_info)

    context = {
        'name': name,
        'address':     address,
        'phone_number': phone_number,
        'location': location,
        'rooms': rooms,
        'description': description,
        'additional_info': additional_info,
        'booker_name': booker_name,
        'booked_by_user_id': booked_by_user_id,
        'no_of_rooms': no_of_rooms,
        'square_fit': square_fit,
        'no_of_bath ': no_of_bath,
        'no_of_kitchen': no_of_kitchen,
        'is_electricity': is_electricity,
        'is_water': is_water,
        'is_gas ': is_gas,
        'is_internet': is_internet,
        'is_furnished': is_furnished,
        'is_available': is_available,
        'created_datetime': created_datetime,
        'modified_datetime': modified_datetime,
        'booking_date': booking_date,
        'rent': rent,
        'images_list': images_list,
    }
    if video:
        context['video_path']= video.video_path,
        context['video_pk']= video.pk
    
    if request.method == 'POST':
        electricity = int(request.POST.get('electricity'))
        water = int(request.POST.get('water'))
        gas = int(request.POST.get('gas'))
        internet = int(request.POST.get('internet'))
        furnished = int(request.POST.get('furnished'))
        no_of_bath = int(request.POST.get('no_of_bath'))
        print(no_of_bath)
        rent = float(request.POST.get('rent'))
        rooms = int(request.POST.get('rooms'))
        is_available = int(request.POST.get('is_available'))
        obj_add.name=request.POST.get('name')
        obj_add.address=request.POST.get('address')
        obj_add.phone_number=request.POST.get('phone_number')
        obj_add.square_fit=request.POST.get('square_fit')
            # longitude=request.POST.get('longitude'),
            # latitude=request.POST.get('latitude'),
        obj_add.location=request.POST.get('location')
        obj_add.description=request.POST.get('description')
        obj_add.additional_info=request.POST.get('additional_info')
        obj_add.no_of_rooms=rooms
        obj_add.no_of_bath=no_of_bath
        obj_add.no_of_kitchen=int(request.POST.get('kitchen'))
        obj_add.is_available=is_available
        obj_add.is_electricity=electricity
        obj_add.is_water=water
        obj_add.is_gas=gas
        obj_add.is_internet=internet
        obj_add.is_furnished=furnished
        obj_add.rent=rent
        obj_add.save()
        return redirect('get_user_data')

    return render(request, 'edit_home.html', context)




@csrf_exempt
def delete_image(request):
    if request.method == 'POST':
        pk = int(request.POST.get('pk'))
        house_images.objects.get(pk=pk).delete()
        return JsonResponse(True, safe=False)


@csrf_exempt
def delete_video(request):
    if request.method == 'POST':
        pk = int(request.POST.get('pk'))
        house_video.objects.get(pk=pk).delete()
        return JsonResponse(True, safe=False)