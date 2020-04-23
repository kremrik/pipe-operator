# Fake Python pipe operator

### Description
This simple project is something I built for fun while trying to emulate one of my favorite concepts in programming: the Linux pipe
There are many very obvious differences:
1. No part of these pipelines are executed until you run the entire thing - in this regard, they could be considered lazy
2. This `pipe` object can support multiple inputs from one stage to the next, although it's unclear when this is useful and goes against functional programming best-practices
That being said, they're still fun!

### Examples
```python
from pipe import pipe

@pipe
def stage1() -> int:
    return 1

@pipe
def stage2(x: int) -> int:
    return x + 1

pipeline = stage1 | stage2
print(pipeline.run())
# 2
```

```python
@pipe
def clean_str(string: str) -> str:
    return string.strip()

@pipe
def replace_cheer(string: str) -> str:
    bad_char = "!"
    good_char = "."
    return string.replace(bad_char, good_char)

pipeline = clean_str(" hello, world!\n") | replace_cheer
print(pipeline.run())
# hello, world.
```