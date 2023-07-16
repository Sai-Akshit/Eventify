import pandas as pd
import csv

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError

from .models import Participant
from .forms import ParticipantForm
from .decorators import unauthenticated_user

@login_required(login_url='/login')
def home(request):
    context = {}
    data = Participant.objects.all()

    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    return render(request, 'main/home.html', context)

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('main:verifyUser')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('main:login')
        
    return render(request, 'main/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def upload_file(request):
    context = {}
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        try:
            df = pd.read_excel(excel_file, sheet_name='Sheet1')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('main:upload_file')
        try:
            for index, row in df.iterrows():
                obj = Participant()
                obj.name = row['Name'].title()
                obj.email = row['Email']
                obj.regNum = row['Registration Number'].upper()
                obj.course = row['Course']
                obj.branch = row['Branch'].upper()
                obj.year = row['Year']

                obj.save()
        except Exception as e:
            context['error'] = str(e)
            return render(request, 'main/upload.html', context)
        return redirect('main:home')
    return render(request, 'main/upload.html', context)

@login_required(login_url='/login')
def verifyUser(request):
    """View to verify the user with their registration number"""
    context = {}
    if request.method == 'POST':
        regNum = request.POST.get('regNo').upper()
        try:
            user = Participant.objects.get(regNum=regNum)
            if not user.verified:
                user.verified = True
                user.save()
                context['message'] = 'User verified successfully'
                return render(request, 'main/scan.html', context)
            else:
                context['error'] = 'User already verified'
                return render(request, 'main/scan.html', context)
        except Participant.DoesNotExist:
            context['error'] = 'Invalid Registration Number'
        except Exception as e:
            context['error'] = str(e)
        
    return render(request, 'main/scan.html', context)

@login_required(login_url='/login')
def download_data(request):
    """View to download emails of verified participants"""
    data = Participant.objects.filter(verified=True).values_list('email', flat=True)
    emails = [i for i in data]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="verified_emails.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'usernameOrEmail'])

    for email in emails:
        writer.writerow(['', email])

    return response

def registerUser(request):
    """View to register a participant"""
    context = {
        'years': ['1', '2', '3', '4'],
    }
    if request.method == 'POST':
        name = request.POST.get('name').title()
        email = request.POST.get('email')
        regNum = request.POST.get('regno').upper()
        course = request.POST.get('course')
        branch = request.POST.get('branch').upper()
        year = request.POST.get('year')

        try:
            participant = Participant(name=name, email=email, regNum=regNum, course=course, branch=branch, year=year)
            participant.full_clean()
            participant.save()
        except ValidationError as e:
            return HttpResponseServerError(str(e))

        return render(request, 'main/success.html')

    return render(request, 'main/register.html', context)

def deleteUser(request):
    # Django view that deletes the user from the database
    if request.method == 'POST':
        regNum = request.POST.get('regNo').upper()
        try:
            user = Participant.objects.get(regNum=regNum)
            user.delete()
            return HttpResponse('User deleted successfully')
        except Participant.DoesNotExist:
            return HttpResponseServerError('Invalid Registration Number')
        except Exception as e:
            return HttpResponseServerError(str(e))