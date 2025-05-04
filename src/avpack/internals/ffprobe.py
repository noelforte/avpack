import shutil
from subprocess import SubprocessError, run

from pydantic import BaseModel

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
    tags: dict[str, str]
    disposition: dict[str, bool]
    start_time: float


class VideoStream(Stream):
    """A video stream"""

    codec_type: str = "video"
    width: int
    height: int
    r_frame_rate: str


class AudioStream(Stream):
    """An audio stream"""

    codec_type: str = "audio"
    sample_rate: int
    channels: int
    channel_layout: str


class SubtitleStream(Stream):
    """A subtitle stream"""

    codec_type: str = "subtitle"


class Chapter(BaseModel):
    """A media chapter"""

    id: int
    time_base: str
    start: int
    end: int
    start_time: float
    end_time: float
    tags: dict[str, str]


class Format(BaseModel):
    """A media container format"""

    nb_streams: int
    start_time: float
    duration: float
    tags: dict[str, str]


class ProbeData(BaseModel):
    """An object containing ffprobe data"""

    streams: tuple[VideoStream | AudioStream | SubtitleStream | Stream, ...]
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
