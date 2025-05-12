import os
import shutil
from typing import TYPE_CHECKING, cast

from pydantic import BaseModel, ValidationError, field_validator
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, HorizontalGroup
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Input, Label

if TYPE_CHECKING:
    from avpack.app import AVPack


class ExternalTools(BaseModel):
    ffmpeg: str = ""
    ffprobe: str = ""
    model_config = {"revalidate_instances": "always"}

    @classmethod
    def auto_detect(cls):
        return cls.model_construct(
            ffmpeg=shutil.which("ffmpeg"), ffprobe=shutil.which("ffprobe")
        )

    @field_validator("*", mode="after")
    @classmethod
    def validate_cmd(cls, value: str):
        if (
            os.access(value, os.X_OK)
            and os.path.isabs(value)
            and os.path.isfile(value)
        ):
            return value
        raise ValueError(f"`{value}` is not executable")


class ToolsConfigScreen(ModalScreen[ExternalTools]):
    BINDING_GROUP_TITLE = "Tools Config Bindings"
    BINDINGS = [
        Binding(
            "escape",
            "dismiss",
            "Cancel",
            tooltip="Cancel and return to main screen",
        ),
        Binding(
            "ctrl+s", "save", "Save config", tooltip="Save and apply config"
        ),
    ]
    DEFAULT_CSS = """
    ToolsConfigScreen {
        align: center middle;
    }

    #form {
        grid-gutter: 0 1;
        grid-rows: 1 2;
        grid-size: 2;
        layout: grid;
    }

    .input-label-row {
        column-span: 2;
    }
    """

    def compose(self) -> ComposeResult:
        app = cast("AVPack", self.app)

        with Container(id="form", classes="modal-box") as container:
            container.border_title = "Configure 'ff' tool paths"

            with HorizontalGroup(classes="input-label-row"):
                yield Label("Path to `ffmpeg`")
                yield Label(
                    "Path is not valid",
                    id="ffmpeg-error-label",
                    classes="error-label",
                )

            yield Input(app.tools.ffmpeg, classes="tool-path", id="ffmpeg-path")

            with HorizontalGroup(classes="input-label-row"):
                yield Label("Path to `ffprobe`")
                yield Label(
                    "Path is not valid",
                    id="ffprobe-error-label",
                    classes="error-label",
                )

            yield Input(
                app.tools.ffprobe, classes="tool-path", id="ffprobe-path"
            )

            yield Button("Save", "success", action="screen.save")
            yield Button("Auto-detect", "default", action="screen.auto_detect")

        yield Footer(show_command_palette=False)

    def action_save(self):
        try:
            self.dismiss(
                ExternalTools(
                    ffmpeg=self.ffmpeg_path.value,
                    ffprobe=self.ffprobe_path.value,
                )
            )
        except ValidationError as invalid:
            for error in invalid.errors():
                invalid_field = error.get("loc")[0]
                self.query_one(f"#{invalid_field}-path", Input).add_class(
                    "-invalid"
                )
                self.query_one(
                    f"#{invalid_field}-error-label", Label
                ).styles.display = "block"

    def action_auto_detect(self):
        detected = ExternalTools.auto_detect()
        self.ffmpeg_path.value = detected.ffmpeg
        self.ffprobe_path.value = detected.ffprobe

    @property
    def ffmpeg_path(self) -> Input:
        return self.query_one("#ffmpeg-path", Input)

    @property
    def ffprobe_path(self) -> Input:
        return self.query_one("#ffprobe-path", Input)
