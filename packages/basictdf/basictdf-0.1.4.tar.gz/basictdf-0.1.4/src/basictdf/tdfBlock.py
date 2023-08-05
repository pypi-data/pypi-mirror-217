from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import IO, Optional

__all__ = ["Block", "BlockType"]
__doc__ = "Block and block type classes."


class BlockType(Enum):
    unusedSlot = 0  # TDF_DATABLOCK_NOBLOCK
    notDefined = 1  # TDF_DATABLOCK_NOTYPE
    calibrationData = 2  # TDF_DATABLOCK_CALIB
    calibrationData2D = 3  # TDF_DATABLOCK_DATA2D4C
    data2D = 4  # TDF_DATABLOCK_DATA2D
    data3D = 5  # TDF_DATABLOCK_DATA3D
    opticalSystemConfiguration = 6  # TDF_DATABLOCK_OPTISETUP
    forcePlatformsCalibrationData = 7  # TDF_DATABLOCK_CALPLAT
    forcePlatformsCalibrationData2D = 8  # TDF_DATABLOCK_DATA2D4P
    forcePlatformsData = 9  # TDF_DATABLOCK_DATAPLAT
    anthropometricData = 10  # TDF_DATABLOCK_ANTHROPO
    electromyographicData = 11  # TDF_DATABLOCK_DATAEMG
    forceAndTorqueData = 12  # TDF_DATABLOCK_FORCE3D
    volumetricData = 13  # TDF_DATABLOCK_VOLUME
    analogData = 14  # TDF_DATABLOCK_GENPURPOSE
    generalCalibrationData = 15  # TDF_DATABLOCK_CALGENPURP
    temporalEventsData = 16  # TDF_DATABLOCK_EVENTS


class Block(ABC):
    type = BlockType.notDefined

    def __init__(
        self,
        creation_date: Optional[datetime] = None,
        last_modification_date: Optional[datetime] = None,
        last_access_date: Optional[datetime] = None,
    ):
        self.creation_date = (
            creation_date if creation_date is not None else datetime.now()
        )
        self.last_modification_date = (
            last_modification_date
            if last_modification_date is not None
            else datetime.now()
        )
        self.last_access_date = (
            last_access_date if last_access_date is not None else datetime.now()
        )

    @abstractmethod
    def nBytes(self) -> int:
        pass

    @abstractmethod
    def _build(self, file: IO[bytes], format: int):
        pass

    @abstractmethod
    def _write(self, file: IO[bytes]):
        pass

    def __repr__(self):
        return self.__class__.__name__ + "(" + str(self.__class__.type) + ")"


class NotImplementedBlock(Block):
    type = BlockType.notDefined

    @classmethod
    def _build(cls, *args, **kwargs):
        raise NotImplementedError(
            f"Buidling blocks of type {cls.type} is yet implemented"
        )

    def _write(self, *args, **kwargs):
        raise NotImplementedError(
            f"Writing blocks type {self.type} is not implemented yet."
        )


class CalibrationData2D(NotImplementedBlock):
    type = BlockType.calibrationData2D


class Data2D(NotImplementedBlock):
    type = BlockType.data2D


class ForcePlatformsCalibrationData(NotImplementedBlock):
    type = BlockType.forcePlatformsCalibrationData


class ForcePlatformsCalibrationData2D(NotImplementedBlock):
    type = BlockType.forcePlatformsCalibrationData2D


class ForcePlatformsData(NotImplementedBlock):
    type = BlockType.forcePlatformsData


class AnthropometricData(NotImplementedBlock):
    type = BlockType.anthropometricData


class VolumetricData(NotImplementedBlock):
    type = BlockType.volumetricData


class AnalogData(NotImplementedBlock):
    type = BlockType.analogData


class GeneralCalibrationData(NotImplementedBlock):
    type = BlockType.generalCalibrationData


class UnusedBlock(NotImplementedBlock):
    type = BlockType.unusedSlot


class NotDefinedBlock(NotImplementedBlock):
    type = BlockType.notDefined
