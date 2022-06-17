# SHAREWISH

## Описание сайта
SHAREWISH - социальная сеть, позволяющая делиться своими желаниями, узнавать самые тайные желания своих друзей и исполнять их. 
Данный сайт позволяет как вести личную страницу со своми желаниями, так и делиться ими с друзьями.

## Запуск
Перед началом работы установите python==3.9. Распакуйте пароект в отдельную папку. Импортируйте все зависимости с помощью команды из корня ```pip install -r requierments.txt```
В командной строке создаём переменную окружения ```set APP_SETTINGS=config.Config```. Создайте папку db в корне. Вызовите ```python manage.py``` из корня и переходим по адресу localhost:5000.

## Описание функционала
На главной странице для неавторизированного пользователя есть возможность посмотреть все публичные желания.
После входа или регистрации, пользователь может: 
	добавлять/удалять/изменять свои желания, 
	редактировать личные данные, 
	добавлять/отправлять заявки/удалять друзей.
У желания есть заголовок, описание, ссылка на страницу с конкретным товаром, изображение и область видимости - публичное/приватное.



