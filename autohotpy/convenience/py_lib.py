from importlib import import_module
import operator


class PyLib:
    def __getattr__(self, attr: str):
        try:
            return library[attr]
        except KeyError:
            raise AttributeError(
                f'"{attr}" is not an attribute of <Python Library>'
            ) from None

    def __repr__(self):
        return "<Python Library>"

    def __str__(self):
        return repr(self)

    def __dir__(self):
        return list(library.keys())


library = {"import": import_module}

library.update(**__builtins__)
library.update(**operator.__dict__)

# for loc in [builtins, operator]:
#     for name in dir(loc):
#         if name.startswith("__") and name.endswith("__"):
#             continue
#         try:
#             library[name] = get_val(loc, name)
#         except AttributeError:
#             continue

#         sname = name
#         while sname.endswith("_"):
#             sname = sname[:-1]
#         library[sname] = library[name]

pylib = PyLib()
