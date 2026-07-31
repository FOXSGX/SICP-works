""" Homework 6: OOP and Inheritance """

#####################
# Required Problems #
#####################

class Semiring:
    """A base class representing objects that can form a semiring."""

    def add(self, other):
        """Returns the sum of self and other."""
        pass
    
    def mult(self, other):
        """Returns the product of self and other."""
        pass
    
    def negative(self):
        """Returns the additive inverse of self."""
        pass

    def zero(self):
        """Returns the additive identity element."""
        pass

    def one(self):
        """Returns the multiplicative identity element."""
        pass

    # Problem 1.3
    def ntimes(self, n):
        """Returns self added to itself n times.
        >>> base = Integer(3)
        >>> base.ntimes(4)
        12
        >>> p = Polynomial([1, 1])  # Represents x + 1
        >>> p.ntimes(3)
        3x + 3
        """
        assert n >= 0, "n must be a non-negative integer."
        if n == 0:
            return self.zero()
        ans = self.zero()
        for _ in range(n):
            ans = ans.add(self)
        return ans
        

    # Problem 1.3
    def power(self, n):
        """Returns self raised to the power of n using repeated multiplication.
        >>> base = Integer(2)
        >>> base.power(0)
        1
        >>> p = Polynomial([1, 1])  # Represents x + 1
        >>> p.power(3)
        x^3 + 3x^2 + 3x + 1
        """
        assert n >= 0, "Exponent must be a positive integer."
        if n == 0:
            return self.one()
        import copy
        ans = copy.deepcopy(self)
        for _ in range(n-1):
            ans = ans.mult(self)
        return ans

# Problem 1.3
def subst_poly(poly, x):
    """Substitutes the Semiring x into the polynomial poly and returns the result.
    For matrices, constant terms are multiplied by the identity matrix.
    >>> poly = Polynomial([1, -2, 3])  # Represents 3x^2 - 2x + 1
    >>> n = Integer(3)
    >>> p = Polynomial([0, 0, 1])  # x^2
    >>> m = Matrix([[1, 2, 3], [2, 1, 1], [2, 3, 3]])
    >>> subst_poly(poly, n)
    22
    >>> subst_poly(poly, m)
    [[32, 35, 36],
     [14, 23, 28],
     [38, 42, 49]]
    >>> subst_poly(poly, p)
    3x^4 - 2x^2 + 1
    """
    from copy import deepcopy
    c = poly.coefficients
    copy = deepcopy(x)
    x = x.zero()
    for i in range(len(c)):
        if c[i] < 0:
            x = x.add(copy.power(i).ntimes(-c[i]).negative())
        else:
            x = x.add(copy.power(i).ntimes(c[i]))
    return x



# Problem 1.1
class Matrix(Semiring):
    """A class representing 3x3 matrices."""

    def __init__(self, elements):
        """Initializes a 3x3 matrix with the given list of lists.
        >>> Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]
        """
        self.elements = elements
    
    def add(self, other):
        """Returns a new Matrix representing the sum of self and other.
        >>> m1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> m2 = Matrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
        >>> m1.add(m2)
        [[10, 10, 10],
         [10, 10, 10],
         [10, 10, 10]]
        """
        return Matrix([[self.elements[j][i] + other.elements[j][i] for i in range(3)] for j in range(3)])
        
    
    def mult(self, other):
        """Returns a new Matrix representing the product of self and other.
        >>> m1 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        >>> m2 = Matrix([[9, 8, 7], [6, 5, 4], [3, 2, 1]])
        >>> m1.mult(m2)
        [[30, 24, 18],
         [84, 69, 54],
         [138, 114, 90]]
        """
        return Matrix([[sum(self.elements[i][x]*other.elements[x][j] for x in range(3)) for j in range(3)] for i in range(3)])
    
    def negative(self):
        """Returns a new Matrix representing the additive inverse of self.
        >>> m = Matrix([[1, -2, 3], [-4, 5, -6], [7, -8, 9]])
        >>> m.negative()
        [[-1, 2, -3],
         [4, -5, 6],
         [-7, 8, -9]]
        """
        return Matrix([[-self.elements[j][i] for i in range(3)] for j in range(3)])

    def zero(self):
        """Returns the zero matrix."""
        return Matrix([[0]*3 for _ in range(3)])
    
    def one(self):
        """Returns the identity matrix."""
        return Matrix([[1 if i == j else 0 for i in range(3)] for j in range(3)])
    
    def __repr__(self):
        """Returns the string representation of the matrix.
        You are not supposed to understand this code now.
        """
        rows = [str(row) for row in self.elements]
        return "[{}]".format(",\n ".join(rows))

# Problem 1.2
class Polynomial(Semiring):
    """A class representing polynomials."""

    def __init__(self, coefficients):
        """Initializes a Polynomial with the given list of coefficients.
        The coefficient at index i corresponds to the term with degree i.
        >>> p = Polynomial([1, 2, 3])  # Represents 3x^2 + 2x + 1
        >>> p.coefficients
        [1, 2, 3]
        """
        self.coefficients = coefficients
    
    def add(self, other):
        """Returns a new Polynomial representing the sum of self and other.
        >>> p1 = Polynomial([1, 2])      # 2x + 1
        >>> p2 = Polynomial([3, 4, 5])   # 5x^2 + 4x + 3
        >>> p1.add(p2)
        5x^2 + 6x + 4
        """
        c1 = self.coefficients
        c2 = other.coefficients
        ans = []
        if len(c1) > len(c2):
            c1,c2 = c2,c1
        c1 += [0]*(len(c2)-len(c1))
        for i in range(len(c1)):
            ans.append(c1[i]+c2[i])
        return Polynomial(ans)
            
            
    
    def mult(self, other):
        """Returns a new Polynomial representing the product of self and other.
        >>> p1 = Polynomial([1, 2])      # 2x + 1
        >>> p2 = Polynomial([3, 4])      # 4x + 3
        >>> p1.mult(p2)
        8x^2 + 10x + 3
        >>> i1 = Integer(2)
        >>> import copy
        >>> i2 = copy.deepcopy(i1)
        >>> i1.mult(i2)
        4
        """
        c1 = self.coefficients
        c2 = other.coefficients
        ans = Polynomial.zero(self)
        add_l = []
        for i in range(len(c1)):
            add_l += [0] * i
            for j in range(len(c2)):
                add_l.append(c1[i]*c2[j])
            ans = ans.add(Polynomial(add_l))
            add_l = []
        return ans

            

    
    def negative(self):
        """Returns a new Polynomial representing the additive inverse of self.
        >>> p = Polynomial([1, -2, 3])  # 3x^2 - 2x + 1
        >>> p.negative()
        -3x^2 + 2x - 1
        """
        c = self.coefficients
        ans = []
        for i in range(len(c)):
            ans.append(-c[i])
        return Polynomial(ans)

    def zero(self):
        """Returns the zero polynomial."""
        return Polynomial([0])

    def one(self):
        """Returns the identity polynomial."""
        return Polynomial([1])

    def __repr__(self):
        """Returns the string representation of the polynomial.
        You are not supposed to understand this code now.
        >>> p = Polynomial([1, 0, 3])  # Represents 1 + 0x + 3x^2
        >>> repr(p)
        '3x^2 + 1'
        """
        terms = []
        for power, coeff in enumerate(self.coefficients):
            if coeff != 0:
                if power == 0:
                    terms.append(f'{coeff}')
                    continue
                elif power == 1:
                    base = 'x'
                else:
                    base = f'x^{power}'

                if coeff == 1:
                    terms.append(base)
                else:
                    terms.append(f'{coeff}{base}')
        return " + ".join(reversed(terms)).replace(" + -", " - ") if terms else "0"

class Integer(Polynomial):
    """A class representing a single integer as a polynomial."""

    def __init__(self, value):
        """Initializes a Integer with the given value.
        >>> Integer(5)
        5
        """
        super().__init__([value])
        

    def zero(self):
        """Returns the additive identity integer (0)."""
        return Integer(0)

    def one(self):
        """Returns the multiplicative identity integer (1)."""
        return Integer(1)

import random

# Problem 2.1
class Buff:
    """
    Represents a temporary stat modification (buff or debuff).
    Duration decreases each turn until it expires.
    """
    
    def __init__(self, name, attack_bonus=0, defense_bonus=0, duration=3):
        self.name          = name
        self.attack_bonus  = attack_bonus
        self.defense_bonus = defense_bonus
        self.duration      = duration
    
    def decrease_duration(self):
        """Decrease duration by 1. Returns True if expired.
        >>> buff = Buff("Test Buff", attack_bonus=5, defense_bonus=3, duration=2)
        >>> buff.decrease_duration()
        False
        >>> buff.decrease_duration()
        True
        """
        self.duration -= 1
        return self.duration <= 0
    
    def copy(self):
        """Returns a copy of the buff."""
        return Buff(self.name, self.attack_bonus, self.defense_bonus, self.duration)

    def __repr__(self):
        """Returns a string representation of the buff.
        You are not supposed to understand this code now."""
        stats = []
        if self.attack_bonus != 0:
            stats.append(f"ATK {self.attack_bonus:+d}")
        if self.defense_bonus != 0:
            stats.append(f"DEF {self.defense_bonus:+d}")
        stat_str = ", ".join(stats) if stats else "No effect"
        return f"{self.name}: {stat_str} ({self.duration} turns)"


class Equipment:
    """
    Base class for all equipment (weapons and armor).
    Equipment can be equipped by the player to boost stats.
    """
    
    def __init__(self, name, attack_bonus=0, defense_bonus=0, price=0):
        self.name = name
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.price = price

    def __repr__(self):
        """Returns a string representation of the equipment.
        You are not supposed to understand this code now."""
        stats = []
        if self.attack_bonus > 0:
            stats.append(f"ATK +{self.attack_bonus}")
        if self.defense_bonus > 0:
            stats.append(f"DEF +{self.defense_bonus}")
        return f"{self.name} ({', '.join(stats)})" if stats else self.name


class Weapon(Equipment):
    """Weapon subclass for attack-focused equipment."""
    
    def __init__(self, name, attack_bonus, price=0):
        """Initialize a Weapon with the given name, attack bonus, and price.
        >>> sword = Weapon("Sword", attack_bonus=10, price=100)
        >>> print(sword)
        Sword (ATK +10)
        >>> print(sword.price)
        100
        """
        super().__init__(name=name,attack_bonus=attack_bonus,defense_bonus=0,price=price)


class Armor(Equipment):
    """Armor subclass for defense-focused equipment."""
    
    def __init__(self, name, defense_bonus, price=0):
        """Initialize an Armor with the given name, defense bonus, and price.
        >>> shield = Armor("Shield", defense_bonus=8, price=80)
        >>> print(shield)
        Shield (DEF +8)
        >>> print(shield.price)
        80
        """
        super().__init__(name,attack_bonus=0,defense_bonus=defense_bonus,price=price)


# Problem 2.2
class Character:
    """Base class for all characters in the game."""
    
    def __init__(self, name, max_hp, attack, defense):
        self.name         = name
        self.max_hp       = max_hp
        self.current_hp   = max_hp
        self.base_attack  = attack
        self.base_defense = defense
        self.buffs        = []
    
    def is_alive(self):
        return self.current_hp > 0
    
    def get_attack(self):
        """Calculate total attack including buffs.
        >>> char = Character("Student", max_hp=100, attack=20, defense=10)
        >>> buff = Buff("Might", attack_bonus=5, duration=2)
        >>> char.buffs.append(buff)
        >>> char.get_attack()
        25
        """
        att = self.base_attack
        for i in self.buffs:
            att += i.attack_bonus
        return att

    
    def get_defense(self):
        """Calculate total defense including buffs.
        >>> char = Character("Student", max_hp=100, attack=20, defense=10)
        >>> buff = Buff("Shield", defense_bonus=3, duration=2)
        >>> char.buffs.append(buff)
        >>> char.get_defense()
        13
        """
        deff = self.base_defense
        for j in self.buffs:
            deff += j.defense_bonus
        return deff
    
    def take_damage(self, damage):
        """Apply damage, accounting for defense. Returns actual damage taken.
        >>> char = Character("Student", max_hp=100, attack=20, defense=10)
        >>> char.take_damage(25)
        15
        >>> char.current_hp
        85
        """
        if damage < 0:
            return 0
        if damage < self.get_defense():
            return 0
        dam = damage - self.get_defense()
        if dam > self.current_hp:
            ans = self.current_hp
            self.current_hp = 0
            return ans
        self.current_hp -= dam
        return dam
    
    def heal(self, amount):
        """Heal the character. Returns actual amount healed."
        >>> char = Character("Student", max_hp=100, attack=20, defense=10)
        >>> char.current_hp = 50
        >>> char.heal(30)
        30
        >>> char.current_hp
        80
        """
        if self.current_hp + amount <= self.max_hp:
            self.current_hp += amount
            return amount
        else:
            ans = self.max_hp - self.current_hp
            self.current_hp = self.max_hp
            return ans
        
    
    def update_buffs(self):
        """Update all buffs (decrease duration, remove expired).
        >>> char = Character("Student", max_hp=100, attack=20, defense=10)
        >>> buff1 = Buff("Might", attack_bonus=5, duration=1)
        >>> buff2 = Buff("Shield", defense_bonus=3, duration=2)
        >>> char.buffs.extend([buff1, buff2])
        >>> len(char.buffs)
        2
        >>> char.update_buffs()
        >>> len(char.buffs)
        1
        >>> char.update_buffs()
        >>> len(char.buffs)
        0
        """
        remove_l = []
        for buff in self.buffs:
            if buff.decrease_duration():
                remove_l.append(buff)
        for buff in remove_l:
            self.buffs.remove(buff)

    
    def basic_attack(self, target):
        """Perform a basic attack on target."""
        damage = self.get_attack()
        actual_damage = target.take_damage(damage)
        return f"{self.name} attacks {target.name} for {actual_damage} damage!"
    
    def magic_attack(self, target):
        """Perform a magic attack. Can be overridden by subclasses.
        Return a string describing the attack.
        >>> char = Character("Mage", max_hp=80, attack=15, defense=5)
        >>> enemy = Character("Goblin", max_hp=50, attack=10, defense=2)
        >>> result = char.magic_attack(enemy)
        >>> print(result)
        Mage uses magic attack on Goblin for 20 damage!
        >>> enemy.current_hp
        30
        >>> char.buffs[0]
        Exhaustion: ATK -5, DEF -3 (2 turns)
        """
        damage = int(self.get_attack()*1.5)
        actual_damage = target.take_damage(damage)
        self.buffs.append(Buff("Exhaustion", attack_bonus=-5, defense_bonus=-3, duration=2))
        return f"{self.name} uses magic attack on {target.name} for {actual_damage} damage!"

    def __repr__(self):
        """Return a status string for the character.
        You are not supposed to understand this code now."""
        filled = int((self.current_hp / self.max_hp) * 20) if self.max_hp > 0 else 0
        empty = 20 - filled
        hp_bar = f"[{'█' * filled}{'░' * empty}]"
        if self.buffs:
            buff_descriptions = ", \n  ".join(str(buff) for buff in self.buffs)
            buff_info = f" Buffs: [{buff_descriptions}]"
        else:
            buff_info = ""
        return f"{self.name}:\n{hp_bar} ({self.current_hp}/{self.max_hp} HP)\n{buff_info}"


# Problem 2.3
class Player(Character):
    """
    Player character class.
    Extends Character with leveling, equipment, and inventory systems.
    """
    
    def __init__(self, name):
        super().__init__(name, max_hp=100, attack=15, defense=5)
        self.level = 1
        self.experience = 0
        self.gold = 50
        self.equipped_weapon = None
        self.equipped_armor = None
        self.potions = 3
    
    def get_attack(self):
        """Override to include weapon bonus.
        >>> player = Player("Student")
        >>> sword = Weapon("Sword", attack_bonus=10)
        >>> player.equip_weapon(sword)
        >>> player.get_attack()
        25
        """
        att = super().get_attack()
        if self.equipped_weapon:
            att += self.equipped_weapon.attack_bonus
        return att
    
    def get_defense(self):
        """Override to include armor bonus.
        >>> player = Player("Student")
        >>> shield = Armor("Shield", defense_bonus=8)
        >>> player.equip_armor(shield)
        >>> player.get_defense()
        13
        """
        deff = super().get_defense()
        if self.equipped_armor:
            deff += self.equipped_armor.defense_bonus
        return deff 
    
    def equip_weapon(self, weapon):
        """Equip a weapon."""
        self.equipped_weapon = weapon
    
    def equip_armor(self, armor):
        """Equip armor."""
        self.equipped_armor = armor
    
    def spend_gold(self, amount):
        """Spend gold. Returns True if successful, False if not enough gold.
        >>> player = Player("Student")
        >>> player.spend_gold(30)
        True
        >>> player.gold
        20
        """
        if self.gold >= amount:
            self.gold -= amount
            return True
        else:
            return False
    
    def use_potion(self):
        """Use a health potion.
        Return a string description if used, else None.
        >>> player = Player("Student")
        >>> player.current_hp = 40
        >>> player.use_potion()
        'Used a potion! Restored 50 HP.'
        >>> player.current_hp
        90
        >>> player.potions
        2
        """
        if self.potions > 0:
            healed = self.heal(50)
            self.potions -= 1
            return f"Used a potion! Restored {healed} HP."
    
    def add_experience(self, amount):
        """Add experience and check for level up.
        Return a string if leveled up, else None.
        >>> player = Player("Student")
        >>> player.current_hp = 80
        >>> player.add_experience(60)
        'Level Up! You are now level 2!'
        >>> player.level
        2
        >>> player.current_hp
        120
        >>> player.add_experience(30)
        >>> player.level
        2
        >>> player.add_experience(70)
        'Level Up! You are now level 3!'
        >>> player.level
        3
        >>> player.base_attack
        25
        """
        exp_needed = self.level * 50
        if amount + self.experience >= exp_needed:
            self.experience = self.experience + amount - exp_needed
            self.level += 1
            self.max_hp += 20
            self.base_attack += 5
            self.base_defense += 2
            self.current_hp = self.max_hp
            return f"Level Up! You are now level {self.level}!"
        else:
            self.experience += amount


class Enemy(Character):
    """
    Enemy character class.
    Base class for all enemies including TAs and Boss.
    """
    
    def __init__(self, name, max_hp, attack, defense, exp_reward, gold_reward):
        super().__init__(name, max_hp, attack, defense)
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        self.description = "A mysterious enemy"
    
    def choose_action(self, player):
        pass

    def need_buff(self):
        if len(self.buffs) == 0:
            return True
        elif len(self.buffs) == 1:
            return self.buffs[0].name == "Exhaustion"
        return False


class TA(Enemy):
    """
    Teaching Assistant enemy class.
    Each TA has a specialty and scales with difficulty.
    """
    
    def __init__(self, name, difficulty, specialty_buff, description):
        hp      = 50 + (difficulty * 15)
        attack  = 8  + (difficulty * 3 )
        defense = 2  + (difficulty * 1 )
        exp     = 30 + (difficulty * 10)
        gold    = 20 + (difficulty * 15)
        
        super().__init__(name, hp, attack, defense, exp, gold)
        self.specialty_buff = specialty_buff 
        self.description    = description
    
    def choose_action(self, player):
        """Choose action based on current HP and buffs."""
        if not any(buff.name == self.specialty_buff['buff'].name for buff in self.buffs):
            self.buffs.append(self.specialty_buff['buff'].copy())
            return f"{self.name} {self.specialty_buff['message']}"
        else:
            rand_action = random.choices([self.basic_attack, self.magic_attack], weights=[70, 30])[0]
            return rand_action(player)


class Boss(Enemy):
    """
    Final boss character with enhanced abilities.
    """
    
    def __init__(self):
        super().__init__(
            name="Professor Lambda",
            max_hp=300,
            attack=25,
            defense=10,
            exp_reward=200,
            gold_reward=500
        )
        self.description = "The legendary SICP professor who has mastered all paradigms!"
        # If needed, you can add more attributes here.
        self.phase = 1
    
    def choose_action(self, player):
        """Choose action based on current HP and buffs.
        Return a string describing the action taken.
        >>> boss = Boss()
        >>> player = Player("Student")
        >>> boss.current_hp = 210
        >>> boss.choose_action(player)
        'Professor Lambda attacks Student for 20 damage!'
        >>> player.current_hp
        80
        >>> boss.current_hp = 200
        >>> boss.choose_action(player)
        'Professor Lambda enters a frenzy! (ATK +40, DEF -20)'
        >>> boss.choose_action(player)
        'Professor Lambda uses magic attack on Student for 80 damage!'
        >>> player.current_hp
        0
        """
        if self.current_hp < self.max_hp*0.7 and self.phase == 1:
            self.buffs.append(Buff("Frenzy", attack_bonus=40, defense_bonus=-20, duration=999))
            self.phase = 2
            return f"{self.name} enters a frenzy! (ATK +40, DEF -20)"
        if self.phase == 1:
            return self.basic_attack(player)
        if self.phase == 2:
            return self.magic_attack(player)