# -*- coding: cp1251 -*-
from dataclasses import dataclass
from abc import ABC, abstractmethod
from math import fabs
from math import ceil
from sys import maxsize
from functools import wraps
import random
import time
from datetime import datetime
# Для отношения М:N заводим отдельные классы с айди и атрибутами
# Для отношения 1:N добавляем к зависимому классу айди того объекта которому он принадлежит

# список имен для тестов
names_list = ["Ильина София Марковна", "Алексеев Арсений Андреевич", "Левина Нина Владимировна", "Волкова Стефания Филипповна",
            "Авдеев Фёдор Артёмович", "Гуляев Филипп Маркович", "Щукина Василиса Александровна", "Авдеева Алёна Михайловна", "Васильев Фёдор Ильич", "Андрианова Василиса Леонидовна",
             "Иванова Софья Никитична", "Захарова Мария Даниэльевна", "Дмитриева Полина Евгеньевна", "Покровская Алиса Матвеевна", "Николаева Ника Фёдоровна", "Зайцев Артём Юрьевич",
              "Попов Дмитрий Иванович", "Нечаева Виктория Александровна", "Захарова Лилия Всеволодовна", "Игнатьева София Станиславовна", "Алексеева Анна Максимовна", "Кузнецов Михаил Даниилович",
             "Гусева Дарья Денисовна", "Кузнецова Ника Александровна", "Иванов Денис Максимович", "Балашова Анастасия Владимировна", "Лавров Матвей Владиславович",
             "Самсонов Константин Владимирович", "Соколова Елена Семёновна"]
# список продуктов для тестов
items_names_list = ["Шоколадно-ореховая паста", "Шоколад с арахисом", "Йогурт питьевой дыня-клубника-земляника", "Йогурт греческий злаки-клетчатка льна",
            "Ролл Калифорния с лососем", "Сладкие яблоки", "Маца традиционная", "Фалафель безглютеновый", "Фреш рол з сьомгою", "Паляниця сырна",
            "Панини с моцареллой буффало и томатами", "Морковь", "Круассан с яблоками", "Чипсы со вкусом чили и лайма", "Фруктовый салат с йогуртом",
            "Пенне арабьята", "Йогурт с карамелью", "Йогурт с кокосом и ванилью", "Земляника", "Зелёный перец", "Батон",
            "Ролл с креветкой", "Сок яблоко-сельдерей", "Попкорн с карамелью", "Сливочный суп с форелью", "Карпаччо из осьминога",
            "Хлеб тостовый", "Хлебцы с морковью", "Сыр с белой плесенью", "Чипсы со вкусом бекона", "Сладкая кукуруза",
            "Клубника в шоколаде", "Вафли с топлёным молоком", "Кубинский кофе", "Йогурт питьевой малина-базилик",
            "Конфеты с фундуком", "Глазированный сырок с карамелью", "Запеченные фаланги краба", "Апельсиновый сок"]

# store list словарь айди - магазин


@dataclass
class Item_Store: # класс отношение предмета и магазина
    store_id: int
    item_id: int
    item_quantity: int
    name: str


@dataclass
class Provider_Store: # класс отношение доставщика и магазина
    store_id: int
    provider_id: int
    request_list: list


@dataclass
class Provider_Item: # класс отношение доставщика и товара
    provider_id: int
    item_id: int
    item_quantity: int
    name: str


@dataclass
class Item: # класс товара
    item_id: int
    name: str
    provider_id: int
    store_id: int
    unit_price: float


@dataclass
class Order: # класс заказа
    order_status: str
    item_list: dict
    creation_time: float
    finish_time: float
    courier_id: int
    storekeeper_id: int
    user_id: int
    distance: float

def froze_it(cls): # создание декоратара запрещающего добавление новых полей
    cls.__frozen = False

    def frozensetattr(self, key, value):
        if self.__frozen and not hasattr(self, key): # hasattr возвращает флаг указывающий содержит ли объект  указанный атрибут
            print("Запрещен доступ к классу {}. Невозможно поставить {} = {}"
                  .format(cls.__name__, key, value)) # выводит предупреждение
        else:
            object.__setattr__(self, key, value)

    def init_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.__frozen = True
        return wrapper

    cls.__setattr__ = frozensetattr
    cls.__init__ = init_decorator(cls.__init__)

    return cls


class Interface: # интерфейс создающий предметы, магазины, провайдеров для тестов и хранящий данные о них
    def __init__(self):
        self.providers_list = dict()
        self.item_store = []
        self.provider_item = []
        self.items_list = []
        self.stores_list = dict() # словарь где по айди возвращается магазин
        for _ in range(random.randint(1, 10)): # создание провайдера
            id = random.randint(1, maxsize)
            provider = Provider(id)
            self.providers_list[id] = provider
            for __ in range(random.randint(1, 100)): # создание предметов у провайдера
                item_id = random.randint(1, maxsize)
                item_name = items_names_list[random.randint(0, len(items_names_list) - 1)]
                quantity = random.randint(1, 30)
                item = Item(item_id, item_name, id, -1, random.uniform(0.5, 1000.5))
                self.items_list.append(item)
                self.provider_item.append(Provider_Item(id, item_id, quantity, item_name))

        for _ in range(random.randint(1, 10)): # создание складов
            id = random.randint(1, maxsize)
            store = Store(id)
            self.stores_list[id] = store

        for _ in range(random.randint(1, 1000)): # создание предметов которые отправляются к рандомным складам
            item_id = random.randint(1, maxsize)
            store_id = random.choice([key for key in self.stores_list.keys()])
            provider_id = random.choice([key for key in self.providers_list.keys()])
            item_name = items_names_list[random.randint(0, len(items_names_list) - 1)]
            item = Item(item_id, item_name, provider_id, store_id, random.uniform(0.5, 1000.5))
            self.item_store.append(Item_Store(store_id, item_id, random.randint(1, 30), item_name))
            self.items_list.append(item)

    def get_id(self, store_id, name): # возвращает айди предмета
        for item in self.item_store:
            if item.name.lower() == name and item.store_id == store_id:
                return item.item_id
        id = -1
        return id

    def get_amount_and_price(self, store_id, item_id): # возвращает количество предмета на складе и цену
        for item in self.item_store:
            if item.item_id == item_id and item.store_id == store_id:
                price = self.get_price(item_id)
                return item.item_quantity, price
        return -1, -1

    def get_price(self, item_id): # возвращает цену
        for item in self.items_list:
            if item.item_id == item_id:
                return item.unit_price
        return -1

    def delete_item(self, item_id, store_id, amount): # удаляет предмет со склада
        for item in self.item_store:
            if item.item_id == item_id and item.store_id == store_id:
                item.item_quantity -= amount
                return

    def delete_item_provider(self, item_id, provider_id, amount): # удаляет предмет у провайдера
        for item in self.provider_item:
            if item.item_id == item_id and item.provider_id == provider_id:
                item.item_quantity -= amount
                return

    def choose_store(self, location): # выбор магазина основываясь на часах работы и локации
        closest_store = 0
        distance = maxsize
        curr_time = time.time()
        curr_hour = (time.localtime(curr_time)).tm_hour
        myobj = datetime.now()
        for id in self.stores_list:
            if fabs(self.stores_list[id].location - location) < distance and self.stores_list[id].open_hour < myobj.hour < self.stores_list[id].close_hour:
                closest_store = id
                distance = fabs(self.stores_list[id].location - location)
        return closest_store, distance

    def get_item_name(self, item_id): # возвращает имя объекта по айди
        for item in self.items_list:
            if item.item_id == item_id:
                return item.name
        return "Объект не найден"

    def get_request_list(self, store_id): # создает список запроса провайдеру
        request_list = dict()
        for i in range(random.randint(1, 10)):
            request_list[items_names_list[random.randint(0, len(items_names_list) - 1)]] = random.randint(1, 30)
        return request_list

    def request_id(self, provider_id, item_name): # возвращает айди запрошенного айтема по имени
        for item in self.provider_item:
            if item.name == item_name and item.provider_id == provider_id:
                return item.item_id
        id = -1
        return id

    def return_item(self, item_id, store_id): # возвращает айтем
        for item in self.items_list:
            if item.item_id == item_id:
                item.store_id = store_id
                return item

    def update_stock(self, item_id, store_id, quantity): # добавляет на склад предмет в определенном количестве
        item_name = ""
        for item in self.items_list:
            if item.item_id == item_id:
                item_name = item.name
        print("Был доставлен {0} в количестве {1} штук".format(item_name, quantity))
        self.item_store.append(Item_Store(store_id, item_id, quantity, item_name))

    def send_request(self): # отправить запрос от магазина провайдеру (выбирает рандомный для теста)
        store_id = random.choice([key for key in self.stores_list.keys()])
        self.stores_list[store_id].send_request(self.get_provider())

    def take_order(self, closest_store_id, ordered_items, coordinates, user_id): # магазин берет заказ
        self.stores_list[closest_store_id].take_order(ordered_items, coordinates, user_id)

    def get_store(self, store_id): # возвращает магазин по айди
        return self.stores_list[store_id]

    def get_order_time(self, closest_store_id, coordinates): # возвращает примерное время сколько займет доставка заказа
        courier_speed = 30
        return fabs(self.stores_list[closest_store_id].location - coordinates) / courier_speed

    def print_request(self, request_list): # распечатать заказ провайдеру
        for request in request_list:
            print("Был заказан {0} в количестве {1} штук".format(request, request_list[request]))

    def get_provider(self): # возвращает рандомного провайдера
        return self.providers_list[random.choice([key for key in self.providers_list.keys()])]

    def add_worker(self): # добавить нового работника
        new_id = random.randint(0, maxsize)
        name = names_list[random.randint(0, len(names_list) - 1)]
        store_id = random.choice([key for key in self.stores_list.keys()])
        self.stores_list[store_id].get_worker(new_id, name)

class Provider:
    def __init__(self, id):
        self.id = id

    def send_order(self, store_id, request_list):
        orders = dict() # заказ это словарь из айди предмета и его количества в запросе
        for request in request_list:
            item_id = interface.request_id(self.id, request)
            if item_id != -1:
                orders[item_id] = request_list[request]
            else:
                print("Товар {0} отсутствует".format(request))
        self.update_stocks(store_id, orders)

    def update_stocks(self, store_id, orders): # обновить склады
        for order in orders:
            interface.delete_item_provider(order, self.id, orders[order])
            interface.update_stock(order, store_id, orders[order])


@froze_it
class Worker(ABC):
    def __init__(self, name, store_id, id):
        self.name = name
        self.shift_start = 0
        self.shift_end = 0
        self.store_id = store_id
        self.payment = 0
        self.hourly_rate = 300
        self.id = id
        self.free = True # маячок свободен ли в данный момент работник

    def set_name(self, name):
        self: name = name

    def get_name(self):
        return self.name

    def get_shift(self):
        return self.shift

    # выбирает сколько часов продлится смена
    def set_shift(self):
        hours = random.randint(1, 24) # рандомный генератор, сколько часов продлится смена работника
        self.shift_end = time.time() + hours * 3600 # высчитываем конец смены
        self.shift_start = time.time() # начало смены
        print("Работник {0} работает с {1} до {2}".format(self.name, time.ctime(self.shift_start), time.ctime(self.shift_end)))

    def get_payment(self):
        hours = (self.shift_end - self.shift_start) // 3600 # высчитаем сколько часов длилась смена
        shift_payment = hours * self.hourly_rate # получаем зп
        print("Работник {0} заработал {1} условных единиц денег за {2}-часовую смену".format(self.name, shift_payment, hours))

    @abstractmethod # абстрактный метод получения заказа работником
    def get_order(self, order):
        pass


class Courier(Worker):
    def get_order(self, order):
        free = False
        print("Заказ был получен курьером")
        order.order_status = "Заказ получен курьером"
        self.deliever(order) # получили заказ и доставляем

    def deliever(self, order):
        speed = 30
        self.leave_store() # покидает магазин (одна минута на выход)
        order.order_status = "Курьер покинул магазин и в процессе доставки"
        time.sleep(order.distance / speed) # отправляется доставить заказ
        users_list[order.user_id].take_order() # клиент забирает заказ
        print("Заказ был вручен. Курьер возвращается на склад")
        order.order_status = "Заказ вручен"
        d = order.distance
        order.finish_time = time.time() # сохраняем время конца заказа

        order_info(order) # выводим информацию о заказе
        del order # удаляем его

        self.come_back(d) # курьер возвращается

    def leave_store(self):
        time.sleep(60)

    def come_back(self, distance): # возврат курьера
        time.sleep(distance)
        self.free = True
        if time.time() >= self.shift_end:
            self.get_payment()


class Storekeeper(Worker):
    # время сборки одного товара 45 сек
    def get_order(self, order):
        print("Заказ получен сборщиком")
        order.order_status = "Получен сборщиком" # обновляем статус
        self.free = False
        self.pack_order(order) # сборщик собирает заказ

    def pack_order(self, order):
        for item in order.item_list:
            interface.get_store(self.store_id).delete_item(item, order.item_list[item])
            print("Сборщик упаковывает " + interface.get_item_name(item))
            time.sleep(45)
        self.give_to_courier(interface.get_store(self.store_id).get_courier(order.courier_id), order)

    def give_to_courier(self, courier, order):
        courier.get_order(order)
        self.free = True
        if time.time() >= self.shift_end:
            self.get_payment()
@froze_it
class Store:
    def __init__(self, id):
        self.id = id
        self.location = random.uniform(1.5, 100.5)
        self.open_hour = random.randint(1, 22)
        self.close_hour = random.randint(self.open_hour + 1, 24)

        self.couriers_list = dict()
        self.storekeepers_list = dict()
        # создает курьеров и кладовщиков
        for i in range(random.randint(1, 10)):
            new_id = random.randint(0, maxsize)
            courier = Courier(names_list[random.randint(0, len(names_list) - 1)], self.id, new_id)
            self.couriers_list[new_id] = courier
            courier.set_shift()
        for i in range(random.randint(1, 10)):
            new_id = random.randint(0, maxsize)
            storekeeper = Storekeeper(names_list[random.randint(0, len(names_list) - 1)], self.id, new_id)
            self.storekeepers_list[new_id] = storekeeper
            storekeeper.set_shift()

    def delete_item(self, item_id, amount): # удаление предмета
        interface.delete_item(id, item_id, amount)

    def send_request(self, provider): # отправить запрос на получение предметов от провайдера
        request_list = dict()
        for i in range(random.randint(1, 30)):
            request_list[items_names_list[random.randint(0, len(items_names_list) - 1)]] = random.randint(1, 10)
        interface.print_request(request_list)
        provider.send_order(self.id, request_list)

    def get_courier(self, courier_id): # получить курьера
        return self.couriers_list[courier_id]

    def take_order(self, ordered_items, distance, user_id): # взять заказ
        courier_id = self.set_courier()
        storekeeper_id = self.set_storekeeper()
        order = Order("Принят в работу", ordered_items, time.time(), -1, courier_id, storekeeper_id, user_id, fabs(self.location - distance))
        self.storekeepers_list[storekeeper_id].get_order(order)

    def get_amount_and_price(self, item_id, amount):
        interface.get_amount_and_price(self.id, item_id)

    def set_courier(self):
        for key in self.couriers_list.keys():
            if self.couriers_list[key].free is True and random.randint(0, 10) != 5: # вероятность что курьер не придет 1\10
                self.couriers_list[key].payment -= 500 # начисление штрафа
                return self.couriers_list[key].id
            else:
                continue

    # дать заказу курьера

    def set_storekeeper(self):
        for key in self.storekeepers_list.keys():
            if self.storekeepers_list[key].free is True:
                return self.storekeepers_list[key].id

    # дать заказу кладовщика

    def get_worker(self, worker_id, worker_name):
        if (random.randint(0, 1) == 0):
            courier = Courier(worker_name, self.id, worker_id)
            self.couriers_list[worker_id] = courier
            courier.set_shift()
        else:
            storekeeper = Storekeeper(worker_name, self.id, worker_id)
            self.storekeepers_list[worker_id] = storekeeper
            storekeeper.set_shift()

    # взять работника к себе и дать ему смену


# Что находится в заказе? Статус доставки, список товаров, время создания-время доставки, кто собирал-доставлял
@froze_it
class User:
    def __init__(self):
        self.id = random.randint(0, maxsize)

    def make_order(self):
        ordered_items = dict()
        print("Введите ваши координаты")
        coordinates = float(input())
        closest_store_id, distance = interface.choose_store(coordinates)
        print("Введите название нужного товара")
        string = input()
        total_price = 0
        while string != '':
            string = string.lower()
            item_id = interface.get_id(closest_store_id, string)
            if item_id != -1:
                print("Введите требуемое количество")
                item_amount = input()
                while not item_amount.isalnum():
                    item_amount = input()
                item_amount = int(item_amount)
                store_amount, price = interface.get_amount_and_price(closest_store_id, item_id)
                if item_amount <= store_amount:
                    ordered_items[item_id] = store_amount
                    total_price += price * store_amount
                else:
                    print("Требуемое количество товаров недоступно. Можно заказать товар в количестве: ", int(store_amount))
                    beacon = agree_menu()
                    if beacon:
                        ordered_items[item_id] = store_amount
                        total_price += price * store_amount
            else:
                print("Запрошенного товара нет. Отменить заказ? Да или Нет")
                beacon = agree_menu()
                if beacon:
                    return
            print("Введите следующий товар. Нажмите энтер когда все")
            string = input().lower()

        print("Цена заказа: {0} условных единиц денег".format(ceil(total_price)))
        print("Ожидаемое время доставки заказа {0} минут".format(ceil(interface.get_order_time(closest_store_id, coordinates))))

        interface.take_order(closest_store_id, ordered_items, coordinates, self.id)

    # сделать заказ
    def take_order(self):
        time.sleep(60)
# забрать заказ


def agree_menu():
    string = input().lower()
    print("Да или Нет")
    if string == "да":
        return True
    elif string != "нет":
        print("Некорректный ответ")
    else:
        return False
    while string != "нет" and string != "да":
        string = input().lower()
        if string == "да":
            return True
        elif string != "нет":
            print("Некорректный ответ")
        else:
            return False


def order_info(order):
    order_time = ceil((order.finish_time - order.creation_time) / 60)
    print("Заказ был создан {0} и доставлен {1}".format(time.ctime(ceil(order.creation_time)), time.ctime(ceil(order.finish_time))))
    print("Заказ был доставлен за {0} минут".format(order_time))


global interface
interface = Interface()
interface.send_request()
New_User = User()
users_list = dict()
users_list[New_User.id] = New_User
New_User.name = "Саша"
New_User.make_order()
interface.add_worker()
