# Time formatting, conversions etc.

def format_times(times, start_time):
    start_seconds = int(start_time["hour"]) * 3600 + int(start_time["minute"]) * 60
    formatted_times = []

    for sec in times:
        total = start_seconds + sec
        hour = int((total // 3600) % 24)
        minute = int((total % 3600) // 60)
        formatted_times.append({"hour": hour, "minute": minute})

    return formatted_times

# def create_timetable(departure_times, )