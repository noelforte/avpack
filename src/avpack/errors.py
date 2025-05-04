from textwrap import dedent

from textual.app import ComposeResult
from textual.containers import Center, Grid, VerticalGroup
from textual.content import Content
from textual.screen import ModalScreen
from textual.visual import VisualType
from textual.widgets import Button, Static


class ErrorModal(ModalScreen[None]):
    def __init__(self, message: VisualType) -> None:
        super().__init__()
        self.error_message = message

    def compose(self) -> ComposeResult:
        yield VerticalGroup(
            Static(self.error_message),
            Center(
                Button("OK", "error", action="app.pop_screen"),
            ),
        )
