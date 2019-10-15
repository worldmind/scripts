import pytest
import drawer


def test_draw():
    commands = iter([
        'C 20 4',
        'L 1 2 6 2',
        'L 6 3 6 4',
        'R 16 1 20 3',
        'B 10 3 o',
    ])
    results = [
        '''
----------------------
|                    |
|                    |
|                    |
|                    |
----------------------
''',
        '''
----------------------
|                    |
|xxxxxx              |
|                    |
|                    |
----------------------
''',
        '''
----------------------
|                    |
|xxxxxx              |
|     x              |
|     x              |
----------------------
''',
        '''
----------------------
|               xxxxx|
|xxxxxx         x   x|
|     x         xxxxx|
|     x              |
----------------------
''',
        '''
----------------------
|oooooooooooooooxxxxx|
|xxxxxxooooooooox   x|
|     xoooooooooxxxxx|
|     xoooooooooooooo|
----------------------
'''
    ]
    results = [x.strip('\r\n') for x in results]
    for screen, expected in zip(drawer.draw(commands), results):
        assert screen == expected


def test_fill_all():
    commands = iter([
        'C 20 4',
        'B 10 3 o',
    ])
    results = [
        '''
----------------------
|                    |
|                    |
|                    |
|                    |
----------------------
''',
        '''
----------------------
|oooooooooooooooooooo|
|oooooooooooooooooooo|
|oooooooooooooooooooo|
|oooooooooooooooooooo|
----------------------
''',
    ]
    results = [x.strip('\r\n') for x in results]
    for screen, expected in zip(drawer.draw(commands), results):
        assert screen == expected


def test_wrong_line_type():
    commands = iter([
        'C 20 4',
        'L 1 2 6 4'
    ])
    with pytest.raises(drawer.WrongLineTypeError):
        for screen in drawer.draw(commands):
            print(screen)


def test_wrong_line():
    commands = iter([
        'C 20 4',
        'Ld 1 2 6 2'
    ])
    with pytest.raises(drawer.ParsingError):
        for screen in drawer.draw(commands):
            print(screen)


def test_wrong_rectangle():
    commands = iter([
        'C 20 4',
        'Re 1 2 6 2'
    ])
    with pytest.raises(drawer.ParsingError):
        for screen in drawer.draw(commands):
            print(screen)


def test_wrong_fill():
    commands = iter([
        'C 20 4',
        'B 1s 2 o'
    ])
    with pytest.raises(drawer.ParsingError):
        for screen in drawer.draw(commands):
            print(screen)


def test_wrong_canvas():
    commands = iter([
        'Can 20 4',
    ])
    with pytest.raises(drawer.CanvasParsingError):
        for screen in drawer.draw(commands):
            print(screen)


def test_outside_canvas():
    commands = iter([
        'C 20 4',
        'R 1 200 6 2'
    ])
    with pytest.raises(drawer.OutsideCanvasError):
        for screen in drawer.draw(commands):
            print(screen)
