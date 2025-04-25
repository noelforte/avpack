from typing import TYPE_CHECKING, cast

from textual.command import DiscoveryHit, Hit, Hits, Provider
from textual.types import IgnoreReturnCallbackType

CommandType = tuple[str, IgnoreReturnCallbackType, str, bool]

if TYPE_CHECKING:
    from ffpack.app import Ffpack


class FfpackCommandProvider(Provider):
    """Common app commands for ffpack"""

    @property
    def commands(self) -> tuple[CommandType, ...]:
        screen = self.screen
        app = cast(Ffpack, screen.app)

        commands_to_show: list[CommandType] = []

        from ffpack.app import MainScreen

        # If on main screen
        if isinstance(screen, MainScreen):
            commands_to_show.append(
                (
                    "config: Set tool paths",
                    app.action_show_tools_config,
                    "Configure paths for ffmpeg/ffprobe",
                    True,
                )
            )

            commands_to_show.append(
                (
                    "help: Show keybindings sidebar",
                    app.action_show_help_panel,
                    "Display keybindings for the current screen in sidebar",
                    True,
                ),
            )

            commands_to_show.append(
                ("app: Quit Ffpack", app.action_quit, "Quit ffpack", True),
            )

        return tuple(commands_to_show)

    async def discover(self) -> Hits:
        """Handle a request for the discovery commands for this provider.

        Yields:
            Commands that can be discovered.
        """
        for name, runnable, help_text, show_discovery in self.commands:
            if show_discovery:
                yield DiscoveryHit(name, runnable, help=help_text)

    async def search(self, query: str) -> Hits:
        """Handle a request to search for commands that match the query.

        Args:
            query: The user input to be matched.

        Yields:
            Command hits for use in the command palette.
        """
        matcher = self.matcher(query)
        for name, runnable, help_text, _ in self.commands:
            if (match := matcher.match(name)) > 0:
                yield Hit(
                    match,
                    matcher.highlight(name),
                    runnable,
                    help=help_text,
                )
