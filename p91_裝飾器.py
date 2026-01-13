# 1.Component(抽象元件)
from abc import ABC,abstractmethod
from enum import Enum

# 正確解法: size 交給 Component, 配料交給 Decorator
# 杯型列舉
class Size(Enum):
    SMALL = "小杯"
    MEDIUM = "中杯"
    LARGE = "大杯"

# 先定義加料核心表
class AddonType(Enum):
    SOY = "豆漿"
    MILK = "牛奶"
    SUGAR = "糖"

# 加料價格資料(只改這裡就好)
ADDON_PRICE_TABLE = {
    AddonType.SOY:{
        Size.SMALL:15,
        Size.MEDIUM: 20,
        Size.LARGE: 25,
    },
    AddonType.MILK:{
        Size.SMALL: 8,
        Size.MEDIUM: 10,
        Size.LARGE: 12,
    },
    AddonType.SUGAR:{
        Size.SMALL: 3,
        Size.MEDIUM: 5,
        Size.LARGE:7,
    }
}

class Beverage(ABC):
    def __init__(self, size: Size):
        self._size = size
    
    def get_size(self) -> Size:
        return self._size
    
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
        return f"{self._size.value} 咖啡"
    
    def cost(self) -> float:
        base_price = {
            Size.SMALL:50,
            Size.MEDIUM: 60,
            Size.LARGE:70
        }
        return base_price[self._size]
    
# 3.Decorator(抽象裝飾者)
"""
⚠️ 關鍵重點：
👉 裝飾者本身也是一個 Component
👉 而且「裡面包著一個 Component」
"""
class CondimentDecorator(Beverage):
    def __init__(self, beverage: Beverage):
        self._beverage = beverage
        super().__init__(beverage.get_size())

# 通用 Decorator:Addon(只此一個)
class Addon(CondimentDecorator):
    def __init__(self, beverage: Beverage, addon_type:AddonType):
        super().__init__(beverage)
        self._addon_type = addon_type

    def get_description(self) -> str:
        return (
            self._beverage.get_description()
            + " + "
            + self._addon_type.value
        )
    def cost(self) -> float:
        addon_price = ADDON_PRICE_TABLE[self._addon_type][self.get_size()]
        return self._beverage.cost() + addon_price
    

# 實際使用(重點來了)
if __name__ == "__main__":
    beverage = Coffee(Size.MEDIUM)  # 中杯咖啡
    beverage = Addon(beverage, AddonType.MILK)    # 加牛奶
    beverage = Addon(beverage, AddonType.SUGAR)      # 再加糖
    beverage = Addon(beverage, AddonType.SOY)    # 加豆漿
    print(beverage.get_description())
    print(f"總價: {beverage.cost()} 元")
    
