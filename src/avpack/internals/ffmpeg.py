import re
import subprocess
from collections.abc import Iterable
from subprocess import PIPE, Popen
from typing import Any

from avpack.internals.data import MediaData

TOTAL_DURATION = 60.026633


__TIMESTAMP_PATTERN = re.compile(
    r"^(?P<h>\d+):(?P<m>\d+):(?P<s>[\d]+).(?P<ms>\d+)"
)
__PROGRESS_PATTERN = re.compile(r"progress=\w+")


class FFMpegEncoder:
    def __init__(
        self,
        input: MediaData,
        profile: EncodeProfile | None = None,
        dry_run: bool = False,
    ) -> None:
        self.bin = "ffmpeg"
        self.args = ["-progress", "-", "-nostats"]
        self.process: Popen[bytes] | None = None
        self.input = input
        self.dry_run = dry_run
        self.profile = profile or EncodeProfile()

    # Given ffmpeg input, return current progress as a float
    def get_progress(self, data: str):
        match = __TIMESTAMP_PATTERN.match(data)

        if match is None:
            return

        hours, minutes, seconds = match.groups()

        return sum(
            [
                float(hours) * 3600,  # compute hours
                float(minutes) * 60,  # compute minutes
                float(seconds),  # compute seconds
            ]
        )

    def run(
        self,
        duration_override: float | None = None,
        **extra: Any,
    ) -> Iterable[float]:
        """
        Run ffmpeg with an optional duration override
        """

        if self.dry_run:
            yield from [0, 100]

        if duration_override:
            self.input.format.duration = duration_override

        self.process = subprocess.Popen(
            TEST_ARGS,
            universal_newlines=False,
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
        )

        yield 0

        while True:
            if self.process.stdout is None:
                continue

            line = (
                self.process.stdout.readline()
                .decode("utf-8", errors="replace")
                .strip()
            )

            if line == "" and self.process.poll() is not None:
                break

            progress = self.get_progress(line)
            if progress is not None:
                yield progress

        if self.process.returncode != 0:
            raise RuntimeError(f"Error running ffmpeg: {self.process.stderr}")

        yield 100
        self.process = None

    def quit(self) -> None:
        if self.process is None:
            raise RuntimeError("No process found. Did you run the command?")

        self.process.communicate(b"q")
        self.process.wait()
        self.process = None
