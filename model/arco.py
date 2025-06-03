from dataclasses import dataclass

from model.orders import Order


@dataclass
class Arco:
    nodo1:Order
    nodo2:Order
    peso: int