import enum

class Speed(enum.Enum):

    slow = 1
    normal = 2
    fast = 3

print(Speed(1))