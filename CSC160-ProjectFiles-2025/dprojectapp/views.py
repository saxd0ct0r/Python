from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from .models import Customer
# Create your views here.

#def index(request):
#    return HttpResponse('Hello World!')

#def new(request):
#    return HttpResponse('New Page')

from .models import Product
from .models import Customer

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})


def add(request):
  template = loader.get_template('add.html')
  return HttpResponse(template.render({}, request))


def addrecord(request):
  x = request.POST['first']
  y = request.POST['last']
  z = request.POST['middle']
  a = request.POST['email']
  b = request.POST['phone']
  c = request.POST['avatar']
  customers = Customer(fname=x, lname=y, mi=z, email=a, phone=b, avatar_url=c)
  customers.save()
  return HttpResponseRedirect(reverse('index'))


def delete(request, id):
  customers = Customer.objects.get(id=id)
  customers.delete()
  return HttpResponseRedirect(reverse('index'))


def update(request, id):
  mycustomer = Customer.objects.get(id=id)
  template = loader.get_template('update.html')
  context = {
    'mycustomer': mycustomer,
  }
  return HttpResponse(template.render(context, request))


def updaterecord(request, id):
  first = request.POST['first']
  last = request.POST['last']
  middle = request.POST['middle']
  email = request.POST['email']
  phone = request.POST['phone']
  avatar = request.POST['avatar']
  customers = Customer.objects.get(id=id)  
  customers.fname = first
  customers.lname = last
  customers.mi = middle
  customers.email = email
  customers.phone = phone
  customers.avatar_url = avatar
  customers.save()
  return HttpResponseRedirect(reverse('index'))


def cust(request):
  customers = Customer.objects.all()
  return render(request, 'customers.html', {'customers': customers})


'''
def cust(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customers': customers})


def add(request):
    template = loader.get_template('add.html')
    return HttpResponse(template.render({}, request))

def newcustomer(request):
  x = request.POST['fname']
  y = request.POST['lname']
  customer = Customers(fname=x, lname=y)
  customer.save()
  return HttpResponseRedirect(reverse('index'))




def addrecord(request):
    f = request.POST['fname']
#    l = request.POST['lname']
#    m = request.Post['middle']
#    e = request.Post['email']
#    p = request.Post['phone']
#    a = request.Post['avatar']
#    customer = Customer(fname=f, lname=l, mi=m, email=e, phone=p, avatar_url=a)
    customer = Customer(fname=f)
    customer.save()
    
    return HttpResponseRedirect(reverse('index'))
'''


