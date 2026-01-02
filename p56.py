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

# ConcreteSubject:WeatherData
class WeatherData(Subject):
    def __init__(self):
        self._observers = []
        self._temperature = 0
        self._humidity = 0
        self._pressure = 0

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
        self.notifyObservers()

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




