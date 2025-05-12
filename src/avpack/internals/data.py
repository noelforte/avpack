import shutil
from subprocess import SubprocessError, run
from typing import Annotated

from pydantic import BaseModel, Discriminator, Tag

FFPROBE = shutil.which("ffprobe")
FFPROBE_ARGS = [
    "-of",
    "json",
    "-show_streams",
    "-show_chapters",
    "-show_format",
]


class Stream(BaseModel):
    """A generic stream"""

    index: int
    codec_type: str
    time_base: str
    tags: dict[str, str] | None = None
    disposition: dict[str, bool] | None = None
    start_time: float | None = None


class VideoStream(Stream):
    """A video stream"""

    width: int
    height: int
    r_frame_rate: str


class AudioStream(Stream):
    """An audio stream"""

    sample_rate: int
    channels: int
    channel_layout: str | None = None


class SubtitleStream(Stream):
    """A subtitle stream"""


class Chapter(BaseModel):
    """A media chapter"""

    id: int
    time_base: str
    start: int
    end: int
    start_time: float
    end_time: float
    tags: dict[str, str] | None = None


class Format(BaseModel):
    """A media container format"""

    nb_streams: int
    duration: float
    start_time: float | None = None
    tags: dict[str, str] | None = None


def disambiguate_stream_types(v: dict[str, str] | Stream):
    codec = v.get("codec_type") if isinstance(v, dict) else v.codec_type
    return codec if codec in ("video", "audio", "subtitle") else "..."


class MediaData(BaseModel):
    """An object containing ffprobe data"""

    streams: tuple[
        Annotated[
            Annotated[VideoStream, Tag("video")]
            | Annotated[AudioStream, Tag("audio")]
            | Annotated[SubtitleStream, Tag("subtitle")]
            | Annotated[Stream, Tag("...")],
            Discriminator(disambiguate_stream_types),
        ],
        ...,
    ]
    chapters: tuple[Chapter, ...]
    format: Format

    @classmethod
    def from_path(cls, input: str):
        if FFPROBE is None:
            raise SubprocessError("ffprobe not found")

        probe = run(
            [FFPROBE, *FFPROBE_ARGS, input], capture_output=True, check=True
        )

        return cls.model_validate_json(probe.stdout)

    @property
    def video_streams(self) -> tuple[VideoStream, ...]:
        return tuple(
            stream for stream in self.streams if isinstance(stream, VideoStream)
        )

    @property
    def audio_streams(self) -> tuple[AudioStream, ...]:
        return tuple(
            stream for stream in self.streams if isinstance(stream, AudioStream)
        )

    @property
    def subtitle_streams(self) -> tuple[SubtitleStream, ...]:
        return tuple(
            stream
            for stream in self.streams
            if isinstance(stream, SubtitleStream)
        )
