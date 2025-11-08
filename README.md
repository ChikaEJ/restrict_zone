# YOLO Intrusion Detection (Test Task)

## Описание
Система детектирует людей с помощью YOLO и отслеживает проникновения в заранее размеченные запрещённые зоны. Зоны рисуются поверх кадра и сохраняются в `restricted_zones.json`.
## Структура файлов и папок
    restrict_zone/
    ├── app/
    │   ├── core/      
    │   ├── detector.py
    │   ├── tracker.py
    │   ├── alarm_manager.py
    │   ├── zone_editor.py
    │   ├── utils.py
    │   └── main.py
    ├── videos/
    ├── output/
    ├── .env
    ├── requirements.txt
    ├── Dockerfile
    └── docker-compose.yml

## Требования
- Python 3.11+
- OpenCV, Ultralytics (YOLOv8), deep-sort-realtime

## Установка и запуск без Docker

1. Открываем терминал MacBook (PowerShell, GitBash для Windows) и переходим в папку где будет ваше приложение.
2. Копируем строку ниже и запускаем ее в терминале(PowerShell, GitBash для Windows).
```bash
git clone git@github.com:ChikaEJ/restrict_zone.git
```
3. Переходим внутрь папки "restrict_zone"
```bash
cd restrict_zone
```
4. Создаем виртуальное окружение venv и активируем.
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
source venv/Scripts/activate #GitBash
```
5. Установка всех зависимостей.
```bash
pip install -r requirements.txt
```
6. Переименуйте файл .env_example в .env
7. Запуск программы
```bash
python -m app.main
```
### Для того что бы поменять запрещенную область перед запуском основной программы (то есть команды "python -m app.main"), запустите следующую команду
```bash
python -m app.zone_editor
```
1. Мышкой установите 4 точки области
2. Нажмите на латинице клавишу "с" для подтверждения выбранной области
3. Нажмите "s" для сохранения координат
4. Нажмите "q" или "ESC" для выхода из окна
5. После сохранения запустите команду
```bash
python -m app.main
```
## Установка и запуск с помощью Docker

1. Выполняем первые 1, 2, 3, 6 шаги как в инструкции без Докера
2. Затем запускаем следующую команду
```bash
docker compose up -d
```
### Если так же хотите поменять запретную область запустите следующую команду.
```bash
docker compose exec yolo-tracker python -m app.zone_editor
```
## Полезные команды
### Остановить контейнер
```
docker compose down
```

### Пересобрать контейнер (если изменился код)
```
docker compose up -d --build
```

### Просмотреть логи
```
docker compose logs -f
```

## Как это работает

#### YOLO детектирует объекты класса person на каждом кадре.
#### DeepSORT присваивает уникальные track_id каждому человеку.
#### Координаты центра объекта проверяются функцией point_in_poly() — находится ли он в одной из запрещённых зон.
#### Если объект находится внутри зоны, активируется сигнал тревоги (ALARM!).
#### Видео с визуальной индикацией сохраняется в /output.

## Лицензия

Проект создан для тестового задания.
Использование YOLOv8 и DeepSORT регулируется их собственными лицензиями:

[Ultralytics YOLO License](https://github.com/ultralytics/ultralytics/blob/main/LICENSE)

[DeepSORT License](https://github.com/nwojke/deep_sort)

## Автор
Эралиев Чингиз