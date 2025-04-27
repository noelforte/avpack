from dataclasses import dataclass

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.message import Message
from textual.reactive import reactive
from textual.widget import AwaitMount
from textual.widgets import Label

from ffpack.widgets.center_middle import CenterMiddle
from ffpack.widgets.media_item import MediaItem


class EncodingQueue(Vertical):
    BINDINGS = [
        Binding("a", "add_item", "Add item"),
        Binding("backspace", "item_delete", "Delete item"),
        Binding("up", "cursor_up", "Select previous item"),
        Binding("down", "cursor_down", "Select previous item"),
    ]

    can_focus = True
    can_focus_children = False

    index = reactive[int | None](None, init=False)
    """The index of the currently highlighted item."""

    @dataclass
    class ItemsChanged(Message):
        path: str

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

    def action_add_item(self, path: str) -> AwaitMount:
        self.post_message(self.ItemsChanged(path))
        return self.queue.mount(MediaItem(path))

    @on(ItemsChanged)
    def set_empty_state(self) -> None:
        self.set_class(self.items_count == 0, "empty")

    @property
    def items_count(self):
        return len(self.queue._nodes)
