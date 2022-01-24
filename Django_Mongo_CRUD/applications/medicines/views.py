from django.shortcuts import render,redirect

from applications.medicines.forms import MedicineForm
from applications.medicines.models import Medicine
# Create your views here.

def index(request):
    return render(request,'index.html')

def list(request):
    context = {'medicines' : Medicine.objects.all()}
    return render(request,'list.html',context)

def edit(request,req_id):
    medicine = Medicine.objects.get(medicine_id = req_id)
    if request.method == 'POST':
        form = MedicineForm(request.POST,instance=medicine)
        form.save()
        return list(request)
    return render(request,'edit.html',{'medicines' : medicine})

def form(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        form.save()
        return index(request)
    return render(request,'form.html')

def borrar(request,req_id):
    to_be_deleted = Medicine.objects.get(medicine_id = req_id)
    if request.method == 'POST':
        to_be_deleted.delete()
        return list(request)
    return render(request,'delete.html',{'medicines' : to_be_deleted})
