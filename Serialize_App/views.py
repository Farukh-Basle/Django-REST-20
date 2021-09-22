
from django.shortcuts import render
from Serialize_App.models import Employee
from Serialize_App.forms import EmployeeModelForm
from django.http  import HttpResponse
import json
from django.views import View
from django.core.serializers import serialize

from Serialize_App.mixins import SerialzeMixin
from Serialize_App.mixins import is_json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Non_Id Based operations
# @csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class EmployeeListView(SerialzeMixin,  View):
    def get(self,request): # db --->> qs --->> dict --->> json ---> browser
        employee_list = Employee.objects.all()  # [{ }, { }, { },..]  or [ ]

        json_meta_data = serialize('json', employee_list)

        json_data = self.user_serialize(json_meta_data)

        return HttpResponse(json_data, content_type='application/json', status=200)



    def post(self,request): # browser --->> json --->> dict --->> qs -->> db
        data = request.body
        valid_json = is_json(data) #  True  |  False

        if not valid_json:
            json_data = json.dumps({'message' : 'Please send valid JSON type data'})
            return HttpResponse(json_data, content_type='application/json', status=400)

        emp_data = json.loads(data)

        form = EmployeeModelForm(emp_data)

        if form.is_valid():
            form.save()
            json_data = json.dumps(form.data)
            return HttpResponse(json_data,content_type='application/json',status=201)
        else:
            json_data = json.dumps(form.errors)
            return HttpResponse(json_data, content_type='application/json',status=400)



# Id Based operations
@method_decorator(csrf_exempt, name='dispatch')
class EmployeeDetailView(SerialzeMixin, View):
    def get(self, request,id): # db---qs ---dict --- json --- browser
        try:
            employee = Employee.objects.get(eno=id)
        except Employee.DoesNotExist:
            json_data = json.dumps({'message' : 'Requested resource not available to get.'})
            return HttpResponse(json_data,content_type='application/json', status=404)
        else:
            # emp_dict = {
            #     "eno" : employee.eno,
            #     "ename" : employee.ename,
            #     "salary" : employee.salary,
            #     "email" : employee.email,
            # }
            # json_data = json.dumps(emp_dict)
           
            json_meta_data = serialize('json',[employee])

            json_data = self.user_serialize(json_meta_data)

            return HttpResponse(json_data, content_type='application/json', status=200)


    def get_object_by_id(self,id):
        try:
            employee = Employee.objects.get(eno=id)
        except Employee.DoesNotExist:
            employee = None
        return employee



    def put(self, request,id):
        employee = self.get_object_by_id(id)  #  object  |   None

        if employee is None:
            json_data = json.dumps({'message': 'Requested resource not available to Update.'})
            return HttpResponse(json_data, content_type='application/json', status=404)

        data = request.body
        valid_json = is_json(data)  # True  | False

        if not valid_json:
            json_data = json.dumps({'message': 'Please send valid JSON type data'})
            return HttpResponse(json_data, content_type='application/json', status=400)


        emp_dict = json.loads(data)

        # original_data = {
        #     "eno" : employee.eno,
        #     "ename" : employee.ename,
        #     "salary" : employee.salary,
        #     "email" : employee.email,
        # }
        # original_data.update(emp_dict)

        # employee.update(emp_dict)

        form = EmployeeModelForm(emp_dict, instance=employee)

        if form.is_valid():
            form.save()
            json_data = json.dumps(form.data)
            return HttpResponse(json_data, content_type='application/json', status=200)
        else:
            json_data = json.dumps(form.errors)
            return HttpResponse(json_data, content_type='application/json',status=400)


    def delete(self, request,id):
        employee = self.get_object_by_id(id) # object | None

        if employee is None:
            json_data = json.dumps({'message': 'Requested resource not available to Delete.'})
            return HttpResponse(json_data, content_type='application/json', status=404)
        else:
            employee.delete()
            json_data = json.dumps({'message': 'Requested resource Deleted successfully.'})
            return HttpResponse(json_data, content_type='application/json',status=204)





