"""Usefully filters to use in your handlers."""
from __future__ import annotations

__all__ = (
    "FilterCombine",
    "TextFilter",
    "ImageFilter",
    "VideoFilter",
    "AudioFilter",
    "DocumentFilter",
    "StickerFilter",
    "ReactionFilter",
    "UnsupportedMsgFilter",
    "LocationFilter",
    "ContactsFilter",
    "CallbackFilter",
    "MessageStatusFilter"
)

import re
from typing import Callable, TYPE_CHECKING, Iterable, TypeVar, TypeAlias, Type
from pywa import utils
from pywa.errors import WhatsAppError, ReEngagementMessage, MessageUndeliverable
from pywa.types import MessageType as Mt, Message as Msg, MessageStatus as Ms, MessageStatusType as Mst, \
    CallbackButton, CallbackSelection

if TYPE_CHECKING:
    from pywa import WhatsApp as Wa

    MessageT: TypeAlias = Callable[[Wa, Msg], bool]
    CallbackT: TypeAlias = Callable[[Wa, CallbackButton | CallbackSelection], bool]
    MessageStatusT: TypeAlias = Callable[[Wa, Ms], bool]

T = TypeVar("T")


class FilterCombine:
    """
    Combine filters with ``and`` & ``or`` like operators.

    If you need to combine filters with ``and`` or ``or``, use ``FilterCombine.all`` or ``FilterCombine.any``.

    Here are some examples:

    >>> from pywa.filters import FilterCombine as FC  # short name for convenience

    Matches messages that start with "Hello" and end with "World" or have a length between 1 and 10:

    >>> FC.all(TextFilter.startswith("Hello"), FC.any(TextFilter.endswith("World"), TextFilter.length((1, 10))))

    Matches messages that are either images or videos with a caption:

    >>> FC.any(ImageFilter.ANY, FC.all(VideoFilter.mimetype("video/mp4"), VideoFilter.HAS_CAPTION))

    Keep in mind that all macth-filters (``match``, ``startswith``, ``endswith``, ``contains`` etc.) returns True if
    any of the given matches are found. so there is no need to use ``FC.any`` with them.
    """

    @staticmethod
    def all(*filters: Callable[[Wa, T], bool]) -> Callable[[Wa, T], bool]:
        """
        Filter for messages that pass all the given filters.

        >>> FilterCombine.all(TextFilter.startswith("World"), TextFilter.contains("Word"))
        """
        return lambda wa, m: all(f(wa, m) for f in filters)

    @staticmethod
    def any(*filters: Callable[[Wa, T], bool]) -> Callable[[Wa, T], bool]:
        """
        Filter for messages that pass any of the given filters.

        >>> FilterCombine.any(TextFilter.contains("Hello"), TextFilter.contains("World"))
        """
        return lambda wa, m: any(f(wa, m) for f in filters)


class _BaseUpdateFilter:

    __message_types__: tuple[Mt, ...] = ()
    
    @classmethod
    def _match_type(cls, m: Msg) -> bool:
        return m.type in cls.__message_types__

    @classmethod
    def from_user(cls, *numbers: str) -> MessageT:
        """
        Filter for messages that are sent from the given numbers.
            - Aliases: ``from_numbers``, ``from_number``

        >>> TextFilter.from_user("1234567890", "0987654321")
        """
        only_nums_pattern = re.compile(r"\D")
        numbers = tuple(re.sub(only_nums_pattern, "", n) for n in numbers)
        return lambda wa, m: cls._match_type(m) and any(n == m.from_user.wa_id for n in numbers)

    from_users = from_user  # alias
    from_number = from_user  # alias
    from_numbers = from_user  # alias


class _UpdateWithForwardedFilter(_BaseUpdateFilter):
    FORWARDED: MessageT = lambda wa, m: m.forwarded
    """Filter for forwarded messages."""


class _MediaFilter(_UpdateWithForwardedFilter):

    @classmethod
    def mimetype(cls, *mime_types: str) -> MessageT:
        """
        Filter for media messages that match any of the given mime types.
        See https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media#supported-media-types

            - Aliases: ``mimetypes``, ``mime_type``, ``mime_types``

        >>> ImageFilter.mimetype("image/png")
        >>> VideoFilter.mimetypes("video/mp4", "video/3gpp")
        >>> AudioFilter.mimetypes("audio/mpeg", "audio/ogg")
        >>> DocumentFilter.mimetypes("application/pdf", "application/msword")
        >>> StickerFilter.mime_type("image/webp")
        """
        return lambda wa, m: cls._match_type(m) and any(
            t == getattr(m, cls.__message_types__[0].value).mime_type for t in mime_types
        )

    mimetypes = mimetype  # alias
    mime_type = mimetype  # alias
    mime_types = mimetype  # alias


class _MediaWithCaptionFilter(_MediaFilter):
    @classmethod
    def _has_caption(cls, wa: Wa, m: Msg) -> bool:
        return m.type == cls.__message_types__[0] and m.caption is not None

    HAS_CAPTION: MessageT = _has_caption
    """Filter for media messages that have a caption."""


class TextFilter(_UpdateWithForwardedFilter):
    """Useful filters for text messages."""
    
    __message_types__ = (Mt.TEXT,)

    ANY: MessageT = lambda wa, m: m.type == Mt.TEXT
    """Filter for all text messages."""

    @staticmethod
    def match(*matches: str, ignore_case: bool = False) -> MessageT:
        """
        Filter for text messages that match exactly the given text/s.
            - Aliases: ``same_as``, ``matches``, ``equals``

        >>> TextFilter.match("Hello", "Hi")

        Args:
            matches: The text/s to filter for.
            ignore_case: Whether to ignore case when matching (default: ``False``).
        """
        matches = tuple(m.lower() for m in matches) if ignore_case else matches
        return lambda wa, m: TextFilter._match_type(m) and any(
            (m.text.lower() if ignore_case else m.text) == t for t in matches
        )

    same_as = match  # alias
    matches = match # alias
    equals = match  # alias

    @staticmethod
    def contain(*matches: str, ignore_case: bool = False) -> MessageT:
        """
        Filter for text messages that contain the given text/s.
            - Aliases: ``contains``, ``include``, ``includes``

        >>> TextFilter.contain("Cat", "Dog", ignore_case=True)

        Args:
            matches: The text/s to filter for.
            ignore_case: Whether to ignore case when matching. (default: ``False``).
        """
        matches = tuple(m.lower() for m in matches) if ignore_case else matches
        return lambda wa, m: TextFilter._match_type(m) and any(
            t in (m.text.lower() if ignore_case else m.text) for t in matches
        )

    contains = contain  # alias
    include = contain  # alias
    includes = contain  # alias

    @staticmethod
    def startswith(*matches: str, ignore_case: bool = False) -> MessageT:
        """
        Filter for text messages that start with the given text/s.

        >>> TextFilter.startswith("What", "When", ignore_case=True)

        Args:
            matches: The text/s to filter for.
            ignore_case: Whether to ignore case when matching (default: ``False``).
        """
        matches = tuple(m.lower() for m in matches) if ignore_case else matches
        return lambda wa, m: TextFilter._match_type(m) and any(
            (m.text.lower() if ignore_case else m.text).startswith(t) for t in matches
        )

    @staticmethod
    def endswith(*matches: str, ignore_case: bool = False) -> MessageT:
        """
        Filter for text messages that end with the given text/s.

        >>> TextFilter.endswith("Bye", "See you", ignore_case=True)

        Args:
            matches: The text/s to filter for.
            ignore_case: Whether to ignore case when matching (default: ``False``).
        """
        matches = tuple(m.lower() for m in matches) if ignore_case else matches
        return lambda wa, m: TextFilter._match_type(m) and any(
            (m.text.lower() if ignore_case else m.text).endswith(t) for t in matches
        )

    @staticmethod
    def regex(*patterns: str | re.Pattern, flags: int = 0) -> MessageT:
        """
        Filter for text messages that match the given regex/regexes.
            - Aliases: ``regexes``, ``pattern``, ``patterns``

        >>> TextFilter.regex(r"Hello\s+World", r"Bye\s+World", flags=re.IGNORECASE)

        Args:
            patterns: The regex/regexes to filter for.
            flags: The regex flags to use (default: ``0``).
        """
        patterns = tuple(re.compile(p, flags) if isinstance(p, str) else p for p in patterns)
        return lambda wa, m: TextFilter._match_type(m) and any(re.match(p, m.text, flags) for p in patterns)

    regexes = regex  # alias
    pattern = regex  # alias
    patterns = regex  # alias

    @staticmethod
    def length(*lengths: tuple[int, int]) -> MessageT:
        """
        Filter for text messages that have a length between the given range/s.
            - Aliases: ``length_between``

        >>> TextFilter.length((1, 10), (50, 100))

        Args:
            lengths: The length range/s to filter for (e.g. (1, 10), (50, 100)).
        """
        return lambda wa, m: TextFilter._match_type(m) and any(i[0] <= len(m.text) <= i[1] for i in lengths)

    length_between = length  # alias

    @staticmethod
    def command(*cmds: str, prefixes: str | Iterable[str] = "!", ignore_case: bool = False) -> MessageT:
        """
        Filter for text messages that are commands.
            - Aliases: ``commands``, ``cmd``, ``cmds``

        >>> TextFilter.command("start", "hello", prefixes=("!", "/"), ignore_case=True)

        Args:
            cmds: The command/s to filter for (e.g. "start", "hello").
            prefixes: The prefix/s to filter for (default: "!", i.e. "!start").
            ignore_case: Whether to ignore case when matching (default: ``False``).
        """
        cmds = tuple(c.lower() for c in cmds) if ignore_case else cmds
        return lambda wa, m: TextFilter._match_type(m) and any(
            m.text[0] in prefixes and (m.text[1:].lower() if ignore_case else m.text[1:]).startswith(c for c in cmds)
        )
    commands = command  # alias
    cmd = command  # alias
    cmds = command  # alias


class ImageFilter(_MediaWithCaptionFilter):
    """Useful filters for image messages."""

    __message_types__ = (Mt.IMAGE,)

    ANY: MessageT = lambda wa, m: ImageFilter._match_type(m)
    """Filter for all image messages."""


class VideoFilter(_MediaWithCaptionFilter):
    """Useful filters for video messages."""

    __message_types__ = (Mt.VIDEO,)

    ANY: MessageT = lambda wa, m: VideoFilter._match_type(m)
    """Filter for all video messages."""


class DocumentFilter(_MediaWithCaptionFilter):
    """Useful filters for document messages."""

    __message_types__ = (Mt.DOCUMENT,)

    ANY: MessageT = lambda wa, m: DocumentFilter._match_type(m)
    """Filter for all document messages."""


class AudioFilter(_MediaFilter):
    """Useful filters for audio messages."""

    __message_types__ = (Mt.AUDIO,)

    ANY: MessageT = lambda wa, m: AudioFilter._match_type(m)
    """Filter for all audio messages."""

    VOICE: MessageT = lambda wa, m: AudioFilter._match_type(m) and m.audio.voice
    """Filter for audio messages that are voice notes."""

    AUDIO: MessageT = lambda wa, m: AudioFilter._match_type(m) and not m.audio.voice
    """Filter for audio messages that are audio files."""


class StickerFilter(_MediaFilter):
    """Useful filters for sticker messages."""

    __message_types__ = (Mt.STICKER,)

    ANY: MessageT = lambda wa, m: StickerFilter._match_type(m)
    """Filter for all sticker messages."""

    ANIMATED: MessageT = lambda wa, m: StickerFilter._match_type(m) and m.sticker.animated
    """Filter for animated sticker messages."""

    STATIC: MessageT = lambda wa, m: StickerFilter._match_type(m) and not m.sticker.animated
    """Filter for static sticker messages."""


class LocationFilter(_UpdateWithForwardedFilter):
    """Useful filters for location messages."""

    __message_types__ = (Mt.LOCATION,)

    ANY: MessageT = lambda wa, m: LocationFilter._match_type(m)
    """Filter for all location messages."""

    @staticmethod
    def in_radius(lat: float, lon: float, radius: float | int) -> MessageT:
        """
        Filter for location messages that are in a given radius.

        >>> LocationFilter.in_radius(lat=37.48508108998884, lon=-122.14744733542707, radius=1)

        Args:
            lat: Latitude of the center of the radius.
            lon: Longitude of the center of the radius.
            radius: Radius in kilometers.
        """

        def _in_radius(_: Wa, msg: Msg) -> bool:
            return LocationFilter._match_type(msg) and \
                utils.get_distance(
                    lat1=lat, lon1=lon, lat2=msg.location.latitude, lon2=msg.location.longitude
                ) <= radius

        return _in_radius


class ReactionFilter(_BaseUpdateFilter):
    """Useful filters for reaction messages."""

    __message_types__ = (Mt.REACTION,)

    ANY: MessageT = lambda wa, m: ReactionFilter._match_type(m)
    """Filter for all reaction updates (added or removed)."""

    ADDED: MessageT = lambda wa, m: ReactionFilter._match_type(m) and m.reaction.emoji is not None
    """Filter for reaction messages that were added."""

    REMOVED: MessageT = lambda wa, m: ReactionFilter._match_type(m) and m.reaction.emoji is None
    """Filter for reaction messages that were removed."""

    @staticmethod
    def emoji(*emojis: str) -> MessageT:
        """
        Filter for custom reaction messages. pass emojis as strings.
            - Aliases: ``emojis``, ``reaction``, ``reactions``

        >>> ReactionFilter.emoji("👍", "👎")
        """
        return lambda wa, m: ReactionFilter._match_type(m) and m.reaction.emoji in emojis

    emojis = emoji  # alias
    reaction = emoji  # alias
    reactions = emoji  # alias


class ContactsFilter(_UpdateWithForwardedFilter):
    """Useful filters for contact messages."""

    __message_types__ = (Mt.CONTACTS,)

    ANY: MessageT = lambda wa, m: ContactsFilter._match_type(m)
    """Filter for all contacts messages."""

    HAS_WA: MessageT = lambda wa, m: ContactsFilter._match_type(m) and (
        any((p.wa_id for p in (phone for contact in m.contacts for phone in contact.phones)))
    )
    """Filter for contacts messages that have a WhatsApp account."""

    @staticmethod
    def count(min_count: int, max_count: int) -> MessageT:
        """
        Filter for contacts messages that have a number of contacts between min_count and max_count.
            - Aliases: ``contacts_count``, ``contacts_count_between``

        >>> ContactsFilter.count(1, 1) # ensure only 1 contact
        >>> ContactsFilter.count(1, 5) # between 1 and 5 contacts
        """
        return lambda wa, m: ContactsFilter._match_type(m) and min_count <= len(m.contacts) <= max_count

    contacts_count = count  # alias
    contacts_count_between = count  # alias

    @staticmethod
    def phone(*phones: str) -> MessageT:
        """
        Filter for contacts messages that have the given phone number/s.
            - Aliases: ``phones``, ``phone_number``, ``phone_numbers``

        >>> ContactsFilter.phone("+1 555-555-5555", "972123456789")
        """
        only_nums_pattern = re.compile(r"\D")
        phones = [re.sub(only_nums_pattern, "", p) for p in phones]
        return lambda wa, m: ContactsFilter._match_type(m) and (
            any(re.sub(only_nums_pattern, "", p.phone) in phones for contact in m.contacts for p in contact.phones)
        )

    phones = phone  # alias
    phone_number = phone  # alias
    phone_numbers = phone  # alias


class UnsupportedMsgFilter(_BaseUpdateFilter):
    """Useful filters for unsupported messages."""

    __message_types__ = (Mt.UNSUPPORTED,)

    ANY: MessageT = lambda wa, m: m.type == Mt.UNSUPPORTED
    """Filter for all unsupported messages."""


class CallbackFilter(_BaseUpdateFilter):
    """Useful filters for callback queries."""

    __message_types__ = (Mt.INTERACTIVE,)

    ANY: CallbackT = lambda wa, c: True
    """Filter for all callback queries (the default)."""

    @staticmethod
    def data_match(*matches: str, ignore_case: bool = False) -> CallbackT:
        """
        Filter for callbacks their data match exactly the given string/s.
            - Aliases: ``data_equals``, ``data_matches``, ``data_same_as``

        >>> CallbackFilter.data_match("menu")
        >>> CallbackFilter.data_match("back", "return", "exit")

        Args:
            matches: The string/s to match.
            ignore_case: Whether to ignore case when matching (default: False).
        """
        matches = tuple(m.lower() for m in matches) if ignore_case else matches
        return lambda wa, c: any((c.data.lower() if ignore_case else c.data) == m for m in matches)

    data_equals = data_match
    data_same_as = data_match
    data_matches = data_match

    @staticmethod
    def data_startswith(*matches: str, ignore_case: bool = False) -> CallbackT:
        """
        Filter for callbacks their data starts with the given string/s.

        >>> CallbackFilter.data_startswith("id:")

        Args:
            matches: The string/s to match.
            ignore_case: Whether to ignore case when matching (default: False).
        """
        matches = tuple(m.lower() for m in matches) if ignore_case else matches
        return lambda wa, c: any((c.data.lower() if ignore_case else c.data).startswith(m for m in matches))

    @staticmethod
    def data_endswith(*matches: str, ignore_case: bool = False) -> CallbackT:
        """
        Filter for callbacks their data ends with the given string/s.

        >>> CallbackFilter.data_endswith(":true", ":false")

        Args:
            matches: The string/s to match.
            ignore_case: Whether to ignore case when matching (default: False).
        """
        matches = tuple(m.lower() for m in matches) if ignore_case else matches
        return lambda wa, c: any((c.data.lower() if ignore_case else c.data).endswith(m for m in matches))

    @staticmethod
    def data_contain(*matches: str, ignore_case: bool = False) -> CallbackT:
        """
        Filter for callbacks their data contains the given string/s.
            - Aliases: ``data_contains``, ``data_include``, ``data_includes``

        >>> CallbackFilter.data_contain("back")

        Args:
            matches: The string/s to match.
            ignore_case: Whether to ignore case when matching (default: False).
        """
        matches = tuple(m.lower() for m in matches) if ignore_case else matches
        return lambda wa, c: any((m in (c.data.lower() if ignore_case else c.data) for m in matches))

    data_contains = data_contain
    data_include = data_contain
    data_includes = data_contain

    @staticmethod
    def data_regex(*patterns: str | re.Pattern, flags: int = 0) -> CallbackT:
        """
        Filter for callbacks their data matches the given regex/regexes.

        >>> CallbackFilter.data_regex(r"^\d+$")  # only digits

        Args:
            patterns: The regex/regexes to match.
            flags: The regex flags to use (default: 0).
        """
        patterns = tuple(re.compile(p) if isinstance(p, str) else p for p in patterns)
        return lambda wa, c: any((re.match(p, c.data, flags) for p in patterns))


class MessageStatusFilter(_BaseUpdateFilter):
    """Useful filters for message status updates."""

    __message_types__ = (Mt.MESSAGE_STATUS,)

    SENT: MessageStatusT = lambda wa, data: data.status == Mst.SENT
    """Filter for messages that have been sent."""

    DELIVERED: MessageStatusT = lambda wa, data: data.status == Mst.DELIVERED
    """Filter for messages that have been delivered."""

    READ: MessageStatusT = lambda wa, data: data.status == Mst.READ
    """Filter for messages that have been read."""

    FAILED: MessageStatusT = lambda wa, data: data.status == Mst.FAILED
    """Filter for messages that have failed to send (than you can access to the ``error`` attribute)."""

    @staticmethod
    def failed_with_error_code(*codes: int) -> MessageStatusT:
        """
        Filter for messages that have failed to send with the given error code/s.
            - Aliases: ``failed_with_error_codes``

        >>> MessageStatusFilter.failed_with_error_code(131056) # Too many requests
        """
        return lambda wa, s: s.status == Mst.FAILED and s.error.error_code in codes

    failed_with_error_codes = failed_with_error_code  # alias

    @staticmethod
    def failed_with_exception(*exceptions: Type[WhatsAppError]) -> MessageStatusT:
        """
        Filter for messages that have failed to send with the given exception/s.
            - Aliases: ``failed_with_exceptions``

        >>> MessageStatusFilter.failed_with_exception(ReEngagementMessage, MessageUndeliverable)
        """
        return lambda wa, s: s.status == Mst.FAILED and isinstance(s.error, exceptions)

    failed_with_exceptions = failed_with_exception  # alias

