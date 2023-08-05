# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import functools
import itertools
import pathlib
import re

from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar, Literal, Optional, Protocol, cast

import imageio.plugins.freeimage
import imageio.v3
import numpy as np
import numpy.typing as npt

from no_vtf.image import Image, ImageData, ImageDataTypes
from no_vtf.image.modifier.fp_precision_modifier import FPPrecisionModifier
from no_vtf.image.modifier.modifier import ImageModifier
from no_vtf.io.io import IO


@dataclass(frozen=True, kw_only=True)
class ImageIO(IO[Image[ImageDataTypes]]):
    format: str

    compress: Optional[bool] = None
    fps: Optional[int] = None

    @classmethod
    def _initialize(cls) -> None:
        # download() seems to be untyped because of implicit reexport
        imageio.plugins.freeimage.download()  # type: ignore[no-untyped-call]

    _format_pattern: ClassVar[re.Pattern[str]] = re.compile(r"[a-z0-9]+", re.ASCII | re.IGNORECASE)

    def __post_init__(self) -> None:
        assert self._is_initialized(), "IO.initialize() must be called early"

        if not self._format_pattern.fullmatch(self.format):
            raise RuntimeError(f"Invalid format: {self.format}")

    def write_sequence(self, path: pathlib.Path, sequence: Sequence[Image[ImageDataTypes]]) -> None:
        backend = self._get_backend()
        backend.write(path, sequence)

    def readback_sequence(
        self, path: pathlib.Path, sequence: Sequence[Image[ImageDataTypes]]
    ) -> None:
        backend = self._get_backend()
        backend.readback(path, sequence)

    def _get_backend(self) -> _ImageIOBackend:
        compress = self.compress
        if compress is None:
            compress = True

        extension = f".{self.format}"

        backend: _ImageIOBackend
        match self.format.lower():
            case "apng":
                backend = _ImageIOApngBackend(compress=compress, fps=self.fps)
            case "exr":
                backend = _ImageIOExrBackend(compress=compress)
            case "png":
                backend = _ImageIOPngBackend(compress=compress)
            case "targa" | "tga":
                backend = _ImageIOTgaBackend(compress=compress)
            case "tiff":
                backend = _ImageIOTiffBackend(compress=compress)
            case _:
                backend = _ImageIOBackend(extension=extension)
        return backend


class _Opener(Protocol):
    def __call__(
        self,
        uri: imageio.typing.ImageResource,
        io_mode: Literal["r", "w"],
        *,
        extension: Optional[str] = None,
        format_hint: Optional[str] = None,
    ) -> imageio.core.v3_plugin_api.PluginV3:
        ...


class _ImageIOBackend:
    def __init__(self, *, extension: Optional[str] = None) -> None:
        self._extension = extension

    def write(self, path: pathlib.Path, sequence: Sequence[Image[ImageDataTypes]]) -> None:
        opener = self._get_opener()
        with opener(path, "w", extension=self._extension) as image_resource:
            for image in sequence:
                kwargs = self._get_writer_kwargs(image)
                image = self._postprocess(image)
                data = self._get_data(image)

                image_resource.write(data, **kwargs)

    def readback(self, path: pathlib.Path, sequence: Sequence[Image[ImageDataTypes]]) -> None:
        opener = self._get_opener()
        with opener(path, "r", extension=self._extension) as image_resource:
            for image, read_data in itertools.zip_longest(sequence, image_resource.iter()):
                if image is None or read_data is None:
                    raise RuntimeError(
                        f"{path!r}: Number of frames differs from what is in the file"
                    )

                image = self._postprocess(image)
                data = self._get_data(image)

                if data.dtype != read_data.dtype:
                    raise RuntimeError(f"{path!r}: Data type differs from what is in the file")

                if not self._compare_data(data, read_data):
                    raise RuntimeError(f"{path!r}: Data differs from what is in the file")

    def _get_opener(self) -> _Opener:
        return cast(_Opener, imageio.v3.imopen)

    def _get_writer_kwargs(self, image: Image[ImageDataTypes]) -> dict[str, object]:
        return {}

    def _postprocess(self, image: Image[ImageDataTypes]) -> Image[ImageDataTypes]:
        return image

    def _get_data(self, image: Image[ImageDataTypes]) -> ImageData:
        data = image.data()

        # write luminance into three channels when alpha is present
        if image.channels == "la":
            l_uint8: npt.NDArray[ImageDataTypes] = data[:, :, [0]]
            a_uint8: npt.NDArray[ImageDataTypes] = data[:, :, [1]]
            data = np.dstack((l_uint8, l_uint8, l_uint8, a_uint8))

        # remove last axis if its length is 1
        if data.shape[-1] == 1:
            data = data[..., 0]

        return data

    def _compare_data(self, data: ImageData, read_data: ImageData) -> bool:
        return np.array_equal(data, read_data)


class _ImageIOPillowBackend(_ImageIOBackend):
    def __init__(self, *, extension: Optional[str] = None) -> None:
        super().__init__(extension=extension)

    def _get_opener(self) -> _Opener:
        return functools.partial(imageio.v3.imopen, plugin="pillow")


class _ImageIOPngBackend(_ImageIOPillowBackend):
    def __init__(self, *, compress: bool = True, extension: str = ".png") -> None:
        super().__init__(extension=extension)
        self.compress = compress

    def _get_writer_kwargs(self, image: Image[ImageDataTypes]) -> dict[str, object]:
        kwargs = super()._get_writer_kwargs(image)
        if not self.compress:
            kwargs["compress_level"] = 0
        return kwargs


class _ImageIOApngBackend(_ImageIOPngBackend):
    def __init__(self, *, compress: bool = True, fps: Optional[int] = None) -> None:
        super().__init__(compress=compress, extension=".apng")
        self._fps = fps

    def _get_writer_kwargs(self, image: Image[ImageDataTypes]) -> dict[str, object]:
        kwargs = super()._get_writer_kwargs(image)
        if self._fps:
            kwargs["duration"] = 1000 / self._fps
        return kwargs


class _ImageIOLegacyBackend(_ImageIOBackend):
    def __init__(
        self, *, imageio_format: Optional[str] = None, extension: Optional[str] = None
    ) -> None:
        super().__init__(extension=extension)
        self._imageio_format = imageio_format

    def _get_opener(self) -> _Opener:
        return functools.partial(imageio.v3.imopen, legacy_mode=True, plugin=self._imageio_format)


class _ImageIOFreeImageBackend(_ImageIOLegacyBackend):
    IO_FLAGS: ClassVar = imageio.plugins.freeimage.IO_FLAGS

    def __init__(self, *, imageio_format: str, extension: str) -> None:
        super().__init__(imageio_format=imageio_format, extension=extension)

    def _get_writer_kwargs(self, image: Image[ImageDataTypes]) -> dict[str, object]:
        kwargs = super()._get_writer_kwargs(image)
        kwargs["flags"] = self._get_flags(image)
        return kwargs

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        return 0


class _ImageIOExrBackend(_ImageIOFreeImageBackend):
    _fp_force_32_bits: ClassVar[
        ImageModifier[ImageDataTypes, ImageDataTypes]
    ] = FPPrecisionModifier(min=32, max=32)

    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(imageio_format="EXR-FI", extension=".exr")
        self.compress = compress

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        flags = 0
        flags |= self.IO_FLAGS.EXR_ZIP if self.compress else self.IO_FLAGS.EXR_NONE
        if not np.issubdtype(image.data().dtype, np.float16):
            flags |= self.IO_FLAGS.EXR_FLOAT
        return flags

    def _postprocess(self, image: Image[ImageDataTypes]) -> Image[ImageDataTypes]:
        return self._fp_force_32_bits(image)


class _ImageIOTgaBackend(_ImageIOFreeImageBackend):
    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(imageio_format="TARGA-FI", extension=".tga")
        self.compress = compress

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        flags = 0
        flags |= self.IO_FLAGS.TARGA_SAVE_RLE if self.compress else self.IO_FLAGS.TARGA_DEFAULT
        return flags


class _ImageIOTiffBackend(_ImageIOFreeImageBackend):
    _fp_force_32_bits: ClassVar[
        ImageModifier[ImageDataTypes, ImageDataTypes]
    ] = FPPrecisionModifier(min=32, max=32)

    def __init__(self, *, compress: bool = True) -> None:
        super().__init__(imageio_format="TIFF-FI", extension=".tiff")
        self.compress = compress

    def _get_flags(self, image: Image[ImageDataTypes]) -> int:
        flags = 0
        flags |= self.IO_FLAGS.TIFF_DEFAULT if self.compress else self.IO_FLAGS.TIFF_NONE
        return flags

    def _postprocess(self, image: Image[ImageDataTypes]) -> Image[ImageDataTypes]:
        return self._fp_force_32_bits(image)
