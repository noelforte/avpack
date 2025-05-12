from textual.app import ComposeResult
from textual.content import Content
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

from avpack.encode_profile import EncodeProfile
from avpack.internals.data import MediaData


class MediaItem(Widget):
    """An item to encode"""

    highlighted = reactive(False)

    def __init__(self, input: str) -> None:
        super().__init__()
        self.input = input
        self.data = MediaData.from_path(input)
        self.profile = EncodeProfile()

        self.INPUT_SECTION = Content.from_markup(
            "[bold]Input File:[/bold] $input\n[bold]Streams:[/bold] $streams",
            input=self.input,
            streams=self.data.format.nb_streams,
        )

    def compose(self) -> ComposeResult:
        self.set_class(self.highlighted, "selected")
        yield Static(self.INPUT_SECTION)
