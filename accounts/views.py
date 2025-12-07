from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # 1. Get the form instance but do not save to DB yet
            user = form.save(commit=False)
            
            # 2. Get the password from cleaned_data
            password = form.cleaned_data['password']
            
            # 3. Manually encrypt (hash) the password
            user.set_password(password)
            
            # 4. Handle Username (Model requires it, but Form doesn't have it)
            # usually we generate it from email
            email = form.cleaned_data['email']
            username = email.split("@")[0]
            user.username = username

            # 5. Handle is_active
            # Your model default is False. If you don't have email verification yet,
            # you must set this to True to login.
            # user.is_active = True 
            
            # 6. Save the user object finally
            user.save()
            
            # user activation
            current_site=get_current_site(request); 
            mail_subject='please activate your account'
            message=render_to_string('accounts/account_verification_email.html',
                        {
                            'user':user,
                            'domain':current_site,
                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                            'token':default_token_generator.make_token(user)
                        }     )

            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])    
            send_email.send()                                      
            
            # messages.success(request,'Registration successful')
            # send verfication email to your email to your email address
            return redirect('/accounts/login/?command=verification&email='+email)
           



            # messages.success(request, 'Registration successful. You can now login.')
            # return redirect('login')
            
    else:
        form = RegistrationForm()
        
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(req):
    if req.method=='POST':
        email=req.POST['email']
        password=req.POST['password']

        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(req,user)
            return redirect('home')
        else:
            messages.error(req,'invalid login credential')  
            return redirect('login')      
    return render(req,'accounts/login.html')

# only will be able to logout if you are logged in . you cannot logout maunally
@login_required(login_url='login')
def logout(req):
    auth.logout(req)
    messages.success(req,'you are logged out')
    return redirect('login')


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        # messages.success(request,'congratualtion your account is activated. ')
        return redirect('login')
    else:
        messages.error(request,'invalid activatoin link')
        return redirect('register')


@login_required(login_url='login') #force to login without 
def dashboard(request):
    return render(request,'accounts/dashboard.html')



# check if email exist
def forgotPassword(req):
    if req.method=='POST':
        email=req.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)


            current_site=get_current_site(req); 
            mail_subject='Reset your password'
            message=render_to_string('accounts/reset_password_email.html',
                        {
                            'user':user,
                            'domain':current_site,
                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                            'token':default_token_generator.make_token(user)
                        }     )

            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])    
            send_email.send()     

            messages.success(req,'password reset email has been sent to your email address')  
            return redirect('login')                               
            

        else: 
            messages.error(req,'Account does not exist')  
            return redirect('forcePassword')
    return render(req,'accounts/forgotPassword.html')
    

def resetpassword_validate(req,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):  
        req.session['uid']=uid; 
        messages.success(req,'please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(req,'this link has been expired!')
        return redirect('login')
    

def resetPassword(req):
    if req.method=='POST':
        password=req.POST['password']
        confirmed_password=req.POST['confirmed_password']

        if password==confirmed_password:
           uid=req.session.get('uid')
           user=Account.objects.get(pk=uid)
           user.set_password(password)
           user.save()
           messages.success(req,'password reset succeful')
           return redirect('login')    

        else:
            messages.error(req,'Password does not match')
            return redirect('resetPassword')    
    else:
        return render(req,'accounts/resetPassword.html')