# Это Telegram-бот на Python сделан в учебных целях и работает

Бот сделан на базе фреймворка [aiogram](https://github.com/aiogram/aiogram)
Он умеет редактировать(наипримитивнейшим образом) список пользователей находящихся на сервере MySQL в таблице **tel_user**:

CREATE TABLE tel_user (id INT, name VARCHAR(40), status INT, telegram_id INT, PRIMARY KEY (id))

Бот конфигурируется с помощью файла bot.ini, который делатся по шаблону bot.ini.example. В bot.ini прописываются:

- ваш токен доступа
- параметры подключения к серверу MySQL
- user_id пользователя, у которого будут права админа и он сможет редактировать список пользователей

После запуска бот может:

- /adduser - добавить пользователя в БД
- /showuser - посмотреть список пользователей
- /deluser - удалить пользователя из БД
- /state - текущее состояние диалога от FSM
- cancel - прервать текущую процедуру (диалог)


## Вдохновляли и помогали

- [Книга по написанию ботов для Telegram на языке Python](https://mastergroosha.github.io/telegram-tutorial-2/)
- Веселые ребята из группы [aiogram ru](https://t.me/aiogram_ru)
- [Видеоуроки Кости](https://www.youtube.com/c/PhysicsisSimple/videos)
- [Шаблон](https://github.com/Tishka17/tgbot_template), взятый за основу и личные советы его автора
 
