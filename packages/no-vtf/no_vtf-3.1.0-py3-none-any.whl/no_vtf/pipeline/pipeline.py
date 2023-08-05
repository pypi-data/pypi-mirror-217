# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import pathlib
import re

from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Generic, Literal, Optional, TypeVar, overload

from no_vtf.image.channel_separator import ChannelSeparator
from no_vtf.image.image import Image, ImageDataTypes
from no_vtf.io.bytes import BytesIO
from no_vtf.io.image import ImageIO
from no_vtf.io.io import IO
from no_vtf.texture.decoder.decoder import TextureDecoder
from no_vtf.texture.extractor.extractor import TextureExtractor
from no_vtf.texture.filter.filter import TextureFilter
from no_vtf.texture.namer.namer import TextureNamer

_A_contra = TypeVar("_A_contra", contravariant=True)
_I = TypeVar("_I", bound=ImageDataTypes)
_T = TypeVar("_T")


@dataclass(frozen=True, kw_only=True)
class Pipeline(Generic[_T, _I]):
    @dataclass(frozen=True, kw_only=True)
    class Receipt:
        io_done: bool

    input_extension_pattern: Optional[re.Pattern[str]] = None

    FORMAT_RAW: Literal["raw"] = "raw"
    FORMAT_SKIP: Literal["skip"] = "skip"
    ldr_format: str
    hdr_format: str

    animate: bool = False
    fps: Optional[int] = None
    separate_channels: bool = False

    compress: Optional[bool] = None

    write: Optional[bool] = None
    readback: bool = False

    extractor: TextureExtractor[_T]
    filter: Optional[TextureFilter[_T]]
    decoder: TextureDecoder[_T, _I]
    namer: TextureNamer[_T]

    @classmethod
    def initialize(cls) -> None:
        IO.initialize()

    @overload
    def __call__(self, input_file: pathlib.Path, *, output_file: pathlib.Path) -> Pipeline.Receipt:
        ...

    @overload
    def __call__(
        self, input_file: pathlib.Path, *, output_directory: pathlib.Path
    ) -> Pipeline.Receipt:
        ...

    def __call__(
        self,
        input_file: pathlib.Path,
        *,
        output_file: Optional[pathlib.Path] = None,
        output_directory: Optional[pathlib.Path] = None,
    ) -> Pipeline.Receipt:
        textures = self.extractor(input_file)

        if self.filter:
            textures = self.filter(textures)

        images_by_output_path = self._group_images(
            textures, input_file, output_file=output_file, output_directory=output_directory
        )

        if not self.animate:
            io_done = self._process_individual(images_by_output_path)
        else:
            io_done = self._process_sequences(images_by_output_path)

        return Pipeline.Receipt(io_done=io_done)

    def _group_images(
        self,
        textures: Sequence[_T],
        input_file: pathlib.Path,
        *,
        output_file: Optional[pathlib.Path] = None,
        output_directory: Optional[pathlib.Path] = None,
    ) -> dict[pathlib.Path, list[Image[_I]]]:
        images_by_output_path: defaultdict[pathlib.Path, list[Image[_I]]] = defaultdict(list)
        for texture in textures:
            image = self.decoder(texture)

            image_format = self._get_image_format(image)
            if _compare_formats(image_format, self.FORMAT_SKIP):
                continue

            will_separate_channels = (
                not _compare_formats(image_format, self.FORMAT_RAW) and self.separate_channels
            )

            images = []
            if will_separate_channels:
                channel_separator = ChannelSeparator()
                images = list(channel_separator(image))
            else:
                images = [image]

            for image in images:
                image_output_file = output_file
                if image_output_file is None:
                    assert output_directory is not None, "output path must be set"
                    image_output_file = self._get_output_file(
                        input_file,
                        output_directory,
                        texture,
                        image,
                        name_channels=will_separate_channels,
                    )

                images_by_output_path[image_output_file].append(image)
        return images_by_output_path

    def _get_image_format(self, image: Image[_I]) -> str:
        image_format = self.hdr_format if image.dynamic_range == "hdr" else self.ldr_format
        return image_format

    def _get_output_file(
        self,
        input_file: pathlib.Path,
        output_directory: pathlib.Path,
        texture: _T,
        image: Image[_I],
        *,
        name_channels: bool,
    ) -> pathlib.Path:
        input_name = input_file.name
        if self.input_extension_pattern:
            input_name = re.sub(self.input_extension_pattern, "", input_name)

        output_name = self.namer(input_name, texture)
        if name_channels:
            output_name += "_" + image.channels
        output_name += "." + self._get_image_format(image)

        output_file = output_directory / output_name
        return output_file

    def _process_individual(
        self, images_by_output_path: dict[pathlib.Path, list[Image[_I]]]
    ) -> bool:
        io_done = False

        for image_output_path, images in images_by_output_path.items():
            for image in images:
                image_format = self._get_image_format(image)
                if _compare_formats(image_format, self.FORMAT_RAW):
                    assert image.raw, "image must have raw data set"
                    io_done = self._do_io(BytesIO(), image_output_path, [image.raw]) or io_done
                else:
                    image_io = ImageIO(format=image_format, compress=self.compress, fps=self.fps)
                    io_done = self._do_io(image_io, image_output_path, [image]) or io_done

        return io_done

    def _process_sequences(
        self, images_by_output_path: dict[pathlib.Path, list[Image[_I]]]
    ) -> bool:
        io_done = False

        for image_output_path, images in images_by_output_path.items():
            if not images:
                continue

            assert (
                len(set(map(self._get_image_format, images))) == 1
            ), "image format must be the same for all images"
            image_format = self._get_image_format(images[0])

            if _compare_formats(image_format, self.FORMAT_RAW):
                raw_sequence = []
                for image in images:
                    assert image.raw, "image must have raw data set"
                    raw_sequence.append(image.raw)

                io_done = self._do_io(BytesIO(), image_output_path, raw_sequence) or io_done
            else:
                if any(map(lambda image: image.dynamic_range == "hdr", images)):
                    raise RuntimeError("Animating HDR textures is not supported")

                image_io = ImageIO(format=image_format, compress=self.compress, fps=self.fps)
                io_done = self._do_io(image_io, image_output_path, images) or io_done

        return io_done

    def _do_io(self, io: IO[_A_contra], path: pathlib.Path, sequence: Sequence[_A_contra]) -> bool:
        io_done = False

        if self.write is not False:
            io_done = self._write(io, path, sequence) or io_done

        if self.readback:
            io.readback_sequence(path, sequence)
            io_done = True

        return io_done

    def _write(self, io: IO[_A_contra], path: pathlib.Path, sequence: Sequence[_A_contra]) -> bool:
        assert self.write is not False, "_write() must not be called when writing is disabled"
        skip_existing = self.write is None
        if skip_existing and path.is_file():
            return False

        path.parent.mkdir(parents=True, exist_ok=True)
        io.write_sequence(path, sequence)

        return True


def _compare_formats(a: str, b: str) -> bool:
    return a.lower() == b.lower()
