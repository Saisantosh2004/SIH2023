from django.shortcuts import render
from .compare import get_product_data


def product_form_view(request):
    if request.method == 'POST':
        
        print(request.POST['text'])
        search_query=request.POST['text']
        products = get_product_data(search_query)

        return render(request,'index.html',{'products':products})
    
    else:
        
        pass

    return render(request, 'index.html')

