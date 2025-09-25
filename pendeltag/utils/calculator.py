# Physics/time calculation functions

def calculate_travel_time(s, vmax, a, r):
    s_0 = (vmax ** 2) / (2 * a)
    s_1 = (vmax ** 2) / (2 * r)

    if s <= s_0:
        t = (2 * s * ((1 / a) + (1 / r))) ** 0.5
    elif s > s_0:
        t = vmax * ((1 / a) + (1 / r)) + ((s - s_0 - s_1) / vmax)
    else:
        t = 0
    return t

def calculate_distance_deltas(stations):
    distance_deltas = []
    # Calculate the segment distance
    for i in range(len(stations) - 1):
        d0 = float(stations[i]['distance'])
        d1 = float(stations[i + 1]['distance'])
        delta = d1 - d0
        distance_deltas.append(delta)
    return distance_deltas

def calculate_time_deltas(distance_deltas, vmax, a, r):
    time_deltas = []
    travel_time = 0
    # The starting station departs at time 0
    time_deltas.append(travel_time)
    for distance_delta in distance_deltas:
        # Multiply by 1000 to convert km to m if needed.
        travel_time += calculate_travel_time(distance_delta * 1000, vmax, a, r)
        time_deltas.append(travel_time)
    return time_deltas

def calculate_departure_for_stations(distance_deltas, vmax, a, r):
    # This returns one departure time per stop (including the final station)
    time_deltas = calculate_time_deltas(distance_deltas, vmax, a, r)
    departure_times = []
    offset = 60  # waiting time between stops (in seconds)
    for i, t in enumerate(time_deltas):
        departure_times.append(t + (i * offset))
    return departure_times