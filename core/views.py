from django.shortcuts import render
from .models import *
from django.contrib.auth.views import logout_then_login
from .forms import *
from django.shortcuts import redirect

def comprar(request):
    if not request.user.is_authenticated:
        return redirect(to="login")
    carro = request.session.get("carro", [])
    total = 0
    for item in carro:
        total += item[5]
    venta = Venta()
    venta.total = total
    venta.cliente = request.user
    venta.save()
    for item in carro:
        detalle = Detalle()
        detalle.venta = venta
        detalle.producto = Producto.objects.get(codigo=item[0])
        detalle.precio = item[3]
        detalle.cantidad = item[4]
        detalle.save()
    request.session["carro"] = []    
    return redirect(to="carrito")    
        

def dropitem(request, codigo):
    carro = request.session.get("carro", [])
    for item in carro:
        if item[0] == codigo:
            if item[4] > 1:
                item[4] -= 1
                item[5] = item[3] * item[4]
            else:
                carro.remove(item)
            request.session["carro"] = carro
            return redirect(to="carrito")

def addtocar(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    carro = request.session.get("carro", [])
    for item in carro:
        if item[0] == codigo:
            item[4] += 1
            item[5] = item[3] * item[4]
            break
    else:
        carro.append([codigo, producto.descripcion, producto.imagen,
                  producto.precio, 1, producto.precio])
    request.session["carro"] = carro
    return redirect(to="home")

def carrito(request):
    return render(request, 'core/carrito.html', 
        {"carro":request.session.get("carro", [])})

def limpiar(request):
    request.session.flush()
    return redirect(to="home")
    
# Create your views here.
def registro(request):
    if request.method == "POST":
        form = Registro(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="login")
    else:        
        form = Registro()
    return render(request, 'core/registro.html', {'form':form})

def home(request):
    plantas = Producto.objects.all()
    return render(request, 'core/index.html', {'plantas':plantas})

def quienes(request):
    return render(request, 'core/quienes.html')

def logout(request):
    return logout_then_login(request, login_url="login")


