"""iformat is a simple package that prints basic data structures in an indented and readable way. The main `iprint` function supports changing the indent size and expansion threshold, as well as all vanilla `print` arguments. The included `iformat` function provides more customization, and returns a string that has been indented and formatted. An `.iformat` method (returning a string) can be added to any class for that class to be printed with custom formatting.

https://github.com/FinnE145/iprint

https://pypi.org/project/iformat"""


# Copyright (C) 2023  Finn Emmerson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# finne014@gmail.com

# ----------- iPrint ---------- #
_iters = [dict, list, tuple, set]        # NOTE: 'dict' must be first, because it has special cases

def _length(i):
    return (sum([_length(k) + _length(v) + (3 if len(i.keys()) <= 1 else (2 if len(i.keys()) <= 0 else 4)) for k, v in i.items()]) + 1) if type(i) == dict else (sum([_length(x) + 2 for x in i]) if type(i) in _iters else (len(i.__class__.__name__) + _length(i.__dict__) + len(i.__dict__.keys()) - 1 if hasattr(i, "__dict__") else len(str(i))))

def _brackets(datatype, newline = False, indentAmount = 0):
    return [("[" if datatype == list else "(" if datatype == tuple else "{" if datatype in [set, dict] else "") + ("\n" if datatype in _iters and newline else "") + (" " * indentAmount), ("\n" if datatype in _iters and newline else "") + (" " * indentAmount) + ("]" if datatype == list else ")" if datatype == tuple else "}" if datatype in [set, dict] else "")]

def _indent(indentLevel, indentDepth):
    return " " * (indentLevel * indentDepth)

def iformat(i, indentLevel = 0, indentDepth = 4, expansionThreshold = 10):
    il, id, et = indentLevel, indentDepth, expansionThreshold
    length = _length(i)
    if type(i) in _iters:
        return (_brackets(type(i), True if length > et else False, ((il + 1) * id) if length > et else False)[0]\
            + ((",\n" + _indent(il + 1, id)) if length > et else (", ")).join(\
                    [f"{iformat(k, il + 1, id, et)}: {iformat(v, il + 1, id, et)}" for k, v in i.items()]\
                if type(i) == dict else\
                    [iformat(x, il + 1, id, et) for x in i])\
            + _brackets(type(i), True if length > et else False, (il * id) if length > et else 0)[-1])
    else:
        if hasattr(i, "__dict__"):
            if "iformat" in dir(i):
                return i.iformat(il, id, et)
            else:
                return (f"{i.__class__.__name__}({', '.join([f'{k} = {iformat(v, il, id, et)}' for k, v in i.__dict__.items()])})")
        else:
            return str(i)

def iprint(*args, indentDepth = 4, expansionThreshold = 10, sep = " ", end = "\n", file = None, flush = False):
    print(*[iformat(x, 0, indentDepth, expansionThreshold = expansionThreshold) for x in args], sep = sep, end = end, file = file, flush = flush)