# iformat

iformat is a simple package that prints basic data structures in an indented and readable way. The main `iprint` function supports changing the indent size and expansion threshold, as well as all vanilla `print` arguments. The included `iformat` function provides more customization, and returns a string that has been indented and formatted. An `.iformat` method (returning a string) can be added to any class for that class to be printed with custom formatting.

## Parameters:
**`indentDepth`:** *(`iprint` and `iformat`)*\
Specifies how many spaces should be inserted as one indent level. Default `4`.

**`expansionThreshold`**: *(`iprint` and `iformat`)*\
Specifies how long an object must be when printed before it is shown in a muilti-line format. Default `10`.\
Ex:
```py
iprint([1, 2, 3], expansionThreshold = 10)
# [1, 2, 3]

iprint([1, 2, 3], expansionThreshold = 8)
# [
#   1,
#   2,
#   3
# ]
```

**`indentLevel`:** *(`iformat` only)*\
Specifies the indent level of the returned output string. Default `0`.

https://github.com/FinnE145/iprint
https://pypi.org/project/iformat