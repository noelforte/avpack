from typing import Any

from pydantic_core import ValidationError
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer, Label

from ffpack import VERSION
from ffpack.commands import FfpackCommandProvider
from ffpack.internals.tools import FfTools, ToolsConfigScreen
from ffpack.widgets import EncodingQueue


class AppHeader(Horizontal):
    def compose(self) -> ComposeResult:
        yield Label(f"[b]ffpack[/b] [dim]v{VERSION}[/dim]", id="app-title")


class MainScreen(Screen[None]):
    def compose(self) -> ComposeResult:
        yield AppHeader()
        yield EncodingQueue()
        yield Footer(show_command_palette=False)


class Ffpack(App[None], inherit_bindings=False):
    """Main ffpack app class"""

    ALLOW_SELECT = False
    COMMANDS = {FfpackCommandProvider}
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
    CSS_PATH = "ffpack.tcss"

    tools: FfTools

    def on_mount(self) -> None:
        # Set default theme
        self.theme = "textual-dark"

        # Attempt to auto-detect tools
        self.tools = FfTools.auto_detect()

        try:
            FfTools.model_validate(self.tools, from_attributes=True)
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
    Ffpack().run()


if __name__ == "__main__":
    run()
