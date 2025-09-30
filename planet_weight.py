# Name | Surface gravity
# Sun 28.02 g
# Mercury 0.377 g
# Venus 0.904 g
# Earth 1 g
# Moon 0.165 4 g
# Mars 0.38 g
# Phobos 0.000 581 g
# Deimos 0.000 306 g
# Ceres 0.029 g
# Jupiter 2.53 g
# Io 0.183 g
# Europa 0.134 g
# Ganymede 0.146 g
# Callisto 0.126 g
# Saturn 1.065 g
# Titan 0.138 g
# Enceladus 0.011 3 g
# Uranus 0.886 g
# Neptune 1.14 g
# Triton 0.079 g
# Pluto 0.063 g
# Eris 0.084 g
# 67P-CG 0.000 017 g

import numpy as np
import json
import logging

weight_names = ["Neutron Star",
                "White Dwarf",
                "Sun",
                "Jupiter",
                "Neptune",
                "Saturn",
                "Uranus",
                "Earth",
                "Venus",
                "Mars",
                "Mercury",
                "Titan",
                "Ganymede",
                "Io",
                "Europa",
                "Moon",
                "Triton",
                "Pluto",
                "Ceres",
                "Phobos",
                "Enceladus",
                "ISS",
                "Olympus Mons"]
weight_factor = [200000000000,
                 100000,
                 28.02,
                 2.53,
                 1.14,
                 1.065,
                 0.886,
                 1,
                 0.904,
                 0.38,
                 0.377,
                 0.138,
                 0.146,
                 0.183,
                 0.134,
                 0.1654,
                 0.079,
                 0.063,
                 0.029,
                 0.000581,
                 0.0113,
                 0,
                 0.37506
                 ]

assert len(weight_names) == len(weight_factor)

def get_planet_weights(earth_weight, rounding=2, zero_floor=True):
    earth_weights = [earth_weight]*len(weight_factor)
    # print(f"earth_weights = {earth_weights}")
    # print(f"weight_factor = {weight_factor}")
    results=np.around(np.multiply(earth_weights,weight_factor), decimals=rounding)
    if zero_floor:
        logging.debug("Clipping weights to [0, inf[")
        results = np.clip(results, 0, None)
    return results

# returns a json list where the key is the planet name and the value is the weight on that planet
def get_weight_json(earth_weight, rounding=2):
    return json.dumps(dict(zip(weight_names, get_planet_weights(earth_weight, rounding))))


if __name__== "__main__":
  print(f"result is: {get_weight_json(100)}")
  print(f"Raw result is: {get_planet_weights(100)}")
