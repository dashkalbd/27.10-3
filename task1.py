# Point 1: product with name, price and quantity
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        # these go through the setters below (point 2 check)
        self.price = price
        self.quantity = quantity

    # Point 2: price can't be negative
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною")
        self._price = value

    # Point 2: quantity can't be negative
    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("Кількість не може бути від'ємною")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.price} грн x {self.quantity} шт"


# Point 3: order stores a list of products
class Order:
    def __init__(self):
        self.products = []

    # Point 4: add a product to the order
    def add_product(self, product):
        self.products.append(product)

    # Point 4: total price of the whole order
    @property
    def total_price(self):
        total = 0
        for product in self.products:
            total = total + product.price * product.quantity
        return total

    # Point 5: order1 + order2 -> new order with products of both
    def __add__(self, other):
        new_order = Order()
        new_order.products = self.products + other.products
        return new_order

    # Point 6: len(order) -> number of positions
    def __len__(self):
        return len(self.products)

    # Point 7: order[0] -> product by index
    def __getitem__(self, index):
        return self.products[index]

    def __str__(self):
        lines = [str(product) for product in self.products]
        return "\n".join(lines) + f"\nРазом: {self.total_price} грн"


# Point 8: functor that calculates the discount
class DiscountCalculator:
    def __init__(self, percent, min_sum):
        self.percent = percent
        self.min_sum = min_sum

    def __call__(self, order_or_sum):
        # accepts an Order or just a number
        if isinstance(order_or_sum, Order):
            total = order_or_sum.total_price
        else:
            total = order_or_sum

        # rule: discount only if the sum is big enough
        if total >= self.min_sum:
            return total * self.percent / 100
        return 0


# Test point 2: negative values are not allowed
try:
    bad = Product("Помилка", -100, 1)
except ValueError as error:
    print("Помилка:", error)

# Test points 3-4: two orders
order1 = Order()
order1.add_product(Product("Ноутбук", 30000, 1))
order1.add_product(Product("Мишка", 500, 2))

order2 = Order()
order2.add_product(Product("Навушники", 2000, 1))

print()
print("Замовлення 1:")
print(order1)

print()
print("Замовлення 2:")
print(order2)

# Test point 5: merge orders
order3 = order1 + order2
print()
print("Об'єднане замовлення:")
print(order3)

# Test point 6: number of positions
print()
print("Позицій у замовленні 3:", len(order3))

# Test point 7: product by index
print("Перший товар:", order3[0])
print("Останній товар:", order3[2])

# Test point 8: discount from an order and from a number
discount = DiscountCalculator(10, 5000)
print()
print("Знижка на замовлення 3:", discount(order3), "грн")
print("Знижка на замовлення 2:", discount(order2), "грн")
print("Знижка на суму 8000:", discount(8000), "грн")