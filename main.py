import datetime
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers


base_url = 'https://habr.com/ru/all/'
headers = Headers().generate()
response = requests.get(base_url, headers=headers).text
soup = BeautifulSoup(response, 'html.parser')
posts = soup.find_all('div', class_="tm-article-snippet")


def log_with_path(path):  #Логгер с путем к файлу-логу
    def logger(some_function):  #Сублоггер принимает функцию и создает внутри обертку с лог-файлом
        def new_function(*args, **kwargs):
            log_dict = {}
            log_dict['date_and_time'] = datetime.datetime.now()
            log_dict['function_name'] = some_function.__name__
            log_dict['arguments'] = f'{args}, {kwargs}'
            print("Начинается вызвов функции!")
            result = some_function(*args, **kwargs)
            log_dict['result'] = result
            with open(path, "a") as file:  # Добавляем информацию в файл-лог, без перезаписи
                for key, value  in log_dict.items():
                    file.write(f'{key}--{value}\n')
                file.write('-------------\n')
            return result
        return new_function
    return logger


@log_with_path('/home/igor/IT/Netology/Decorators/log_dir/log_info.txt')  #Абсолютный адрес файл-лога
# @log_path('log_info.txt') #Если создаем файл, например, в текущей директории(относительный адрес)
def scraping(keywords):
    for post in posts:
        for keyword in keywords:
            if keyword in post.text:
                date_time = post.find('span', class_='tm-article-snippet__datetime-published').text
                title = post.find(class_="tm-article-snippet__title-link").text
                href = post.find('a', class_="tm-article-snippet__title-link").attrs['href']
                link = base_url + href
                return(f"<{date_time}>-<{title}>-<{link}>")


print(scraping(keywords=['дизайн', 'фото', 'web', 'python', 'разработчика', 'Телеграм', 'МГЛУ'])
)

