from enum import Enum


class QueueStatus(Enum):
    ARRIVED_IN_ZO = 2
    SUMMONED_IN_PP = 3
    ANNULLED = 9