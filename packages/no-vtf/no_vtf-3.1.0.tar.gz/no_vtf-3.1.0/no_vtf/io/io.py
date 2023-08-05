# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pathlib

from abc import abstractmethod
from collections.abc import Sequence
from typing import ClassVar, Generic, TypeVar

import no_vtf.io  # noqa: F401  # define all task runners for IO.initialize()

_A_contra = TypeVar("_A_contra", contravariant=True)


class IO(Generic[_A_contra]):
    _initialized: ClassVar[bool] = False

    @classmethod
    def initialize(cls) -> None:
        for subclass in cls.__subclasses__():
            subclass._initialize()

        cls._initialized = True

    @classmethod
    def _is_initialized(cls) -> bool:
        return cls._initialized

    @classmethod
    def _initialize(cls) -> None:
        pass

    def write(self, path: pathlib.Path, data: _A_contra, /) -> None:
        self.write_sequence(path, [data])

    def readback(self, path: pathlib.Path, data: _A_contra, /) -> None:
        self.readback_sequence(path, [data])

    @abstractmethod
    def write_sequence(self, path: pathlib.Path, sequence: Sequence[_A_contra], /) -> None:
        ...

    @abstractmethod
    def readback_sequence(self, path: pathlib.Path, sequence: Sequence[_A_contra], /) -> None:
        ...
