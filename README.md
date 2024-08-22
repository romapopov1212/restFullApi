проводил тесты через postman
POST http://127.0.0.1:8000/api/cars/ - для добавления автомобиля
шаблон JSON файла:
{
  "brand": "бренд",
  "model": "модель",
  "year": год,
  "fuel_type": "тип топлива",
  "transmission": "тип трансмиссии",
  "mileage": пробег,
  "price": цена
}

пример JSON файла:
{
  "brand": "Cadillac",
  "model": "Escalade",
  "year": 2023,
  "fuel_type": "бензин",
  "transmission": "автоматическая",
  "mileage": 0,
  "price": 10000000
}

получение списка всех автомобилей:
GET http://127.0.0.1:8000/api/cars/ 

получение по id: 
GET http://127.0.0.1:8000/api/cars/{id}/

получение списка автомобиля с фильтрами:
GET http://127.0.0.1:8000/api/cars/?brand={бренд}&model={модель}&year={год}&fuel_type={тип топлива}&transmission={тип трасмиссии}&mileage_min={минимальный пробег}&mileage_max={максимальный пробег}&price_min={минимальная цена}&price_max={максимальная цена} 

пример для фильтра:
http://127.0.0.1:8000/api/cars/?brand=Cadillac&model=Escalade&year=2023&fuel_type=бензин&transmission=автоматическая&mileage_min=0&mileage_max=10&price_min=0&price_max=10000000

удаление автомобиля по id:
DELETE http://127.0.0.1:8000/api/cars/{id}/ 
