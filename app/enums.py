from enum import Enum

class ProductStatus(Enum):
    ACTIVE = 'active'
    PROGRESS = 'progress'
    OUT_OF_STOCK = 'out_of_stock'

class Category(Enum):
    TERRACOTTA = 'Terracotta'
    BANANA_FIBER = 'Banana_fiber'
    JUTE = 'Jute'
    MACRAME = 'Macrame'
    MOONJ = "Moonj"


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"