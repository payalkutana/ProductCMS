from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from .handler_methods import send_activation_email
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from .models import CustomUser

def activate_account(request, uidb64, token):
    try:

        uid = force_str(urlsafe_base64_decode(uidb64).decode())
        user = CustomUser.objects.get(pk=uid)
        print(uid,user)
        
        if default_token_generator.check_token(user, token):
           
            if request.method == 'POST':

                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                
                if password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return render(request, 'user/failure.html')

                user.set_password(password)
                user.is_active = True
                user.save()

                return redirect('login')
        
            return render(request, 'user/set_password.html')

        else:
            messages.error(request, 'Invalid activation link or token has expired.')
            return render(request, 'user/failure.html')

    except Exception as e:
        print(e)
        messages.error(request, 'Invalid activation link.')
        return render(request, 'user/failure.html') 

def home(request, pk=None):
    user = get_object_or_404(CustomUser,id=pk)
    print("Home ",user.id)
    return render(request, 'user/index.html', {'user_id':user.id})

def ListUserView(request):
    if request.method == "GET":
        users = CustomUser.objects.all()
        print(users)
        return render(request, 'user/list_user.html', {"users":users})

def UpdateUserView(request,pk):
    print("login user :",request.user)
    user = get_object_or_404(CustomUser,id=pk)
    if request.method == "POST":
        try:
            serializer = CustomUserSerializer(user, data=request.POST, partial=True)
            if serializer.is_valid():
                serializer.save()
                messages.success(request, 'User updated successfully!')
                if request.user.is_superuser:
                    return redirect('list_user')
                else:
                    return render(request, 'user/index.html', {'user_id':user.id})
            
            messages.error(request, 'Something Went Wrong!')
            if request.user.is_superuser:
                    return redirect('list_user')
            else:
                return render(request, 'user/index.html', {'user_id':user.id})
        
        except Exception as e:
            messages.error(request, str(e))
            return redirect('list_user')
        
    return render(request, 'user/update_user.html', {"user":user, "login_user":request.user})

def DeleteUserView(request, pk):
    user = get_object_or_404(CustomUser,id=pk)

    if request.method == "POST":
        try:
            user.delete()
            messages.success(request, 'User Deleted successfully!')
            return redirect('list_user')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('list_user')
        
    return redirect('list_user')

class AdminView(APIView):
    def get(self,request):
        return render(request,'user/admin_index.html')
  
class CreateUserView(APIView):
    def get(self, request):
        return render(request, 'user/create_user.html')
    
    def post(self, request):
        # print(request.data)
        serializer = CustomUserSerializer(data=request.data)
       
        if serializer.is_valid():
            user = serializer.save()  

            print("user:",user.pk)
            send_activation_email(user)
            messages.info(request, 'User Created Successfully!')
            return redirect('list_user')
        else:
            messages.error(request,str(serializer.error))
            return render(request, 'user/failure.html')

class UpdateProfileView(APIView):
    pass

class LoginView(APIView):
    def get(self,request):
        return render(request,'user/login.html')
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username == None:
            return render(request, 'user/failure.html')
        
        if  password == None:
            return render(request, 'user/failure.html')
            
        print("username :", username)
        print('password :',password)

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            print("User Authentication Success")
            token, created = Token.objects.get_or_create(user=user)
            if user.is_superuser:
                return redirect('admin_index')
            
            return render(request, 'user/index.html', {'user_id':user.id})
        
        else:
            messages.error(request, 'Something Went Wrong! Try Again')
            return redirect('login')
 