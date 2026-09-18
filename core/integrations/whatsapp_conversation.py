"""Privacy-conscious WhatsApp seller conversation state machine."""

from __future__ import annotations

import hashlib
import hmac
import os
import secrets
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, Optional, Tuple


class ConversationState(str, Enum):
    """Explicit seller states supported by the current onboarding flow."""

    READY = "ready"


class Language(str, Enum):
    """Supported WhatsApp conversation languages."""

    ENGLISH = "en"
    SINHALA = "si"
    TAMIL = "ta"


@dataclass(frozen=True)
class QuotaSnapshot:
    """Non-secret merchant verification-credit information."""

    tier: str
    limit: int
    remaining: int
    used: int = 0


@dataclass(frozen=True)
class ConversationReply:
    """A state-machine response safe to send back to the seller."""

    text: str
    state: ConversationState
    language: Language
    duplicate: bool = False


@dataclass
class _SellerSession:
    state: ConversationState
    language: Language
    touched_at: float


_ONBOARDING = {
    Language.ENGLISH: (
        "👋 Welcome to VeriSlip. Send a JPEG/PNG payment slip for verification. "
        "Commands: help, balance. Languages: English, සිංහල, தமிழ்."
    ),
    Language.SINHALA: (
        "👋 VeriSlip වෙත සාදරයෙන් පිළිගනිමු. පරීක්ෂා කිරීමට JPEG/PNG ගෙවීම් "
        "පතක් එවන්න. විධාන: උදව්, ශේෂය."
    ),
    Language.TAMIL: (
        "👋 VeriSlip-க்கு வரவேற்கிறோம். சரிபார்க்க JPEG/PNG பணச்சீட்டை அனுப்பவும். "
        "கட்டளைகள்: உதவி, மீதம்."
    ),
}

_HELP = {
    Language.ENGLISH: (
        "VeriSlip help:\n• Send a JPEG/PNG slip to verify it\n"
        "• balance — show your verification credits\n"
        "• English / සිංහල / தமிழ் — change language"
    ),
    Language.SINHALA: (
        "VeriSlip උදව්:\n• පරීක්ෂා කිරීමට JPEG/PNG පතක් එවන්න\n"
        "• ශේෂය — ඉතිරි පරීක්ෂණ ණය බලන්න\n"
        "• English / සිංහල / தமிழ் — භාෂාව වෙනස් කරන්න"
    ),
    Language.TAMIL: (
        "VeriSlip உதவி:\n• சரிபார்க்க JPEG/PNG பணச்சீட்டை அனுப்பவும்\n"
        "• மீதம் — மீதமுள்ள சரிபார்ப்பு வரவுகளைப் பார்க்கவும்\n"
        "• English / සිංහල / தமிழ் — மொழியை மாற்றவும்"
    ),
}

_UNKNOWN = {
    Language.ENGLISH: "I did not understand that command. Send help to see available commands.",
    Language.SINHALA: "එම විධානය තේරුණේ නැත. විධාන බැලීමට උදව් යවන්න.",
    Language.TAMIL: "அந்த கட்டளை புரியவில்லை. கட்டளைகளைப் பார்க்க உதவி அனுப்பவும்.",
}

_LANGUAGE_CHANGED = {
    Language.ENGLISH: "Language changed to English.",
    Language.SINHALA: "භාෂාව සිංහලට වෙනස් කරන ලදී.",
    Language.TAMIL: "மொழி தமிழுக்கு மாற்றப்பட்டது.",
}

_HELP_COMMANDS = frozenset({"help", "menu", "උදව්", "உதவி"})
_BALANCE_COMMANDS = frozenset({"balance", "quota", "ශේෂය", "மீதம்"})
_LANGUAGE_COMMANDS = {
    "english": Language.ENGLISH,
    "en": Language.ENGLISH,
    "සිංහල": Language.SINHALA,
    "sinhala": Language.SINHALA,
    "si": Language.SINHALA,
    "தமிழ்": Language.TAMIL,
    "tamil": Language.TAMIL,
    "ta": Language.TAMIL,
}
_STATE_HASH_KEY = secrets.token_bytes(32)


def _fingerprint(value: str) -> str:
    return hmac.new(_STATE_HASH_KEY, value.encode("utf-8"), hashlib.sha256).hexdigest()


def _normalize_command(text: str) -> str:
    return " ".join(text.strip().casefold().split()).lstrip("/")


def _detect_language(text: str) -> Language:
    if any("\u0d80" <= character <= "\u0dff" for character in text):
        return Language.SINHALA
    if any("\u0b80" <= character <= "\u0bff" for character in text):
        return Language.TAMIL
    return Language.ENGLISH


def _balance_message(language: Language, quota: QuotaSnapshot) -> str:
    if language is Language.SINHALA:
        return (
            f"සැලැස්ම: {quota.tier}. ඉතිරි ඉල්ලීම්: "
            f"{quota.remaining}/{quota.limit}."
        )
    if language is Language.TAMIL:
        return (
            f"திட்டம்: {quota.tier}. மீதமுள்ள கோரிக்கைகள்: "
            f"{quota.remaining}/{quota.limit}."
        )
    return (
        f"Plan: {quota.tier}. Verification credits remaining: "
        f"{quota.remaining}/{quota.limit}."
    )


def duplicate_verification_message(language: Language) -> str:
    """Return a localized reply for an idempotently ignored media message."""
    if language is Language.SINHALA:
        return "මෙම ගෙවීම් පත දැනටමත් සකසා ඇත. නැවත ණයක් අය නොකෙරේ."
    if language is Language.TAMIL:
        return "இந்த பணச்சீட்டு ஏற்கனவே செயலாக்கப்பட்டது. மீண்டும் வரவு கழிக்கப்படாது."
    return "This payment slip message was already processed. No additional credit was charged."


def quota_exhausted_message(
    language: Language, upgrade_url: Optional[str]
) -> str:
    """Return a localized exhausted-quota response with the configured link."""
    link = upgrade_url or "Contact VeriSlip support to upgrade."
    if language is Language.SINHALA:
        return f"ඔබගේ නොමිලේ පරීක්ෂණ ණය අවසන්. උත්ශ්‍රේණි කිරීමට: {link}"
    if language is Language.TAMIL:
        return f"உங்கள் இலவச சரிபார்ப்பு வரவுகள் முடிந்துவிட்டன. மேம்படுத்த: {link}"
    return f"Your free verification credits are exhausted. Upgrade here: {link}"


def quota_reached_message(language: Language, upgrade_url: Optional[str]) -> str:
    """Notify a merchant immediately after their final free verification."""
    return quota_exhausted_message(language, upgrade_url)


class InMemoryConversationStore:
    """Thread-safe local state with bounded, expiring idempotency records.

    Only process-keyed HMAC-SHA-256 fingerprints of seller identifiers and
    message IDs are stored; message text, phone numbers, images, credentials,
    and access tokens are not.
    """

    def __init__(
        self,
        *,
        session_ttl_seconds: int = 30 * 24 * 60 * 60,
        idempotency_ttl_seconds: int = 24 * 60 * 60,
        max_records: int = 10_000,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if session_ttl_seconds <= 0 or idempotency_ttl_seconds <= 0:
            raise ValueError("Conversation state TTLs must be positive.")
        if max_records <= 0:
            raise ValueError("Conversation state capacity must be positive.")
        self._sessions: Dict[str, _SellerSession] = {}
        self._replies: Dict[Tuple[str, str], Tuple[ConversationReply, float]] = {}
        self._session_ttl = session_ttl_seconds
        self._idempotency_ttl = idempotency_ttl_seconds
        self._max_records = max_records
        self._clock = clock
        self._lock = threading.Lock()

    def _purge(self, now: float) -> None:
        if len(self._sessions) + len(self._replies) < self._max_records:
            return
        self._sessions = {
            key: value
            for key, value in self._sessions.items()
            if now - value.touched_at <= self._session_ttl
        }
        self._replies = {
            key: value for key, value in self._replies.items() if value[1] > now
        }
        while len(self._sessions) + len(self._replies) >= self._max_records:
            oldest_session = min(
                self._sessions,
                key=lambda key: self._sessions[key].touched_at,
                default=None,
            )
            oldest_reply = min(
                self._replies,
                key=lambda key: self._replies[key][1],
                default=None,
            )
            if oldest_session is None:
                assert oldest_reply is not None
                self._replies.pop(oldest_reply)
            elif oldest_reply is None:
                self._sessions.pop(oldest_session)
            elif (
                self._sessions[oldest_session].touched_at
                <= self._replies[oldest_reply][1]
            ):
                self._sessions.pop(oldest_session)
            else:
                self._replies.pop(oldest_reply)

    def process(
        self,
        seller_identifier: str,
        text: str,
        quota: QuotaSnapshot,
        message_id: Optional[str] = None,
    ) -> ConversationReply:
        """Atomically transition one seller session and render its reply."""
        seller_key = _fingerprint(seller_identifier)
        message_key = _fingerprint(message_id) if message_id else None
        now = self._clock()
        with self._lock:
            self._purge(now)
            cache_key = (seller_key, message_key) if message_key else None
            if cache_key:
                cached = self._replies.get(cache_key)
                if cached and cached[1] > now:
                    reply = cached[0]
                    return ConversationReply(
                        text=reply.text,
                        state=reply.state,
                        language=reply.language,
                        duplicate=True,
                    )

            command = _normalize_command(text)
            requested_language = _LANGUAGE_COMMANDS.get(command)
            session = self._sessions.get(seller_key)
            if session is None or now - session.touched_at > self._session_ttl:
                language = requested_language or _detect_language(text)
                session = _SellerSession(ConversationState.READY, language, now)
                self._sessions[seller_key] = session
                onboarding = _ONBOARDING[language]
                if command in _HELP_COMMANDS:
                    onboarding = f"{onboarding}\n\n{_HELP[language]}"
                elif command in _BALANCE_COMMANDS:
                    onboarding = f"{onboarding}\n\n{_balance_message(language, quota)}"
                reply = ConversationReply(onboarding, session.state, language)
            else:
                language = session.language
                if requested_language:
                    language = requested_language
                    session.language = language
                    text_reply = _LANGUAGE_CHANGED[language]
                elif command in _HELP_COMMANDS:
                    text_reply = _HELP[language]
                elif command in _BALANCE_COMMANDS:
                    text_reply = _balance_message(language, quota)
                else:
                    text_reply = _UNKNOWN[language]
                session.touched_at = now
                reply = ConversationReply(text_reply, session.state, language)

            if cache_key:
                self._replies[cache_key] = (
                    reply,
                    now + self._idempotency_ttl,
                )
            return reply

    def seller_language(self, seller_identifier: str) -> Language:
        """Register an image-only seller or return their selected language."""
        seller_key = _fingerprint(seller_identifier)
        now = self._clock()
        with self._lock:
            self._purge(now)
            session = self._sessions.get(seller_key)
            if session is None or now - session.touched_at > self._session_ttl:
                session = _SellerSession(
                    ConversationState.READY, Language.ENGLISH, now
                )
                self._sessions[seller_key] = session
            else:
                session.touched_at = now
            return session.language

    def clear(self) -> None:
        """Clear local state for deterministic tests."""
        with self._lock:
            self._sessions.clear()
            self._replies.clear()


conversation_store = InMemoryConversationStore(
    session_ttl_seconds=int(
        os.getenv("VERISLIP_WHATSAPP_SESSION_TTL_SECONDS", str(30 * 24 * 60 * 60))
    ),
    idempotency_ttl_seconds=int(
        os.getenv("VERISLIP_WHATSAPP_IDEMPOTENCY_TTL_SECONDS", str(24 * 60 * 60))
    ),
    max_records=int(os.getenv("VERISLIP_WHATSAPP_STATE_MAX_RECORDS", "10000")),
)
