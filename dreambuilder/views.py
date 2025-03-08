import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
import datetime
from dreambuilder.models import *
import random

# Create your views here.
def home(request):
    return render(request,'admin/index.html')

def logins(request):
    return render(request,'index.html')

def loginpost(request):
    name=request.POST['textfield']
    paswrd=request.POST['textfield2']
    res = Login.objects.filter(username=name,password=paswrd)
    if res.exists():
        loginid=res[0].id
        request.session['logid']=loginid
        request.session['log']='lo'
        if res[0].usertype == 'admin':
            return render(request,'admin/index.html')
        elif res[0].usertype == 'contractor':
            return render(request,'contractor/index.html')
        elif res[0].usertype == 'dealer':
            return render(request,'dealer/index.html')
        else:
            return HttpResponse("<script>alert('Permission Not Granted');window.location='/'</script>")
    else:
        return HttpResponse("<script>alert('Unvalid Username or Password');window.location='/'</script>")

def logout(request):
    request.session['logid']=""
    return HttpResponse("<script>alert('logout');window.location='/'</script>")



def view_material(request):
       vew=Material.objects.all()
       return render(request,'admin/ViewMaterial.html', {'data':vew})

def add_material(request):
    return render(request,'admin/AddMaterial.html')

def add_material_post(request):
    met = request.POST['textfield']
    obj = Material()
    obj.material_name = met
    obj.save()
    return HttpResponse("<script>alert('added');window.location='/view_material#uu'</script>")

def update_material(request,id):
    mat = Material.objects.get(id=id)
    return render(request,'admin/UpdateMaterial.html', {'data': mat})

def update_material_post(request,id):
    met = request.POST['textfield']
    Material.objects.filter(id=id).update(
        material_name=met
    )
    return HttpResponse("<script>alert('added');window.location='/view_material'</script>")

def delete_material_post(request,id):
    Material.objects.get(id=id).delete()
    return HttpResponse("<script>alert('removed');window.location='/view_material'</script>")

def confirm_pass(request):
    return render(request, 'admin/confirmpass.html')

def confirm_pass_post(request):
    mail = request.POST['textfield']
    qry=Login.objects.get(username=mail)

    import smtplib

    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login('dreambuildermac@gmail.com', 'acwi hyqk qzkn gkom')
    msg = MIMEMultipart()  # create a message.........."
    msg['From'] = "dreambuildermac@gmail.com"
    msg['To'] = mail
    msg['Subject'] = "Your Password for Dream Builder Website."
    body = "Your Password is:- - " + str(qry.password)
    msg.attach(MIMEText(body, 'plain'))
    s.send_message(msg)
    return HttpResponse("<script>alert('Success!!');window.location='/'</script>")


def add_plan(request):
    return render(request,'admin/Add plan.html')

def add_plan_post(request):
    rm_count = request.POST['textfield']
    bd_count = request.POST['textfield2']
    br_count = request.POST['textfield3']
    pln = request.FILES['fileField']
    dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fs = FileSystemStorage()
    fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\'+dt+'.jpg', pln)
    img = "/static/plan/"+dt+'.jpg'
    obj =Plan()
    obj.room_count=rm_count
    obj.bedroom_count=bd_count
    obj.bathroom_count=br_count
    obj.plan_image=img
    obj.save()
    return HttpResponse("<script>alert('added');window.location='/view_plan'</script>")

def view_plan(request):
    pln = Plan.objects.all()
    return render(request,'admin/View_plan.html', {'data': pln})

def update_plan_post(request,id):
    try:
        rm_count = request.POST['textfield']
        bd_count = request.POST['textfield2']
        br_count = request.POST['textfield3']
        pln = request.FILES['fileField']
        dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        fs = FileSystemStorage()
        fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg', pln)
        img = "/static/plan/" + dt + '.jpg'
        Plan.objects.filter(id=id).update(
            plan_image = img,
            room_count = rm_count,
            bedroom_count=bd_count,
            bathroom_count=br_count
        )
        return HttpResponse("<script>alert('added');window.location='/view_plan'</script>")
    except Exception as e:
        rm_count = request.POST['textfield']
        bd_count = request.POST['textfield2']
        br_count = request.POST['textfield3']

        Plan.objects.filter(id=id).update(
            room_count=rm_count,
            bedroom_count=bd_count,
            bathroom_count=br_count
        )
        return HttpResponse("<script>alert('added');window.location='/view_plan'</script>")

def delete_plan_post(request,id):
    Plan.objects.get(id=id).delete()
    return HttpResponse("<script>alert('removed');window.location='/view_plan'</script>")


def update_plan(request, id):
    pln = Plan.objects.get(id=id)
    return render(request,'admin/Update plan.html', {'data': pln})

def view_contractor_appproval(request):
    vdl = Contractor.objects.filter(LOGIN__usertype='pending')
    return render(request,'admin/ApproveContractor.html',{'data': vdl})

def view_dealer_appproval(request):
    vdl = Dealer.objects.filter(LOGIN__usertype='pending')
    return render(request,'admin/ApproveDealer.html',{'data': vdl})

def dealer_reject(request,id):
    Login.objects.filter(id=id).update(usertype='rejected')
    return HttpResponse("<script>alert('Rejected');window.location='/view_dealer_appproval'</script>")

def contractor_reject(request,id):
    Login.objects.filter(id=id).update(usertype='rejected')
    return HttpResponse("<script>alert('Rejected');window.location='/view_contractor_appproval'</script>")

def block_contractor(request,id):
    Login.objects.filter(id=id).update(usertype='blocked')
    return HttpResponse("<script>alert('Blocked');window.location='/view_contractor_appproval'</script>")

def unblock_contractor(request,id):
    Login.objects.filter(id=id).update(usertype='contractor')
    return HttpResponse("<script>alert('Unblock');window.location='/view_contractor_appproval'</script>")

def unblock_dealer(request,id):
    Login.objects.filter(id=id).update(usertype='dealer')
    return HttpResponse("<script>alert('Unblock');window.location='/view_dealer_appproval'</script>")

def approve_contractor(request,id):
    Login.objects.filter(id=id).update(usertype='contractor')
    return HttpResponse("<script>alert('Contractor Added Sucessfully');window.location='/view_contractor_appproval'</script>")

def approve_dealer(request,id):
    Login.objects.filter(id=id).update(usertype='dealer')
    return HttpResponse("<script>alert('Dealer Added Sucessfully');window.location='/view_dealer_appproval'</script>")


def view_contractor_appproved(request):
    vdl = Contractor.objects.all()
    li=[]
    for i in vdl:
        if i.LOGIN.usertype=='contractor' or i.LOGIN.usertype == 'blocked':
            li.append(i)
    return render(request,'admin/View contractor.html',{'data': li})

def view_dealer_appproval(request):
    dlr=Dealer.objects.filter(LOGIN__usertype="pending")
    return render(request,'admin/ApproveDealer.html',{'data': dlr})

def view_dealer_appproved(request):
    dlr = Dealer.objects.filter(LOGIN__usertype="dealer")
    li = []
    for i in dlr:
        if i.LOGIN.usertype == 'dealer' or i.LOGIN.usertype == 'blocked':
            li.append(i)
    return render(request,'admin/View_dealer.html',{'data': li})

def block_dealer(request,id):
    Login.objects.filter(id=id).update(usertype='blocked')
    return HttpResponse("<script>alert('Blocked');window.location='/view_dealer_appproval'</script>")

def unblock_dealer(request,id):
    Login.objects.filter(id=id).update(usertype='dealer')
    return HttpResponse("<script>alert('Unblocked');window.location='/view_dealer_appproval'</script>")

def block_client(request,id):
    Login.objects.filter(id=id).update(usertype='blocked')
    return HttpResponse("<script>alert('Blocked');window.location='/view_client'</script>")

def unblock_client(request,id):
    Login.objects.filter(id=id).update(usertype='client')
    return HttpResponse("<script>alert('Unblocked');window.location='/view_client'</script>")

def view_client(request):
    cln = Client.objects.all()
    return render(request,'admin/View_client.html', {'data': cln})

def view_dealer_complaint(request):
    cmp = DealerComplaint.objects.all()
    return render(request, 'admin/View_dealer_complaint.html',{'data': cmp})

def view_contractor_complaint(request):
    cmp = ContractorComplaint.objects.all()
    return render(request, 'admin/View_contractor_complaint.html',{'data': cmp})

def client(request):
    return render(request,'admin/Client.html')

def client_post(request):
    cname = request.POST['textfield69']
    dob = request.POST['textfield2']
    email = request.POST['textfield3']
    mobile = request.POST['textfield4']
    building = request.POST['textfield5']
    landmark = request.POST['textfield6']
    town = request.POST['textfield7']
    pincode = request.POST['textfield8']
    state = request.POST['select']
    profile = request.FILES['fileField']
    dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fs = FileSystemStorage()
    fs.save(r'C:\Users\chinm\PycharmProjects\dreambuilders\dreambuilder\static\plan\\' + dt + 'profile' + '.jpg', profile)
    img = "/static/plan/" + dt + 'profile' + '.jpg'
    obj = Client()
    obj.name = cname
    obj.email = email
    obj.phone = mobile
    obj.dob = dob
    obj.building = building
    obj.landmark = landmark
    obj.town = town
    obj.pincode = pincode
    obj.state = state
    # obj.profile = profile
    obj.profile = img
    obj.save()
    return HttpResponse("<script>alert('Regestration Completed');window.location='/'</script>")




# def feedback(request):
#     return render(request,'admin/Feedback.html')

def view_feedback(request):
    vfdk = Feedback.objects.all()
    return render(request,'admin/View_Feedback.html',{'data': vfdk})


def changepass(request):
    return render(request,'admin/changepassw.html')


def changepass_post(request):
    old = request.POST['textfield']
    new = request.POST['textfield2']
    con = request.POST['textfield3']
    data = Login.objects.filter(password=old)
    if data.exists():
        if new == con:
            Login.objects.filter(usertype='admin').update(password = con)
            return HttpResponse("<script>alert('password changed sucessfully');window.location='/changepass'</script>")

        else:
            return HttpResponse("<script>alert('check again');window.location='/changepass'</script>")
    else:
        return HttpResponse("<script>alert('incorrect data');window.location='/changepass'</script>")

# =================================================================
def contractor_plan(request):
    return render(request,'contractor/contractor plan.html')

def contractor_plan_post(request):
    pln = request.FILES['fileField']
    disc = request.POST['textarea']
    dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fs = FileSystemStorage()
    fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\ContractorPlan\\' + dt + '.jpg', pln)
    img = "/static/ContractorPlan/" + dt + '.jpg'
    obj=ContractorPlan()
    obj.plan=img
    obj.discription=disc
    obj.date=dt
    obj.save()

def addcontractor(request):
    return render(request,'contractor/Contractor.html')

def contractor_post(request):
    pname = request.POST['textfield']
    dob = request.POST['textfield3']
    email = request.POST['textfield4']
    phone = request.POST['textfield5']
    busi_name = request.POST['textfield6']
    type = request.POST['RadioGroup1']
    Building = request.POST['textfield7']
    landmark = request.POST['textfield8']
    town = request.POST['textfield9']
    pincode = request.POST['textfield10']
    state = request.POST['select']
    contact = request.POST['textarea3']
    License_num = request.POST['textfield11']
    issued_state = request.POST['select2']
    insurance = request.POST['RadioGroup2']
    work_exp = request.POST['textarea4']
    # past_projct = request.FILES['fileField']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + 'profile' + '.jpg',
            past_projct)
    project_img = "/static/plan/" + dt  + '.jpg'
    yrs_exp = request.POST['textfield13']
    area_epertise = request.POST['textarea5']
    ref = request.POST['textarea6']
    profile_img = request.FILES['fileField2']
    fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + 'profile' + '.jpg', profile_img)
    img = "/static/plan/" + dt + 'profile'  + '.jpg'
    password = request.POST['textfield14']
    alog=Login()
    alog.username = email
    alog.password = password
    alog.usertype = 'pending'
    alog.save()
    obj = Contractor()
    obj.LOGIN=alog
    obj.name = pname
    obj.email = email
    obj.age = "1"
    obj.dob = dob
    obj.phone = phone
    obj.business_name = busi_name
    obj.business_type = type
    obj.building = Building
    obj.landmark = landmark
    obj.town = town
    obj.pincode = pincode
    obj.state = state
    obj.contact_info = contact
    obj.license_num = License_num
    obj.state_issue = issued_state
    obj.insurance_info = insurance
    obj.work_exp = work_exp
    obj.past_project = '1'
    obj.area_expertise = area_epertise
    obj.work_exp = yrs_exp
    obj.reference = ref
    obj.profile = img
    obj.save()
    return HttpResponse("<script>alert('Regestration Request Send');window.location='/'</script>")
# def contractorreview(request):
#     render(request,'contractor/ContractorReview.html')

def edit_contractor(request):
    con = Contractor.objects.get(LOGIN_id= request.session['logid'])
    return render(request,'contractor/editcontractor.html',{'data': con})

def edit_contractor_post(request):
    try:
        pname = request.POST['textfield']
        dob = request.POST['textfield3']
        email = request.POST['textfield4']
        phone = request.POST['textfield5']
        busi_name = request.POST['textfield6']
        type = request.POST['RadioGroup1']
        Building = request.POST['textfield7']
        landmark = request.POST['textfield8']
        town = request.POST['textfield9']
        pincode = request.POST['textfield10']
        state = request.POST['select']
        contact = request.POST['textarea3']
        License_num = request.POST['textfield11']
        issued_state = request.POST['select2']
        insurance = request.POST['RadioGroup2']
        work_exp = request.POST['textarea4']
        dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        area_epertise = request.POST['textarea5']
        ref = request.POST['textarea6']
        profile_img = request.FILES['fileField2']
        fs = FileSystemStorage()
        print(profile_img)
        fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + 'profile' + '.jpg', profile_img)
        img = "/static/plan/" + dt +'profile'+'.jpg'
        Contractor.objects.filter(LOGIN= request.session['logid']).update(phone=phone,email=email,name=pname,dob=dob,business_name=busi_name,business_type=type,building=Building,landmark=landmark,town=town,pincode=pincode,state=state,contact_info=contact,license_num=License_num,state_issue=issued_state,insurance_info=insurance,work_exp=work_exp,area_expertise=area_epertise,reference=ref,profile=img)
        return HttpResponse("<script>alert('updated');window.location='/edit_contractor'</script>")
    except Exception as e:
        print("bbbbbbbbbbbb")
        pname = request.POST['textfield']
        dob = request.POST['textfield3']
        email = request.POST['textfield4']
        phone = request.POST['textfield5']
        busi_name = request.POST['textfield6']
        type = request.POST['RadioGroup1']
        Building = request.POST['textfield7']
        landmark = request.POST['textfield8']
        town = request.POST['textfield9']
        pincode = request.POST['textfield10']
        state = request.POST['select']
        contact = request.POST['textarea3']
        License_num = request.POST['textfield11']
        issued_state = request.POST['select2']
        insurance = request.POST['RadioGroup2']
        work_exp = request.POST['textarea4']
        area_epertise = request.POST['textarea5']
        ref = request.POST['textarea6']
        Contractor.objects.filter(LOGIN_id= request.session['logid']).update(phone=phone, email=email, name=pname, dob=dob, business_name=busi_name,business_type=type,
                                                building=Building, landmark=landmark, town=town,
                                                pincode=pincode, state=state, contact_info=contact,
                                                license_num=License_num, state_issue=issued_state,
                                                insurance_info=insurance, work_exp=work_exp,
                                                area_expertise=area_epertise, reference=ref)
        return HttpResponse("<script>alert('updated');window.location='/edit_contractor'</script>")



def view_contractor_review(request):
    vcr = ContractorReview.objects.all()
    return render(request,'contractor/ContractorReview.html',{'data': vcr})

def daily_report(request,id):
    return render(request, 'contractor/DailyReport.html',{'id':id})

def daily_report_post(request,id):
    date = request.POST['textfield']
    discription = request.POST['textarea']
    labour_num = request.POST['textfield2']
    time = request.POST['textfield3']
    consumed = request.POST['textarea2']
    # did=request.session['did']
    con = Contractor.objects.get(LOGIN= request.session['logid'])
    obj = DailyReport()
    obj.CLIENT_id = id
    obj.date = date
    obj.discription = discription
    obj.labour_num = labour_num
    obj.time = time
    obj.consumed = consumed
    obj.CONTRACTOR=con
    obj.save()
    return HttpResponse("<script>alert('Daily report added');window.location='/view_user_approved'</script>")

def view_daily_report(request,id):
    request.session['did']=id
    data=DailyReport.objects.filter(CONTRACTOR__LOGIN=request.session['logid'])
    # data=DailyReport.objects.all()
    return render(request, 'contractor/ViewDailyReport.html',{'data':data})

def update_daily_report(request,id):
    dal = DailyReport.objects.get(id=id)
    return render(request, 'contractor/EditDailyReport.html', {'data': dal,"id":id})

def update_daily_report_post(request,id):
    date = request.POST['textfield']
    discription = request.POST['textarea']
    labour_num = request.POST['textfield2']
    time = request.POST['textfield3']
    consumed = request.POST['textarea2']
    data = DailyReport.objects.filter(id=id).update(date=date,discription=discription,labour_num=labour_num,time=time,consumed=consumed)
    print(data)
    did=request.session['did']
    return HttpResponse('<script>alert("edited");window.location="/view_daily_report/'+did+'#section_4"</script>')

def remove_daily_report(request,id):
    DailyReport.objects.get(id=id).delete()

    did=request.session['did']
    return HttpResponse("<script>alert('removed');window.location='/view_daily_report/"+did+"#section_4'</script>")

def document(request):
    return render(request, 'contractor/document.html')

def document_post(request):
    doc = request.POST['fileField']
    obj = Document()
    obj.doc = doc
    obj.save()

def feedback(request):
    return render(request, 'contractor/Feedback.html')

def feedback_post(request):
    dt = datetime.datetime.now().strftime('%d/%m/%Y')
    tm = datetime.datetime.now().strftime('%H:%M:%S')
    feedback = request.POST['textarea']
    obj = Feedback()
    obj.date = dt
    obj.time = tm
    obj.type = 'contractor'
    obj.feedback = feedback
    obj.LOGIN_id = request.session['logid']
    obj.save()
    return HttpResponse("<script>alert('Feedback send');window.location='/feedback'</script>")

def update_finance(request,id):
    fin = Finance.objects.get(id=id)
    return render(request, 'contractor/UpdateFinance.html', {'data': fin})


def update_finance_post(request,id):
    fid=request.session['reqid']
    date = request.POST['textfield']
    disc = request.POST['textfield2']
    income = request.POST['textfield3']
    expense = request.POST['textfield4']
    print(date,disc,"uppppppppp")

    Finance.objects.filter(id=id).update(date=date,discription=disc,income=income,expense=expense)
    return HttpResponse('<script>alert("edited");window.location="/finance/' + fid + '#section_4"</script>')

def delete_finance(request,id):
    fid = request.session['reqid']
    Finance.objects.get(id=id).delete()
    return HttpResponse('<script>alert("removed");window.location="/finance/' + fid + '#section_4"</script>')

def finance(request,id):
    print("sdxfcgvhb")
    request.session['reqid']=id
    ob=UserRequest.objects.get(id=id)
    obj = Finance.objects.filter(USERREQUEST=id, CONTRACTOR__LOGIN=request.session['logid'])

    sum = 0
    sume = 0
    simp = 0
    for i in obj:
        print(i)
        sum=int(sum)+int(i.income)
        sume=int(sume)+int(i.expense)
        print(sum,sume,"ttttttt")
    simp=int(sum)-int(sume)
    print(obj)
    return render(request, 'contractor/finance.html',{"data": obj,'ob':ob,'id':id,"sum":sum,"sume":sume,"simp":simp})

def finance_post(request,id):

    date = request.POST.getlist('textfield')
    disc = request.POST.getlist('textfield2')
    income = request.POST.getlist('textfield3')
    expense = request.POST.getlist('textfield4')
    print(expense,"uuuu")
    fin = UserRequest.objects.get(id=id)
    for i in range(0,len(date)):
        if date[i] != '':
            obj = Finance()
            obj.date = date[i]
            obj.CONTRACTOR = Contractor.objects.get(LOGIN_id=request.session['logid'])
            obj.discription = disc[i]
            obj.income = income[i]
            obj.expense = expense[i]
            obj.USERREQUEST=fin
            obj.save()
    return HttpResponse('<script>alert("Added");window.location="/finance/'+id+'#section_4"</script>')

def gallery(request):
    return render(request, 'contractor/gallery.html')

def gallery_post(request):
    img = request.FILES['fileField']
    disc =  request.POST['textarea']
    print(request.session['logid'])

    dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fs=FileSystemStorage()
    fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + 'profile' + '.jpg',
            img)
    img = "/static/plan/" + dt + 'profile' + '.jpg'
    obj = Gallary()
    obj.image = img
    obj.discription = disc
    obj.CONTRACTOR = Contractor.objects.get(LOGIN_id=request.session['logid'])
    obj.save()
    return HttpResponse("<script>alert('Added');window.location='/view_gallery#section_4'</script>")

def progress(request):
    return render(request, 'contractor/Progress.html')

def progress_post(request):
    date = request.POST['textfield']
    worker_no = request.POST['textfield2']
    disc = request.POST['textarea']
    time=request.POST['textfield4']
    work = request.POST['textfield3']
    obj = Progress()
    obj.date = date
    obj.labour_num = worker_no
    obj.discription = disc
    obj.time = time
    obj.phases = work
    obj.save()

def view_user_request(request):
    vusr = UserRequest.objects.filter(CONTRACTOR__LOGIN=request.session['logid'], status="pending")
    print(vusr)
    return  render(request,'contractor/UserRequest.html',{'data': vusr})

def view_user_approved(request):
    vusr = UserRequest.objects.filter(CONTRACTOR__LOGIN=request.session['logid'], status="approved")
    return  render(request,'contractor/ViewUserApproved.html',{'data': vusr})

def view_order(request):
    vorder = UserRequest.objects.all()
    return render(request,'contractor/order.html',{'data': vorder})

def order_sub(request):
    return render(request,'contractor/order.html')

def order_sub_post(request):
    qnty = request.POST['textfield']
    obj = OrderSub()
    obj.qnty = qnty
    obj.save()

# def chatt(request):
#     return render(request, 'contractor/chat.html')
#
# def chat_post(request):
#     msg = request.POST['textarea']
#     date = request.POST['textfield']
#     obj = Chat()
#     obj.message = msg
#     obj.date = date
#     obj.save()

def dealer_complaint(request):
    dlr = Dealer.objects.all()
    return render(request,'contractor/Dealer complaint.html',{'data':dlr})

def dealer_complaint_post(request):
    cmplt = request.POST['textarea']
    dllr = request.POST['dealer']
    dat = datetime.datetime.now().strftime("%d/%m/%Y")
    tim = datetime.datetime.now().strftime("%H:%M:%S")
    obj = DealerComplaint()
    obj.complain = cmplt
    obj.DEALER_id = dllr
    obj.date = dat
    obj.time = tim
    obj.save()
    return HttpResponse("<script>alert('Dealer have been reported');window.location='/dealer_complaint'</script>")


def contractor_changepass(request):
    return render(request,'contractor/changepassw.html')


def contrctor_changepass_post(request):
    old = request.POST['textfield']
    new = request.POST['textfield2']
    con = request.POST['textfield3']
    data = Login.objects.filter(id=request.session['logid'],password=old)
    if data.exists():
        if new == con:
            Login.objects.filter(id=request.session['logid'],usertype='contractor').update(password = con)
            return HttpResponse("<script>alert('password changed sucessfully');window.location='/contractor_changepass'</script>")

        else:
            return HttpResponse("<script>alert('check again');window.location='/contractor_changepass'</script>")
    else:
        return HttpResponse("<script>alert('incorrect data');window.location='/contractor_changepass'</script>")

# def view_gallery(request):
#     gal = Gallary.objects.all()
#     return render(request, 'contractor/gly.html', {'data': gal})
def view_gallery(request):
    gal = Gallary.objects.filter(CONTRACTOR__LOGIN=request.session['logid'])
    return render(request, 'contractor/gly.html', {'data': gal})

def remove_gallery(request,id):
    Gallary.objects.get(id=id).delete()
    return HttpResponse("<script>alert('removed');window.location='/view_gallery'</script>")

def edit_gallery(request,id):
    crt = Gallary.objects.get(id=id)
    return render(request, 'contractor/edit_contractor_gallery.html', {'data': crt})

def edit_gallery_post(request,id):
    try:
        img = request.FILES['fileField']
        disc = request.POST['textarea']
        dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        fs = FileSystemStorage()
        fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg',img)
        imge = "/static/plan/" + dt + '.jpg'
        Gallary.objects.filter(id=id).update(image = imge,discription=disc)
        return HttpResponse("<script>alert('updated');window.location='/view_gallery#section_4'</script>")
    except Exception as e:
        disc = request.POST['textarea']
        Gallary.objects.filter(id=id).update(discription=disc)
        return HttpResponse("<script>alert('updated');window.location='/view_gallery#section_4'</script>")

def approve_contractor_user(request,id):
    UserRequest.objects.filter(id=id).update(status='approved')
    return HttpResponse("<script>alert('Request Accepted Sucessfully');window.location='/view_user_approved'</script>")

def reject_contractor_user(request,id):
    UserRequest.objects.filter(id=id).update(status='rejected')
    return HttpResponse("<script>alert('Request Rejectted Sucessfully');window.location='/view_user_approved'</script>")

def vault(request,id):
    return render(request, 'contractor/Vault.html',{'id':id})

def vault_post(request,id):
    file = request.FILES['fileField']
    disc =  request.POST['textarea']
    dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fs = FileSystemStorage()
    fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg',file)
    fil = "/static/plan/" + dt + '.jpg'
    obj = Vault()
    obj.CLIENT_id=id
    obj.discription = disc
    obj.file = fil
    obj.save()
    return HttpResponse("<script>alert('Document Added');window.location='/view_user_approved#section_4'</script>")

def view_vault(request,id):
    vcr = Vault.objects.all()
    return render(request, 'contractor/VIewVault.html', {'data': vcr,'id': id})

def purchase(request):
    pur = Product.objects.all()
    return render(request, 'contractor/purchase.html', {'data': pur})

def product_search(request):
    kywd = request.POST['keyword']
    obj = Product.objects.filter(pname__icontains=kywd)
    return render(request, 'contractor/Purchase.html', {'data':obj})

def addcart(request,id):
    pur = Product.objects.get(id=id)
    return render(request,'contractor/addcart.html',{'data': pur})

def addcart_post(request,id):
    quantity = request.POST['textfield']
    qry=Cart.objects.filter(PRODUCT=id,CONTRACTOR__LOGIN=request.session['logid'])
    if qry.exists():
        Cart.objects.filter(id=qry[0].id).update(quantity=int(qry[0].quantity)+int(quantity))
        return HttpResponse("<script>alert('Added To Cart');window.location='/cart#section_4'</script>")

    else:
        obj = Cart()
        obj.quantity = quantity
        obj.PRODUCT_id=id
        obj.CONTRACTOR=Contractor.objects.get(LOGIN=request.session['logid'])
        obj.save()
        return HttpResponse("<script>alert('Added To Cart');window.location='/cart#section_4'</script>")

def cart(request):
    obj= Contractor.objects.get(LOGIN=request.session['logid'])
    pur = Cart.objects.filter(CONTRACTOR_id=obj)

    sum=0
    data=[]
    for i in pur:

        qt=int(i.quantity)*int(i.PRODUCT.price)
        sum = sum + qt
        # print("summmm",sum)
        print(qt)
        data.append(
            {
                "id":i.id,
                "pname":i.PRODUCT.pname,
                "price":i.PRODUCT.price,
                "quantity":i.quantity,
                "qt":qt,
                "pic":i.PRODUCT.pic,
            }
        )
    #     print(i.PRODUCT.pname,i.PRODUCT.pic)
    # print(data)
    return render(request, 'contractor/cart.html', {'data': data,'sum':sum})

def remove_cart(request,id):
    Cart.objects.get(id=id).delete()
    return HttpResponse("<script>alert('removed');window.location='/cart'</script>")

def edit_cart(request,id):
    crt = Cart.objects.get(id=id)
    print(crt.PRODUCT.pic)
    return render(request, 'contractor/editcart.html',{'data': crt})

def edit_cart_post(request,id):
    quantity = request.POST.get('textfield')
    Cart.objects.filter(id=id).update(quantity = quantity)
    return HttpResponse("<script>alert('updated');window.location='/cart#section_4'</script>")

# def delivery_address(request):
#     return render(request,'contractor/DeliveryAddress.html')

def delivery_address(request):
    return render(request, 'contractor/DeliveryAddress.html')

def delivery_address_post(request):
    building = request.POST['te']
    landmark = request.POST['textarea']
    town = request.POST['textfield2']
    pincode = request.POST['textfield4']
    state = request.POST['select']
    res=Cart.objects.filter(CONTRACTOR__LOGIN_id=request.session['logid'])
    list=[]
    for j in res:
        if j.PRODUCT.DEALER.id not in list:
            list.append(j.PRODUCT.DEALER.id)
            print(list, "lisss")
            for i in list:
                print(i,"dealer")
                obj = Order()
                dat = datetime.datetime.now().strftime("%Y-%m-%d")
                # stat = 'pending'
                obj.building = building
                obj.landmark = landmark
                obj.town = town
                obj.pincode = pincode
                obj.status = 'pending'
                obj.state = state
                obj.date = dat
                obj.DEALER_id=i
                obj.CONTRACTOR=Contractor.objects.get(LOGIN=request.session['logid'])
                obj.save()

                for i in res:
                    sbj = OrderSub()
                    sbj.qnty = i.quantity
                    sbj.PRODUCT=i.PRODUCT
                    sbj.ORDER=obj
                    sbj.save()
            Cart.objects.filter(id=i.id).delete()
    return HttpResponse("<script>alert('Order placed');window.location='/purchase'</script>")

def view_order_status(request):
    vos = Order.objects.filter(CONTRACTOR__LOGIN_id=request.session['logid'])
    return render(request, 'contractor/ViewOrderStatus.html',{'data': vos})
# =================================web chat=======================================================


def chatt(request,u):
    request.session['head']="CHAT"
    request.session['uid'] = u
    return render(request,'contractor/chat.html',{'u':u})


def chatsnd(request,u):
        d=datetime.datetime.now().strftime("%Y-%m-%d")
        # t=datetime.datetime.now().strftime("%H:%M:%S")
        c = request.session['logid']
        b=request.POST['n']
        m=request.POST['m']
        cc = Contractor.objects.get(LOGIN__id=c)
        uu = Client.objects.get(id=request.session['uid'])
        obj=Chat()
        obj.date=d
        obj.type='contractor'
        obj.CONTRACTOR_id=cc.id
        obj.CLIENT_id=uu.id
        obj.message=m
        obj.save()
        print(obj)
        v = {}
        if int(obj) > 0:
            v["status"] = "ok"
        else:
            v["status"] = "error"
        r = JsonResponse.encode(v)
        return r
    # else:
    #     return redirect('/')

def chatrply(request):
    # if request.session['log']=="lo":
        c = request.session['logid']
        cc=Contractor.objects.get(LOGIN__id=c)
        uu=Client.objects.get(id=request.session['uid'])
        res = Chat.objects.filter(CONTRACTOR=cc,CLIENT=uu)
        v = []
        if len(res) > 0:
            for i in res:
                v.append({
                    'type':i.type,
                    'chat':i.message,
                    'name':i.CLIENT.name,
                    'upic':i.CLIENT.profile,
                    'dtime':i.date,
                    'tname':i.CONTRACTOR.name,
                })
            # print(v)
            return JsonResponse({"status": "ok", "data": v, "id": cc.id})
        else:
            return JsonResponse({"status": "error"})




def more_order_status(request,id):
    vos = OrderSub.objects.filter(ORDER=id)
    data = []
    for i in vos:
        qt = int(i.qnty) * int(i.PRODUCT.price)
        print(qt)
        data.append(
            {
                "id": i.id,
                "pname": i.PRODUCT.pname,
                "price": i.PRODUCT.price,
                "quantity": i.qnty,
                "qt": qt,
                "pic": i.PRODUCT.pic,
            }
        )
    return render(request, 'contractor/MoreOrderStatus.html', {'data': data})

def contractor_order_manager(request):
    vos = Order.objects.filter(CONTRACTOR__LOGIN_id=request.session['logid'])
    return render(request, 'contractor/ContractorOrderManage.html',{'data': vos})

def contractor_order_manager_post(request):
    fdate = request.POST['textfield']
    todate = request.POST['textfield2']
    print(fdate,todate)
    vos = Order.objects.filter(CONTRACTOR__LOGIN_id=request.session['logid'],date__range=[fdate,todate])
    return render(request, 'contractor/ContractorOrderManage.html',{'data': vos})

def addprogress(request,id):
    res=Progress.objects.filter(USERREQUEST=id)
    if res.exists():
        res = Progress.objects.get(USERREQUEST=id)
        return render(request, 'contractor/AddProgress2.html', {'id': id,'data':res})
    return render(request, 'contractor/AddProgress.html',{'id':id})



def addprogress_post2(request,id):
    if 'fileField' in request.FILES  :
        img = request.FILES['fileField']
        fs = FileSystemStorage()
        dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg', img)
        imge = "/static/plan/" + dt + '.jpg'
        Progress.objects.filter(id=id).update(img = imge)
        return HttpResponse("<script>alert('Progress updated');window.location='/view_user_approved#section_4'</script>")
    # if  'fileField2' in request.FILES:
    #     pdf = request.FILES['filefield2']
    #     fs = FileSystemStorage()
    #     dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    #     fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.pdf', pdf)
    #     pedo = "/static/plan/" + dt + '.pdf'
    #     Progress.objects.filter(id=id).update(pdf=pedo)
    #     return HttpResponse("<script>alert('Progress updated');window.location='/view_user_approved#section_4'</script>")
    else:
        st = datetime.datetime.now().strftime('%d/%m/%Y')
        percentage = request.POST['textfield']
        phase = request.POST['phase']
        dis = request.POST['textarea']
        sdate = request.POST['textfield2']
        edate = request.POST['textfield3']
        print(sdate,edate)
        Pq=Progress.objects.filter(id=id).update(date = st,percentage = percentage,phase = phase,sdate = sdate,edate = edate,discription=dis)
        if Pq >0:
            return HttpResponse("<script>alert('Progress update');window.location='/view_user_approved#section_4'</script>")
        else:
            return HttpResponse("<script>alert('No updation');window.location='/view_user_approved#section_4'</script>")


def addprogress_post(request,id):
    st = datetime.datetime.now().strftime('%d/%m/%Y')
    percentage = request.POST['textfield']
    phase = request.POST['phase']
    img = request.FILES['fileField']
    # pdf = request.FILES['fileField2']
    sdate = request.POST['textfield2']
    edate = request.POST['textfield3']
    Discription = request.POST['textarea']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg',img)
    # fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.pdf',pdf)
    imge = "/static/plan/" + dt +'.jpg'
    # pedo = "/static/plan/" + dt + '.pdf'
    obj = Progress()
    obj.date = st
    obj.discription = Discription
    obj.USERREQUEST_id = id
    obj.percentage = percentage
    obj.phase = phase
    obj.img = imge
    # obj.pdf = pedo
    obj.sdate = sdate
    obj.edate = edate
    obj.save()
    return HttpResponse("<script>alert('Progress Added');window.location='/view_user_approved'</script>")

#==========================================================================

def adddealer(request):
    return render(request,'dealer/Dealer.html')

def dealer_post(request):
    pname = request.POST['textfield']
    dob = request.POST['textfield2']
    email = request.POST['textfield3']
    phone = request.POST['textfield4']
    bname = request.POST['textfield5']
    type = request.POST['RadioGroup1']
    Building = request.POST['textfield6']
    landmark = request.POST['textfield7']
    town = request.POST['textfield8']
    pincode = request.POST['textfield9']
    state = request.POST['select']
    ref = request.POST['textarea2']
    profile_img = request.FILES['fileField']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + 'profile' + '.jpg', profile_img)
    img = "/static/plan/" + dt + 'profile'  + '.jpg'
    password = request.POST['textfield10']
    alog=Login()
    alog.username = email
    alog.password = password
    alog.usertype = 'pending'
    alog.save()
    obj = Dealer()
    obj.LOGIN=alog
    obj.Dealer_name = pname
    obj.email = email
    obj.dob = dob
    obj.phone = phone
    obj.business_name = bname
    obj.business_type = type
    obj.building = Building
    obj.landmark = landmark
    obj.town = town
    obj.pincode = pincode
    obj.state = state
    obj.reference = ref
    obj.profile = img
    obj.save()
    return HttpResponse("<script>alert('Regestration Request Send');window.location='/'</script>")

def edit_dealer(request):
    con = Dealer.objects.get(LOGIN_id= request.session['logid'])
    return render(request,'dealer/editdealer.html',{'data': con})

def dealerchangepass(request):
    return render(request,'dealer/dealerchangepassw.html')


def dealerchangepass_post(request):
    old = request.POST['textfield']
    new = request.POST['textfield2']
    con = request.POST['textfield3']
    data = Login.objects.filter(password=old)
    if data.exists():
        if new == con:
            Login.objects.filter(usertype='dealer').update(password = con)
            return HttpResponse("<script>alert('password changed sucessfully');window.location='/dealerchangepass#section_4'</script>")

        else:
            return HttpResponse("<script>alert('check again');window.location='/dealerchangepass#section_4'</script>")
    else:
        return HttpResponse("<script>alert('incorrect data');window.location='/dealerchangepass#section_4'</script>")

def edit_dealer_post(request):
    try:
        pname = request.POST['textfield']
        dob = request.POST['textfield3']
        email = request.POST['textfield4']
        phone = request.POST['textfield5']
        busi_name = request.POST['textfield6']
        type = request.POST['RadioGroup1']
        Building = request.POST['textfield7']
        landmark = request.POST['textfield8']
        town = request.POST['textfield9']
        pincode = request.POST['textfield10']
        state = request.POST['select']
        # contact = request.POST['textarea3']
        # License_num = request.POST['textfield11']
        # issued_state = request.POST['select2']
        # insurance = request.POST['RadioGroup2']
        # work_exp = request.POST['textarea4']
        fs = FileSystemStorage()
        dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        # area_epertise = request.POST['textarea5']
        # ref = request.POST['textarea6']
        profile_img = request.FILES['fileField2']
        fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + 'profile' + '.jpg', profile_img)
        img = "/static/plan/" + dt + 'profile'  + '.jpg'
        Dealer.objects.filter(LOGIN_id=request.session['logid']).update(phone=phone, email=email, Dealer_name=pname, dob=dob,
                                                                        business_name=busi_name, business_type=type,
                                                                        building=Building, landmark=landmark, town=town,
                                                                        pincode=pincode, state=state, profile=img)
        return HttpResponse("<script>alert('updated');window.location='/edit_dealer#section_4'</script>")
    except Exception as e:
        pname = request.POST['textfield']
        dob = request.POST['textfield3']
        email = request.POST['textfield4']
        phone = request.POST['textfield5']
        busi_name = request.POST['textfield6']
        type = request.POST['RadioGroup1']
        Building = request.POST['textfield7']
        landmark = request.POST['textfield8']
        town = request.POST['textfield9']
        pincode = request.POST['textfield10']
        state = request.POST['select']
        # contact = request.POST['textarea3']
        # License_num = request.POST['textfield11']
        # issued_state = request.POST['select2']
        # insurance = request.POST['RadioGroup2']
        # work_exp = request.POST['textarea4']
        # area_epertise = request.POST['textarea5']
        # ref = request.POST['textarea6']
        Dealer.objects.filter(LOGIN_id= request.session['logid']).update(phone=phone, email=email, Dealer_name=pname, dob=dob, business_name=busi_name,business_type=type,
                                                building=Building, landmark=landmark, town=town,
                                                pincode=pincode, state=state)
        return HttpResponse("<script>alert('updated');window.location='/edit_dealer#section_4'</script>")

def view_contractor_product_request(request):
    print(request.session['logid'])
    obj = Order.objects.filter(status='pending',DEALER__LOGIN=request.session['logid'])
    print(obj)
    return render(request,'dealer/ContractorProductRequest.html',{'data': obj})


def view_contractor_product_request_sub(request,id):
    obj = OrderSub.objects.filter(ORDER=id)
    ar=[]
    for i in obj:
        qt = int(i.qnty) * int(i.PRODUCT.price)
        ar.append({
            "pname":i.PRODUCT.pname,
            "id": i.id,
            "qnty": i.qnty,
            "qt": qt,
        })
    return render(request,'dealer/ContractorProductRequestSub.html',{'data': ar})

def approve_contractor_request(request,id):
    Order.objects.filter(id=id).update(status='approved')
    return HttpResponse("<script>alert('Request Accepted Sucessfully');window.location='/view_contractor_product_request'</script>")

def reject_contractor_request(request,id):
    Order.objects.filter(id=id).update(status='rejected')
    return HttpResponse("<script>alert('Request Rejected Sucessfully');window.location='/view_contractor_product_request'</script>")

def dealer_feedback(request):
    return render(request, 'dealer/DealerFeedback.html')

def dealer_feedback_post(request):
    dt = datetime.datetime.now().strftime('%d/%m/%Y')
    tm = datetime.datetime.now().strftime('%H:%M:%S')
    feedback = request.POST['textarea']
    obj = Feedback()
    obj.date = dt
    obj.time = tm
    obj.type = 'dealer'
    obj.feedback = feedback
    obj.LOGIN_id = request.session['logid']
    obj.save()
    return HttpResponse("<script>alert('Feedback send');window.location='/dealer_feedback'</script>")

def product_purchase(request):
    pur = Product.objects.all()
    return render(request, 'dealer/product_purchase.html', {'data': pur})

def add_product(request):
    return render(request, 'dealer/AddProduct.html')

def dealer_product_search(request):
    kywd = request.POST['keyword']
    obj = Product.objects.filter(pname__icontains=kywd)
    return render(request, 'dealer/product_purchase.html', {'data':obj})

def add_product_post(request):
    pname = request.POST['textfield']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    pimg = request.FILES['fileField']
    fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg',pimg)
    # fs.save(r'C:\Users\user\PycharmProjects\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg',pimg)
    img = "/static/plan/" + dt + '.jpg'
    disc = request.POST['textarea']
    price = request.POST['textfield2']
    status = request.POST['RadioGroup1']
    obj = Product()
    obj.pname = pname
    obj.pic = img
    obj.discri = disc
    obj.price = price
    obj.status=status
    obj.DEALER = Dealer.objects.get(LOGIN=request.session['logid'])
    obj.save()
    return HttpResponse("<script>alert('Product Add');window.location='/product_purchase#section_4'</script>")

def edit_product(request,id):
    pd = Product.objects.get(id=id)
    return render(request, 'dealer/EditProduct.html',{'data': pd})

def edit_product_post(request,id):
    pname = request.POST['textfield']
    disc = request.POST['textarea']
    price = request.POST['textfield2']
    status = request.POST['RadioGroup1']
    if 'fileField' in request.FILES:
        fs = FileSystemStorage()
        dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        pimg = request.FILES['fileField']
        fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg', pimg)
        # fs.save(r'C:\Users\user\PycharmProjects\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg', pimg)
        img = "/static/plan/" + dt + '.jpg'
        Product.objects.filter(id=id).update( pic=img)
        return HttpResponse("<script>alert('Edited');window.location='/product_purchase#section_4'</script>")

    Product.objects.filter(id=id).update(pname=pname,discri=disc, price=price, status=status)
    return HttpResponse("<script>alert('Edit');window.location='/product_purchase#section_4'</script>")

def remove_product(request,id):
    Product.objects.get(id=id).delete()
    return HttpResponse("<script>alert('removed');window.location='/product_purchase'</script>")

def view_contractor_approved_product(request):
    print(request.session['logid'])
    obj = Order.objects.filter(status='approved',DEALER__LOGIN=request.session['logid'])
    return render(request,'dealer/ApprovedProduct.html',{'data': obj})

def view_contractor_approved_product_sub(request,id):
    obj = OrderSub.objects.filter(ORDER=id)
    ar=[]
    for i in obj:
        qt = int(i.qnty) * int(i.PRODUCT.price)
        ar.append({
            "pname":i.PRODUCT.pname,
            "id": i.id,
            "qnty": i.qnty,
            "qt": qt,
        })
    return render(request,'dealer/ContractorProductRequestSub.html',{'data': ar})

def contractor_complaint(request,id):

    return render(request,'dealer/Contractor complaint.html',{'id':id})

def contractor_complaint_post(request,id):
    cmplt = request.POST['textarea']
    dllr = request.POST['contractor']
    dat = datetime.datetime.now().strftime("%d/%m/%Y")
    tim = datetime.datetime.now().strftime("%H:%M:%S")
    obj = DealerComplaint()
    obj.complain = cmplt
    obj.CONTRACTOR_id = id
    obj.date = dat
    obj.time = tim
    obj.save()
    return HttpResponse("<script>alert('Contractor have been reported');window.location='/contractor_complaint'</script>")


#=======================================================================================================================

def and_login(request):
    username = request.POST['username']
    password = request.POST['password']
    obj=Login.objects.filter(username=username,password=password)
    if obj.exists():
        type:obj[0].usertype
        # lid:obj[0].id
        cl = Client.objects.get(LOGIN=obj[0].id)
        return JsonResponse({"status": "ok","type":'type',"lid":obj[0].id,"image":cl.profile,"name":cl.name,"email":cl.email,'password':obj[0].password,'username':obj[0].username})
    else:
        if Login.objects.filter(username=username).exists():
            return JsonResponse({"status": "username"})
        else:
            return JsonResponse({"status":"non"})

def userregistration(request):
    try:
        na=request.POST['na']
        em=request.POST['em']
        phon=request.POST['phon']
        la=request.POST['la']
        bu=request.POST['bu']
        t=request.POST['t']
        sta=request.POST['sta']
        pin=request.POST['pin']
        p=request.POST['p']
        d=request.POST['d']
        pic=request.FILES['pic']
        fs = FileSystemStorage()
        dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg', pic)
        # fs.save(r'C:\Users\user\PycharmProjects\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg', pimg)
        img = "/static/plan/" + dt + '.jpg'
        obj=Login()
        obj.username=em
        obj.password=p
        obj.usertype='client'
        obj.save()
        obj2=Client()
        obj2.LOGIN=obj
        obj2.profile=img
        obj2.name=na
        obj2.email=em
        obj2.phone=phon
        obj2.landmark=la
        obj2.building=bu
        obj2.town=t
        obj2.state=sta
        obj2.pincode=pin
        obj2.dob=d
        obj2.save()
        return JsonResponse({'status':"ok"})
    except Exception:
        na = request.POST['na']
        em = request.POST['em']
        phon = request.POST['phon']
        la = request.POST['la']
        bu = request.POST['bu']
        t = request.POST['t']
        sta = request.POST['sta']
        pin = request.POST['pin']
        p = request.POST['p']
        d = request.POST['d']
        obj = Login()
        obj.username = em
        obj.password = p
        obj.usertype = 'client'
        obj.save()
        obj2 = Client()
        obj2.LOGIN = obj
        obj2.profile = '/static/plan/boy.png'
        obj2.name = na
        obj2.email = em
        obj2.phone = phon
        obj2.landmark = la
        obj2.building = bu
        obj2.town = t
        obj2.state = sta
        obj2.pincode = pin
        obj2.dob = d
        obj2.save()
        return JsonResponse({'status': "ok"})
# def and_contractor_search(request):
#     kywd = request.POST['keyword']
#     obj = Contractor.objects.filter(business_name__icontains=kywd)
#     if obj.exists():
#         ary=[]
#         for i in obj:
#             obj1=ContractorReview.objects.filter(Contractor=i.id)
#             ary.append({
#                 'compname':i.business_name,
#                 'contname': i.name,
#                 'profile': i.profile,
#                 'rating':obj1,
#             })
#     return JsonResponse({"status":"ok",'data':ary})

# def and_contractor_search(request):
#     kywd = request.POST['src']
#     obj = Contractor.objects.filter(business_name__icontains=kywd)
#     if obj.exists():
#         ary=[]
#         for i in obj:
#             obj1=ContractorReview.objects.filter(CONTRACTOR=i.id)
#             if obj1.exists():
#                 ratings = [review.rating for review in obj1]
#                 avg_rating = sum(ratings) / len(ratings) if ratings else 0
#                 ary.append({
#                     'compname': i.business_name,
#                     'contname': i.name,
#                     'profile': i.profile,
#                     'reference': i.reference,
#                     'avg_rating': 0,
#                     "id":i.id
#                 })
#
#             ary.append({
#                 'compname':i.business_name,
#                 'contname': i.name,
#                 'profile': i.profile,
#                 'avg_rating':avg_rating,
#                 'reference': i.reference,
#                 'id':i.id,
#             })
#             print(avg_rating)
#         return JsonResponse({"status":"ok",'data':ary})
#     return JsonResponse({"status":"no"})

from django.http import JsonResponse

def and_contractor_search(request):
    kywd = request.POST['src']
    obj = Contractor.objects.filter(business_name__icontains=kywd)
    if obj.exists():
        ary = []
        for i in obj:
            obj1 = ContractorReview.objects.filter(CONTRACTOR=i.id)
            if obj1.exists():
                ratings = [float(review.rating) for review in obj1]  # Convert ratings to floats
                avg_rating = sum(ratings) / len(ratings) if ratings else 0
            else:
                avg_rating = 0

            ary.append({
                'compname': i.business_name,
                'contname': i.name,
                'profile': i.profile,
                'reference': i.reference,
                'avg_rating': avg_rating,
                "id": i.id
            })
            print(avg_rating)
        return JsonResponse({"status": "ok", 'data': ary})
    return JsonResponse({"status": "no"})



def and_contractor_all(request):
    obj = Contractor.objects.filter(LOGIN__usertype="contractor")
    if obj.exists():
        avg_rating = 0

        ary=[]
        for i in obj:
            obj1=ContractorReview.objects.filter(CONTRACTOR=i.id)
            r = 0
            if obj1.exists():
                for j in obj1:
                    r += float(j.rating)
                avg_rating += r / len(obj1)

            ary.append({
                'compname': i.business_name,
                'contname': i.name,
                'profile': i.profile,
                'reference': i.reference,
                'avg_rating': avg_rating,
                "id": i.id
            })
            avg_rating = 0
        print(ary)
        print(r)
        return JsonResponse({"status":"ok",'data':ary})
    return JsonResponse({"status":"no"})

def and_contractor_gallery(request):
    cid = request.POST['cid']
    print(cid)
    obj = Gallary.objects.filter(CONTRACTOR=cid)
    if obj.exists():
        ary = []
        for i in obj:
                ary.append({
                    'images': i.image,
                    'discription': i.discription,
                    "id": i.id
                })
        return JsonResponse({"status":"ok","data":ary})
    return JsonResponse({"status":"no"})

def and_view_plan_search(request):
    filters = {}
    if 'room' in request.POST and request.POST['room'].isdigit():
        filters['room_count'] = int(request.POST['room'])
    if 'bed' in request.POST and request.POST['bed'].isdigit():
        filters['bedroom_count'] = int(request.POST['bed'])
    if 'bath' in request.POST and request.POST['bath'].isdigit():
        filters['bathroom_count'] = int(request.POST['bath'])

    obj = Plan.objects.filter(**filters)
    if obj.exists():
        ary = []
        for i in obj:
            ary.append({
                'id': i.id,
                'pic': i.plan_image,
                'bed': i.bedroom_count,
                'bath': i.bathroom_count,
                "room": i.room_count
            })
        return JsonResponse({"status":"ok","data":ary})
    return JsonResponse({"status":"no"})

def and_view_plan(request):
    obj = Plan.objects.all()
    if obj.exists():
        ary = []
        for i in obj:
                ary.append({
                    'id': i.id,
                    'pic': i.plan_image,
                    'bed': i.bedroom_count,
                    'bath': i.bathroom_count,
                    "room": i.room_count
                })
        return JsonResponse({"status":"ok","data":ary})
    return JsonResponse({"status":"no"})

def and_contractor_review(request):
    cid=request.POST['id']
    obj =ContractorReview.objects.filter(CONTRACTOR_id=cid)
    if obj.exists():
        ary = []
        for i in obj:
            ary.append({
                'date': i.date,
                'discription': i.discription,
                'rating': i.rating,
                'clnt':i.CLIENT.name,
                "id": i.id
            })
        return JsonResponse({"status": "ok", "data": ary})
    return JsonResponse({"status": "no"})

def add_chat(request):
    lid = request.POST['lid']
    toid = request.POST['toid']
    message = request.POST['message']
    d=datetime.datetime.now().strftime("%Y-%m-%d")
    t=datetime.datetime.now().strftime("%H:%m:%d")
    expid = Contractor.objects.get(id=toid)
    uid = Client.objects.get(LOGIN=lid)
    obj=Chat()
    obj.date=d
    obj.time=t
    obj.type='user'
    obj.CONTRACTOR_id=expid.id
    obj.CLIENT_id=uid.id
    obj.message=message
    obj.save()
    return JsonResponse({'status':"Inserted"})



def view_chat(request):
    lid = request.POST['lid']
    toid = request.POST['toid']
    print(toid,'kkk')
    lastid = request.POST['lastid']
    res=Chat.objects.filter(CLIENT=Client.objects.get(LOGIN=lid))
    res=Chat.objects.filter(Q(CLIENT=Client.objects.get(LOGIN=lid),CONTRACTOR=toid),Q(id__gt=lastid))
    # if res.exists():

    ar=[]
    for i in res:
        ar.append({
            "id":i.id,
            "date":i.date,
            "userid":i.CLIENT.id,
            "sid":i.type,
            "chat":i.message,
        })
    return JsonResponse({'status':"ok",'data':ar})
    # return JsonResponse({'status': "no"})


def and_view_profile(request):
    lid=request.POST['lid']
    res=Client.objects.get(LOGIN=lid)
    return JsonResponse({'status':'ok','uname':res.name,'em':res.email,'phon':res.phone,'dob':res.dob,'building':res.building,'landmark':res.landmark,
                         'town':res.town,'pi':res.pincode,'state':res.state,'img':res.profile})
def edit_userregistration(request):
    try:
        lid = request.POST['lid']
        na = request.POST['na']
        em = request.POST['em']
        phon = request.POST['phon']
        la = request.POST['la']
        bu = request.POST['bu']
        t = request.POST['t']
        sta = request.POST['sta']
        pin = request.POST['pin']
        d = request.POST['d']
        pic = request.FILES['pic']
        fs = FileSystemStorage()
        dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg', pic)
        img = "/static/plan/" + dt + '.jpg'
        Client.objects.filter(LOGIN=lid).update(name=na,email=em,phone=phon,dob=d,building=bu,landmark=la,town=t,pincode=pin,state=sta,profile=img)
        return JsonResponse({'status': "ok"})
    except Exception as e:
        lid = request.POST['lid']
        na = request.POST['na']
        em = request.POST['em']
        phon = request.POST['phon']
        la = request.POST['la']
        bu = request.POST['bu']
        t = request.POST['t']
        sta = request.POST['sta']
        pin = request.POST['pin']
        d = request.POST['d']
        Client.objects.filter(LOGIN=lid).update(name=na, email=em, phone=phon, dob=d, building=bu, landmark=la, town=t,
                                                pincode=pin, state= sta)
        return JsonResponse({'status': "ok"})
def and_send_feedback(request):
    lid=request.POST['lid']
    fee=request.POST['fee']
    obj=Feedback()
    obj.date=datetime.datetime.now().strftime("%Y-%m-%d")
    obj.time=datetime.datetime.now().strftime("%H:%M:%S")
    obj.type='client'
    obj.LOGIN_id=lid
    obj.feedback=fee
    obj.save()
    return JsonResponse({'status': "ok"})

def and_frgt(request):
    lid=request.POST['lid']
    mail=request.POST['fee']
    res=Login.objects.filter(username=mail,id=lid)
    if res.exists():
        import smtplib
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login('dreambuildermac@gmail.com', 'acwi hyqk qzkn gkom')
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "dreambuildermac@gmail.com"
        msg['To'] = mail
        msg['Subject'] = "Your Password for Dream Builder Website."
        body = "Your Password is:- - " + str(res.password)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        return JsonResponse({'status': "ok"})
    else:
        return JsonResponse({'status': "no"})
def and_send_request(request):
    lid=request.POST['lid']
    cid=request.POST['cid']
    dis=request.POST['dis']
    loc=request.POST['loc']
    obj=UserRequest()
    obj.CLIENT=Client.objects.get(LOGIN=lid)
    obj.CONTRACTOR=Contractor.objects.get(id=cid)
    obj.discription=dis
    obj.addr=loc
    obj.date=datetime.datetime.now().strftime("%Y-%m-%d")
    obj.status='pending'
    obj.time=datetime.datetime.now().strftime("%H:%M:%S")
    obj.save()
    return JsonResponse({'status': "ok"})

def and_view_request(request):
    lid=request.POST['lid']
    res=UserRequest.objects.filter(CLIENT__LOGIN=lid)
    l=[]
    for i in res:
        l.append({
            "id": i.id,
            "status": i.status,
            "d": i.date,
            "cname": i.CONTRACTOR.name,
            "cid": i.CONTRACTOR.id,
            "cphn": i.CONTRACTOR.phone,
            "cemail": i.CONTRACTOR.email,
            "loc": i.addr,
            "ad": i.discription,
        })
    print(l)
    return JsonResponse({'status': "ok",'data':l})

def and_send_complaint(request):
    lid=request.POST['lid']
    cid=request.POST['cid']
    comp=request.POST['complain']
    obj=ContractorComplaint()
    obj.CLIENT = Client.objects.get(LOGIN=lid)
    obj.CONTRACTOR = Contractor.objects.get(id=cid)
    obj.date=datetime.datetime.now().strftime("%Y-%m-%d")
    obj.response='pending'
    obj.complain = comp
    obj.save()
    return JsonResponse({'status': "ok"})

def and_upload_document(request):
    lid = request.POST['lid']
    id = request.POST['id']
    doc = request.FILES['doc']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    fs.save(r'C:\Users\chinm\PycharmProjects\13.1.2003\dreambuilders\dreambuilder\static\plan\\' + dt + '.jpg', doc)
    path = "/static/plan/" + dt + '.jpg'
    obj=Document()
    obj.CLIENT = Client.objects.get(LOGIN=lid)
    obj.CONTRACTOR = Contractor.objects.get(id=id)
    obj.doc=path
    obj.save()
    return JsonResponse({'status': "ok"})

def and_view_document(request):
    lid=request.POST['lid']
    obj = Document.objects.filter(CLIENT__LOGIN=lid)
    if obj.exists():
        ary = []
        for i in obj:
                ary.append({
                    'id': i.id,
                    'doc': i.doc,
                })
        return JsonResponse({"status":"ok","data":ary})
    return JsonResponse({"status":"no"})

# def and_progress(request):
#     rid=request.POST['rid']
#     res=Progress.objects.filter(USERREQUEST=rid)
#     if res.exists():
#         l = {
#                 "phs": res.phase,
#                 "p1": res.percentage,
#                 "discri": res.discription,
#                 "sdate": res.sdate,
#                 "edate": res.edate,
#                 "im": res.img,
#             }
#         return JsonResponse({'status': "ok",'data':l})
#     return JsonResponse({"status":"no"})

def and_progress(request):
    rid = request.POST['rid']
    res = Progress.objects.filter(USERREQUEST=rid)
    print(res)
    if res.exists():
        res = res.first()  # Get the first object from the queryset
        avg = ContractorReview.objects.filter(CLIENT=res.USERREQUEST.CLIENT,CONTRACTOR=res.USERREQUEST.CONTRACTOR)
        print(avg, "fgh")
        if avg.exists():
            l = {
                "phs": res.phase,
                "p1": res.percentage,
                "discri": res.discription,
                "rev": avg[0].discription,
                "sdate": res.sdate,
                "edate": res.edate,
                "im": res.img,
                "r": avg[0].rating
            }
            print(l)
            return JsonResponse({'status': "ok", 'data': l})
        else:
            l = {
                "phs": res.phase,
                "p1": res.percentage,
                "discri": res.discription,
                "rev": '',
                "sdate": res.sdate,
                "edate": res.edate,
                "im": res.img,
                "r": '0.0'
            }
            print(l)
            return JsonResponse({'status': "ok", 'data': l})
    return JsonResponse({"status": "no"})


def and_change_password(request):
    lid=request.POST['lid']
    old = request.POST['op']
    new = request.POST['np']
    # con = request.POST['cp']
    data = Login.objects.filter(id=lid, password=old)
    if data.exists():
        Login.objects.filter(id=lid, usertype='client').update(password=new)
        return JsonResponse({'status': "ok"})
    else:
        return JsonResponse({'status': "not"})

def and_send_rating(request):
    rid = request.POST['rid']
    lid = request.POST['lid']
    r = request.POST['r']
    r8 = request.POST['r8']
    rr =  ContractorReview.objects.filter(CLIENT = Client.objects.get(LOGIN=lid),CONTRACTOR = UserRequest.objects.get(id = rid).CONTRACTOR)
    if rr.exists():
        robj = ContractorReview.objects.get(id = rr[0].id)
        robj.date = datetime.datetime.now().date()
        robj.rating = r
        robj.discription = r8
        robj.CONTRACTOR = UserRequest.objects.get(id=rid).CONTRACTOR
        robj.CLIENT = Client.objects.get(LOGIN=lid)
        robj.save()
        return JsonResponse({'status': "ok"})

    robj = ContractorReview()
    robj.date = datetime.datetime.now().date()
    robj.rating= r
    robj.discription = r8
    robj.CONTRACTOR = UserRequest.objects.get(id = rid).CONTRACTOR
    robj.CLIENT = Client.objects.get(LOGIN=lid)
    robj.save()
    return JsonResponse({'status': "ok"})
############        main checking
def boq1(request):
    return render(request, "contractor/boq1.html")

def boq1_post(request):
    num_floors=request.POST['t1']
    print("Number of floors : ", num_floors)
    return render(request, "contractor/boq2.html", {'floor':num_floors, 'cnt':1})

def start_page(request):

    # Define the size of a single brick
    request.session['BRICK_VOLUME'] = 0.0012
    request.session['CEMENT_BAG_VOLUME'] = 0.035
    request.session['PAINT_CAN_COVERAGE'] = 10

    #   Define the cement-to-sand ratio
    request.session['MORTAR_CEMENT_RATIO'] = 1/6
    request.session['PLASTER_THICKNESS'] = 0.02

    #   Define the proportions of the concrete mix for the lintel
    request.session['LINTEL_CEMENT_RATIO'] = 1
    request.session['LINTEL_SAND_RATIO'] = 1.5
    request.session['LINTEL_AGGREGATE_RATIO'] = 3

    #   Define the percentage of steel in the lintel
    request.session['STEEL_PERCENTAGE'] = 0.02


    return render(request,"contractor/page1.html")
def page1post(request):
    wall_cnt=int(request.POST['textfield'])     #   take number of walls
    request.session['wall_cnt']=wall_cnt
    return render(request, "contractor/page2.html", {'cnt':1})
def page2post(request):
    # wallno = int(request.POST['textfield4'])
    thickness = float(request.POST['textfield'])
    length = float(request.POST['textfield2'])
    height = float(request.POST['textfield3'])
    request.session['wall_thickness'] = thickness
    request.session['wall_length'] = length
    request.session['height'] = height
    return render(request, "contractor/door1.html")

def door1_post(request):
    door_no=int(request.POST['textfield'])
    request.session['door_no']=door_no
    return render(request, "contractor/door2.html")
def door2_post(request):
    door_width=float(request.POST['textfield2'])
    door_height=float(request.POST['textfield3'])
    request.session['door_width']=door_width
    request.session['door_height']=door_height
    return render(request, "contractor/windows1.html")
def windows1_post(request):
    window_no=int(request.POST['textfield'])
    request.session['window_no']=window_no
    return render(request, "contractor/window2.html")
def window2_post(request):
    window_width=float(request.POST['textfield2'])
    window_height=float(request.POST['textfield3'])
    request.session['window_width']=window_width
    request.session['window_height']=window_height
    return render(request, "contractor/vent1.html")

def vent1_post(request):
    vent_no = int(request.POST['textfield'])
    request.session['vent_no'] = vent_no
    return render(request, "contractor/vent2.html")

def vent2_post(request):
    vent_width = float(request.POST['textfield2'])
    vent_height = float(request.POST['textfield3'])
    request.session['vent_width'] = vent_width
    request.session['vent_height'] = vent_height
    return render(request, "contractor/lintel.html")

def lintel_post(request):
    lintel_length = float(request.POST['textfield'])
    lintel_height = float(request.POST['textfield2'])
    lintel_width = float(request.POST['textfield3'])

    request.session['lintel_length'] = lintel_length
    request.session['lintel_height'] = lintel_height
    request.session['lintel_width'] = lintel_width
    return render(request, "contractor/slab.html")

def slab_post(request):
    slab_length = float(request.POST['textfield'])
    slab_width = float(request.POST['textfield2'])
    slab_thickness = float(request.POST['textfield3'])
    request.session['slab_length'] = slab_length
    request.session['slab_width'] = slab_width
    request.session['slab_thickness'] = slab_thickness

    # Calculate the volume of the wall
    thickness = request.session['wall_thickness']
    length = request.session['wall_length']
    height = request.session['height']
    wall_volume = length * height * thickness

    # Subtract the volume of the door and windows
    num_door = request.session['door_no']
    door_width = request.session['door_width']
    door_height = request.session['door_height']
    door_volume = door_height * door_width * thickness * num_door

    num_windows = request.session['window_no']
    window_width = request.session['window_width']
    window_height = request.session['window_height']
    window_volume = num_windows * window_height * window_width * thickness

    num_vent = request.session['vent_no']
    vent_width = request.session['vent_width']
    vent_height = request.session['vent_height']
    vent_volume = vent_height * vent_width * thickness * num_vent
    net_wall_volume = wall_volume - door_volume - window_volume - vent_volume

    # Calculate the volume of mortar needed (assuming 30% of the wall volume)
    mortar_volume = net_wall_volume * 0.3

    # Define the size of a single brick
    BRICK_VOLUME = request.session['BRICK_VOLUME']
    CEMENT_BAG_VOLUME = request.session['CEMENT_BAG_VOLUME']
    PAINT_CAN_COVERAGE = request.session['PAINT_CAN_COVERAGE']

    #   Define the cement-to-sand ratio
    MORTAR_CEMENT_RATIO = request.session['MORTAR_CEMENT_RATIO']
    PLASTER_THICKNESS = request.session['PLASTER_THICKNESS']

    #   Define the proportions of the concrete mix for the lintel
    LINTEL_CEMENT_RATIO = request.session['LINTEL_CEMENT_RATIO']
    LINTEL_SAND_RATIO = request.session['LINTEL_SAND_RATIO']
    LINTEL_AGGREGATE_RATIO = request.session['LINTEL_AGGREGATE_RATIO']

    #   Define the percentage of steel in the lintel
    STEEL_PERCENTAGE = request.session['STEEL_PERCENTAGE']

    # Calculate the quantity of materials needed for the masonry work
    bricks_needed = net_wall_volume / BRICK_VOLUME
    cement_bags_needed_for_masonry = (mortar_volume * MORTAR_CEMENT_RATIO) / CEMENT_BAG_VOLUME

    # Calculate the area of the wall
    wall_area = length * height

    # Subtract the area of the door and windows
    door_area = door_height * door_width * num_door
    window_area = num_windows * window_height * window_width
    vent_area = num_vent * vent_height * vent_width
    net_wall_area = wall_area - door_area - window_area

    # Calculate the volume of plaster needed (assuming a 2cm thick layer of plaster)
    plaster_volume = net_wall_area * PLASTER_THICKNESS

    # Calculate the quantity of materials needed for the plastering work
    cement_bags_needed_for_plaster = (plaster_volume * MORTAR_CEMENT_RATIO) / CEMENT_BAG_VOLUME

    # Calculate the quantity of materials needed for the painting work
    paint_cans_needed = net_wall_area / PAINT_CAN_COVERAGE

    # Calculate the volume of the lintel
    lintel_length = request.session['lintel_length']
    lintel_height = request.session['lintel_height']
    lintel_width = request.session['lintel_width']
    lintel_volume = lintel_length * lintel_height * lintel_width

    # Calculate the total volume of the materials for the lintel
    total_materials_volume = LINTEL_CEMENT_RATIO + LINTEL_SAND_RATIO + LINTEL_AGGREGATE_RATIO

    # Calculate the quantity of each material needed for the lintel
    cement_needed_for_lintel = (LINTEL_CEMENT_RATIO / total_materials_volume) * lintel_volume
    sand_needed_for_lintel = (LINTEL_SAND_RATIO / total_materials_volume) * lintel_volume
    aggregate_needed_for_lintel = (LINTEL_AGGREGATE_RATIO / total_materials_volume) * lintel_volume

    # Calculate the quantity of steel needed for the lintel
    steel_needed_for_lintel = STEEL_PERCENTAGE * lintel_volume  # in cubic meters

    # Calculate the volume of the slab
    slab_volume = slab_length * slab_width * slab_thickness

    # Calculate the quantity of each material needed for the slab
    cement_needed_for_slab = (LINTEL_CEMENT_RATIO / total_materials_volume) * slab_volume
    sand_needed_for_slab = (LINTEL_SAND_RATIO / total_materials_volume) * slab_volume
    aggregate_needed_for_slab = (LINTEL_AGGREGATE_RATIO / total_materials_volume) * slab_volume

    # Calculate the quantity of steel needed for the slab
    steel_needed_for_slab = STEEL_PERCENTAGE * slab_volume  # in cubic meters

    return render(request, "contractor/material_result.html", {'bricks_needed':round(bricks_needed), 'cement_bags_needed_for_masonry':round(cement_bags_needed_for_masonry),
                                                  'cement_bags_needed_for_plaster':round(cement_bags_needed_for_plaster), 'paint_cans_needed':round(paint_cans_needed),
                                                    'cement_needed_for_lintel':round(cement_needed_for_lintel, 2), 'sand_needed_for_lintel':round(sand_needed_for_lintel, 2),
                                                    'aggregate_needed_for_lintel':round(aggregate_needed_for_lintel, 2), 'steel_needed_for_lintel':round(steel_needed_for_lintel, 2),
                                                    'cement_needed_for_slab':round(cement_needed_for_slab, 2), 'sand_needed_for_slab':round(sand_needed_for_slab, 2),
                                                    'aggregate_needed_for_slab':round(aggregate_needed_for_slab, 2), 'steel_needed_for_slab':round(steel_needed_for_slab, 2)})