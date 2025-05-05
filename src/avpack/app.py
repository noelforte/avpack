from typing import Any

from pydantic_core import ValidationError
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer, Label

from avpack import VERSION
from avpack.commands import AVPackCommandProvider
from avpack.internals.tools import FFTools, ToolsConfigScreen
from avpack.widgets.encoding_queue import EncodingQueue


class AppHeader(Horizontal):
    def compose(self) -> ComposeResult:
        yield Label(f"[b]avpack[/b] [dim]v{VERSION}[/dim]", id="app-title")


class MainScreen(Screen[None]):
    def compose(self) -> ComposeResult:
        yield AppHeader()
        yield EncodingQueue()
        yield Footer(show_command_palette=False)


class AVPack(App[None], inherit_bindings=False):
    """Main avpack app class"""

    ALLOW_SELECT = False
    COMMANDS = {AVPackCommandProvider}
    BINDING_GROUP_TITLE = "Global Keybinds"
    BINDINGS = [
        Binding(
            "ctrl+q",
            "app.quit",
            "Quit",
            show=True,
            tooltip="Quit the application",
        ),
        Binding(
            "ctrl+p",
            "command_palette",
            "Commands",
            show=True,
            tooltip="Show command palette",
        ),
    ]
    CSS_PATH = "avpack.tcss"

    tools: FFTools

    def on_mount(self) -> None:
        # Set default theme
        self.theme = "textual-dark"

        # Attempt to auto-detect tools
        self.tools = FFTools.auto_detect()

        try:
            FFTools.model_validate(self.tools, from_attributes=True)
        except ValidationError:
            self.notify(
                "Ensure `ffmpeg` and `ffprobe` are on your $PATH "
                "or set their paths manually.\n\n"
                "[@click=app.show_tools_config]Configure Tools[/]",
                title="Missing commands",
                severity="error",
                timeout=10,
                markup=True,
            )

    def get_default_screen(self) -> Screen[Any]:
        return MainScreen()

    def action_show_tools_config(self) -> None:
        self.push_screen(ToolsConfigScreen())


def run() -> None:
    AVPack().run()


if __name__ == "__main__":
    run()
