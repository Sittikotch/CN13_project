from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from database.models import *
import sys, requests, json

def index(request):
    print("index")
    return render(request, 'index.html')

def login(request):
    print("login")

    if request.method == "POST":
        print("post login")
        try :
            access_token = request.POST.get('access_token')
            params = {
                'access_token': access_token,
            }
            check_verify_response = requests.get('https://api.line.me/oauth2/v2.1/verify', params=params)

            if check_verify_response.status_code == status.HTTP_200_OK:
                headers = {
                    'Authorization':f'Bearer {access_token}',
                }
                response = requests.get('https://api.line.me/v2/profile', headers=headers)
                userId = json.loads(response.text)["userId"]

                form = StudentForm(request.POST)
                sid = request.POST.get('sid')
                fname = request.POST.get('fname')
                lname = request.POST.get('lname')
                tel = request.POST.get('tel')
                dept = request.POST.get('dept')

                print(sid)
                print(fname)
                print(lname)
                print(tel)
                print(dept)

                if form.is_valid:
                    if Student.objects.filter(userId=userId).exists():
                        message.info(request, 'This Employee Id Already Used!')
                        return HttpResponse(json.dumps(userId), content_type='application/json')
                    else:
                        try:
                            nstudent = Student(
                                userId = userId,
                                sid = sid,
                                fname = fname,
                                lname = lname,
                                tel = tel,
                                dept = dept,
                            )
                            nstudent.save()
                            return HttpResponse(json.dumps(nstudent), content_type='application/json')
                        except KeyError as e:
                            messages.info(request, "Can't saved in DB")
                            return HttpResponse(json.dumps(userId), content_type='application/json')
        except Exception as e:
            print("{0} : {1}".format(sys.exc_info()[-1].tb_lineno,str(e)))
            return HttpResponse(json.dumps({'message': 'Get some errors'},default=str), content_type="application/json")
    else:
        form = StudentForm()
        return render(request, 'login.html')

def line_api(request):
    print("line_api")
    try :
        access_token = request.POST.get('access_token')
        params = {
            'access_token': access_token,
        }
        check_verify_response = requests.get('https://api.line.me/oauth2/v2.1/verify', params=params)

        if check_verify_response.status_code == status.HTTP_200_OK:
            headers = {
                'Authorization':f'Bearer {access_token}',
            }
            response = requests.get('https://api.line.me/v2/profile', headers=headers)
            userId = json.loads(response.text)["userId"]
            
            data = {
                'is_taken': Student.objects.filter(userId=userId).exists()
            }

            if(data['is_taken']):
                student = Student.objects.get(userId=userId)
                data['userId'] = student.userId
                data['sid'] = student.sid
                data['fname'] = student.fname
                data['lname'] = student.lname
                data['tel'] = student.tel
                data['dept'] = student.dept

                print("return data")
                return HttpResponse(json.dumps(data), content_type='application/json')  
            
            print("return empty")
            return HttpResponse(json.dumps(data), content_type='application/json')  

    except Exception as e:
        print("{0} : {1}".format(sys.exc_info()[-1].tb_lineno,str(e)))
        return HttpResponse(json.dumps({'message': 'Get some errors'},default=str), content_type="application/json")


# def line_api_add_db(request):
#     if request.method == "POST":
#         print("line_api_add_db")
#         try :
#             access_token = request.POST.get('access_token')
#             params = {
#                 'access_token': access_token,
#             }
#             check_verify_response = requests.get('https://api.line.me/oauth2/v2.1/verify', params=params)

#             if check_verify_response.status_code == status.HTTP_200_OK:
#                 headers = {
#                     'Authorization':f'Bearer {access_token}',
#                 }
#                 response = requests.get('https://api.line.me/v2/profile', headers=headers)
#                 userId = json.loads(response.text)["userId"]

#                 form = StudentForm(request.POST)
#                 sid = request.POST.get('sid')
#                 fname = request.POST.get('fname')
#                 lname = request.POST.get('lname')
#                 tel = request.POST.get('tel')
#                 dept = request.POST.get('dept')

#                 if form.is_valid:
#                     if Student.objects.filter(userId=userId).exists():
#                         message.info(request, 'This Employee Id Already Used!')
#                     else:
#                         try:
#                             nstudent = Student(
#                                 userId = userId,
#                                 sid = sid,
#                                 fname = fname,
#                                 lname = lname,
#                                 tel = tel,
#                                 dept = dept,
#                             )
#                             nstudent.save()
#                             return HttpResponse(json.dumps(nstudent), content_type='application/json')
#                         except KeyError as e:
#                             messages.info(request, "Can't saved in DB")
#         except Exception as e:
#             print("{0} : {1}".format(sys.exc_info()[-1].tb_lineno,str(e)))
#             return HttpResponse(json.dumps({'message': 'Get some errors'},default=str), content_type="application/json")
#     else:
#         form = StudentForm()
#         return render(request,"login.html",{})
