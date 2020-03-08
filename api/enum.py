from collections import namedtuple
from enum import Enum

choice = namedtuple('Choice', 'name value')


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return [choice(e.value, e.name) for e in cls]


class Gender(ChoiceEnum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class CnhType(ChoiceEnum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'


class VehicleType(ChoiceEnum):
    CAMINHAO_3_4 = 1
    CAMINHAO_TOCO = 2
    CAMINHAO_TRUCK = 3
    CARRETA_SIMPLES = 4
    CARRETA_EIXO_ESTENDIDO = 5
