from typing import Optional

import mimetypes
from dataclasses import dataclass

__all__ = ()

@dataclass
class MimeType:
    mime_type_string: str

    def get_file_extension(self) -> Optional[str]:
        return mimetypes.guess_extension(
            self.mime_type_string, strict = True
        )