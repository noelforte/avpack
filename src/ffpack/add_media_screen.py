from textual.binding import Binding
from textual.screen import ModalScreen


class AddMediaScreen(ModalScreen[str]):
    """A screen requesting media items to add"""

    BINDINGS = [
        Binding("escape", "dismiss", "Cancel", tooltip="Cancel and return to main screen"),
        Binding("ctrl+s", "apply", "Save config", tooltip=""),
    ]
