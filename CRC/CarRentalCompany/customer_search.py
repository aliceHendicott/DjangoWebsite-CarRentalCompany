from .models import User as modelsUser


def handle_customer_search(fields):
    search_type = ""
    search = ""
    for field, value in fields.items():
        if field == 'csrfmiddlewaretoken':
            continue
        if field == 'search_options':
            search_type = value
        if field == 'search_input':
            search = value
    results = ""
    if search_type == 'user_name':
        results = modelsUser.objects.filter(user_name=search)
    elif search_type == 'id':
        results = modelsUser.objects.filter(id=search)
    elif search_type == 'user_phone':
        results = modelsUser.objects.filter(user_phone=search)
    if len(results) == 0:
        return -1
    else:
        return results

