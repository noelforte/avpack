from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.message import Message
from textual.reactive import reactive
from textual.widget import AwaitMount
from textual.widgets import Label

from .center_middle import CenterMiddle
from .file_picker import MediaFileOpen
from .media_item import MediaItem

if TYPE_CHECKING:
    from avpack.app import AVPack


class EncodingQueue(Vertical):
    BINDINGS = [
        Binding("a", "add", "Add item"),
        Binding("backspace", "delete", "Delete item"),
        Binding("up", "next", "Select previous item"),
        Binding("down", "prev", "Select previous item"),
    ]

    can_focus = True
    can_focus_children = False

    index = reactive[int | None](None, init=False)
    """The index of the currently highlighted item."""

    @dataclass
    class ItemsChanged(Message):
        path: str

    @on(ItemsChanged)
    def set_empty_state(self) -> None:
        self.set_class(self.items_count == 0, "empty")
        self.refresh_bindings()

    @work
    async def action_add(self) -> AwaitMount | None:
        app = cast("AVPack", self.app)

        if file := await app.push_screen_wait(
            MediaFileOpen(location="~", title="Add an item to encode")
        ):
            path = file.as_posix()
            self.post_message(self.ItemsChanged(path))
            return self.queue.mount(MediaItem(path))

    @property
    def items_count(self):
        return len(self.queue._nodes)

    def __init__(
        self,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(id=id, classes=classes, disabled=disabled)
        self.queue = VerticalScroll(id="queue")

    def compose(self) -> ComposeResult:
        self.set_empty_state()
        yield CenterMiddle(Label("No items to encode"), id="empty-message")
        yield self.queue

    def check_action(
        self, action: str, parameters: tuple[object, ...]
    ) -> bool | None:
        """Check if an action may run."""
        return not (
            action in ("next", "prev", "delete") and self.items_count == 0
        )
