import pyaudio
import struct
import math
import time
import json

"""
Constants and definitions
"""
RATE = 44100
INPUT_BLOCK_TIME = 0.01  # seconds
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)

PULSE_THRESHOLD = 0.6
MIN_SECONDS_BETWEEN_PULSES = 0.28


def get_rms(block):
    # RMS amplitude is defined as the square root of the
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block) / 2
    format = "%dh" % (count)
    shorts = struct.unpack(format, block)

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample * (1.0 / 32768.0)
        sum_squares += n * n

    return math.sqrt(sum_squares / count)


def is_pulse(pulse_block):
    global last_pulse_timestamp

    amplitude = get_rms(pulse_block)

    if amplitude > PULSE_THRESHOLD:
        if get_current_timestamp() - last_pulse_timestamp >= MIN_SECONDS_BETWEEN_PULSES:
            return True

    return False


def get_current_timestamp():
    return time.time()


def get_pulse_stream(pyaudio_instance):
    return pyaudio_instance.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=RATE,
            input=True,
            frames_per_buffer=INPUT_FRAMES_PER_BLOCK
    )


def listen_for_pulses(pulse_stream):
    global last_pulse_timestamp, first_pulse

    while True:
        try:
            pulse_block = pulse_stream.read(INPUT_FRAMES_PER_BLOCK)

            if is_pulse(pulse_block):
                seconds_between_pulses = get_current_timestamp() - last_pulse_timestamp

                last_pulse_timestamp = get_current_timestamp()

                if not first_pulse:
                    print json.dumps({
                        'seconds_between_pulses': seconds_between_pulses
                    })
                else:
                    first_pulse = False

        except IOError, e:
            print("Error recording: ", e)


"""
Program
"""

pAudio = pyaudio.PyAudio()
pulse_stream = get_pulse_stream(pAudio)

last_pulse_timestamp = 0
first_pulse = True

listen_for_pulses(pulse_stream)
