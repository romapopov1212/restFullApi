import json
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Car

@method_decorator(csrf_exempt, name='dispatch')
class CarListView(View):
    def get(self, request):
        filter_criteria = {
            'brand': 'brand__iexact',
            'model': 'model__iexact',
            'year': 'year',
            'fuel_type': 'fuel_type__iexact',
            'transmission': 'transmission__iexact',
            'mileage_min': 'mileage__gte',
            'mileage_max': 'mileage__lte',
            'price_min': 'price__gte',
            'price_max': 'price__lte'
        }

        cars = Car.objects.all()
        for param, field in filter_criteria.items():
            value = request.GET.get(param)
            if value:
                if param in ['mileage_min', 'mileage_max', 'price_min', 'price_max']:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                cars = cars.filter(**{field: value})
        cars_data = list(cars.values('id', 'brand', 'model', 'year', 'fuel_type', 'transmission', 'mileage', 'price'))
        return JsonResponse(cars_data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            car = Car(
                brand=data.get('brand'),
                model=data.get('model'),
                year=data.get('year'),
                fuel_type=data.get('fuel_type'),
                transmission=data.get('transmission'),
                mileage=data.get('mileage'),
                price=data.get('price')
            )
            car.clean()
            car.save() 
            
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
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=400)
        except (KeyError, json.JSONDecodeError):
            return HttpResponseBadRequest("Invalid data")

@method_decorator(csrf_exempt, name='dispatch')
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
            return JsonResponse({"error": "Car not found"}, status=404)

    def delete(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
            car.delete()
            return JsonResponse({"message": "Car deleted successfully"}, status=204)
        except Car.DoesNotExist:
            return JsonResponse({"error": "Car not found"}, status=404)
    

