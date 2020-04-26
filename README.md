#### Как установить
1. Установим virtualenv
`sudo apt-get install python3-venv`
2. Создаем виртуальное окружене
`python3 -m venv .env`
3. Переключаемся на созданную среду
`source .env/bin/activate`
4. Ставим зависимости
`pip install -r requirements.txt`

#### Как использовать
1. Переключаемся на заранее созданную среду
`source .env/bin/activate`
2. Запуск
`python3 main.py <PARAMS>`.  Например: `python3 main.py --filename data.json`

Список доступных параметров:

* --filename FILENAME  - путь к файлу откуда будут читаться данные. (Формат файла см ниже). Обязательный параметр.
* --target_domain DOMAIN - Домен, переходы с которого мы хотим учитывать как "наши". Значение по умолчнию: "ours.com"
* --shop_domain DOMAIN - Домен магазина. Значение по умолчнию "shop.com"
* --finish_url URL - URL, куда переходит пользователь совершивший покупку. Значение по умолчнию "https://shop.com/checkout"
* --ignore-errors - Флаг. Если выставлен, то при загрузке данных мы будем игнорировать некорректные записи. Значение по умолчанию: false
* --another_domains DOMAIN [DOMAIN...] - Рекламные домены конкурентов. Значение по умолчанию: "theirs1.com", "theirs2.com"
* -h, --help - Показ справочной информации.

Важно! Все переходы с доменов не входящих в --another\_domains, --target\_domain, --shop\_domain - считаются внешними переходами

Формат данных во входных файлах:
```
[
    {
        "client_id": "...",
        "User-Agent": "...",
        "document.location": "...",
        "document.referer": "...",
        "date": "..."
    },
    ...
]
```

#### Как работает
Програма условно можно быть разделена на 2 куска:

1. Загрузка данных в оперативную память. Цель его: получение отсортированной по возрастанию последовательности переходов
2. Обработка загруженных данных. Цель его: анализ данных и получение ответа.

Программа возвращает последовательность переходов с нашего домена, которые привели к покупкам, а также количество покупок, которые произошли после переходов.
Программа игнорирует user-agent.

#### Запуск тестов
1. Переключаемся на заранее созданную среду
`source .env/bin/activate`
2. Запуск тестов
`python -m pytest tests/ -v`

Перед коммитом желательно запускать скрипт `bash precommit.sh`. Данный скрипт запускает не только тесты, но и линтеры flake8 и mypy

#### Объяснения некоторых нюансов
1. "А почему не используется Docker файл?" - т.к. входными данными являются файлы, их не очень удобно прокидывать в Docker файл. Можно конечно использовать механизм volume при запуске образа, но кажется это усложняет использование и требует наличие установленного docker на целевой системе.
2. "Зачем требование к возрастание логов к функции `build_statistics`"? Парсинг из файла это хорошо, однако, если мы подключаем БД или какие-нибудь инструменты большх вычислений, то мы можем запросить эти инструменты отсортировать нам данные и передать в эту функцию уже генератор и сможем не "взорваться" по памяти.

#### Технические аспекты
Разработка проведена на ОС Ubuntu 18.04

#### Что можно улучшить
1. Добавить тест загрузки файлов
2. Фильтр
3. Добавить неразличимость для ссылок по нашему домену от схемы url и последовательности параметров. Например: https://ours.com/data?a=1&b=2 была эквивалентно http://ours.com/data?b=2&a=1
4. Разнести отдельно requirements.txt для запуска и для разработки и тестов
