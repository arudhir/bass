#!/usr/bin/env python3
''' '''
from bassgui import Entry

__all__ = ['LARGE_FONT', 'entries', 'entries_by_school']

try:
    assert True #toggle to test
    LARGE_FONT = ("Avenir Next", 12)
    entries = {}
    entries_by_school = {}
except AssertionError as err:
    entries = { 1: Entry(1, 'Illinois', ('Robert', 'Bobbert'), fishes=[]),
                2: Entry(2, 'Fisher\'s Guild', ('xxFish3rxx', 'SH4RK_B455'), fishes=[]),
                3: Entry(3, 'Illinois', ('Roberto', 'Boberto'), fishes=[1, 2, 0, 4, 5]),
                4: Entry(4, 'Michigan', ('Rob', 'Bob'), fishes=[19, 0, 39, 0, 59]),
                5: Entry(5, 'Harvard', ('R', 'B'), fishes=[0, 0, 0, 0, 511])}
    entries_by_school = {}
    """
    entries_by_school = {
         'Illinois': [Entry(3, 'Illinois', ('Roberto', 'Boberto'), 90, 4, 45), 
                      Entry(1, 'Illinois', ('Robert', 'Bobbert'), 100, 5, 80)],
         'Fisher\'s Guild': [Entry(2, 'Michigan', ('xxFish3rxx', 'SH4RK_B455'), 1000, 1, 1000)]}"""
