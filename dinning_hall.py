import threading
import random
import time
import requests

class Dinning_Hall:
    def __init__(self, tables, n_waiters):
        self.tables = tables
        self.n_waiters = n_waiters
        self.order_id = 0
        self.tables_lock = threading.Lock()

    def generate_order(self, waiter_id, table_id):
        n_items = random.randint(1,3)
        items = [random.randint(1,13) for _ in range(n_items)]
        priority = random.randint(1,5)
        time_stamp = time.time()
        order = {
            "order_id":self.order_id, 
            "table_id": table_id,
            "waiter_id": waiter_id,
            "items": items,
            "priority": priority,
            "pick_up_time": time_stamp
            }
        self.order_id += 1
        return order

    def free_table(self, table_id):
        self.tables_lock.acquire()
        self.tables[table_id]["status"] = True
        self.tables_lock.release()

    
    def Waiter_working(self, waiter_id):
        while True:
            self.tables_lock.acquire()
            free_tables = any([table["status"] for table in self.tables])
            if free_tables:
                for i in range(len(self.tables)):
                    if self.tables[i]["status"]:
                        chosen_table_id = i
                        self.tables[i]["status"] = False
                        break
            else:
                self.tables_lock.release()
                continue

            self.tables_lock.release()
            order = self.generate_order(waiter_id, chosen_table_id)
            print(order)
            requests.post("http://127.0.0.1:4000/order",json = order)
            time.sleep(2)
    

    def Run_restaurant(self):
        for i in range(self.n_waiters):
            waiter = threading.Thread(target = self.Waiter_working, args = (i,))
            time.sleep(1)
            waiter.start()






