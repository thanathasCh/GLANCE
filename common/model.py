from typing import List, Dict
from dataclasses import dataclass


@dataclass
class VideoResponse:
    inputId: int
    videoUrl: str
    scanSpeed: float
    scanDate: str


@dataclass
class Product:
    productId: int
    coordinate: str


@dataclass
class ShelfProduct:
    shelfImagePath: str
    rowNumber: 0
    number: 0
    productlist: List[Product]

    def addProduct(self, productId: int, coordinate: str):
        self.productlist.append(Product(productId, coordinate))


@dataclass
class ShelfModel:
    inputId: int
    shelfProductlist: List[ShelfProduct]

    def addShelfProduct(self, shelfProduct: ShelfProduct):
        self.shelfProductlist.append(shelfProduct)


def class2dict(instance, built_dict={}):
    if not hasattr(instance, "__dict__"):
        return instance
    new_subdic = vars(instance)
    for key, value in new_subdic.items():
        new_subdic[key] = class2dict(value)
    return new_subdic