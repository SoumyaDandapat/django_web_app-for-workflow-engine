from django.shortcuts import render , redirect
from django.template import RequestContext
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.messages import constants as messages
from django.contrib import messages
from django.contrib.auth import authenticate ,logout ,login
from django.views.decorators.csrf import csrf_protect ,csrf_exempt
from bson.json_util import dumps
import pymongo
import json
Total_fields = 8
# Create your views here.

#def index(request):
#    return render(request, 'utility/index.html')

Email = " <label for=\"fname\">Email:</label><input type=\"email\" id=\"email\" name=\"email\"  /> <br><br>"
start = "<form id=\"login-form\" class=\"form\" action=\"\post_data\" method=\"POST\" id=\"form1\" >  "
Name = " <label for=\"fname\">First name:</label><input type=\"text\" id=\"fname\" name=\"fname\" /> <br><br>"
Date = "<label for=\"date\">Date:</label><input type=\"date\" id=\"date\" name=\"date\" /> <br><br>"
Bdate = "<label for=\"date\">Birth Day:</label><input type=\"date\" id=\"date\" name=\"bdate\" /> <br><br>"
myfile = "<label for=\"myfile\">Select a file:</label><input type=\"file\" id=\"myfile\" name=\"myfile\" /> <br><br>"
quantity = "<label for=\"quantity\">Quantity (More than 1):</label><input type=\"number\" id=\"quantity\" name=\"quantity\" min = \"1\"\" /> <br><br>"
description = "<label for=\"description\">Description: </label><input type=\"text\" id=\"description\" name=\"description\" style=\"width: 400px; height: 100px;\"><br><br>"
url = "<label for=\"url\">Add website:</label><input type=\"url\" id=\"url\" name=\"url\"><br><br>"
end =  "<input type=\"submit\" value=\"Submit\"> </form>"

my_client = pymongo.MongoClient("mongodb+srv://aman_kumar_214:amanrani214@mongodbms-nvis8.mongodb.net/test?retryWrites=true&w=majority")
db = my_client.test

try:
   print("MongoDB version is %s" %my_client.server_info()['version'])
   print("database is connected succesfully")
except pymongo.errors.OperationFaliure as error:
   print(error)

mycol = db["new_form"]
myval_x = db["template"]
privilage = db["admin"]

#mycol.insert_one( { "Name": "Aman", "Age": 21 } )

First = ""
second = ""
x = ""

def registration(request):
    return render(request, 'utility/registration.html')   


def form(request):
    print("inside form function")
    if request.method == 'POST':
            if request.POST.get('name') and request.POST.get('email') and request.POST.get('password'):
                post=Post()
                post.name= request.POST.get('name')
                print(post.name)
                post.email_address= request.POST.get('email')
                post.password= request.POST.get('password')
                if User.objects.filter(username = request.POST.get('email') ).exists():
                    messages.info(request, 'username Taken')
                    return redirect('registration')
                else:

                    user = User.objects.create_user(
                        username = request.POST.get('email'),
                        password = request.POST.get('password')
                    )
                    post.save()
                    
                    return HttpResponse('HEllo aman')

            else:
                return HttpResponse("hello aman")

@csrf_exempt
def login_request(request):
    print("inside login_request function")
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print('aman')
        y = True
        if y:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            print(username)
            print(password)
            print(user)
            if user is not None:
                login(request, user)
                y = myval_x.find( { "Name": "Admin" } )
                First = y[0]['field_name1']
                second = y[0]['field_name2']
                third = y[0]['field_name3']
                fourth = y[0]['field_name4']
                fifth = y[0]['field_name5']
                sixth = y[0]['field_name6']
                seventh = y[0]['field_name7']
                eighth= y[0]['field_name8']
                print(y[0]['field_name1'])
                '''
                if First == "Name":
                    x=start+Name +Email+end
                else:
                    x=start+Email+Name+end
                '''
                x=start
                x=x+check(First)
                x=x+check(second)
                x=x+check(third)
                x=x+check(fourth)
                x=x+check(fifth)
                x=x+check(sixth)
                x=x+check(seventh)
                x=x+check(eighth)
                x=x+end
                if len(x)>1:
                    return HttpResponse(x)
                else :
                    return HttpResponse("you are loggoed in")
                
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    print('kumar')
    form = AuthenticationForm()
    return render( request, 'utility/index.html')

@csrf_exempt
def post_data(request):
    print("inside post_data function")
    if request.method == 'POST':
        Name = request.POST.get('fname')
        Email = request.POST.get('email')
        date = request.POST.get('date')
        Bdate = request.POST.get('bdate')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        url = request.POST.get('url')
        myfile = request.POST.get('myfile')
        print(Name)
        print(Email)
        print(Bdate)
        print(quantity)
        print(description)
        print(url)
        mycol.insert_one( { "Firstname": Name, "Email": Email, "date ": date , "Birthday": Bdate, "Description": description ,"Quantity":quantity, "Url": url ,"Myfile": myfile } )
        return HttpResponse("data entered")

def check(z):
    if z == "Name":
        return Name
    elif z == "Email":
        return Email
    elif z == "Date":
        return Date
    elif z == "Bdate":
        return Bdate
    elif z == "myfile":
        return myfile
    elif z == "quantity":
        return quantity
    elif z == "description":
        return description
    elif z == "url":
        return url
    else:
        return ""


def get_data(request):
    print("inside get_data function")
    if request.method == 'POST':
      
        First = request.POST.get('field_name1')
        second = request.POST.get('field_name2')
        third = request.POST.get('field_name3')
        fourth = request.POST.get('field_name4')
        fifth = request.POST.get('field_name5')
        sixth = request.POST.get('field_name6')
        seventh = request.POST.get('field_name7')
        eighth = request.POST.get('field_name8')
        #fieldname = request.POST.get('field_name')
        #Email = request.POST.get('Email')
        #Price = request.POST.get('price')
        print(First)
        print(second)
        #mycol.insert_one( { "Firstname": Firstname, "Lastname": Lastname, "Email id ": Email } )
        #end =   " <button type=\"submit\" form=\"form1\" value=\"Submit\">Submit</button>  "
        ''' 
        if First == "Name":
            x = start+Name+Email+end
        else:
            x= start+Email+Name+end
        '''
        x=start
        x=x+check(First)
        x=x+check(second)
        x=x+check(third)
        x=x+check(fourth)
        x=x+check(fifth)
        x=x+check(sixth)
        x=x+check(seventh)
        x=x+check(eighth)
        x=x+end
        myval_x.remove({})
        myval_x.insert_one( { "Name": "Admin" , "field_name1": First ,"field_name2": second ,"field_name3": third,"field_name4": fourth,"field_name5": fifth,"field_name6": sixth,"field_name7": seventh,"field_name8": eighth } )
        return HttpResponse(x)
        
        #return render( request, "AMAN")
    form = AuthenticationForm()
    return render( request, 'utility/form.html')
@csrf_exempt
def admin(request):
    y = myval_x.find( { "Name": "Admin" } )
    print(Total_fields)
    context ={}
    context['number_of_fields'] = Total_fields
    for i in range(1,Total_fields+1):
        print(i)
        context[f'field_name{i}'] = y[0][f'field_name{i}']
    if request.method == 'GET':
        print("inside admin fn")
        
        print(y[0][f'field_name{i}'])
        print(y[0])
        return render(request,'utility/admin.html',{'dictionary': context})
    elif request.method == "POST":
        index = request.POST.get('index')
        fields = request.POST.get('fields')
        fields = [x.strip() for x in fields.split(',')]
        if(len(fields)!=0):
            privilage.insert_one({"index":index,"fields":fields})
        for obj in privilage.find():
            if obj['index'] == index :
                print(obj)
        print(index)
        print(fields)
        request.method = "GET"
        return render(request,'utility/admin.html',{'dictionary': context})

    