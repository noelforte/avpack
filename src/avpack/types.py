from typing import Literal

# General types
type AudioSampleRate = Literal[44_100, 48_000, 96_000]

# libx264 types
type H264Profile = Literal["baseline", "main", "high"]
type H264Level = Literal[
    "1.0",
    "1.1",
    "1.2",
    "1.3",
    "2.0",
    "2.1",
    "2.2",
    "3.0",
    "3.1",
    "3.2",
    "4.0",
    "4.1",
    "4.2",
    "5.0",
    "5.1",
    "5.2",
    "6.0",
    "6.1",
    "6.2",
]

# AAC types
type AacProfile = Literal["aac_low", "mpeg2_aac_low", "aac_ltp", "aac_main"]

# pixel format types
type PixelFormat = Literal[
    "yuv420p",
    "yuv422p",
    "yuv444p",
    "nv12",
    "nv16",
    "nv21",
    "yuv420p10le",
    "yuv422p10le",
    "yuv444p10le",
    "nv20le",
    "gray",
    "gray10le",
]

# HLS types
type HlsMediaType = Literal["mpegts", "fmp4"]
type HlsVideoCodec = Literal["libx264", "libx265"]
type HlsAudioCodec = Literal["aac", "flac", "ac3", "eac3"]
