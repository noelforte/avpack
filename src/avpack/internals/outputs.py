from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt

from avpack.types import AudioSampleRate, PixelFormat


class VideoOutput(BaseModel):
    """A video output"""

    bitrate: Annotated[PositiveInt, Field(description="Video bitrate in kbps")]
    height: Annotated[int, Field(description="Video frame height")]
    level: Annotated[str, Field(description="Level for libx264")]
    pixel_format: Annotated[
        PixelFormat, Field(description="Pixel format to use")
    ] = "yuv420p"
    profile: Annotated[str | None, Field(description="Video profile to use")]
    width: Annotated[int, Field(description="Video frame width")] = -2


class AudioOutput(BaseModel):
    """An audio output"""

    bitrate: Annotated[PositiveInt, Field(description="Audio bitrate in kbps")]
    channels: Annotated[
        PositiveInt, Field(description="Number of audio channels")
    ] = 2
    profile: Annotated[
        str | None, Field(description="Audio profile to use")
    ] = None
    sample_rate: Annotated[
        AudioSampleRate, Field(description="Audio sample rate")
    ] = 48000
