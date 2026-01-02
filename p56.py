from abc import ABC, abstractmethod

# Observer 介面(只管 update)
class Observer(ABC):
    @abstractmethod
    def update(self, temperature, humidity, pressure):
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

# DisplayElement 介面(只管顯示)
class DisplayElement(ABC):
    @abstractmethod
    def display(self):
        pass

# 「狀態用 Observer，高溫警告用 Event」
# 新增 Event 和 EventBus(完全不影響原本的 Observer)
from dataclasses import dataclass

@dataclass
class HighTemperatureEvent:
    temperature:float

class EventBus:
    def __init__(self):
        self._subscribers = []

    def subscribe(self, handler):
        self._subscribers.append(handler)

    def publish(self, event):
        for handler in self._subscribers:
            handler(event)

# ConcreteSubject:WeatherData
from typing import Optional
class WeatherData(Subject):
    def __init__(self, event_bus: Optional[EventBus] = None):
        self._observers = []
        self._temperature = 0
        self._humidity = 0
        self._pressure = 0

        # 新增:EventBus + 狀態旗標
        self._event_bus = event_bus
        self._high_temp_sent = False

    def registerObserver(self, observer:Observer):
        self._observers.append(observer)

    def removeObserver(self, observer):
        self._observers.remove(observer)

    def notifyObservers(self):
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._pressure)

    # 狀態改變點
    def setMeasurements(self, temperature, humidity, pressure):
        self._temperature = temperature
        self._humidity= humidity
        self._pressure = pressure
        # 1.狀態同步
        self.notifyObservers()

        #2.高溫警告
        if self._event_bus: # 保護層, EventBus 可為 None
            if temperature >= 35 and not self._high_temp_sent:
                self._event_bus.publish(HighTemperatureEvent(temperature))
                self._high_temp_sent = True

            if temperature < 35:
                self._high_temp_sent = False


# Concrete Observers(同時也是 Display)
# CurrentConditionsDisplay
class CurrentConditionsDisplay(Observer, DisplayElement):
    def __init__(self, weatherData: Subject):
        self._temperature = 0
        self._humidity = 0
        weatherData.registerObserver(self)

    def update(self, temperature, humidity, pressure):
        self._temperature = temperature
        self._humidity = humidity
        self.display()

    def display(self):
        print(f"[目前狀況] 溫度={self._temperature}, 濕度={self._humidity}")

# StatisticsDisplay
class StatisticsDisplay(Observer, DisplayElement):
    def __init__(self, weatherData: Subject):
        self._temperatures = []
        weatherData.registerObserver(self)

    def update(self, temperature, humidity, pressure):
        self._temperatures.append(temperature)
        self.display()

    def display(self):
        avg = sum(self._temperatures)/ len(self._temperatures)
        print(f"[統計] 平均溫度={avg:.1f}")

# ForecastDisplay
class ForecastDisplay(Observer, DisplayElement):
    def __init__(self, weatherData: Subject):
        self._pressure = 0
        weatherData.registerObserver(self)

    def update(self, temperature, humidity, pressure):
        self._pressure = pressure
        self.display()

    def display(self):
        print(f"[預報] 氣壓={self._pressure} -> 天氣變化中")

# 實際執行

weatherData = WeatherData()

current = CurrentConditionsDisplay(weatherData)
stats = StatisticsDisplay(weatherData)
forecast = ForecastDisplay(weatherData)

weatherData.setMeasurements(25, 65, 1013)
weatherData.setMeasurements(28, 70, 1009)

# 新增的觀察者：HeatIndexDisplay
class HeatIndexDisplay(Observer, DisplayElement):
    def __init__(self, weatherData: Subject):
        self._heatIndex = 0.0
        weatherData.registerObserver(self)

    def update(self, temperature, humidity, pressure):
        # 呼叫計算體感溫度的邏輯
        self._heatIndex = self._compute_heat_index(temperature, humidity)
        self.display()

    def _compute_heat_index(self, t, rh):
        """
        這是一個簡化版的酷熱指數公式 (攝氏)
        """
        index = (float)((16.923 + (0.185212 * t) + (5.37941 * rh) - (0.100254 * t * rh) +
                (0.00941695 * (t**2)) + (0.00728898 * (rh**2)) +
                (0.000345372 * (t**2 * rh)) - (0.000814971 * (t * rh**2)) +
                (0.0000102102 * (t**2 * rh**2)) - (0.000038646 * (t**3)) + (0.0000291583 * (rh**3)) + (0.00000142721 * (t**3 * rh)) +
                (0.000000197483 * (t * rh**3)) - (0.0000000218429 * (t**3 * rh**2)) +
                0.000000000843296 * (t**2 * rh**3)) -
                (0.0000000000481975 * (t**3 * rh**3)))
        return index

    def display(self):
        print(f"[體感溫度] 酷熱指數為 {self._heatIndex:.2f} °C")

# --- 執行部分 ---
weatherData = WeatherData()

# 註冊原本的顯示器
current_display = CurrentConditionsDisplay(weatherData)
# 🔴 註冊新的體感溫度顯示器
heat_index_display = HeatIndexDisplay(weatherData)

# 當數據更新時，兩個顯示器都會自動收到通知並顯示
print("第一次更新數據：")
weatherData.setMeasurements(27, 80, 1013) 

print("\n第二次更新數據：")
weatherData.setMeasurements(32, 85, 1013)



# 新增:高溫警告系統(只吃 Event)
class HighTemperatureAlarm:
    def on_high_temp(self, event: HighTemperatureEvent):
        print(f" 高溫警告! 目前溫度 {event.temperature}°C")

# 執行驗收(重點在[Observer + Event] 同時存在)
event_bus = EventBus()
weatherData = WeatherData(event_bus)

# Observer (狀態顯示)
CurrentConditionsDisplay(weatherData)
HeatIndexDisplay(weatherData)

# Event(高溫警告)
alarm = HighTemperatureAlarm()
event_bus.subscribe(alarm.on_high_temp)

print("第一次更新: ")
weatherData.setMeasurements(30, 70, 1013)

print("\n第二次更新 (超過門檻): ")
weatherData.setMeasurements(36, 80, 1013)

print("\n第三次更新 (仍然高溫,不重複警告): ")
weatherData.setMeasurements(37, 82, 1013)

print("\n第四次更新 (降溫再升高): ")
weatherData.setMeasurements(33, 70, 1013)
weatherData.setMeasurements(36, 75, 1013)

