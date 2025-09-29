from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from colegio_project.schema import schema
from graphql import graphql_sync

def graphiql_interface(request):
    return render(request, 'graphene/graphiql.html')

@csrf_exempt
@require_http_methods(["POST"])
def graphql_endpoint(request):
    try:
        data = json.loads(request.body)
        query = data.get('query')
        variables = data.get('variables')
        
        result = graphql_sync(schema, query, variable_values=variables)
        
        response_data = {
            'data': result.data
        }
        
        if result.errors:
            response_data['errors'] = [str(error) for error in result.errors]
        
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({
            'errors': [str(e)]
        }, status=400)