import ctypes
from os import strerror
from time import monotonic as std_monotonic

# Load the standard C library
libc = ctypes.CDLL("libc.so.6")


# Define the timespec structure
class timespec(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_longlong), ("tv_nsec", ctypes.c_longlong)]


# Define clock_gettime from the standard C library
libc.clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(timespec)]


def monotonic():
    # CLOCK_MONOTONIC constant, usually has the value of 1
    CLOCK_MONOTONIC = 1

    # Create a timespec instance
    t = timespec()

    # Clock_gettime takes two parameters: clock_id and a pointer to timespec structure
    # Call clock_gettime and store the result in the timespec instance
    if libc.clock_gettime(CLOCK_MONOTONIC, ctypes.byref(t)) != 0:
        # If clock_gettime failed, retrieve the error number and raise an OSError
        err = ctypes.get_errno()
        raise OSError(err, strerror(err))

    # Convert the time to seconds and return
    return t.tv_sec + t.tv_nsec / 1e9


# Example usage
if __name__ == "__main__":
    print(monotonic())
    print(std_monotonic())
