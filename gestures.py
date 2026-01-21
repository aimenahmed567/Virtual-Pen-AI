def is_inside(x, y, box):
    x1, y1, x2, y2 = box
    return x1 < x < x2 and y1 < y < y2


def fingers_state(lm_list):
    if not lm_list or len(lm_list) < 13:
        return {"index": False, "middle": False}

    lm = {i: (x, y) for i, x, y in lm_list}
    index_up = lm[8][1] < lm[6][1]
    middle_up = lm[12][1] < lm[10][1]
    return {"index": index_up, "middle": middle_up}


def is_draw_gesture(lm_list):
    s = fingers_state(lm_list)
    return s["index"] and not s["middle"]


def is_stop_gesture(lm_list):
    s = fingers_state(lm_list)
    return s["index"] and s["middle"]
