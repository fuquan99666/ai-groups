# resources/__init__.py

from . import texts

class Resources:
    def __init__(self):
        self._texts = {
            'banner': texts.BANNER,
            'help': texts.HELP_TEXT,
            'errors': texts.ERROR_MESSAGES
        }
    
    def get_text(self, key: str, **kwargs) -> str:
        """获取文本资源（支持字符串格式化）"""
        if key in self._texts['errors']:
            return self._texts['errors'][key].format(**kwargs)
        return self._texts.get(key, "")
resources = Resources()