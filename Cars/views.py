import json
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views import View
from .models import Car

class CarListView(View):
    def get(self, request):
        cars = Car.objects.all()
        
        # Фильтрация по параметрам
        brand = request.GET.get('brand')
        if brand:
            cars = cars.filter(brand__iexact=brand)

        model = request.GET.get('model')
        if model:
            cars = cars.filter(model__iexact=model)

        year = request.GET.get('year')
        if year:
            cars = cars.filter(year=year)

        fuel_type = request.GET.get('fuel_type')
        if fuel_type:
            cars = cars.filter(fuel_type__iexact=fuel_type)

        transmission = request.GET.get('transmission')
        if transmission:
            cars = cars.filter(transmission__iexact=transmission)

        mileage_min = request.GET.get('mileage_min')
        if mileage_min:
            cars = cars.filter(mileage__gte=mileage_min)

        mileage_max = request.GET.get('mileage_max')
        if mileage_max:
            cars = cars.filter(mileage__lte=mileage_max)

        price_min = request.GET.get('price_min')
        if price_min:
            cars = cars.filter(price__gte=price_min)

        price_max = request.GET.get('price_max')
        if price_max:
            cars = cars.filter(price__lte=price_max)

        cars_data = list(cars.values('id', 'brand', 'model', 'year', 'fuel_type', 'transmission', 'mileage', 'price'))
        return JsonResponse(cars_data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            car = Car.objects.create(
                brand=data['brand'],
                model=data['model'],
                year=data['year'],
                fuel_type=data['fuel_type'],
                transmission=data['transmission'],
                mileage=data['mileage'],
                price=data['price']
            )
            return JsonResponse({
                "id": car.id,
                "brand": car.brand,
                "model": car.model,
                "year": car.year,
                "fuel_type": car.fuel_type,
                "transmission": car.transmission,
                "mileage": car.mileage,
                "price": car.price,
            }, status=201)
        except (KeyError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid data")

class CarDetailView(View):
    def get(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
            car_data = {
                "id": car.id,
                "brand": car.brand,
                "model": car.model,
                "year": car.year,
                "fuel_type": car.fuel_type,
                "transmission": car.transmission,
                "mileage": car.mileage,
                "price": car.price,
            }
            return JsonResponse(car_data)
        except Car.DoesNotExist:
            return HttpResponse(status=404)
