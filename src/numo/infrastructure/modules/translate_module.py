import re
from typing import Optional
import aiohttp
from numo.domain.interfaces.numo_module import NumoModule
from numo.infrastructure.modules.languages import languages


class TranslateModule(NumoModule):
    """
    Language translation module.
    Provides text translation services using Google Translate API.
    Supports multiple languages and automatic language detection.
    """

    def __init__(self):
        """Initialize with translation pattern and language codes."""
        self._pattern = r"^(.+?)\s+in\s+([a-zA-Z-]+)$"
        self._languages = languages
        self._api_url = "https://translate.googleapis.com/translate_a/single"

    def _is_valid_language(self, lang_code: str) -> bool:
        """Check if a language code is supported."""
        lang_code = lang_code.lower()
        for code, name in self._languages.items():
            if lang_code in name.lower() or name.lower() in lang_code:
                return True
        return lang_code in self._languages

    async def run(self, source: str) -> Optional[str]:
        """
        Translate text between languages.

        Args:
            source: Input in format: "text in language"

        Returns:
            str: Translated text if successful
            None: For any error or invalid input

        Example:
            >>> module = TranslateModule()
            >>> await module.run('hello in spanish')  # Returns "hola"
            >>> await module.run('invalid')  # Returns None
        """
        if not source or not isinstance(source, str):
            return None

        # Parse translation request
        match = re.match(self._pattern, source, re.IGNORECASE)
        if not match:
            return None

        text = match.group(1)
        to_lang = match.group(2).lower()

        # Validate language
        if not self._is_valid_language(to_lang):
            return None

        # Get language code
        target_lang = self._get_language_code(to_lang)
        if not target_lang:
            return None

        # Perform translation
        translated = await self._translate_text(text, "auto", target_lang)
        if translated:
            return translated.lower()
        return None

    def _get_language_code(self, language: str) -> Optional[str]:
        """Convert language name to ISO code."""
        language = language.lower()
        # If it's already a code
        if language in self._languages:
            return language
        # If it's a language name (partial match)
        for code, name in self._languages.items():
            if language in name.lower() or name.lower() in language:
                return code
        return None

    async def _translate_text(
        self, text: str, from_lang: str, to_lang: str
    ) -> Optional[str]:
        """
        Translate text using translation API.

        Args:
            text: Text to translate
            from_lang: Source language code
            to_lang: Target language code

        Returns:
            str: Translated text if successful
            None: For any error
        """
        try:
            params = {
                "client": "gtx",
                "sl": from_lang,
                "tl": to_lang,
                "dt": "t",
                "q": text,
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self._api_url, params=params) as response:
                    if response.status != 200:
                        return None

                    data = await response.json()
                    if not data or not isinstance(data, list):
                        return None

                    # Extract translated text from response
                    translated = ""
                    for item in data[0]:
                        if item and isinstance(item, list) and len(item) > 0:
                            translated += item[0]

                    return translated if translated else None

        except (aiohttp.ClientError, ValueError, KeyError, IndexError):
            return None
