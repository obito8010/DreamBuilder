from django.db import models

# Create your models here.

class  Login(models.Model):
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=250)
    usertype=models.CharField(max_length=250)

class Material(models.Model):
    material_name=models.CharField(max_length=250)
    amount=models.CharField(max_length=250)

class Plan(models.Model):
    plan_image=models.CharField(max_length=250)
    room_count=models.CharField(max_length=250)
    bedroom_count=models.CharField(max_length=250)
    bathroom_count=models.CharField(max_length=250)

class Contractor(models.Model):
    name=models.CharField(max_length=250)
    age = models.CharField(max_length=250)
    email=models.CharField(max_length=250)
    phone=models.CharField(max_length=250)
    dob=models.CharField(max_length=250)
    business_name=models.CharField(max_length=250)
    business_type=models.CharField(max_length=250)
    building = models.CharField(max_length=250)
    landmark = models.CharField(max_length=250)
    town = models.CharField(max_length=250)
    pincode = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    contact_info=models.CharField(max_length=2500)
    license_num=models.CharField(max_length=250)
    state_issue=models.CharField(max_length=250)
    insurance_info=models.CharField(max_length=250)
    work_exp=models.CharField(max_length=2500)
    # past_project=models.CharField(max_length=2500)
    area_expertise=models.CharField(max_length=2500)
    reference=models.CharField(max_length=2500)
    profile=models.CharField(max_length=2500)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Dealer(models.Model):
    Dealer_name=models.CharField(max_length=250)
    dob=models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    phone =models.CharField(max_length=250)
    business_name = models.CharField(max_length=250)
    business_type = models.CharField(max_length=250)
    # contact_info = models.CharField(max_length=2500)
    building = models.CharField(default=1,max_length=2500)
    landmark = models.CharField(default=1,max_length=2500)
    town = models.CharField(default=1,max_length=2500)
    pincode = models.CharField(default=1,max_length=2500)
    state = models.CharField(default=1,max_length=2500)
    reference = models.CharField(max_length=2500)
    profile = models.CharField(max_length=2500)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)

class Client(models.Model):
    name=models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    phone =models.CharField(max_length=100)
    dob = models.CharField(max_length=250)
    building= models.CharField(max_length=250)
    landmark= models.CharField(max_length=250)
    town= models.CharField(max_length=250)
    pincode=models.CharField(max_length=250)
    discription = models.CharField(default=1,max_length=2500)
    state=models.CharField(max_length=250)
    profile=models.CharField(max_length=2500)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)

class DealerComplaint(models.Model):
    date = models.CharField(max_length=250)
    time = models.CharField(default=1,max_length=250)
    complainer = models.CharField(max_length=250)
    defendant = models.CharField(max_length=250)
    complain = models.CharField(max_length=2500)
    response = models.CharField(max_length=2500)
    DEALER = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE,default=1)

class ContractorComplaint(models.Model):
    date = models.CharField(max_length=250)
    complainer = models.CharField(max_length=250)
    defendant = models.CharField(max_length=250)
    complain = models.CharField(max_length=2500)
    response = models.CharField(max_length=2500)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    CLIENT = models.ForeignKey(Client, on_delete=models.CASCADE)

class Feedback(models.Model):
    date = models.CharField(max_length=250)
    time = models.CharField(default=1,max_length=250)
    feedback = models.CharField(max_length=250)
    type = models.CharField(max_length=20)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)

class Gallary(models.Model):
    image = models.CharField(max_length=250)
    discription = models.CharField(max_length=2500)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)

class UserRequest(models.Model):
    date = models.CharField(max_length=250)
    time = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    discription = models.CharField(max_length=500)
    addr = models.CharField(max_length=2500,default=1)
    # doc = models.CharField(max_length=250)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    CLIENT = models.ForeignKey(Client, on_delete=models.CASCADE)

class Chat(models.Model):
    message = models.CharField(max_length=2500)
    date = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    CLIENT = models.ForeignKey(Client, on_delete=models.CASCADE)

class Document(models.Model):
    doc = models.CharField(max_length=250)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    CLIENT = models.ForeignKey(Client, on_delete=models.CASCADE)

class ContractorPlan(models.Model):
    plan = models.CharField(max_length=2500)
    date = models.CharField(max_length=250)
    discription = models.CharField(max_length=2500)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    CLIENT = models.ForeignKey(Client, on_delete=models.CASCADE)

class ContractorReview(models.Model):
    date = models.CharField(max_length=250)
    discription = models.CharField(max_length=2500)
    rating = models.CharField(max_length=250)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    CLIENT = models.ForeignKey(Client, on_delete=models.CASCADE)

class Finance(models.Model):
    date = models.CharField(max_length=250)
    discription = models.CharField(max_length=2500)
    income = models.CharField(max_length=250,default=0)
    expense = models.CharField(max_length=250,default=0)
    USERREQUEST = models.ForeignKey(UserRequest, on_delete=models.CASCADE)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)

class DailyReport(models.Model):
    date = models.CharField(max_length=250)
    discription = models.CharField(max_length=2500)
    labour_num = models.CharField(max_length=250)
    time = models.CharField(max_length=250)
    consumed = models.CharField(max_length=2500)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)


class Order(models.Model):
    date = models.CharField(max_length=250)
    status = models.CharField(max_length=2500)
    payment_status = models.CharField(max_length=250)
    payment_date = models.CharField(max_length=250)
    building = models.CharField(max_length=250)
    landmark = models.CharField(max_length=250)
    town = models.CharField(max_length=250)
    pincode = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    DEALER = models.ForeignKey(Dealer, on_delete=models.CASCADE)

class Progress(models.Model):
    date = models.CharField(default=1,max_length=250)
    phase = models.CharField(default=1,max_length=250)
    percentage = models.CharField(default=1,max_length=2500)
    img = models.CharField(default=1,max_length=250)
    pdf = models.CharField(default=1,max_length=2500)
    discription = models.CharField(default=1,max_length=2500)
    sdate = models.CharField(default=1,max_length=2500)
    edate = models.CharField(default=1,max_length=2500)
    USERREQUEST = models.ForeignKey(UserRequest,default=1, on_delete=models.CASCADE)

class Quantity(models.Model):
    brick = models.CharField(max_length=250)
    cement = models.CharField(max_length=250)
    paint = models.CharField(max_length=250)
    sand = models.CharField(max_length=250)
    aggrigate = models.CharField(max_length=250)
    steel = models.CharField(max_length=250)
    price = models.CharField(max_length=250)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    CLIENT = models.ForeignKey(Client, on_delete=models.CASCADE)

class Vault(models.Model):
    file = models.CharField(max_length=2500)
    discription = models.CharField(max_length=2500)
    CLIENT = models.ForeignKey(Client, on_delete=models.CASCADE)

class Product(models.Model):
     pname = models.CharField(max_length=2500)
     pic = models.CharField(max_length=2500)
     discri = models.CharField(max_length=2500)
     price = models.CharField(max_length=2500)
     status = models.CharField(max_length=2500)
     DEALER = models.ForeignKey(Dealer, on_delete=models.CASCADE)

class OrderSub(models.Model):
    qnty = models.CharField(max_length=250)
    PRODUCT = models.ForeignKey(Product, on_delete=models.CASCADE)
    ORDER = models.ForeignKey(Order, on_delete=models.CASCADE)

class Cart(models.Model):
    PRODUCT = models.ForeignKey(Product, on_delete=models.CASCADE)
    CONTRACTOR = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=2500)
