import json
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
    start_time: float


class VideoStream(Stream):
    """A video stream"""

    width: int
    height: int
    r_frame_rate: str


class AudioStream(Stream):
    """An audio stream"""

    sample_rate: int
    channels: int
    channel_layout: str


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


class ProbeData:
    """An object containing ffprobe data"""

    streams: list[VideoStream | AudioStream | Stream]
    chapters: list[Chapter]
    format: Format

    def __init__(self, input: str):
        if FFPROBE is None:
            raise SubprocessError("ffprobe not found")

        probe = run(
            [FFPROBE, *FFPROBE_ARGS, input], capture_output=True, check=True
        )
        data = json.loads(probe.stdout)

        print(data)

        self.format = Format(**data["format"])
        self.chapters = [Chapter(**entry) for entry in data["chapters"]]
        self.streams = [
            VideoStream(**entry)
            if entry["codec_type"] == "video"
            else AudioStream(**entry)
            if entry["codec_type"] == "audio"
            else Stream(**entry)
            for entry in data["streams"]
        ]
