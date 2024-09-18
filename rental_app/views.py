from django.shortcuts import render, redirect
from rental_app.models import User, HouseDetails, Admin
from django.contrib import messages
from rental_app.functions import handle_uploaded_file
from django.utils import timezone

from django.core.mail import send_mail
from django.conf import settings
from decimal import Decimal
import random as rd
from django.db.models import Q  

# Create your views here.
def index(request):
     return render(request, "home_pages/index.html", {})

def login(request):
     return render(request, "home_pages/login.html", {})

def user_registration(request): 
    return render(request,'home_pages/user_registration.html',{}) 

def add_user_registration(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password") 
        fullName = request.POST.get("fullName")
        address = request.POST.get("address")
        mobile = str(request.POST.get("mobile"))
        aadharNumber = request.POST.get("aadharNumber")
        
        userPic = str(rd.randint(1, 10000)) + request.FILES['userPic'].name
        userType = request.POST.get("userType")
        handle_uploaded_file(request.FILES['userPic'], userPic) 


        if password != confirm_password:
            messages.error(request, "Passwords not match.")
            return redirect("home_pages/user_registration")

        
        user = User.objects.create(
            fullName=fullName,
           
            email=email,
            mobile=mobile,
            address=address,
            aadharNumber=aadharNumber,
            userPic=userPic,
            userType=userType,
            password = password
        )
        user.save()
        return redirect("/login")


    return redirect("user_registration")


def login_validation(request):
    if request.method == "POST":
        try:
            if request.POST.get("userType") == "Landlord" or request.POST.get("userType") =="Tenant":
                user = User.objects.get(email=request.POST.get("email"))
                if user.password == request.POST.get("password") and user.userType == request.POST.get("userType") :
                    request.session['userId'] = user.userId
                    request.session['fullName'] = user.fullName
                    request.session['userType'] = user.userType
                    
                    if user.userType == "Landlord":
                        return render(request,'landlord/home.html', {'user':user})
                    elif user.userType == "Tenant":
                        return render(request,'tenant/home.html', {'user':user})
            elif request.POST.get("userType") == "Admin":
                
                admin=Admin.objects.get(username=request.POST.get("email"))
                print('passoword=', admin.password)
                if admin.password ==request.POST.get("password"):
                    return render(request,'admin/home.html')

            else:
                
                messages.error(request, "Invalid username/password.")
                return redirect("/login")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("/login")
        except Exception as eob1:
            messages.error(request, "Invalid Username/password")
            print("error: ", str(eob1))
            return redirect("/login")


def logout(request):
    return render(request, "home_pages/index.html", {})

def landlord_home(request):
    user = User.objects.get(userId=request.session['userId'])
    return render(request,'landlord/home.html', {"user": user})

def tenant_home(request):
    user = User.objects.get(userId=request.session['userId'])
    if request.method == "POST":
        print("okkkk")
        address = request.POST.get("address")
        numberOfBedRooms = request.POST.get("numberOfBedRooms")
        nearByEmenities = request.POST.get("nearByEmenities")
        rentPrice = request.POST.get("rentPrice")

        
        base_criteria = Q(status="Vacant")

        
        additional_filters = Q()

       
        if address:
            additional_filters &= Q(address__icontains=address)

        if numberOfBedRooms:
            additional_filters &= Q(numberOfBedRooms__icontains=numberOfBedRooms)

        if nearByEmenities:
            additional_filters &= Q(nearByEmenities__icontains=nearByEmenities)

        if rentPrice:
            additional_filters &= Q(rentPrice__lte=rentPrice)

        
        combined_criteria = base_criteria & additional_filters

        
        houses = HouseDetails.objects.filter(combined_criteria)
        print(houses.query)
    else:
        houses = HouseDetails.objects.filter(status="Vacant")
        
    
    return render(request,'tenant/home.html', {"houses":houses ,"user": user})

def landlord_profile(request):
    user = User.objects.get(userId=request.session['userId'])
    return render(request, "landlord/profile.html", {"user": user})

def update_landlord_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        fullName = request.POST.get("fullName")
        aadharNumber = request.POST.get("aadharNumber")
        mobile = str(request.POST.get("mobile"))
        address = request.POST.get("address")
        userType = request.POST.get("userType")

        
        user = User.objects.get(email=email)
        user.fullName=fullName
        user.aadharNumber=aadharNumber
        user.email=email
        user.mobile=mobile
        user.address=address
        user.userType=userType
        user.password = password
        
        user.save()
       


    return redirect("/landlord_profile")


def tenant_profile(request):
    user = User.objects.get(userId=request.session['userId'])
    return render(request, "tenant/profile.html", {"user": user})

def update_tenant_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        fullName = request.POST.get("fullName")
        aadharNumber = request.POST.get("aadharNumber")
        mobile = str(request.POST.get("mobile"))
        address = request.POST.get("address")
        userType = request.POST.get("userType")

        
        user = User.objects.get(email=email)
        user.fullName=fullName
        user.aadharNumber=aadharNumber
        user.email=email
        user.mobile=mobile
        user.address=address
        user.userType=userType
        user.password = password
        
        user.save()
       


    return redirect("/tenant_profile")

def add_rent_house(request):
    user = User.objects.get(userId=request.session['userId'])
    return render(request, "landlord/add_rent_house.html", {'user': user})


def add_house_details(request):
    if request.method == "POST":
        landLordId = request.session['userId']
        registerDate = request.POST.get("registerDate")
        address = request.POST.get("address")
        cityName = request.POST.get("cityName")
        houseType = request.POST.get("houseType")
        houseName = request.POST.get("houseName")
        floorNumber = request.POST.get("floorNumber")
        numberOfBedRooms = request.POST.get("numberOfBedRooms")
        numberOfBathRooms = request.POST.get("numberOfBathRooms")
        squareFeet = request.POST.get("squareFeet")
        houseDescription = request.POST.get("houseDescription")
        utilitiesDescription = request.POST.get("utilitiesDescription")
        nearByEmenities = request.POST.get("nearByEmenities")
        
        rentPrice = request.POST.get("rentPrice")
        status = request.POST.get("status")
        
        # Handle file upload
        #houseImage = str(rd.randint(1, 10000)) + request.FILES['houseImage'].name
        #handle_uploaded_file(request.FILES['houseImage'], houseImage)

        if 'houseImage' in request.FILES:
            houseImage = str(rd.randint(1, 10000)) + request.FILES['houseImage'].name
            handle_uploaded_file(request.FILES['houseImage'], houseImage)
        else:
            houseImage = None  # Handle the case where no file is uploaded

        house = HouseDetails.objects.create(
            landLordId=landLordId,
            registerDate=registerDate,
            address=address,
            cityName=cityName,
            houseType=houseType,
            houseName=houseName,
            floorNumber=floorNumber,
            numberOfBedRooms=numberOfBedRooms,
            numberOfBathRooms=numberOfBathRooms,
            squareFeet=squareFeet,
            houseDescription=houseDescription,
            utilitiesDescription=utilitiesDescription,
            houseImage=houseImage,
            nearByEmenities=nearByEmenities,
            
            rentPrice=rentPrice,
            status=status,
        )
        house.save()
        #return redirect("/houses")  
    messages.error(request, "House rent details added.")
    return render(request, 'landlord/add_rent_house.html')


def house_list(request):
    user = User.objects.get(userId=request.session['userId'])
    houses = HouseDetails.objects.filter(landLordId=request.session['userId'])
    return render(request, 'landlord/house_list.html', {'houses': houses,'user':user})

def delete_house(request, house_id):
    house = HouseDetails.objects.get(houseId=house_id)
    house.delete()
    return redirect('/house_list')

def edit_house(request, house_id):
    user = User.objects.get(userId=request.session['userId'])
    house = HouseDetails.objects.get(houseId=house_id)
   
    return render(request, 'landlord/edit_house.html', {'house': house, 'user': user})

def update_house(request, house_id):
    
    house = HouseDetails.objects.get(houseId=house_id)
    if request.method == 'POST':
        
        house.landLordId = request.POST['landLordId']
        house.registerDate = request.POST['registerDate']
        house.address = request.POST['address']
        house.cityName = request.POST['cityName']
        house.houseType = request.POST['houseType']
        house.houseName = request.POST['houseName']
        house.floorNumber = request.POST['floorNumber']
        house.numberOfBedRooms = request.POST['numberOfBedRooms']
        house.numberOfBathRooms = request.POST['numberOfBathRooms']
        house.squareFeet = request.POST['squareFeet']
        house.houseDescription = request.POST['houseDescription']
        house.utilitiesDescription = request.POST['utilitiesDescription']
        house.houseImage = request.POST['houseImage']
        house.nearByEmenities = request.POST['nearByEmenities']
        
        house.rentPrice = request.POST['rentPrice']
        house.status = request.POST['status']
        
        house.save()
        return redirect('/house_list')
    
    return render(request, 'landlord/edit_house.html', {'house': house})
"""
def show_rent_houses(request):  
    houses = HouseDetails.objects.all()  
    user = User.objects.get(userId=request.session['userId'])
    return render(request,"tenant/show_rent_houses.html",{'houses':houses, "user": user}) 
"""
def landlord_details(request, landlord_id):
    landlord = User.objects.get(userId=landlord_id)
    user = User.objects.get(userId=request.session['userId'])
    return render(request, 'tenant/landlord_details.html', {'landlord': landlord, 'user': user})

def admin_home(request):
    return render(request,'admin/home.html')

def admin_landlords(request):
    users = User.objects.filter(userType='Landlord')
    return render(request, 'admin/landlords.html', {'users': users})

def admin_tenants(request):
    users = User.objects.filter(userType='Tenant')
    return render(request, 'admin/tenants.html', {'users': users})

def admin_landlord_houses(request):
    houses = HouseDetails.objects.all()
    return render(request, 'admin/house_list.html', {'houses': houses})