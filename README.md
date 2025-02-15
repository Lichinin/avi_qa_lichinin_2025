**Тестовое задание для стажёра QA-направления (зимняя волна 2025)**

Автор: Виталий Личинин

В проекте реализована автоматизация API и UI тесткейсов.

Имеется возможность запуска тестов локально и на удаленном сервере(Selenoid).

Имеется возможность запуска тестов в несколько потоков.

**Оглавление**
- [Цели](#цели)
- [Используемые библиотеки](#используемые-библиотеки)
- [Структура проекта](#структура-проекта)
- [Задание 1](#задание-1)
- [Задание 2.1](#задание-21)
- [Задание 2.2](#задание-22)
- [Запуск проекта](#запуск-проекта)
- [Результаты выполнения тестов](#результаты-выполнения-тестов)
- [Примеры отчетности Allure](#примеры-отчетности-allure)


***
### Цели.
- Поиск и приоритезация багов
- Создание и автоматизация UI-тестов веб-ресурса 
- Создание и автоматизация API-тестов
- Построение отчетности через Allure
- Внедрение логирования для критически важного функционала
***

### Используемые библиотеки.
allure-pytest==2.13.5

Cerberus==1.3.7

pytest==8.3.4

pytest-xdist==3.6.1

requests==2.32.3

selenium==4.28.1

***
### Структура проекта.
```
avi_qa_lichinin_2025                                               
├─ allure-report                                                   
├─ allure-results                                                  
├─ api_client                                                      
│  └─ api_client.py                                                
├─ constants                                                       
│  └─ constants.py                                                 
├─ locators                                                        
│  └─ locators.py                                                  
├─ log                                                             
├─ pages                                                           
│  ├─ base_page.py                                                 
│  ├─ details_page.py                                              
│  └─ products_page.py                                             
├─ schemas                                                         
│  └─ schemas.py                                                   
├─ tests                                                           
│  ├─ test_api                                                     
│  │  └─ test_api.py                                               
│  └─ test_ui                                                      
│     ├─ test_create_product.py                                    
│     ├─ test_edit_product.py                                      
│     └─ test_find_product.py                                      
├─ BUGS.md                                                         
├─ conftest.py                                                     
├─ pytest.ini                                                      
├─ README.md                                                       
├─ requirements.txt                                                
└─ TESTCASES.md                                                               
```
* Папка **/allure-report**: Сгенерированный Allure-отчет.

* Папка **/allure-results**: Файлы для генерации Allure-отчета.

* Папка **/api_client**:
  * **api_client.py**: Файл, в котором реализованы методы для выполнения запросов к API

* Папка **/constants**:
  * **constants.py**: Содержит класс с константами.

* Папка **/locators**:
  * **locators.py**: Содержит класс с локаторами.

* Папка **/log**: Логи работы.

* Папка **/pages**:
    * **base_page.py**: Базовый класс PageObject , содержащий общие методы и свойства для всех страниц.
    * **details_page.py**: Класс PageObject для взаимодействия со страницей детализации объявления.
    * **products_page.py**: Класс PageObject для взаимодействия со страницей объявленияс перечнем объявлений.

* Папка **/schemas**:
  * **schemas.py**: Содержит класс с схемами для валидации ответов API-тестов.

* Папка **/tests**:
    * Папка **/test_api**:
        * **test_api.py**: Автотесты API.
    * Папка **/test_ui**:
        * **test_create_product.py**: Автотесты UI создания объявления.
        * **test_edit_product.py**: Автотесты UI редактирования объявления.
        * **test_find_product.py**: Автотесты UI поиска объявления.

* **BUGS.md**: Файл с баг-репортами.

* **conftest.py**: Файл с общими фикстурами для тестов, включая настройку браузера, логгера, тестовых данных и другой общей функциональности.

    Содержит следующие настройки и фикстуры:
    - **pytest_addoption**: Добавляет команды для запуска тестов с различными параметрами, такими как выбор браузера, URL-адрес, уровень логирования, исполнитель (Selenoid) и версия браузера.
    - **logger**: Настраивает логгер RotatingFileHandler для записи информации о ходе выполнения тестов в файл. Создает файл логов с ограничением размера и количества бэкапов. Уровень логирования задается параметром --log_level.
    - **browser**: Настраивает и запускает веб-драйвер для выбранного браузера (Chrome, Firefox или Edge) в зависимости от параметров запуска. Поддерживает запуск тестов локально или в Selenoid.
    - **open_start_page**: Фикстура готовит объект browser с главной страницей проекта.
    - **open_product_details_page**: Фикстура готовит объект browser с страницей детальной информации о продукте.
    - **create_test_product**: Setup-фикстура, создает объявление для теста.

* **pytest.ini**: Файл конфигурации для pytest, содержащий настройки для запуска тестов.
* **README.md**: Файл с описанием проекта, инструкциями по установке и запуску тестов.
* **requirements.txt**: Файл, содержащий список зависимостей проекта, необходимых для его работы.
* **TESTCASES.md**: Файл, содержащий список тесткейсов проекта.

***
### Задание 1.
Баги, найденные на тестовой странице:
| Приоритет | Описание                                                                                   | Актуальное поведение                                                                                     | Ожидаемое поведение                                                                 |
|-----------|--------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| High      | Стоит фильтр "Москва", но среди объявлений есть объявление из Липецка.                      | В списке объявлений присутствует объявление из Липецка.                                                  | Все объявления должны соответствовать выбранному региону (Москва).                  |
| High      | Навигация по страницам показывает неверное количество страниц.                             | Пагинация показывает 100 страниц, что соответствует от 1189 до 1200 объявлений при найденных 61 объявлении. | Пагинация должна показывать корректное количество страниц (6 для 61 объявления).    |
| High      | Не работает сортировка товаров по цене "Дороже".                                             | Сортировка не применяется, объявления не отсортированы по убыванию цены.                                       | Объявления должны быть отсортированы по убыванию цены.                              |
| Medium    | Выбран режим отображения "показать на карте", но объявления отображаются плитками.         | Объявления отображаются в виде плиток.                                                                  | Объявления должны отображаться на карте.                                           |
| Medium    | На странице отображается текст ошибки "Попробуйте обновить страницу или загляните позже - мы обязательно всё починим", хотя сервис доступен.                                | Текст ошибки отображается, хотя сервис доступен.                                              | Если сервис доступен, текст ошибки не должен отображаться.                           |
| Low       | Опечатка в кнопке "Все категории" — написано "Все категори".                                | На кнопке написано "Все категори".                                                                       | На кнопке должно быть написано "Все категории".                                     |

***
### Задание 2.1.
Тесткейсы по заданию находятся в файле [TESTCASES.md](./TESTCASES.md)

* Реализованы API-тесты:
    * **test_getting_product.py**: Тест проверяет получение объявления по его идентификатору.
    * **test_getting_product_stat.py**: Тест проверяет получение статистики объявления по его идентификатору.
    * **test_getting_products_by_seller_id.py**: Тест проверяет получение всех объявлений продавца по его sellerID.
    * **test_create_product.py**: Тест проверяет создание нового объявления.
***

### Задание 2.2.
Тесткейсы по заданию находятся в файле [TESTCASES.md](./TESTCASES.md)

* Реализованы UI-тесты:
    * **test_button_create.py**: Тест проверяет работоспособность кнопки "Создать".
    * **test_create_product.py**: Тест проверяет создание нового объявления.
    * **test_edited_product.py**: Тест проверяет редактирование существующего объявления.
    * **test_find_product.py**: Тест проверяет поиск по объявлениям.


### Запуск проекта.
1. Скачать репозиторий.
    ```
    git clone https://github.com/Lichinin/avi_qa_lichinin_2025.git
    ```
2. Установите виртуальное окружение:
    ```
    python -m venv venv
    ```
3. Активируйте виртуальное окружение:
    ```
    source venv/script/activate
    ```
4. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```
5. Запустить pytest:
    Существует два варианта запуска тестов: локально и на удаленной машине в docker-контейнерах(Selenoid) 
    Для запуска pytest можно использовать следующие флаги (все они не обязательны):
    * --browser: Выбор браузера для тестов(chrome, firefox, edge)
    * --url: Адрес тестируемого ресурса
    * --browser_version: Версия браузера
    * --log_level: Выбор уровня записи информации в log-файлы
    * --executor: Адрес сервера для удаленного выполнения тестов
    * --alluredir=allure-results: Для сохранения папки с отчетностью allure в корень директории проекта
    * -n 2: Количество одновременно запускаемых тестов (в данном примере 2)

    __Пример запуска тестов на локальной машине:__
    ```
    pytest -n 1 -vv --alluredir=allure-results  --browser='chrome' --browser_version='100'
    ```
    Расшифровка параметров:
    n 1: запуск тестов в один поток
    -vv: выполнение информация о тестах
    --alluredir=allure-results: сохранение информации для Allure-отчета в папку allure-results
    --browser='chrome': запуск тестов в браузере Chrome
    --browser_version='100': версия браузера=100

    __Пример запуска тестов на удаленной машине (Selenoid):__
    ```
    pytest -n 2 -vv --alluredir=allure-results --executor=127.0.0.1 --browser='chrome' --browser_version='100'
    ```
    Расшифровка параметров:
    n 2: выполнение тестов в два потока
    -vv: расширенная информация о тестах
    --alluredir=allure-results: сохранение информации для Allure-отчета в папку allure-results
    --executor=127.0.0.1: адрес сервера, на котором будут выполняться тесты
    --browser='chrome': запуск тестов в браузере Chrome
    --browser_version='100': версия браузера=100


### Результат выполнения тестов.
* __Запуск тестов без параметров:__
pytest . -vv
```
(venv) 
Lichi@DESKTOP-62CVRKQ MINGW64 /e/Dev/avi_qa_lichinin_2025 (main)
$ pytest . -vv
========================================================================================== test session starts ==========================================================================================
platform win32 -- Python 3.10.6, pytest-8.3.4, pluggy-1.5.0 -- E:\Dev\avi_qa_lichinin_2025\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: E:\Dev\avi_qa_lichinin_2025
configfile: pytest.ini
plugins: allure-pytest-2.13.5, xdist-3.6.1
collected 8 items

tests/test_api/test_api.py::test_getting_product PASSED                                                                                                                                            [ 12%]
tests/test_api/test_api.py::test_getting_product_stat PASSED                                                                                                                                       [ 25%]
tests/test_api/test_api.py::test_getting_products_by_seller_id PASSED                                                                                                                              [ 37%]
tests/test_api/test_api.py::test_create_product PASSED                                                                                                                                             [ 50%]
tests/test_ui/test_create_product.py::test_button_create PASSED                                                                                                                                    [ 62%]
tests/test_ui/test_create_product.py::test_create_product PASSED                                                                                                                                   [ 75%]
tests/test_ui/test_edit_product.py::test_edited_product PASSED                                                                                                                                     [ 87%]
tests/test_ui/test_find_product.py::test_find_product PASSED                                                                                                                                       [100%]

===================================================================================== 8 passed in 97.65s (0:01:37) ======================================================================================
```

* __Запуск тестов с параметрами:__
pytest . -n 1 -vv --alluredir=allure-results --executor=127.0.0.1 --browser='firefox' --browser_version='125'
```
(venv) 
Lichi@DESKTOP-62CVRKQ MINGW64 /e/Dev/avi_qa_lichinin_2025 (main)
$ pytest . -n 1 -vv --alluredir=allure-results --executor=127.0.0.1 --browser='firefox' --browser_version='125'
========================================================================================== test session starts ==========================================================================================
platform win32 -- Python 3.10.6, pytest-8.3.4, pluggy-1.5.0 -- E:\Dev\avi_qa_lichinin_2025\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: E:\Dev\avi_qa_lichinin_2025
configfile: pytest.ini
plugins: allure-pytest-2.13.5, xdist-3.6.1
1 worker [8 items]     
scheduling tests via LoadScheduling

tests/test_api/test_api.py::test_getting_product 
[gw0] [ 12%] PASSED tests/test_api/test_api.py::test_getting_product 
tests/test_api/test_api.py::test_getting_product_stat
[gw0] [ 25%] PASSED tests/test_api/test_api.py::test_getting_product_stat 
tests/test_api/test_api.py::test_getting_products_by_seller_id
[gw0] [ 37%] PASSED tests/test_api/test_api.py::test_getting_products_by_seller_id 
tests/test_api/test_api.py::test_create_product
[gw0] [ 50%] PASSED tests/test_api/test_api.py::test_create_product 
tests/test_ui/test_create_product.py::test_button_create
[gw0] [ 62%] PASSED tests/test_ui/test_create_product.py::test_button_create 
tests/test_ui/test_create_product.py::test_create_product 
[gw0] [ 75%] PASSED tests/test_ui/test_create_product.py::test_create_product 
tests/test_ui/test_edit_product.py::test_edited_product 
[gw0] [ 87%] PASSED tests/test_ui/test_edit_product.py::test_edited_product 
tests/test_ui/test_find_product.py::test_find_product 
[gw0] [100%] PASSED tests/test_ui/test_find_product.py::test_find_product 

================================================================ 8 passed in 114.32s (0:01:54) ================================================================
```

### Примеры отчетности Allure.
* Summary по тестам:
![общий](https://github.com/user-attachments/assets/6c6e2de1-2c01-4cd2-9ef0-275304b3a1aa)

* Тесткейсы:
![suites](https://github.com/user-attachments/assets/6644d5e4-d4a1-420d-9d74-d7415bd0d7f4)

* Пример отчета по тесткейсу:
![Пример теста](https://github.com/user-attachments/assets/23cc3936-61d9-43c0-b33b-536ebb7f2d81)

