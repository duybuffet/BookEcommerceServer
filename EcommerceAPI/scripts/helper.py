from django.http import HttpResponse
import json

__author__ = 'Duy'


def return_response(data, status):
    data_json = json.dumps(data)
    return HttpResponse(data_json, content_type='application/json', status=status)
