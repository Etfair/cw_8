Инструкция по запуску проекта:
Клонирование репозитория

https://github.com/Etfair/CW_8 

Установка зависимостей
1. Убедитесь, что в системе установлен Python3.x. Если нет, установите его в соответствии с инструкциями для вашей операционной системы.
2. Создайте виртуальное окружение

python3 -m venv venv

3. Активировать виртуальное окружение

source ./venv/Scripts/activate
venv/Scripts/activate.bat

4. Установить зависимости проекта, указанные в файле requirements.txt


Настройка окружения
1. В директории проекта создать файл .env

touch .env

2. Открыть файл

nano .env

3. Записать в файл следующие настройки

DATABASES_DEFAULT_ENGINE=django.db.backends.postgresql_psycopg2
DATABASES_DEFAULT_NAME=name_db
DATABASES_DEFAULT_USER=имя_пользователя
DATABASES_DEFAULT_PASSWORD=пароль_пользователя
DB_HOST=

EMAIL_HOST_USER=почта_для_аутентификации
EMAIL_HOST_PASSWORD=пароль

В каталоге проекта есть шаблон файла .env

Для запуска Docker:

Установите Docker desktop;
В терминале введите команду для создания контейнера:
docker compose build
и
docker compose up

Для применения миграция:
docker compose exec app python manage.py migrate

Создание бот в телеграм

Заходим в Телеграм, в строке «Поиск» находим BotFather – это конструктор чат-ботов в Телеграме, нажимаем «Старт».
Чтобы создать нового, нужно нажать на /newbot.
Главный бот предложит вам придумать имя для вашего бота, которое будут видеть все и смогут по этому имени находить его.
После того как новый бот получил свое имя, а BotFather его принял,
Он предложит придумать никнейм – это будет ссылка на нового робота в Телеграмме.
У каждого бота есть токен – уникальная строка из символов, которая нужна, чтобы установить подлинность робота в системе.
Его следует не терять и скопировать в .env
