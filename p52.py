from abc import ABC, abstractmethod

# Observer 介面
class Observer(ABC):
    @abstractmethod
    def update(self, state):
        pass

# Subject 介面
class Subject(ABC):
    @abstractmethod
    def registerObserver(self, observer: Observer):
        pass

    @abstractmethod
    def removeObserver(self, observer: Observer):
        pass

    @abstractmethod
    def notifyObservers(self):
        pass

# ConcreteSubject (真正的[狀態來源])
class TemperatureSensor(Subject):
    def __init__(self):
        self._observers = []
        self._temperature =None

    def registerObserver(self, observer:Observer):
        self._observers.append(observer)

    def removeObserver(self, observer):
        self._observers.remove(observer)

    def notifyObservers(self):
        for observer in self._observers:
            observer.update(self._temperature)

    # 狀態改變點
    def setTemperature(self, value):
        print(f"[Sensor] 溫度更新為 {value}")
        self._temperature = value
        self.notifyObservers()


# ConcreteObserver (實際訂閱的人)
class DisplayPanel(Observer):
    def update(self, state):
        print(f"[顯示面板] 目前溫度: {state}°C")

class AlarmSystem(Observer):
    def update(self, state):
        if state > 80:
            print("[警報系統] 溫度過高!")


# 實際執行(驗收)
sensor = TemperatureSensor()

display = DisplayPanel()
alarm = AlarmSystem()

sensor.registerObserver(display)
sensor.registerObserver(alarm)

sensor.setTemperature(60)
print("-----")
sensor.setTemperature(90)