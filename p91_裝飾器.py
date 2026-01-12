# 1.Component(抽象元件)
from abc import ABC,abstractmethod
from enum import Enum

# 正確解法: size 交給 Component, 配料交給 Decorator
# 杯型列舉
class Size(Enum):
    SMALL = "小杯"
    MEDIUM = "中杯"
    LARGE = "大杯"

class Beverage(ABC):
    def __init__(self, size: Size):
        self.size = size
    
    def get_size(self) -> Size:
        return self.size
    
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def cost(self) -> float:
        pass

# 2.ConcreteComponent(被裝飾的核心物件)

class Coffee(Beverage):
    def __init__(self, size: Size):
        super().__init__(size)

    def get_description(self) -> str:
        return f"{self.size.value} 咖啡"
    
    def cost(self) -> float:
        base_price = {
            Size.SMALL:50,
            Size.MEDIUM: 60,
            Size.LARGE:70
        }
        return base_price[self.size]
    
# 3.Decorator(抽象裝飾者)
"""
⚠️ 關鍵重點：
👉 裝飾者本身也是一個 Component
👉 而且「裡面包著一個 Component」
"""
class CondimentDecorator(Beverage):
    def __init__(self, beverage: Beverage):
        self._beverage = beverage

    def get_size(self) -> Size:
        return self._beverage.get_size()
    
# 4.ConcreteDecoratorA:牛奶
class Milk(CondimentDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + " + 牛奶"
    
    def cost(self) -> float:
        milk_price = {
            Size.SMALL: 10,
            Size.MEDIUM: 15,
            Size.LARGE: 20
        }
        return self._beverage.cost() + milk_price[self.get_size()]
    
# 5.ConcreteDecoratorB: 糖
class Sugar(CondimentDecorator):
    def get_description(self):
        return self._beverage.get_description() + " + 糖"
    
    def cost(self) -> float:
        return self._beverage.cost() + 5.0
    
# 實際使用(重點來了)
if __name__ == "__main__":
    beverage = Coffee(Size.MEDIUM)  # 中杯咖啡
    beverage = Milk(beverage)       # 加牛奶
    beverage = Sugar(beverage)      # 再加糖

    print(beverage.get_description())
    print(f"總價: {beverage.cost()} 元")
    
