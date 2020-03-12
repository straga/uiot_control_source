import time



def ticks_ms():
    return int(time.perf_counter_ns() / 1000000)

class utime:

    def ticks_ms(self):
        return time.perf_counter_ns()







