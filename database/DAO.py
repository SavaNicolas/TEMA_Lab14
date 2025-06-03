from database.DB_connect import DBConnect
from model.arco import Arco
from model.orders import Order
from model.stores import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
         FROM stores"""
        cursor.execute(query)

        for row in cursor:
            result.append(Store(**row))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(storeid):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
select o.*
from orders o, stores s
where o.store_id = s.store_id
and o.store_id = %s

    """
        cursor.execute(query, (storeid,))

        for row in cursor:
            result.append(Order(**row))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result  # lista di ordini dello store indicato

    @staticmethod
    def getEdges(k,storeid, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select o.order_id as nodo1 ,o2.order_id as nodo2,oi1.quantity+oi2.quantity as peso 
from orders o, orders o2, order_items oi1, order_items oi2  
where o.store_id = o2.store_id 
and o.store_id = %s
and o.order_id = oi1.order_id 
and o2.order_id =oi2.order_id 
and DATEDIFF(o2.order_date,o.order_date)< %s
and DATEDIFF(o2.order_date,o.order_date)> 0
and o.order_id <> o2.order_id
group by o.order_id, o2.order_id
"""
        cursor.execute(query, (storeid, k))

        for row in cursor:
            result.append(Arco(idMap[row["nodo1"]], idMap[row["nodo2"]], row["peso"]))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result  # lista di archi(nodo1,nodo2)
