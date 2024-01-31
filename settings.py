# Перемешать аккаунты
SHUFFLE_WALLET: bool = False

# Множитель газа для транзакций
GAS_MULTIPLIER: float = 1.069

# Количество секунд между транзакциями
SLEEP_BETWEEN_TXS: tuple[int, int] = (5, 10)

# Количество секунд между аккаунтами
SLEEP_BETWEEN_ACCS: tuple[int, int] = (20, 40)

# Количество попыток перевода
RETRY_COUNT: int = 1


# Использовать предустановленные настройки
USE_PRESET: bool = False

# [source_chain, dest_chain, min_amount_to_recieve, max_amount_to_recieve, min_tx_count, max_tx_count]
PRESET: list = ['Klaytn', 'Fuse', 0.00001, 0.0005, 1, 1] 
# -----------------Доступные маршруты-----------------
# Polygon -> Celo, Gnosis, Core, Harmony, Klaytn, Moonbeam, Moonriver, DFK, Fuse
# Celo -> Polygon, Gnosis, Fuse, Moonbeam
# Gnosis -> Polygon, Celo, Klaytn, Moonbeam, Fuse
# Core -> Polygon
# Harmony -> Polygon, Moonbeam, DFK
# Klaytn -> Polygon, Celo, Gnosis, Moonbeam, DFK, Fuse
# Moonbeam -> Polygon, Celo, Gnosis, Harmony, Klaytn, DFK
# Moonriver -> Polygon
# DFK -> Polygon, Harmony, Klaytn, Moonbeam
# Fuse -> Polygon, Celo, Gnosis, Klaytn
# ---------------------------------------------------