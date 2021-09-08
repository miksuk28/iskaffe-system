def __calc_mins(hours, minutes):
    return (hours * 60) + minutes

arg = "00:00"

def convert_to_mins(time):
    if time[2] != ":" or len(time) != 5:
        print("Time is in wrong format! Must be HH:MM")
        return None
    
    hours = time[0] + time[1]
    minutes = time[3] + time[4]

    return __calc_mins(int(hours), int(minutes))

print(convert_to_mins(arg))