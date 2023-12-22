# ngenix-test-assignment

Сздадим и активируем виртуальное окружение
```
$ python -m venv venv/
$ source venv/bin/activate
```

Установим приложение вместе с зависимостями из `pyproject.toml`
```
$ pip install .
```

Создадим архивы со сгенерированными xml-файлами в директории `archives/`
```
$ typer zipxml.cli run archive archives/
```

Запустим скрипт парсинга данных из полученной директории, запишем результат в `stats/`
```
$ typer zipxml.cli run parse archives/ stats/
```
