# Это Telegram-бот на Python сделан в учебных целях и работает

Бот сделан на базе фреймворка [aiogram](https://github.com/aiogram/aiogram)
Он умеет редактировать(наипримитивнейшим образом) список пользователей находящихся на сервере MySQL в таблице *tel_user*:
CREATE TABLE tel_user (id INT, name VARCHAR(40), status INT, telegram_id INT, PRIMARY KEY (id))

Бот конфигурируется с помощью файла bot.ini, который вы должны сделать на основе bot.ini.example, указав в нем ваш токен доступа, параметры подключения к серверу MySQL и user_id пользователя,
у которого будут права админа и он сможет редактировать список пользователей.
-авпва
-ывапывап
                                  
Бот в котором продемонстрирована работа aiogram
# Пишем Telegram-ботов на Python (v2) 

Перед вами [вторая версия](https://mastergroosha.github.io/telegram-tutorial-2/) моей книги по написанию ботов для Telegram на языке Python. 
Первая версия, которая создавалась с 2015 по 2019 годы, доступна [здесь](https://github.com/MasterGroosha/telegram-tutorial).

Для самих ботов используется фреймворк [aiogram](https://github.com/aiogram/aiogram), 
а для книги взят генератор [mkdocs-material](https://squidfunk.github.io/mkdocs-material/).
