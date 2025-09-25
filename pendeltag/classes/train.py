import sys
sys.path.insert(0, '/Users/axelroxenborg/Documents/Programmering/p-uppgift-kth-python/pendeltag')

from utils import calculator as C

# Train class
class Train:
    def __init__(self, vmax, a, r):
        self.vmax = vmax
        self.a = a
        self.r = r

    def travel_time(self, s):
        return C.calculate_travel_time(s, self.vmax, self.a, self.r)
    
    def __str__(self):
        return f'VMAX: {self.vmax}, ACCELERATION: {self.a}, RETARDATION: {self.r}'