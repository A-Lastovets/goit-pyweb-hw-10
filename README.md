# goit-pyweb-hw-10

Працював через docker контейнер: hw10-postgres
запуск: docker-compose up -d

1. скрипт: "python manage.py migrate_mongo_to_postgres"
запустить міграцію з бази данних Mongo до бази данних Postgres

2. Якщо раніше додані користувачі не мають профілю, то можна їх автоматично додати до всіх користувачів
використовуючи цей скрипт: "python manage.py create_missing_profiles"

3. Скрипт: "python manage.py runserver"
Початок роботи сервера:
http://127.0.0.1:8000/  - домашня сторінка
http://127.0.0.1:8000/admin  - перехід на адмін панель. (Адміністратор створений)

Реалізовано можливість реєстрації на сайті та вхід на сайт.
Усі цитати та список авторів доступні для перегляду без автентифікації користувача.
Можна зайти на сторінку кожного автора без автентифікації користувача.
Можливість додавання нового автора на сайт лише для зареєстрованого користувача.
Можливість додавання нової цитати на сайт із зазначенням автора тільки для зареєстрованого користувача.


Quotes - Сторінка цитат

В кінці кожної цитати можна перейти на сторінку з інформацією відповідного автора

"“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”" - Albert Einstein About Author
"“It is our choices, Harry, that show what we truly are, far more than our abilities.”" - J.K. Rowling About Author
"“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”" - Albert Einstein About Author

Додатково:
При переході на сторінку авторів   -   Кожен автор має два посилання: одне на деталі про автора і одне на його цитати

Authors  - сторінка авторів

Eleanor Roosevelt View Details View Quotes
Marilyn Monroe View Details View Quotes
Jane Austen View Details View Quotes
J.K. Rowling View Details View Quotes
