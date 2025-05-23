from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.content import Content
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

if TYPE_CHECKING:
    from avpack.encode_profile import EncodeProfile
    from avpack.internals.ffprobe import ProbeData


class MediaItem(Widget):
    """An item to encode"""

    highlighted = reactive(False)

    def __init__(self, input: str) -> None:
        super().__init__()
        self.input = input
        self.data = ProbeData.from_path(input)
        self.profile = EncodeProfile()

        self.INPUT_SECTION = Content.from_markup(
            "[bold]Input File:[/bold] $input\n[bold]Streams:[/bold] $streams",
            input=self.input,
            streams=self.data.format.nb_streams,
        )

    def compose(self) -> ComposeResult:
        self.set_class(self.highlighted, "selected")
        yield Static(self.INPUT_SECTION)


class MediaItemList(VerticalScroll):
    @dataclass
    class ItemAdded(Message):
        """Posted when item is added"""

        input_path: str
        list: MediaItemList
        item: MediaItem

        @property
        def control(self) -> MediaItemList:
            return self.list

    def add_item(self, path: str):
        new_item = MediaItem(path)
        self.post_message(self.ItemAdded(path, self, new_item))
        await_mount = self.mount(new_item)
        return await_mount

    @on(ItemAdded)
    def is_empty(self):
        self.set_class(len(self) == 0, "empty")

    def __len__(self) -> int:
        return len(self._nodes)
