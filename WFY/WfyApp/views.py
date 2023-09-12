from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from validate_email import validate_email
from .models import Profile
from .forms import LoginForm, SignUpForm
from django.core.mail import EmailMessage
from django.conf import settings
from .decorators import auth_user_should_not_access
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
import threading
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from django.contrib import messages

User = get_user_model()


# Create your views here.
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('Activation.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()


@auth_user_should_not_access
def Login(request):
    form = SignUpForm()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user and not user.is_email_verified:
            messages.error(request, '⚠️ Email is not verified, please check your email inbox')
            return render(request, 'Login.html')

        if not user:
            messages.error(request, '⚠️ Invalid credentials, try again')
            return render(request, 'Login.html')
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            return redirect(reverse('Dashboard'))

    return render(request, 'Login.html', {'form': form})


@auth_user_should_not_access
def Register(request):
    form = SignUpForm()

    if request.method == "POST":
        context = {'has_error': False}
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if len(password1) < 6:
            messages.error(request, '⚠️ Password should be at least 6 characters for greater security')
            return redirect('Register')

        if password1 != password2:
            messages.error(request, '⚠️ Password Mismatch! Your Passwords Do Not Match')
            return redirect('Register')

        if not validate_email(email):
            messages.error(request, '⚠️ Password Mismatch! Your Passwords Do Not Match')
            return redirect('Register')

        if not username:
            messages.error(request, '⚠️ Username is required!')
            return redirect('Register')

        if User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ Username is taken! Choose another one')

            return render(request, 'Register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, '⚠️ Email is taken! Choose another one')

            return render(request, 'Register.html')

        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email)
        user.set_password(password1)
        user.save()

        if not context['has_error']:
            send_activation_email(user, request)

            messages.success(request, '✅ Sign Up Successful! We sent you an email to verify your account')
            return redirect('Register')

    return render(request, 'Register.html', {'form': form})


def Logout(request):
    logout(request)
    messages.success(request, '✅ Successfully Logged Out!')
    return redirect(reverse('Login'))


def ActivateUser(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.success(request, '✅ Email Verified! You can now Log in')
        return redirect(reverse('Login'))

    return render(request, 'Activation Failed.html', {"user": user})


def Dashboard(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        return render(request, 'Dashboard.html', {'user': user})
    else:
        return redirect('Login')


def index(request):
    return render(request, 'wfytemp/index.html')


def about(request):
    return render(request, 'wfytemp/about.html')


def Button(request):
    return render(request, "wfytemp/button.html")


def Profile(request):
    return render(request, "wfytemp/profile.html")


def services(request):
    return render(request, "wfytemp/Services.html")


def sign_in(request):
    return render(request, "wfytemp/sign-in.html")


def sign_up(request):
    return render(request, "wfytemp/sign-up.html")


def after_profile(request):
    return render(request, 'wfytemp/after-profile.html')


def contact(request):
    return render(request, 'wfytemp/contact.html')

#developer Profiles
def Profile1(request):
    return render(request, "developer/profile1.html")

def Profile2(request):
    return render(request, "developer/profile2.html")

def Profile3(request):
    return render(request, "developer/profile3.html")

def Profile4(request):
    return render(request, "developer/profile4.html")

def Profile5(request):
    return render(request, "developer/profile5.html")

def Profile6(request):
    return render(request, "developer/profile6.html")

def Profile7(request):
    return render(request, "developer/profile7.html")

def Profile8(request):
    return render(request, "developer/profile8.html")

def Profile9(request):
    return render(request, "developer/profile9.html")


def contact(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        feedback = request.POST['feedback']

        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO contact_data(full_name, email, feedback) VALUES (%s, %s, %s)", [full_name, email, feedback])
                connection.commit()

                # Add a success message
                messages.success(request, 'Feedback submitted successfully.')

        except IntegrityError as e:
            # Handle the exception, e.g., log the error
            print(f"Error inserting data: {e}")

        # Redirect back to the same page
        return redirect('contact')  # Use the URL name for the contact page

    return render(request, 'wfytemp/contact.html')
