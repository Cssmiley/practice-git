from abc import ABC,abstractmethod
# 武器行為介面
class WeaponBehavior(ABC):
    @abstractmethod
    def useWeapon(self):
        pass

# 不同行為實作
class KnifeBehavior(WeaponBehavior):
    def useWeapon(self):
        print("使用小刀")

class BowAndArrowBehavior(WeaponBehavior):
    def useWeapon(self):
        print("使用弓箭")

class AxeBehavior(WeaponBehavior):
    def useWeapon(self):
        print("使用斧頭")

class SwordBehavior(WeaponBehavior):
    def useWeapon(self):
        print("使用劍")

# Character 類別
class Character:
    def __init__(self, weapon_behavior:WeaponBehavior):
        self.weapon_behavior = weapon_behavior

    def fight(self):
        self.weapon_behavior.useWeapon()

    def setWeapon(self, weapon_behavior:WeaponBehavior):
        print("切換武器")
        self.weapon_behavior = weapon_behavior

# 具體的 character (組合行為)
class Queen(Character):
    def __init__(self):
        super().__init__(
            weapon_behavior=BowAndArrowBehavior()
        )

class King(Character):
    def __init__(self):
        super().__init__(
            weapon_behavior=KnifeBehavior()
        )


class Knight(Character):
    def __init__(self):
        super().__init__(
            weapon_behavior=SwordBehavior()
        )
    
class Troll(Character):
    def __init__(self):
        super().__init__(
            weapon_behavior=AxeBehavior()
        )
    
queen = Queen()
queen.fight()

queen.setWeapon(SwordBehavior())
queen.fight()
