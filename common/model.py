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

    def to_dict(self):
        return {
            'productId': self.productId,
            'coordinate': self.coordinate
        }


@dataclass
class ShelfProduct:
    rowNumber: 0
    number: 0
    index: 0
    productlist: List[Product]

    def addProduct(self, productId: int, coordinate: str):
        self.productlist.append(Product(productId, coordinate))

    
    def to_dict(self):
        return {
            'rowNumber': self.rowNumber,
            'number': self.number,
            'index': self.index,
            'productlist': [x.to_dict() for x in self.productlist]
        }


@dataclass
class ShelfModel:
    inputId: int
    shelfProductlist: List[ShelfProduct]

    def addShelfProduct(self, shelfProduct: ShelfProduct):
        self.shelfProductlist.append(shelfProduct)

    
    def to_dict(self):
        return {
            'inputId': self.inputId,
            'shelfProductlist': str([x.to_dict() for x in self.shelfProductlist])
        }