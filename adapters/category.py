from enum import Enum

"""
Список категорий для поиска по торренту
"""

class Category(Enum):
    All = 0
    Film = 1
    Game = 2 # PS3, Dendy, PC game???
    TV_series = 3
    Book = 4
    Music = 5

# TODO: реализовать
def whichCategory(category_str):
    return Category.All
