from typing import Annotated, Any, ClassVar

from pydantic import BaseModel, Field, PositiveInt

from avpack.types import (
    AacProfile,
    H264Level,
    H264Profile,
    HlsAudioCodec,
    HlsMediaType,
    HlsVideoCodec,
    PixelFormat,
)


# Outputs
class VideoOutput(BaseModel):
    """A video output"""

    height: Annotated[int, Field(description="Video frame height")]
    width: Annotated[int, Field(description="Video frame width")] = -2
    bitrate: Annotated[PositiveInt, Field(description="Video bitrate")]
    profile: Annotated[
        H264Level, Field(description="Encoding profile for libx264")
    ]
    level: Annotated[H264Profile, Field(description="Level for libx264")]
    pixel_format: Annotated[
        PixelFormat, Field(description="Pixel format to use")
    ] = "yuv420p"


class AudioOutput(BaseModel):
    """An audio output"""

    bitrate: Annotated[PositiveInt, Field(description="Audio bitrate")]
    profile: Annotated[
        AacProfile, Field(description="Encoding profile for aac")
    ] = "aac_low"


class MediaOutput(BaseModel):
    """A media output"""

    video: VideoOutput | None = None
    audio: AudioOutput | None = None


# Muxers
class Format[VCodec = Any, ACodec = Any](BaseModel):
    """Base class for muxing an output or set of outputs"""

    name: ClassVar[str]
    """The format name ffmpeg expects"""

    video_codec: Annotated[VCodec, Field(description="Video codec to use")]
    audio_codec: Annotated[ACodec, Field(description="Audio codec to use")]

    outputs: list[MediaOutput]


class Hls(Format):
    """A HLS muxer specification"""

    name: ClassVar[str] = "hls"

    type: Annotated[HlsMediaType, Field(description="Media type to use")] = (
        "mpegts"
    )
    interval: Annotated[
        PositiveInt, Field(description="Length of each segment")
    ] = 4
    segment_name: Annotated[
        str, Field(description="Segment naming template")
    ] = "[stream]/segment_[index]"
    root_playlist: Annotated[
        str, Field(description="Main playlist name", pattern=r"[\w\d]+\.m3u8$")
    ] = "manifest.m3u8"
    video_codec: HlsVideoCodec = "libx264"
    audio_codec: HlsAudioCodec = "aac"


class Mpeg4(Format[str, str]):
    """An MPEG-4 muxer specification"""

    name: ClassVar[str] = "hls"
    video_codec: str = "libx264"
    audio_codec: str = "aac"


# Timeline previews
class TimelinePreview(BaseModel):
    """A timeline preview specification"""

    columns: Annotated[
        PositiveInt, Field(description="Number of images to use per row")
    ] = 6
    tile_height: Annotated[
        PositiveInt, Field(description="Height of each generated thumnail")
    ] = 144
    interval_min: Annotated[
        PositiveInt,
        Field(
            description=(
                "Minimum interval in seconds between"
                "preview frames before increasing image count"
            )
        ),
    ] = 1
    interval_max: Annotated[
        PositiveInt,
        Field(
            description=(
                "Maximum interval in seconds between"
                "preview frames before increasing image count"
            )
        ),
    ] = 5
    max_images: Annotated[
        PositiveInt,
        Field(
            description=(
                "Maximum number of images to generate. Once reached"
                "frames will become more spaced out"
            )
        ),
    ] = 180


class EncodeProfile(BaseModel):
    upscale: bool = False
    timeline_previews: TimelinePreview | None = TimelinePreview()
    muxers: list[Format] = [
        Hls(
            outputs=[
                MediaOutput(
                    video=VideoOutput(
                        height=2160, bitrate=18000, profile="high", level="5.2"
                    ),
                    audio=AudioOutput(bitrate=256, aac_profile="aac_low"),
                ),
                MediaOutput(
                    video=VideoOutput(
                        height=1440, bitrate=10000, profile="high", level="5.2"
                    ),
                    audio=AudioOutput(bitrate=256, aac_profile="aac_low"),
                ),
                MediaOutput(
                    video=VideoOutput(
                        height=1080, bitrate=6000, profile="high", level="5.1"
                    ),
                    audio=AudioOutput(bitrate=256, aac_profile="aac_low"),
                ),
                MediaOutput(
                    video=VideoOutput(
                        height=720, bitrate=3000, profile="high", level="4.2"
                    ),
                    audio=AudioOutput(bitrate=128, aac_profile="aac_low"),
                ),
                MediaOutput(
                    video=VideoOutput(
                        height=480, bitrate=1500, profile="main", level="4.0"
                    ),
                    audio=AudioOutput(bitrate=96, aac_profile="aac_low"),
                ),
                MediaOutput(
                    video=VideoOutput(
                        height=360, bitrate=800, profile="main", level="3.1"
                    ),
                    audio=AudioOutput(bitrate=64, aac_profile="aac_low"),
                ),
                MediaOutput(
                    video=VideoOutput(
                        height=240, bitrate=600, profile="main", level="3.1"
                    ),
                    audio=AudioOutput(bitrate=48, aac_profile="aac_low"),
                ),
            ]
        )
    ]


# # Package profile
# class EncodeProfile(BaseModel):
#     stream: HlsStream = HlsStream()
#     outputs: list[MediaOutput] = [
#     ]
#     skip_upscale: bool = True
#     # timeline previews
#     # package output path
