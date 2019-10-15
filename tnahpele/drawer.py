"""Usage:
  drawer.py <commands_file_name>
  drawer.py (-h | --help)

Draw pseudographics by commands from file.

"""
import re
from docopt import docopt

# Type Point is not bad idea, but I am not sure that it make code more
# readable here because we do a lot of job with coordinates, not with points

VERTICAL_BORDER = '|'
HORIZONTAL_BORDER = '-'
LINE_POINT = 'x'

CANVAS_RE = re.compile(r'''^C \s+
 (?P<width>\d+) \s+
 (?P<height>\d+) \s*$''', re.VERBOSE)
LINE_RE = re.compile(r'''^L \s+
 (?P<x1>\d+) \s+
 (?P<y1>\d+) \s+
 (?P<x2>\d+) \s+
 (?P<y2>\d+) \s*$''', re.VERBOSE)
RECTANGLE_RE = re.compile(r'''^R \s+
 (?P<x1>\d+) \s+
 (?P<y1>\d+) \s+
 (?P<x2>\d+) \s+
 (?P<y2>\d+) \s*$''', re.VERBOSE)
FILL_RE = re.compile(r'''^B \s+
 (?P<x>\d+) \s+
 (?P<y>\d+) \s+
 (?P<color>\w) \s*$''', re.VERBOSE)


class ParsingError(Exception): pass  # noqa
class CanvasParsingError(ParsingError): pass  # noqa
class WrongLineTypeError(Exception): pass  # noqa
class OutsideCanvasError(Exception): pass  # noqa


def parse_canvas_cmd(line):
    res = CANVAS_RE.match(line)
    if res:
        return int(res.group('width')), int(res.group('height'))
    else:
        raise CanvasParsingError(line)


def create_canvas(width, heigth):
    canvas = list()
    for _ in range(width+2):
        canvas.append([' ']*(heigth+2))
    return canvas


def draw_canvas_border(canvas, vertical_char, horizontal_char):
    max_x, max_y = len(canvas)-1, len(canvas[0])-1
    draw_line(canvas, 0, 1, 0, max_y-1, vertical_char)  # left vert
    draw_line(canvas, max_x, 1, max_x, max_y-1, vertical_char)  # right vert
    draw_line(canvas, 0, 0, max_x, 0, horizontal_char)  # top horiz
    draw_line(canvas, 0, max_y, max_x, max_y, horizontal_char)  # bottom horiz


def canvas2string(canvas):
    str = ''
    for y in range(len(canvas[0])):
        for x in range(len(canvas)):
            str = str + canvas[x][y]
        str = str + '\n'
    return str[:-1]


def point_inside_canvas(canvas, x, y):
    max_x, max_y = len(canvas)-2, len(canvas[0])-2
    if 1 <= x <= max_x and 1 <= y <= max_y:
        return True
    else:
        return False


# Can be extended to any points count if will needed
def points_inside_canvas(canvas, x1, y1, x2, y2):
    point1_inside = point_inside_canvas(canvas, x1, y1)
    point2_inside = point_inside_canvas(canvas, x2, y2)
    if point1_inside and point2_inside:
        return True
    return False


def parse_line_cmd(line):
    res = LINE_RE.match(line)
    if res:
        x1, y1 = int(res.group('x1')), int(res.group('y1'))
        x2, y2 = int(res.group('x2')), int(res.group('y2'))
        return x1, y1, x2, y2
    else:
        raise ParsingError(line)


def draw_line(canvas, x1, y1, x2, y2, point_char):
    if x1 == x2:  # vertical line
        for y in range(y1, y2+1):
            canvas[x1][y] = point_char
    elif y1 == y2:  # horizontal line
        for x in range(x1, x2+1):
            canvas[x][y1] = point_char
    else:
        raise WrongLineTypeError('{0} {1} {2} {3}'.format(x1, y1, x2, y2))


def draw_line_if_possible(canvas, x1, y1, x2, y2, point_char):
    if not points_inside_canvas(canvas, x1, y1, x2, y2):
        raise OutsideCanvasError('{0} {1} {2} {3}'.format(x1, y1, x2, y2))
    draw_line(canvas, x1, y1, x2, y2, point_char)


def parse_rectangle_cmd(line):
    res = RECTANGLE_RE.match(line)
    if res:
        x1, y1 = int(res.group('x1')), int(res.group('y1'))
        x2, y2 = int(res.group('x2')), int(res.group('y2'))
        return x1, y1, x2, y2
    else:
        raise ParsingError(line)


def draw_rectangle(canvas, x1, y1, x2, y2, point_char):
    if not points_inside_canvas(canvas, x1, y1, x2, y2):
        raise OutsideCanvasError('{0} {1} {2} {3}'.format(x1, y1, x2, y2))
    draw_line_if_possible(canvas, x1, y1, x1, y2, point_char)  # left vert
    draw_line_if_possible(canvas, x2, y1, x2, y2, point_char)  # right vert
    draw_line_if_possible(canvas, x1, y1, x2, y1, point_char)  # top horiz
    draw_line_if_possible(canvas, x1, y2, x2, y2, point_char)  # bottom horiz


def parse_fill_cmd(line):
    res = FILL_RE.match(line)
    if res:
        return int(res.group('x')), int(res.group('y')), res.group('color')
    else:
        raise ParsingError(line)


def fill(canvas, x, y, color):
    if not point_inside_canvas(canvas, x, y):
        return
    if canvas[x][y] in [VERTICAL_BORDER, HORIZONTAL_BORDER, LINE_POINT]:
        return
    if canvas[x][y] == color:
        return
    canvas[x][y] = color
    fill(canvas, x-1, y, color)
    fill(canvas, x+1, y, color)
    fill(canvas, x, y-1, color)
    fill(canvas, x, y+1, color)


def draw(commands):
    line = next(commands)
    width, heigth = parse_canvas_cmd(line)
    canvas = create_canvas(width, heigth)
    draw_canvas_border(canvas, VERTICAL_BORDER, HORIZONTAL_BORDER)
    yield canvas2string(canvas)
    for line in commands:
        if line[0] == 'L':
            x1, y1, x2, y2 = parse_line_cmd(line)
            draw_line_if_possible(canvas, x1, y1, x2, y2, LINE_POINT)
        elif line[0] == 'R':
            x1, y1, x2, y2 = parse_rectangle_cmd(line)
            draw_rectangle(canvas, x1, y1, x2, y2, LINE_POINT)
        elif line[0] == 'B':
            x, y, color = parse_fill_cmd(line)
            fill(canvas, x, y, color)
        elif line[0] == '#':
            continue
        else:
            raise ParsingError(line)
        yield canvas2string(canvas)


def main():
    arguments = docopt(__doc__)
    try:
        with open(arguments['<commands_file_name>']) as file:
            for screen in draw(file):
                print(screen)
    except CanvasParsingError as e:
        print('First line must be a valid canvas drawing command: ', e)
    except ParsingError as e:
        print('Not valid cmd: ', e)
    except WrongLineTypeError as e:
        print('Vertical and horizontal lines supported only: ', e)
    except OutsideCanvasError as e:
        print('Points outside canvas: ', e)


if __name__ == '__main__':
    main()
