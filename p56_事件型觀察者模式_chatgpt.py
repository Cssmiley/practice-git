# 1.定義事件物件(重點)
from dataclasses import dataclass

@dataclass
class WeatherEvent:
    type: str
    data: dict

# 2.Observer(只接收事件)
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def on_event(self, event:WeatherEvent):
        pass

# 3.Subject(事件發布者)
class Subject(ABC):
    @abstractmethod
    def subscribe(self, observer: Observer):
        pass

    @abstractmethod
    def unsubscribe(self, observer: Observer):
        pass

    @abstractmethod
    def publish(self, event: WeatherEvent):
        pass

# ConcreteSubject: WeatherData(事件來源)
class WeatherData(Subject):
    def __init__(self):
        self._observers = []

    def subscribe(self, observer:Observer):
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer):
        self._observers.remove(observer)

    def publish(self, event: WeatherEvent):
        for observer in self._observers:
            observer.on_event(event)

    # 狀態改變點(轉成事件)
    def setMeasurements(self, temperature, humidity, pressure):
        event = WeatherEvent(
            type="WEATHER_UPDATED",
            data={
                "temperature": temperature,
                "humidity": humidity,
                "pressure": pressure
            }
        )
        print("[WeatherData] 發送天氣膯新事件")
        self.publish(event)

# 5.Concrete Observers(各自解讀事件)
# CurrentConditionDisplay
class CurrentConditionDisplay(Observer):
    def on_event(self, event: WeatherEvent):
        if event.type == "WEATHER_UPDATED":
            t = event.data["temperature"]
            h = event.data["humidity"]
            print(f"[目前狀況] 溫度={t}, 濕度={h}")

# StatisticsDisplay(只關心溫度)
class StatisticsDisplay(Observer):
    def __init__(self):
        self._temps = []

    def on_event(self, event:WeatherEvent):
        if event.type == "WEATHER_UPDATED":
            self._temps.append(event.data["temperature"])
            avg = sum(self._temps) / len(self._temps)
            print(f"[統計] 平均溫度={avg:.1f}")

# ForecastDisplay(只關心氣壓)
class ForecastDisplay(Observer):
    def on_event(self, event:WeatherEvent):
        if event.type == "WEATHER_UPDATED":
            p = event.data["pressure"]
            print(f"[預報] 氣壓={p} -> 天氣趨勢分析中")

# 6.執行驗收
weather = WeatherData()

current = CurrentConditionDisplay()
stats = StatisticsDisplay()
forecast = ForecastDisplay()

weather.subscribe(current)
weather.subscribe(stats)
weather.subscribe(forecast)

weather.setMeasurements(25, 65, 1013)
print("----")
weather.setMeasurements(28, 70, 1009)


# 題目:新增酷熱指數
class HeatIndexDisplay(Observer):
    def on_event(self, event:WeatherEvent):
        if event.type != "WEATHER_UPDATED":
            return
        
        t = event.data["temperature"]
        rh = event.data["humidity"]

        heat_index = self._compute_heat_index(t, rh)
        print(f"[體感溫度] 酷熱指數為 {heat_index:.2f} °C")

    def _compute_heat_index(self, t, rh):
        """
        簡化版酷熱指數公式(攝氏)
        """
        index = (
            16.923
            + 0.185212 * t
            + 5.37941 * rh
            - 0.100254 * t * rh
            + 0.00941695 * t**2
            + 0.00728898 * rh**2
            + 0.000345372 * t**2 * rh
            - 0.000814971 * t * rh**2
            + 0.0000102102 * t**2 * rh**2
            - 0.000038646 * t**3
            + 0.0000291583 * rh**3
            + 0.00000142721 * t**3 * rh
            + 0.000000197483 * t * rh**3
            - 0.0000000218429 * t**3 * rh**2
            + 0.000000000843296 * t**2 * rh**3
            - 0.0000000000481975 * t**3 * rh**3
        )
        return index
# 執行驗收
weather = WeatherData()

current = CurrentConditionDisplay()
stats = StatisticsDisplay()
forecast = ForecastDisplay()
heat = HeatIndexDisplay()

weather.subscribe(current)
weather.subscribe(stats)
weather.subscribe(forecast)
weather.subscribe(heat)

print("第一次更新：")
weather.setMeasurements(27, 80, 1013)

print("\n第二次更新：")
weather.setMeasurements(32, 85, 1013)