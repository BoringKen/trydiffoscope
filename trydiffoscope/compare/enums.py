import enum

class StateEnum(enum.IntEnum):
    queued      = 10
    running     = 20
    identical   = 30
    different   = 40
    error       = 50
    timeout     = 60
