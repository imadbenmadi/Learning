from matplotlib import pyplot as plt

SPEED_OF_LIGHT = 299792458


def do_work(val):
    ...


def introduce_vcpf(data, start, count):
    ...

    end = start + count - 1
    if data[end] < 0:
        raise ValueError
    elif data[end] > SPEED_OF_LIGHT:
        print("warning, probably invalid calculation")
    else:
        do_work(data[end])

    ...





def process_timelike(event):
    ...


def process_spacelike(event):
    ...


def process_events(events):
    for event in events:
        process_event(event)


def process_event(event):
    if is_timelike(event):
        process_timelike(event)
    else:
        process_spacelike(event)


def is_timelike(event):
    return event["dx"] * event["dx"] < event["dt"] * event["dt"]
