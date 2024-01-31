# Merkly
Софт на прогон дешёвых сетей L0 через Меркли

<img src="https://i.postimg.cc/L510rX6m/image.png" /> 

# Доступные маршруты
* Polygon -> Celo, Gnosis, Core, Harmony, Klaytn, Moonbeam, Moonriver, DFK, Fuse
* Celo -> Polygon, Gnosis, Fuse, Moonbeam
* Gnosis -> Polygon, Celo, Klaytn, Moonbeam, Fuse
* Core -> Polygon
* Harmony -> Polygon, Moonbeam, DFK
* Klaytn -> Polygon, Celo, Gnosis, Moonbeam, DFK, Fuse
* Moonbeam -> Polygon, Celo, Gnosis, Harmony, Klaytn, DFK
* Moonriver -> Polygon
* DFK -> Polygon, Harmony, Klaytn, Moonbeam
* Fuse -> Polygon, Celo, Gnosis, Klaytn

# Настройка
* В файл `data/accounts.txt` вписываем приватные ключи с новой строки
* В файле `settings.py` выставляем настройки(каждый пункт подписан)
  
# Установка:
#### *Чтобы отображались эмодзи и всё отображалось корректно лучше использовать VS Code или Windows Terminal*
Открываем cmd и прописываем:
1. `cd путь/к/проекту`
3. `python -m venv venv`
4. `venv\Scripts\activate`
5. `pip install -r requirements.txt`

# Запуск:
```
python main.py
```
