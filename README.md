[![pipeline status](https://gitlab.crja72.ru/django/2024/autumn/course/students/284664-annshevchenkooo-course-1187/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/autumn/course/students/284664-annshevchenkooo-course-1187/-/commits/main)
# lyceum- учебный проект по изучению Django  
## Как запустить проект в dev-режиме:  
#### 0. Склонировать репозиторий  
```git clone https://gitlab.crja72.ru/django/2024/autumn/course/students/284664-annshevchenkooo-course-1187```
#### 1. Перейти в корневую папку проекта  
#### 2. Создать виртуальное окружение:  
Для linux/macOS: ```python3 -m venv venv_name```  
Для Windows: ```py -m venv venv_name```  
venv_name - имя виртуального окружения  
#### 3. Активировать виртуальное окружение:  
Для linux/macOS: ```source venv/bin/activate```  
Для Windows: ```venv\Scripts\activate.bat```  
#### 4. Установить в виртуальном окружении необходимые библиотеки:  
Для всех ОС: ```pip3 install -r requirements/prod.txt```  
Примечание: в директории requirements хранянтся 3 файла с разным набором зависимостей (prod.txt - основные, test.txt - для тестов и dev.txt - для разработки). В данном случае нам нужен prod.txt
#### 5. Находясь в корневой директории (внешняя lyceum), выполнить следующую команду  
Для linux/macOS: ```python manage.py runserver```  
Для Windows: ```py manage.py runserver```  
---
Кем создан: Анна Шевченко 