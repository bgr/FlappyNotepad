#!/usr/bin/python
# -*- coding: utf-8 -*-

logo = """
 ____ _ ____                  ____ _        _
|  __| |__  |____ ___ __ __  | ,  |_|--- __| |
|  __| |    |    |   |  |  | |   <| | |_|    |
| |  | |  , |  | |  ||  |  | | ,  | | | | |  |
|_|  |_|____|  __|  _|___  | |____|_|_| |____|
            |_|  |_|   |___|
"""

game_over = """
 ___ ____        ____    ___     ____
|  _|__  |------|  , |  |   |- -|  , |---
| | |    | ,  , |    |  | | | | |    | |_|
| | |  , | |  | |  __|  | | | ` |  __| |
|___|____|_|__|_|____|  |___|\_/|____|_|
"""

bird = [
"""
/( ,)
^_===
""",
"""
/( ,)
V_===
"""
]


numbers = [
"""
 ___
|   |
| | |
|___|
""",
"""
 _
| |
| |
|_|
""",
"""
 ___
|_  |
|  _|
|___|
""",
"""
 ___
|_  |
|_  |
|___|
""",
"""
 ___
| | |
|_  |
  |_|
""",
"""
 ___
|  _|
|_  |
|___|
""",
"""
 ___
|  _|
| . |
|___|
""",
"""
 ___
|_  |
  | |
  |_|
""",
"""
 ___
| . |
| . |
|___|
""",
"""
 ___
| . |
|_  |
|___|
"""
]


ground = u"""
¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
//  //  //  //  //  //
=======================
"""

pipe_top = """
 |. ===%1%#|
[. =====%1%#]
|. =====%1%#|
 ¯¯¯¯¯¯¯¯¯¯¯
"""

pipe_bottom = """
  ___________
 |. =====%1%#|
 [. =====%1%#]
  |. ===%1%#|
"""


# remove newlines and convert to list

fix = lambda s: s[1:-1].splitlines()

logo = fix(logo)
game_over = fix(game_over)
ground = fix(ground)
pipe_top = fix(pipe_top)
pipe_bottom = fix(pipe_bottom)

for i, el in enumerate(bird):
    bird[i] = fix(el)

for i, el in enumerate(numbers):
    numbers[i] = fix(el)