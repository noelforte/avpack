from pydantic import BaseModel

from avpack.outputs.muxers import Format, Hls, Mpeg4
from avpack.outputs.previews import TimelinePreview
from avpack.outputs.streams import AudioOutput, MuxedOutput, VideoOutput


class EncodeProfile(BaseModel):
    upscale: bool = False
    timeline_previews: TimelinePreview | None = TimelinePreview()
    muxers: list[Format] = [
        Hls.from_streams(
            MuxedOutput(
                video=VideoOutput(
                    height=2160, bitrate=18000, profile="high", level="5.2"
                ),
                audio=AudioOutput(bitrate=256, profile="aac_low"),
            ),
            MuxedOutput(
                video=VideoOutput(
                    height=1440, bitrate=10000, profile="high", level="5.2"
                ),
                audio=AudioOutput(bitrate=256, profile="aac_low"),
            ),
            MuxedOutput(
                video=VideoOutput(
                    height=1080, bitrate=6000, profile="high", level="5.1"
                ),
                audio=AudioOutput(bitrate=256, profile="aac_low"),
            ),
            MuxedOutput(
                video=VideoOutput(
                    height=720, bitrate=3000, profile="high", level="4.2"
                ),
                audio=AudioOutput(bitrate=128, profile="aac_low"),
            ),
            MuxedOutput(
                video=VideoOutput(
                    height=480, bitrate=1500, profile="main", level="4.0"
                ),
                audio=AudioOutput(bitrate=96, profile="aac_low"),
            ),
            MuxedOutput(
                video=VideoOutput(
                    height=360, bitrate=800, profile="main", level="3.1"
                ),
                audio=AudioOutput(bitrate=64, profile="aac_low"),
            ),
            MuxedOutput(
                video=VideoOutput(
                    height=240, bitrate=600, profile="main", level="3.1"
                ),
                audio=AudioOutput(bitrate=48, profile="aac_low"),
            ),
        ),
        Mpeg4(output=[]),
    ]
