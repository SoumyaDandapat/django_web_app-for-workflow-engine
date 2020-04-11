from django.shortcuts import render , redirect 
from django.http import HttpResponse,HttpResponseRedirect
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
Total_fields = 3

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

new_form = db["new_form"]
template = db["template"]
collection1 = db["collection1"]
privilage = db["admin"]
form_data = db['form_data']
db_comment = db['comment']
db_reply = db['reply']


First = ""
second = ""
x = ""

def registration(request):
    return render(request, 'utility/registration.html')   


def form(request):
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
def generate_new_application(request):
    y = template.find( { "Name": "Admin" } )
    First = y[0]['field_name1']
    second = y[0]['field_name2']
    third = y[0]['field_name3']
    fourth = y[0]['field_name4']
    fifth = y[0]['field_name5']
    sixth = y[0]['field_name6']
    seventh = y[0]['field_name7']
    eighth= y[0]['field_name8']
    print(y[0]['field_name1'])
                
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
    return HttpResponse(x)

@csrf_exempt
def post_data(request):
    if request.method == 'POST':
        print("inside post-data fun")
        Name = request.POST.get('fname')
        Email = request.POST.get('email')
        date = request.POST.get('date')
        Bdate = request.POST.get('bdate')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        url = request.POST.get('url')
        myfile = request.POST.get('myfile')
        new_form.insert_one( { "session_id": request.user.username ,"Firstname": Name, "Email": Email, "date": date , "Birthday": Bdate, "description": description ,"quantity":quantity, "url": url ,"myfile": myfile } )
        ob = new_form.find_one({ "session_id": request.user.username ,"Firstname": Name, "Email": Email, "date": date , "Birthday": Bdate, "description": description ,"quantity":quantity, "url": url ,"myfile": myfile })
        print(str(ob['_id']))
        new_form.update({'_id':ob['_id']},{ "session_id": request.user.username ,"Firstname": Name, "Email": Email, "date": date , "Birthday": Bdate, "description": description ,"quantity":quantity, "url": url ,"myfile": myfile ,'form_id':str(ob['_id'])})
        collection1.insert_one({"session_id": request.user.username , "index": "1" ,"status": "pending.." , "form_id":str(ob['_id'])})
        
        return HttpResponseRedirect("/post_login")

@csrf_exempt
def see_form_status(request):
    username = request.user.username
    ob = collection1.find({"session_id":username})
    form_id =  ""
    index = ''
    status = ''
    moderator =''
    context = {}
    comment = ""
    fields = []
    
    for tmp in  ob:
        if tmp['status']!="accepted":
            form_id = tmp['form_id']
            index = tmp['index']
            status = tmp['status']
    if status == "send_back":
        context['send_back'] = True
    else :
        context['send_back'] = False
    context['status'] = status
    context['form_id'] = form_id
    print("see_fr-st " ,username)
    y = template.find( { "Name": "Admin" } )
    First = y[0]['field_name1']
    second = y[0]['field_name2']
    third = y[0]['field_name3']
    fourth = y[0]['field_name4']
    fifth = y[0]['field_name5']
    sixth = y[0]['field_name6']
    seventh = y[0]['field_name7']
    eighth= y[0]['field_name8']
    
    x = new_form.find({"form_id": form_id})
    if status == "send_back":
        y = db_comment.find_one({"form_id":form_id,"index":index})
        comment = y['comment'][-1]
        context['comment'] = comment
    moderator = privilage.find_one({"index":index})['user_email']

    context['moderator'] = moderator
    if check_(First) != "":
        field = check_(First)
        fields.append(field)
        context[field] = x[0][field]
    if check_(second) != "":
        field = check_(second)
        fields.append(field)
        context[field] = x[0][field]
    if check_(third) != "":
        field = check_(third)
        fields.append(field)
        context[field] = x[0][field]
    if check_(fourth) != "":
        field = check_(fourth)
        fields.append(field)
        context[field] = x[0][field]
    if check_(fifth) != "":
        field = check_(fifth)
        fields.append(field)
        context[field] = x[0][field]
    if check_(sixth) != "":
        field = check_(sixth)
        fields.append(field)
        context[field] = x[0][field]
    if check_(seventh) != "":
        field = check_(seventh)
        fields.append(field)
        context[field] = x[0][field]
    if check_(eighth) != "":
        field = check_(eighth)
        fields.append(field)
        context[field] = x[0][field]
    context['fields'] = fields
    print(context)
    return render(request,'utility/display.html', {'data': context} ) 


@csrf_exempt
def see_all_requests(request):
    username = request.user.username
    data = privilage.find({"user_email":username})
    index = 0
    fields = []
    for tmp in data:
        index = tmp['index']
        fields = tmp['fields']
    print(fields)
    print(index)
    
    ob = db_comment.find({"index":str(index),"status":"pending.."})
    print(ob.count())
    data1 = []
    for tmp in ob:
        data1.append(tmp['form_id'])
        print(tmp['form_id'])
    print(data1)
    data3 = {}
    data3['pendindids'] = data1
    data2 = []
    ob = db_comment.find({"index":index,"status":"send_back"})
    for tmp in ob:
        data2.append(tmp['form_id'])
        print(tmp['form_id'])
    data3['send_back'] = data2
    data2 = []
    ob = db_comment.find({"index":index , "status" : "accepted"})
    for tmp in ob:
        data2.append(tmp['form_id'])
        print(tmp['form_id'])
    data3['accepted'] = data2
    ob = db_comment.find({"index":index , "status":"rejected"})
    data2 = []
    for tmp in ob:
        data2.append(tmp['form_id'])
        print(tmp['form_id'])
    data3['rejected'] = data2
    print(data3)
    return render(request,"utility/display_all_requests.html",{'data':data3})

@csrf_exempt
def detailsofformid(request,form_id):
    form_id = form_id
    print("line 189 ", form_id)
    username = request.user.username
    print(username)
    index = privilage.find_one({"user_email":username})['index']
    ob = new_form.find_one({"form_id": form_id })
    print(ob)
    is_generator = False
    if ob :
        if username == ob['session_id'] :
            is_generator = True
    fields = []
    if is_generator:
        ob = template.find_one({"Name":"Admin"})
        for count in range(1,Total_fields+1):
            if ob[f'field_name{count}']:
                fields.append[ob[f'field_name{count}']]
    else :
        fields = privilage.find_one({"user_email":username})['fields']
    print(is_generator)
    print(fields)
    reply = ''
    data = {}
    data['fields'] = fields
    data['is_generator'] = is_generator
    data['form_id'] = form_id
    ob =db_comment.find_one({"form_id":form_id,"index":index})
    if ob['status']=="rejected" or ob['status'] == "accepted":
        data['terminated'] = True
    ob = new_form.find_one({"form_id":form_id})
    for field in fields :
        data[field] = ob[field]
    ob = db_comment.find_one({"form_id":form_id, "index":index})
    if ob is not None :
        data['comment'] = ob['comment']
    ob = db_reply.find_one({"form_id":form_id,'index':index})
    data['reply'] = ''
    if ob is not None:
        data['reply'] = ob['reply']
    if data['reply']:
        tmp = []
        for (reply,comment) in zip(data['reply'],data['comment']):
            tmp.append({"reply":reply,"comment":comment})
        data['conversation'] = tmp
    print(data)
    return render(request,"utility/formdetails.html",{'data':data})

@csrf_exempt
def sendBackForReview(request , form_id):
    if request.method == "POST":
        comment = request.POST['comment']
        username = request.user.username
        print(comment,username,form_id)
        ob1 = privilage.find_one({"user_email":username})
        ob = db_comment.find_one({"form_id":form_id,"username":username})
        if not ob:
            comment_arr = []
            comment_arr.append(comment)
            db_comment.insert_one({"form_id":form_id,"comment":comment_arr,"username":username,"index":ob1['index'],"status":"send_back"})
        else :
            comment_arr = ob['comment']
            comment_arr.append(comment)
            db_comment.update({"form_id":form_id,"username":username},{"$set" : {"comment":comment_arr,"status":"send_back"}})

        collection1.update({"form_id":form_id} , { "$set" : { "index" : ob1['index'] , "status" : "send_back"  } } )
        return HttpResponseRedirect("/post_login")

@csrf_exempt
def reply(request,form_id):
    reply = request.POST.get('comment')
    username = request.user.username
    print(reply,username,form_id)
    ob = collection1.find_one({"form_id":form_id})
    index = ob['index']
    ob = db_reply.find_one({"form_id":form_id,"index":index})
    if not ob:
        reply_arr = []
        reply_arr.append(reply)
        db_reply.insert_one({"form_id":form_id,"reply":reply_arr,"username":username,"index":index})
    else :
        reply_arr = ob['reply']
        reply_arr.append(reply)
        db_reply.update({"form_id":form_id,"index":index},{"$set" : {"reply":reply_arr}})
    collection1.update({"form_id":form_id},{"$set" : {"index":index, "status":"pending.."}})
    return HttpResponseRedirect("/post_login")


@csrf_exempt
def accept(request,form_id):
    
    comment = request.POST.get('comment')
    username = request.user.username
    print(reply,username,form_id)
    ob = collection1.find_one({"form_id":form_id})
    index = ob['index']
    if int(index) == Total_fields:
        ob = db_comment.find_one({"form_id":form_id,"username":username})
        if not ob:
            comment_arr = []
            comment_arr.append(comment)
            db_comment.insert_one({"form_id":form_id,"comment":comment_arr,"username":username,"index":index,"status":"accepted"})
        else :
            comment_arr = ob['comment']
            comment_arr.append(comment)
            db_comment.update({"form_id":form_id,"username":username},{"$set" : {"comment":comment_arr,"status":"accepted"}})
        collection1.update({"form_id":form_id},{"$set" : {"index":str(int(index)),"status":"accepted"}})
    else :
        ob = db_comment.find_one({"form_id":form_id,"username":username})
        if not ob:
            comment_arr = []
            comment_arr.append(comment)
            db_comment.insert_one({"form_id":form_id,"comment":comment_arr,"username":username,"index":index,"status":"accepted"})
        else :
            comment_arr = ob['comment']
            comment_arr.append(comment)
            db_comment.update({"form_id":form_id,"username":username},{"$set" : {"comment":comment_arr,"status":"accepted"}})
        collection1.update({"form_id":form_id},{"$set" : {"index":str(int(index)+1),"status":"pending.."}})
    return HttpResponseRedirect("/post_login")

@csrf_exempt
def reject(request,form_id):
    comment = request.POST.get('comment')
    username = request.user.username
    print(reply,username,form_id)
    ob = collection1.find_one({"form_id":form_id})
    index = ob['index']
    ob = db_comment.find_one({"form_id":form_id,"username":username})
    if not ob:
        comment_arr = []
        comment_arr.append(comment)
        db_comment.insert_one({"form_id":form_id,"comment":comment_arr,"username":username,"index":index,"status":"rejected"})
    else :
        comment_arr = ob['comment']
        comment_arr.append(comment)
        db_comment.update({"form_id":form_id,"username":username},{"$set" : {"comment":comment_arr,"status":"rejected"}})
    collection1.update({"form_id":form_id},{"$set" : {"index":str(int(index)),"status":"rejected"}})
    return HttpResponseRedirect("/post_login")

@csrf_exempt
def see_records(request):
    username = request.user.username
    ob = collection1.find({"session_id":username})
    ids = []
    for tmp in ob :
        ids.append(tmp['form_id'])
    data = {}
    data['ids'] = ids
    return render(request,'utility/form_record.html',{'data':data})

@csrf_exempt
def fd_to_user(request , form_id):
    ob = collection1.find_one({"form_id":form_id})
    index = ob['index']
    status = ob['status']
    comments = {}
    replies = {}
    data = {}
    ob1 = db_comment.find({"form_id":form_id})
    for tmp in ob1:
        comments[tmp['index']] = tmp['comment']
    ob2 = db_reply.find({"form_id":form_id})
    for tmp in ob2:
        replies[tmp['index']] = tmp['reply']
    data['comments'] = comments
    data['replies'] = replies
    data['index'] = index
    data['status'] = status
    return render(request,'utility/fd_to_user.html',{'data':data})

@csrf_exempt
def post_login(request):
    
    username = request.user.username
    print(username)
    k = 0
    count =  new_form.find({"session_id": username }).count()
    count1 = privilage.find({"user_email":username}).count()
    data = {}
    data['moderator'] = False
    data['pending_form'] = False
    if count1> 0:
        data['moderator'] = True
    ob = collection1.find({"session_id": username })
            
    if ob.count()>0:
        for tmp in ob:
            if tmp['status']!="accepted" and tmp['status'] != "rejected":
                data['pending_form'] = True
    
    print(data)
            
    return render(request,'utility/logged_in_portal.html',{'data':data})

@csrf_exempt
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print('aman')

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(username)
        print(password)
        print(user)
        if user is not None :
            login(request,user)
            if not request.session.session_key:
                request.session.save()
            return redirect('post_login')
        
        else :
            messages.error(request,'Invalid login credentials')
            return HttpResponseRedirect("/index")
    print('kumar')
    form = AuthenticationForm()
    return render( request, 'utility/index.html')




def check_(z):
    if z == "Name":
        return 'Firstname'
    elif z == "Email":
        return 'Email'
    elif z == "Date":
        return 'date'
    elif z == "Bdate":
        return 'Birthday'
    elif z == "myfile":
        return 'myfile'
    elif z == "quantity":
        return 'quantity'
    elif z == "description":
        return 'description'
    elif z == "url":
        return 'url'
    else:
        return ""

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

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('index')

@csrf_exempt
def get_data(request):
    if request.method == 'POST':
    
        First = request.POST.get('field_name1')
        second = request.POST.get('field_name2')
        third = request.POST.get('field_name3')
        fourth = request.POST.get('field_name4')
        fifth = request.POST.get('field_name5')
        sixth = request.POST.get('field_name6')
        seventh = request.POST.get('field_name7')
        eighth = request.POST.get('field_name8')
        
        print(First)
        print(second)
        
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
        template.remove({})
        template.insert_one( { "Name": "Admin" , "field_name1": First ,"field_name2": second ,"field_name3": third,"field_name4": fourth,"field_name5": fifth,"field_name6": sixth,"field_name7": seventh,"field_name8": eighth } )
        return HttpResponse(x)
    elif request.method == 'GET':
        form = AuthenticationForm()
        return render( request, 'utility/form.html')

@csrf_exempt
def admin(request):
    y = template.find( { "Name": "Admin" } )
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
        fnd = False
        index = request.POST.get('index')
        user =  request.POST.get('user')
        fields = request.POST.get('fields')
        fields = [x.strip() for x in fields.split(',')]
        for obj in privilage.find():
            if obj['index'] == index :
                print("updating")
                privilage.update({"index":index},{'index':index,'user_email':user,'fields':fields})
                fnd = True
        if not fnd :
            print(fnd)
            privilage.insert_one({'index':index,'user_email':user,'fields':fields})
        
        for obj in privilage.find():
            if obj['index'] == index :
                print(obj)

        print(index)
        print(fields)
        print(user)
        
        return render(request,'utility/admin.html',{'dictionary': context})

def resetAdmin(request):
    privilage.remove()
    return HttpResponseRedirect("/admin")

def user_detail(request):
    print(request.user.username)
    user = collection1.find({"session_id":request.user.username})
    index = user[0]['index']
    yindex = privilage.find({"index": index })
    print(yindex[0])
    fields = yindex[0]['fields']
    print(fields)
    context = {}
    user = new_form.find({"session_id": request.user.username})
    context[fields[0]] = user[0][fields[0]]
    #context[fields[1]] = user[0][fields[1]]
    print(context)
    return HttpResponse("yes")

                    
    