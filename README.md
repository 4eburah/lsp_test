# Тестовое задание от Lightspeed

Тестовое задание от Lightspeed

Описание задачи см. тут https://docs.google.com/document/d/14i2F8cCDo53ZiV13ZWq5I7t3MOp-xItesAYAv85RncA/edit

## Краткое описание решения:

Скрипт для пункта 2 запускается так

`python3 cyclones_to_csv.py 201511`

Скрипт для пункта 4 запускается так

`python3 load_cyclone_history.py -file csv_dir/cyclones_20151111.csv`

## Полное описание решения:

### Пререквизиты

Задание выполнялось на Ubuntu 22.04, PostgreSQL 15.1, python3.10.6. В задании использовался оператор SQL Merge, которого нет в версиях PostgreSQL ранее 15.

В файле lsp_dump находится дамп базы Postgre. В нём создается база lspdb, юзер lspuser с паролем lsplsp. В базе lspdb создается таблица cyclones с исходными данными,
и пустые таблицы cyclones_history и cyclones_stage. Cyclones_stage стейджинговая таблица для загрузки одного дня. DDL двух последних таблиц есть в папке ddl.

Перед выполнением нужно установить python библиотеку psycopg2 либо всё окружение из requirements.txt.

В конфиге config/config.json нужно задать параметры соединения к вашему PosgreSQL.


### Запуск загрузки

#### 1. 

Для обоих скриптов загрузки cyclones_to_csv.py, load_cyclone_history.py можно вывести описание их параметров через -h

`python3 cyclones_to_csv.py -h`

#### 2. 

Для выполнения пункта 2 задания и выгрузки месяца данных из таблицы cyclones в csv фалы, нужно выполнить load_cyclone_history.py

`python3 cyclones_to_csv.py -month 201511`

Месяц передается в формате YYYYMM. Подневные файлы складываютя в папку csv_dir

#### 3.

Для выполнения пункта 3 задания, чтобы выгрузить из cyclones в csv данные за три года (2013-2015), нужно  выполнить

```
chmod u+x to_csv.sh
./to_csv.sh
```

#### 4. 

Для загрузки одного дня из csv файла в cyclones_history нужно выполнить

`python3 load_cyclone_history.py -file csv_dir/cyclones_20151111.csv`

Скрипт по загурзке при этом выполняет следующие шаги.
* Загружает данные из файла в промежуточную таблицу cyclones_stage
* Мержит данные из cyclones_stage в cyclones_history при помощи скрипта slq/merge_to_cyclones_history.sql
* В скрипте merge_to_cyclones_history.sql помимо мержа предварительно делаются delete+update на случай повторной загрузки последнего дня.  
При этом при загрузках новых дней эти операции не выполняются, так как не выполняется условие where.

#### 5. 

Для загрузки всей истории файлов из csv_dir полученных в пункте 3 нужно выполнить sh скрипт

```
chmod u+x csvs_to_db.sh
./csvs_to_db.sh
```

