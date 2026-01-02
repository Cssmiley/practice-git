from abc import ABC,abstractmethod
# 二. 行為介面
# 飛行行為介面
class FlyBehavior(ABC):
    @abstractmethod
    def fly(self):
        pass

# 不同行為實作
class FlyWithWings(FlyBehavior):
    def fly(self):
        print("我用翅膀飛")

class FlyNoWay(FlyBehavior):
    def fly(self):
        print("我不會飛")

# 叫聲行為介面
class QuackBehavior(ABC):
    @abstractmethod
    def quack(self):
        pass

# 不同叫聲實作
class Quack(QuackBehavior):
    def quack(self):
        print("呱呱叫")

class MuteQuack(QuackBehavior):
    def quack(self):
        print("不會叫")

class Squeak(QuackBehavior):
    def quack(self):
        print("吱吱叫(橡皮鴨)")


# 三. Duck 類別(重點來了)
# 這裡正是你圖中 performFly()/performQuack() 的核心
class Duck:
    def __init__(self, fly_behavior:FlyBehavior, quack_behavior:QuackBehavior):
        self.fly_behavior = fly_behavior
        self.quack_behavior = quack_behavior

    def performFly(self):
        self.fly_behavior.fly()

    def performQuack(self):
        self.quack_behavior.quack()

    def swim(self):
        print("所有鴨子都會游泳")

    def display(self):
        raise NotImplementedError
    # 重點: 動態設定行為
    def setFlyBehavior(self, fb):
        self.fly_behavior = fb

    def setQuackBehavior(self, qb):
        self.quack_behavior = qb

# 四. 具體的 Duck (組合行為)
# 野生鴨
class MallardDuck(Duck):
    def __init__(self):
        super().__init__(
            fly_behavior=FlyWithWings(),
            quack_behavior=Quack()
        )

    def display(self):
        print("我是野生鴨")

#橡皮鴨
class RubberDuck(Duck):
    def __init__(self):
        super().__init__(
            fly_behavior=FlyNoWay(),
            quack_behavior=Squeak()
        )

    def display(self):
        print("我是橡皮鴨")


# 五.實際執行看看
duck = MallardDuck()
duck.display()
duck.performFly()
duck.performQuack()

print("-----")

rubber_duck = RubberDuck()
rubber_duck.display()
rubber_duck.performFly()
rubber_duck.performQuack()

# 建立新的鴨子:ModelDuck
class ModelDuck(Duck):
    def __init__(self):
        super().__init__(
            fly_behavior=FlyNoWay(), # 一開始不會飛
            quack_behavior=Quack()
        )
    def display(self):
        print("我是模型鴨")

# 實際示範「動態改變行為」（重點來了）
# 一開始的行為
duck = ModelDuck()
duck.display()

duck.performFly()
duck.performQuack()
# 執行期間[更換飛行策略]
print("安裝火箭中...")

duck.setFlyBehavior(FlyWithWings())
duck.performFly()

# 再加一個新 FlyBehavior（完全不動 Duck）
class FlyRocketPowered(FlyBehavior):
    def fly(self):
        print("用火箭飛行")

# 動態套用
duck.setFlyBehavior(FlyRocketPowered())
duck.performFly()