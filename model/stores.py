from dataclasses import dataclass



@dataclass
class Store:
    store_id:int #key
    store_name:str
    phone:str
    email:str
    street:str
    city:str
    state:str
    zip_code:int

    def __hash__(self):
        return self.store_id

    def __str__(self):
        return f"{self.store_name}"

    def __eq__(self, other):
        return self.store_id == other.store_id