# Physics/time calculation functions

def calculate_travel_time(s, vmax, a, r):
    s_0 = (vmax ** 2) / (2 * a)
    s_1 = (vmax ** 2) / (2 * r)

    if s <= s_0:
        t = pow((2 * s * ((1 / a) + (1 / r))), (1 / 2))
    elif s > s_0:
        t = vmax * ((1 / a) + (1 / r)) + ((s - s_0 - s_1) / vmax)
    
    return t