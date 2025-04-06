from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer


class Ffpack(App[None]):
    """Main ffpack app class"""

    BINDINGS = [Binding("ctrl+q", "app.quit", "Quit", show=True, tooltip="Quit the application")]

    def compose(self) -> ComposeResult:
        yield Footer(show_command_palette=False)


def run() -> None:
    Ffpack().run()


if __name__ == "__main__":
    run()
