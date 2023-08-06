#!python
#cython: language_level=3
from libc.math cimport sqrt

def scale_to(list poly, float scalex, float scaley):
    cdef float x = 0
    cdef float y = 0
    cdef list new = []
    for x, y in poly:
        new.append((x * scalex, y * scaley))
    return new


def scale_from(list poly, float scalex, float scaley):
    cdef float x
    cdef float y
    cdef list new = []
    for x, y in poly:
        new.append((x / scalex, y / scaley))
    return new


def scale_to_(list poly, float scalex, float scaley):
    cdef int i, n
    n = len(poly)
    for i in range(n):
        x, y = poly[i]
        poly[i][0] = x * scalex
        poly[i][1] = y * scaley
    return poly


def scale_from_(list poly, float scalex, float scaley):
    cdef int i, n
    n = len(poly)
    for i in range(n):
        x, y = poly[i]
        poly[i][0] = x / scalex
        poly[i][1] = y / scaley
    return poly


def get_shrink_dist(list poly, float r):
    cdef float A = get_area(poly)
    cdef float L = get_length(poly)
    cdef float d = A * (1 - r**2) / L
    return d


def get_expand_dist(list poly, float r):
    cdef float A = get_area(poly)
    cdef float L = get_length(poly)
    cdef float d = A * r / L
    return d


def get_area(list poly):
    """Calculate area of a polygon.

    Args:
        poly:
            List of tuple representing x, y points.
            Numpy arrays of shape [P, 2] would do too.

    References:
        https://en.wikipedia.org/wiki/Polygon#Area
    """
    cdef int n = len(poly)
    cdef int i
    cdef float area, x1, y1, x2, y2
    area = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    area /= 2
    return area


def get_length(list poly):
    """Calculate the perimeter of a polygon.

    Args:
        poly:
            List of tuple representing x, y points.
            Numpy arrays of shape [P, 2] would do too.

    References:
        https://en.wikipedia.org/wiki/Polygon#Area
    """
    cdef int i, n
    cdef float peri, x1, y1, x2, y2
    n = len(poly)
    peri = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        peri += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return peri


def offset(list poly, float offset):
    cdef int i, n, scale
    cdef float x1, y1, x2, y2, length, x, y
    cdef list new_poly, offset_lines

    scale = 1000
    n = len(poly)
    offset = offset * scale
    offset_lines = []
    new_poly = []

    for i in range(n):
        # Line endpoints
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        # Rescale for accuracy
        x1 = x1 * scale
        x2 = x2 * scale
        y1 = y1 * scale
        y2 = y2 * scale

        # Calculate the direction vector & normal vector
        vx, vy = x2 - x1, y2 - y1
        vx, vy = vy, -vx

        # normalize the normal vector
        length = sqrt(vx**2 + vy**2)
        vx, vy = vx / length, vy / length

        # Offset endpoints -> offset lines
        x1 = x1 - vx * offset
        y1 = y1 - vy * offset
        x2 = x2 - vx * offset
        y2 = y2 - vy * offset
        offset_lines.append((x1, y1, x2, y2))

    # Find intersections
    # New poly vertices are the intersection of the offset lines
    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    for i in range(n):
        (x1, y1, x2, y2) = offset_lines[i]
        (x3, y3, x4, y4) = offset_lines[(i + 1) % n]
        deno = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4) + 1e-6
        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - x4 * y3)) / deno
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - x4 * y3)) / deno
        new_poly.append((x / scale, y / scale))

    return new_poly
