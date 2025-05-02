from textual.content import Content
from textual.reactive import reactive
from textual.widget import Widget


class SequenceLabel(Widget):
    current: reactive[int] = reactive(1, layout=True)
    total: reactive[int] = reactive(1, layout=True)

    DEFAULT_CSS = """
    SequenceLabel {
        width: auto;
        height: auto;
    }
    """

    def __init__(
        self,
        total: int = 1,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        super().__init__(name=name, classes=classes, id=id, disabled=disabled)
        self.total = total

    def render(self):
        return Content.from_markup(
            "\\[$current/$total]", current=self.current, total=self.total
        )

    def update(self, current: int | None = None, total: int | None = None):
        if current is not None:
            self.current = current
        if total is not None:
            self.total = total

    def advance(self, amount: int):
        self.current += amount

    def validate_current(self, amount: int):
        if amount < 1:
            amount = 0
        elif amount > self.total:
            amount = self.total
        return amount
