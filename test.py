
from volume import stl_volume, stl_mass

DENSITY = 1.05 # g/cm^3


a = stl_volume('Detal.stl')
b = stl_mass(a, density=DENSITY)
PRICE = 7 # rub/gram


print(b * PRICE)