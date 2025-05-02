import asyncio
from typing import TYPE_CHECKING, cast

from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import HorizontalGroup, VerticalGroup
from textual.content import Content
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, Label, ProgressBar

from ffpack.widgets.sequence_label import SequenceLabel

if TYPE_CHECKING:
    from ffpack.app import Ffpack


class EncodeProgressScreen(ModalScreen[None]):
    BINDING_GROUP_TITLE = "Encoding Process Bindings"

    BINDINGS = [Binding("ctrl+q", "app.quit", "Quit", tooltip="Quit")]

    DEFAULT_CSS = """
    """

    AUTO_FOCUS = ""

    file_current = reactive(1)
    file_total = reactive(1)
    step_current = reactive(1)
    step_total = reactive(1)

    file_status = reactive("")
    step_status = reactive("")

    def compose(self) -> ComposeResult:
        with VerticalGroup(classes="modal-box"):
            with HorizontalGroup(id="files"):
                yield Label(self.file_status, classes="description")
                yield SequenceLabel()

            with HorizontalGroup(id="steps"):
                yield Label(self.step_status, classes="description")
                yield SequenceLabel()

            yield ProgressBar(id="progress")
            yield Button("Cancel", "default", action="cancel")

    def on_mount(self) -> None:
        self.query_one(ProgressBar).update(total=100)
        self.query_one("#files SequenceLabel", SequenceLabel).update(total=20)
        self.query_one("#steps SequenceLabel", SequenceLabel).update(total=4)
        self.start()

    @work(exclusive=True, exit_on_error=False)
    async def start(self) -> None:
        app = cast("Ffpack", self.app)

        progress = self.query_one(ProgressBar)
        await asyncio.sleep(1)
        for i in range(1, 21, 1):
            print(f"Iteration {i}")
            progress.update(progress=i * 5)
            if i == 10:
                self.query_one("#files SequenceLabel", SequenceLabel).update(
                    current=11
                )
                self.query_one("#steps SequenceLabel", SequenceLabel).update(
                    current=3
                )
            await asyncio.sleep(1)
