"""Usage:
  drawer.py <commands_file_name>
  drawer.py (-h | --help)

Draw pseudographics by commands from file.

"""
import re
from docopt import docopt

CANVAS_VERTICAL_BORDER = '|'
CANVAS_HORIZONTAL_BORDER = '-'
LINE_DOT = 'x'

CANVAS_RE = re.compile(r'^ C \s+ (?P<width>\d+) \s+ (?P<height>\d+) \s*$',  re.VERBOSE)
LINE_RE = re.compile(r'^ L \s+ (?P<x1>\d+) \s+ (?P<y1>\d+) \s+ (?P<x2>\d+) \s+ (?P<y2>\d+) \s*$',  re.VERBOSE)
RECTANGLE_RE = re.compile(r'^ R \s+ (?P<x1>\d+) \s+ (?P<y1>\d+) \s+ (?P<x2>\d+) \s+ (?P<y2>\d+) \s*$',  re.VERBOSE)
FILL_RE = re.compile(r'^ B \s+ (?P<x>\d+) \s+ (?P<y>\d+) \s+ (?P<color>\w) \s*$',  re.VERBOSE)

class ParsingError(Exception): pass
class CanvasParsingError(ParsingError): pass
class WrongLineTypeError(Exception): pass
class OutsideCanvasError(Exception): pass


def parse_canvas_cmd(line):
    res = CANVAS_RE.match(line)
    if res:
        return int(res.group('width')), int(res.group('height'))
    else:
        raise CanvasParsingError(line)


def create_canvas(width, heigth):
    canvas = list()
    for i in range(width+2):
        canvas.append([' ']*(heigth+2))
    return canvas


def draw_canvas_border(canvas, vertical_char, horizontal_char):
    max_x, max_y = len(canvas)-1, len(canvas[0])-1
    draw_line(canvas, 0, 1, 0, max_y-1, vertical_char, True) # left vert
    draw_line(canvas, max_x, 1, max_x, max_y-1, vertical_char, True) # right vert
    draw_line(canvas, 0, 0, max_x, 0, horizontal_char, True) # top horiz
    draw_line(canvas, 0, max_y, max_x, max_y, horizontal_char, True) # bottom horiz


def show(canvas):
    for y in range(len(canvas[0])):
        for x in range(len(canvas)):
            print(canvas[x][y], end='')
        print()


def dot_inside_canvas(canvas, x, y):
    max_x, max_y = len(canvas)-2, len(canvas[0])-2
    if 1 <= x <= max_x and 1 <= y <= max_y:
        return True
    else:
        return False

def parse_line_cmd(line):
    res = LINE_RE.match(line)
    if res:
        return int(res.group('x1')), int(res.group('y1')), int(res.group('x2')), int(res.group('y2'))
    else:
        raise ParsingError(line)


def draw_line(canvas, x1, y1, x2, y2, dot_char, is_border=False):
    if not is_border:
        if not (dot_inside_canvas(canvas, x1, y1) and dot_inside_canvas(canvas, x2, y2)):
            raise OutsideCanvasError('{0} {1} {2} {3}'.format(x1, y1, x2, y2))
    if x1 == x2: # vertical line
        for y in range(y1,y2+1):
            canvas[x1][y] = dot_char
    elif y1 == y2: # horizontal line
        for x in range(x1,x2+1):
            canvas[x][y1] = dot_char
    else:
        raise WrongLineTypeError('{0} {1} {2} {3}'.format(x1, y1, x2, y2))


def parse_rectangle_cmd(line):
    res = RECTANGLE_RE.match(line)
    if res:
        return int(res.group('x1')), int(res.group('y1')), int(res.group('x2')), int(res.group('y2'))
    else:
        raise ParsingError(line)

def draw_rectangle(canvas, x1, y1, x2, y2, dot_char):
    if not (dot_inside_canvas(canvas, x1, y1) and dot_inside_canvas(canvas, x2, y2)):
        raise OutsideCanvasError('{0} {1} {2} {3}'.format(x1, y1, x2, y2))
    draw_line(canvas, x1, y1, x1, y2, dot_char) # left vert
    draw_line(canvas, x2, y1, x2, y2, dot_char) # right vert
    draw_line(canvas, x1, y1, x2, y1, dot_char) # top horiz
    draw_line(canvas, x1, y2, x2, y2, dot_char) # bottom horiz


def parse_fill_cmd(line):
    res = FILL_RE.match(line)
    if res:
        return int(res.group('x')), int(res.group('y')), res.group('color')
    else:
        raise ParsingError(line)


def fill(canvas, x, y, color):
    max_x, max_y = len(canvas)-1, len(canvas[0])-1
    if not dot_inside_canvas(canvas, x, y):
        return
    if canvas[x][y] in [CANVAS_VERTICAL_BORDER, CANVAS_HORIZONTAL_BORDER, LINE_DOT]:
        return
    if canvas[x][y] == color:
        return
    canvas[x][y] = color
    fill(canvas, x-1, y, color)
    fill(canvas, x+1, y, color)
    fill(canvas, x, y-1, color)
    fill(canvas, x, y+1, color)


def draw(file_name):
    with open(file_name) as file:
        line = file.readline()
        width, heigth = parse_canvas_cmd(line)
        canvas = create_canvas(width, heigth)
        draw_canvas_border(canvas, CANVAS_VERTICAL_BORDER, CANVAS_HORIZONTAL_BORDER)
        show(canvas)
        for line in file:
            if line[0] == 'L':
                x1, y1, x2, y2 = parse_line_cmd(line)
                draw_line(canvas, x1, y1, x2, y2, LINE_DOT)
            elif line[0] == 'R':
                x1, y1, x2, y2 = parse_rectangle_cmd(line)
                draw_rectangle(canvas, x1, y1, x2, y2, LINE_DOT)
            elif line[0] == 'B':
                x, y, color = parse_fill_cmd(line)
                fill(canvas, x, y, color)
            elif line[0] == '#':
                continue
            else:
                raise ParsingError(line)
            show(canvas)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    try:
        draw(arguments['<commands_file_name>'])
    except CanvasParsingError as e:
        print('First line must be a valid canvas drawing command: ', e)
    except ParsingError as e:
        print('Not valid cmd: ', e)
    except WrongLineTypeError as e:
        print('Vertical and horizontal lines supported only: ', e)
    except OutsideCanvasError as e:
        print('Points outside canvas: ', e)
