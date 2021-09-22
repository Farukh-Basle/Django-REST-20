
from django.core.serializers  import serialize
import json
class SerialzeMixin(object):
    def user_serialize(self,data):
        emp_dict = json.loads(data)
        employee_list = []
        for emp in emp_dict:
            employee_list.append(emp['fields'])
        json_data = json.dumps(employee_list)

        return json_data


def is_json(data):
    try:
        dict_data = json.loads(data)
        valid = True
    except ValueError:
        valid = False
    return valid

