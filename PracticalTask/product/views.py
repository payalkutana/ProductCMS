from django.shortcuts import render, redirect, get_object_or_404
from .serializer import ProductSerializer
from django.contrib import messages
from .models import product

# Create your views here.
def ProductCreateView(request):

    if request.method == "POST":
        try:
            name = request.POST.get('name')
            price = request.POST.get('price')
            image = request.FILES.get('image')  

            product_obj = product(name=name, price=price, image=image)
            product_obj.save()

            messages.info(request, 'Product Created Successfully!')
            return redirect('product:list_product')
        
        except Exception as e:
            messages.info(request, 'Something Went Wrong!')
            return redirect('product:create_product')
        
    return render(request, 'product/create_product.html')
        
def ProductListView(request):
    print(request.user)
    if request.method == "GET":
        products = product.objects.all()
        return render(request, 'product/list_product.html', {'products': products, 'user':request.user})
    
def ProductUpdateView(request, pk):
        
    product_obj = get_object_or_404(product,id=pk)
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            price = request.POST.get('price')
            image = request.FILES.get('image')  
            product_obj.name = name
            product_obj.price = price
            
            if image:
                product_obj.image = image
            product_obj.save()

            messages.success(request, 'Product updated successfully!')
            return redirect('product:list_product')
        
        except Exception as e:
            messages.error(request, str(e))
            return redirect('product:list_product')
        
    return render(request, 'product/update_product.html', {'product': product_obj})

def ProductDeleteView(request, pk):
    product_obj = get_object_or_404(product,id=pk)

    print(request)

    if request.method == "POST":
        try:
            product_obj.delete()
            messages.success(request, 'Product Deleted successfully!')
            return redirect('product:list_product')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('product:list_product')
        
    return redirect('product:list_product')
    
