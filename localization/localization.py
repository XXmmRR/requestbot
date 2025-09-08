import os
import i18n
from loguru import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCALE_DIR = os.path.join(BASE_DIR, "localization", "locales")

logger.info(f"Locale directory: {LOCALE_DIR}")

i18n.load_path.clear()
i18n.load_path.append(LOCALE_DIR)
i18n.set("file_format", "yml")
i18n.set("fallback", "ru")
i18n.set("locale", "ru")
i18n.set("filename_format", "{locale}.{format}")


def get_translation(key, lang="ru", **kwargs):
    """
    Получить перевод для ключа
    """
    i18n.set("locale", lang)
    
    translation = i18n.t(key, **kwargs)
    
    logger.info(f"Translation for '{key}': '{translation}'")
    return translation
        