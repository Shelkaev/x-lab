import xml.etree.ElementTree as XmlElementTree #Импорт модуля работы с XML-файлами
import httplib2 #Импорт библиотеки для работы с HTTP
import uuid #Импорт библиотеки индификаторов
from config import *** #Из модуля config импортируется некий засекреченый url

#Присвоение переменных
***_HOST = '***'
***_PATH = '/***_xml'
CHUNK_SIZE = 1024 ** 2

#Функция перевода речи в текст через соединение с неким сервером ***
def speech_to_text(filename=None, bytes=None, request_id=uuid.uuid4().hex, topic='notes', lang='ru-RU',
                   key=***_API_KEY):
   #Проверка наличия записи
    if filename:
        with open(filename, 'br') as file:
            bytes = file.read()
    if not bytes:
        raise Exception('Neither file name nor bytes provided.')
    # Конвертация файла в формат PCM 16000 Гц 16 бит
    bytes = convert_to_pcm16b16000r(in_bytes=bytes)
    # Формирование GET запроса
    url = ***_PATH + '?uuid=%s&key=%s&topic=%s&lang=%s' % (
        request_id,
        key,
        topic,
        lang
    )
    # Чтение сконвертированного файла по частям
    chunks = read_chunks(CHUNK_SIZE, bytes)
    # Создание объекта HTTP соединения с сервером
    connection = httplib2.HTTPConnectionWithTimeout(***_HOST)
    # Сеанс обработки POST запроса
    connection.connect()
    connection.putrequest('POST', url)
    connection.putheader('Transfer-Encoding', 'chunked')
    connection.putheader('Content-Type', 'audio/x-pcm;bit=16;rate=16000')
    connection.endheaders()
    # Отправка файла по частям
    for chunk in chunks:
        connection.send(('%s\r\n' % hex(len(chunk))[2:]).encode())
    connection.send(chunk)
    connection.send('\r\n'.encode())

    connection.send('0\r\n\r\n'.encode())
    response = connection.getresponse()
    # Проверка ответа сервера и запись текста в xml формат
    if response.code == 200:
        response_text = response.read()
    xml = XmlElementTree.fromstring(response_text)
   # Проверка на успешное преобразование
    if int(xml.attrib['success']) == 1:
        max_confidence = - float("inf")
        text = ''
        # Вывод текста из объекта xml в переменную text при помощи цикла
        for child in xml:
            if float(child.attrib['confidence']) > max_confidence:
                text = child.text
                max_confidence = float(child.attrib['confidence'])

        if max_confidence != - float("inf"):
            return text
        else:

        raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
    else:
        raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
    else:
    raise SpeechException('Unknown error.\nCode: %s\n\n%s' % (response.code, response.read()))

# Новый класс с наследованием методов от класса Exception
сlass
SpeechException(Exception):
pass
