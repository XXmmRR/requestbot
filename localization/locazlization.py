import os
import i18n

i18n.load_path.append(os.path.join(os.path.dirname(__file__), 'locales'))
i18n.set('file_format', 'yml')
i18n.set('fallback', 'ru')

def get_translation(key, user_id, lang='ru'):
    lang = lang
    i18n.set('locale', lang)
    return i18n.t(key)