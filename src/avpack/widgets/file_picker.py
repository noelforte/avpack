from textual.widgets import Input
from textual_fspicker import FileOpen, FileSave, SelectDirectory


class MediaFileOpen(FileOpen):
    def on_mount(self) -> None:
        super().on_mount()
        self.query_one(Input).placeholder = "Enter a file path"


class MediaFileSave(FileSave):
    def on_mount(self) -> None:
        super().on_mount()
        self.query_one(Input).placeholder = "Enter a file path"


class MediaDirectorySelect(SelectDirectory):
    def on_mount(self) -> None:
        super().on_mount()
        self.query_one(Input).placeholder = "Enter a file path"
