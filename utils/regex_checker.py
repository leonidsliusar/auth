from dataclasses import dataclass
import re


@dataclass
class RegexIn:
    string: str

    def __eq__(self, other: str | re.Pattern):
        if isinstance(other, str):
            other = re.compile(other)
        assert isinstance(other, re.Pattern)
        return other.fullmatch(self.string) is not None
