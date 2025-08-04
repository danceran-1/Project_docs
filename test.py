import psycopg2
from psycopg2 import sql

class ProductManager:
    def __init__(self, dbname, user, password, host='localhost'):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def add_test_products(self):
        products = [
            ('Laptop', 999.99, 15),
            ('Phone', 699.99, 5),
            ('Tablet', 349.99, 8),
            ('Monitor', 249.99, 12),
            ('Keyboard', 49.99, 20),
            ('Mouse', 29.99, 3),
            ('Headphones', 99.99, 7),
            ('Printer', 199.99, 4),
            ('Router', 79.99, 9),
            ('SSD', 129.99, 11)
        ]
        self.cursor.executemany(
            "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
            products
        )
        self.conn.commit()

    def get_low_stock_products(self):
        self.cursor.execute("SELECT * FROM products WHERE quantity < 10")
        return self.cursor.fetchall()

    def update_price_by_name(self, product_name, new_price):
        self.cursor.execute(
            "UPDATE products SET price = %s WHERE name = %s",
            (new_price, product_name)
        )
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    manager = ProductManager('mydatabase', 'postgres', '123')
    manager.add_test_products()
    
    for product in manager.get_low_stock_products():
        print(product)
    
    manager.update_price_by_name('Phone', 749.99)
    manager.close()