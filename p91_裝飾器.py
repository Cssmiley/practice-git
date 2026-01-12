# 1.Component(抽象元件)
from abc import ABC,abstractmethod

class Beverage(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def cost(self) -> float:
        pass

# 2.ConcreteComponent(被裝飾的核心物件)

class Coffee(Beverage):
    def get_description(self) -> str:
        return "咖啡"
    
    def cost(self) -> float:
        return 50.0
    
# 3.Decorator(抽象裝飾者)
"""
⚠️ 關鍵重點：
👉 裝飾者本身也是一個 Component
👉 而且「裡面包著一個 Component」
"""
class CondimentDecorator(Beverage):
    def __init__(self, beverage: Beverage):
        self._beverage = beverage

# 4.ConcreteDecoratorA:牛奶
class Milk(CondimentDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + " + 牛奶"
    
    def cost(self) -> float:
        return self._beverage.cost() + 10.0
    
# 5.ConcreteDecoratorB: 糖
class Sugar(CondimentDecorator):
    def get_description(self):
        return self._beverage.get_description() + " + 糖"
    
    def cost(self) -> float:
        return self._beverage.cost() + 5.0
    
# 實際使用(重點來了)
if __name__ == "__main__":
    beverage = Coffee()        # 一杯咖啡
    beverage = Milk(beverage)  # 加牛奶
    beverage = Sugar(beverage) # 再加糖

    print(beverage.get_description())
    print(f"總價: {beverage.cost()} 元")
    
