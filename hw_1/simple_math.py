class SimpleMath:
    """ Класс с простыми математическими операциями."""
    def square(self,x):
        """Возвращает квадрат числа."""
        return x * x
    def cube(self,x):
        """Возвращает куб числа"""
        return x * x * x

class SimpleMath:
    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b