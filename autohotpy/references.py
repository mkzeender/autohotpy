
from dataclasses import dataclass
from typing import Any

@dataclass(slots=True)
class RefWrapper:
    value: Any
    refcount: int = 0

    def __iadd__(self):
        self.refcount += 1
        return self

    def __isub__(self):
        self.refcount -= 1
        return self


class References(dict):

    def __getitem__(self, obj: Any) -> RefWrapper:
        try:
            return super()[id(obj)]
        except KeyError:
            new = RefWrapper(obj, 0)
            super()[id(obj)] = new
            return new

    def __setitem__(self, obj: Any, value: RefWrapper) -> None:
        assert value.refcount >= 0
        if value.refcount == 0:
            try:
                del self[id(obj)]
            except KeyError:
                pass
        else:
            super()[id(obj)] = value