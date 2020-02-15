from collections import namedtuple


do_home = namedtuple("do_home", "cur_pos")
do_path = namedtuple("do_path", "mode path")

do_segment = namedtuple("do_segment", "path ext")
do_move = namedtuple("do_move", "deltas")


def reader(fn):
    gc = open(fn)
    while 1:
        line = gc.readline()
        if not line:
            break
        yield line[:-1]


def path_gen(lines):
    relative_extrude_mode = None
    current = {
        "X": 0.0,
        "Y": 0.0,
        "Z": 0.0,
        "E": 0.0
    }
    home_position = {
        "X": 12700.0 / 80,
        "Y": -20000.0 / 80,
        "Z": 20000.0 / 1600,
        "E": 0.0
    }
    current_feed = None

    path = []
    current_mode = None
    line_number = 0
    while 1:
        try:
            l = next(lines)
            line_number += 1
        except StopIteration:
            if path and current_mode:
                yield do_path(current_mode, path)
            break

        if ';' in l:
            l = l.split(';')[0]
        l = l.strip()
        if not l:
            continue

        # print("Line:", l)

        if l[0] == "M":
            parts = l.split()
            code = int(parts[0][1:])
            if code == 82:
                relative_extrude_mode = False
                continue
            elif code == 83:
                relative_extrude_mode = True
                continue
            elif code in (84, 104, 105, 106, 107, 109, 140, 190):
                continue
            else:
                print("{}: Unknown M{} command".format(line_number, code))
                break

        if l[0] == "G":
            parts = l.split()
            code = int(parts[0][1:])
            if code == 28:
                if path and current_mode:
                    yield do_path(current_mode, path)
                current_mode = None
                path = []
                print("Do Home")
                current = home_position.copy()
                yield do_home(current.copy())
                continue
            elif code == 92:
                print("Set current", parts[1:])
                abort = False
                for p in parts[1:]:
                    axis = p[0]
                    value = float(p[1:])
                    assert axis == "E"
                    if axis in current:
                        current[axis] = value
                    else:
                        print("{}: Unexpected G92 for {}".format(line_number, p))
                        abort = True
                        break
                if abort:
                    break
                continue
            elif code in (0, 1):
                if path and current_mode != code:
                    yield do_path(current_mode, path)
                    path = []
                current_mode = code
                if not path:
                    path.append(current.copy())
                step = {}
                abort = False
                for p in parts[1:]:
                    axis = p[0]
                    value = float(p[1:])
                    if axis in current:
                        if axis == "E" and relative_extrude_mode:
                            step[axis] = value
                        else:
                            step[axis] = (value - current[axis])
                        current[axis] = value
                    elif axis == "F":
                        current_feed = value
                    else:
                        print("{}: Unexpected G{} for {}".format(line_number, code, p))
                        abort = True
                        break
                if abort:
                    break
                step["F"] = current_feed
                step["line"] = line_number

                path.append(step)
                continue
            else:
                print("{}: Unknown G{} command".format(line_number, code))
                break

        print("{}: Unknown command: {}".format(line_number, l))
        break



def gen_segments(pg):
    extras = [0]
    ext = 0

    path = [[0, 0, 0]]
    x = 0
    y = 0
    z = 0

    for gc_path in pg:
        if isinstance(gc_path, do_home):
            print("do_home")
            yield do_home(gc_path.cur_pos)
            x = gc_path.cur_pos["X"]
            y = gc_path.cur_pos["Y"]
            z = gc_path.cur_pos["Z"]
        elif isinstance(gc_path, do_path):
            if 0:
                print("do_path", gc_path.mode, len(gc_path.path))
                # print("do_path", gc_path.path)

                print("   x:", x, gc_path.path[0]["X"])
                print("   y:", y, gc_path.path[0]["Y"])
                print("   z:", z, gc_path.path[0]["Z"])
            assert (abs(x - gc_path.path[0]["X"]) < 0.1)
            assert (abs(y - gc_path.path[0]["Y"]) < 0.1)
            assert (abs(z - gc_path.path[0]["Z"]) < 0.1)

            gc_segment = gc_path.path[1:]
            gc_seg_len = len(gc_segment)
            for i, p in enumerate(gc_segment):
                # print(i, p)
                if 0:
                    if p["line"] in range(29, 33):
                        print("Debug:", p)
                if ("Z" in p) or ((not "X" in p) and (not "Y" in p)):
                    if len(path) > 1:
                        path.append([x, y, 0])
                        extras.append(ext)

                        yield do_segment(path, extras)
                    if 0:
                        print(f"break at {p} non standart move ({i} of {seg_len})")
                    yield do_move(p)
                    if "X" in p:
                        dx = p["X"]
                        x += dx
                    if "Y" in p:
                        dy = p["Y"]
                        y += dy
                    if "Z" in p:
                        dz = p["Z"]
                        z += dz
                    if "E" in p:
                        de = -p.get("E", 0)
                        ext += de

                    extras = [ext]
                    path = [[x, y, 0]]
                else:
                    dx = p["X"]
                    dy = p["Y"]
                    de = -p.get("E", 0)
                    speed = p["F"] / 60.0 * 3

                    x += dx
                    y += dy
                    path.append([x, y, speed])
                    ext += de
                    extras.append(ext)

                    if len(path) > 100:
                        path.append([x, y, 0])
                        extras.append(ext)

                        yield do_segment(path, extras)

                        extras = [ext]
                        path = [[x, y, 0]]

    if len(path) > 1:
        path.append([x, y, 0])
        extras.append(ext)

        yield do_segment(path, extras)

