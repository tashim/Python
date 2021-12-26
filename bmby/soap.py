from suds.client import Client, WebFault
from suds.transport.http import HttpTransport

# Метод для корректной обработки строк в кодировке UTF-8 как в Python 3, так и в Python 2
import sys

if sys.version_info < (3,):
    def u(x):
        try:
            return x.encode("utf8")
        except UnicodeDecodeError:
            return x
else:
    def u(x):
        if type(x) == type(b''):
            return x.decode('utf8')
        else:
            return x


# Отладочная информация
# import logging
#
# logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)
# logging.getLogger('suds.transport').setLevel(logging.DEBUG)
# logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
# logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

# Дополнительный класс для корректной обработки HTTP-заголовков ответа SOAP-запроса
class MyTransport(HttpTransport):
    def __init__(self, *args, **kwargs):
        HttpTransport.__init__(self, *args, **kwargs)
        self.last_headers = None

    def send(self, request):
        result = HttpTransport.send(self, request)
        self.last_headers = result.headers
        return result


# --- Входные данные ---
# Адрес WSDL-описания сервиса Campaigns (регистрозависимый)
CampaignsURL = 'https://api.direct.yandex.com/v5/campaigns?wsdl'

# OAuth-токен пользователя, от имени которого будут выполняться запросы
token = 'ТОКЕН'

# Логин клиента рекламного агентства
# Обязательный параметр, если запросы выполняются от имени рекламного агентства
clientLogin = 'ЛОГИН_КЛИЕНТА'

# --- Подготовка, выполнение и обработка запроса ---
# Создание HTTP-заголовков запроса
headers = {
    "Authorization": "Bearer " + token,         # OAuth-token. Использование слова Bearer обязательно
    "Client-Login": clientLogin,                # Логин клиента рекламного агентства
    "Accept-Language": "ru",                    # Язык ответных сообщений
}

# Конструктор SOAP-клиента
client = Client(CampaignsURL, location='https://api.direct.yandex.com/v5/campaigns')
client.set_options(transport=MyTransport())     # Установка дополнительно класса для отправки запросов
client.set_options(headers=headers)             # Установка HTTP-заголовков запроса


# Создание тела запроса
params = {
    "SelectionCriteria": {},                    # Критерий отбора кампаний. Для получения всех кампаний должен быть пустым
    "FieldNames": ["Id", "Name"]                # Имена параметров, которые требуется получить
}

# Выполнение запроса
try:
    result = client.service.get(**params)
    print("RequestId: {}".format(client.options.transport.last_headers.get("requestid",False)))
    print("Информация о баллах: {}".format(client.options.transport.last_headers.get("units", False)))
    for campaign in result["Campaigns"]:
        print("Рекламная кампания: {} №{}".format(u(campaign['Name']), campaign['Id']))

except WebFault as err:
    print("Произошла ошибка при обращении к серверу API Директа.")
    print("Код ошибки: {}".format(err.fault['detail']['FaultResponse']['errorCode']))
    print("Описание ошибки: {}".format(u(err.fault['detail']['FaultResponse']['errorDetail'])))
    print("RequestId: {}".format(err.fault['detail']['FaultResponse']['requestId']))

except:
    err = sys.exc_info()
    print('Произошла ошибка при обращении к серверу API Директа: ' + str(err[1]))