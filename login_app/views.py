from django.shortcuts import render,redirect
from django.contrib import messages
import bcrypt
from . models import User


# -------
# from django.utils import timezone
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import User, PasswordResetToken
# import uuid
# ---------

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "GET":
        return redirect("/")

    errors=User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect("/")
    else:
        # include some logic to validate user input before adding them to the database!
        password=request.POST["Password"]
        # create the hash 
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
        print (pw_hash)
        new_user=User.objects.create(
            first_name=request.POST["First_name"],
            last_name=request.POST["Last_name"],
            email=request.POST["Email"],
            password=pw_hash
        )
        request.session["user_id"]=new_user.id
        # messages.success(request, "You have successfully registered!")
    return redirect("/books/dashboard")


def login(request):
    if request.method == "GET":
        return redirect("/")
    errors=User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect("/")
    else:
        logged_user = User.objects.get(email=request.POST["Email"])
        # log user in
        request.session["user_id"] = logged_user.id
        # messages.success(request, "You have successfully logged in!")
        return redirect("/books/dashboard")

def logout(request):
    request.session.clear()
    # request.session.flush()
    return redirect("/")


# -----------
# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         user = User.objects.filter(email=email).first()
#         if user:
#             # Generate a unique token for the user and save it to the database
#             token = str(uuid.uuid4())
#             PasswordResetToken.objects.create(user=user, token=token, created_at=timezone.now())
#             # Send an email to the user with a link to reset their password
#             reset_url = request.build_absolute_uri('/reset_password/') + f'?token={token}'
#             send_mail(
#                 'Reset your password',
#                 f'Click this link to reset your password: {reset_url}',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [user.email],
#                 fail_silently=False,
#             )
#             messages.success(request, 'A password reset link has been sent to your email.')
#         else:
#             messages.error(request, 'That email does not exist in our database.')
#     return render(request, 'forgot_password.html')

# def reset_password(request):
#     token = request.GET.get('token')
#     token_obj = PasswordResetToken.objects.filter(token=token).first()
#     if not token_obj:
#         messages.error(request, 'Invalid or expired password reset link.')
#         return redirect('forgot_password')
#     if (timezone.now() - token_obj.created_at).days > 1:
#         messages.error(request, 'The password reset link has expired.')
#         return redirect('forgot_password')
#     if request.method == 'POST':
#         password = request.POST['password']
#         password_confirm = request.POST['password_confirm']
#         if password != password_confirm:
#             messages.error(request, 'Passwords do not match.')
#         elif len(password) < 7:
#             messages.error(request, 'Password must be at least 7 characters long.')
#         else:
#             # Update the user's password and delete the token
#             user = token_obj.user
#             user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
#             user.save()
#             token_obj.delete()
#             messages.success(request, 'Your password has been reset.')
#             return redirect('login')
#     return

# def ChangePassword(request):
#     return render(request, 'change_password.html')

# def ForgetPassword(request):
#     try: 
#         if request.method == 'POST':
#             username = request.POST.get('username')
#             if not User.objects.filter(username = username).first():
#                 messages.success(request, 'No user found with this email address.')
#                 return redirect("/forget_password/")
            
#             user_obj = User.objects.get(username = username)

#     except Exception as e:
#         print(e)
#     return render(request, "forget_password.html")







