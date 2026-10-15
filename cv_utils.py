import cv2
import numpy as np


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(image, pts, width=400, height=500):
    rect = order_points(pts)
    dst = np.array([[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (width, height))
    return warped, M


def detect_board_polygon(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7,7), 0)
    edged = cv2.Canny(blurred, 50, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        h, w = img.shape[:2]
        return np.array([[0,0],[w-1,0],[w-1,h-1],[0,h-1]], dtype=np.float32)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in contours[:6]:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4 and cv2.contourArea(approx) > 10000:
            pts = approx.reshape(4, 2)
            return pts.astype(np.float32)
    h, w = img.shape[:2]
    return np.array([[0,0],[w-1,0],[w-1,h-1],[0,h-1]], dtype=np.float32)


def find_piece_contours(warped):
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    th = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 11, 4)
    kernel = np.ones((3,3), np.uint8)
    opened = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=1)
    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pieces = []
    h, w = warped.shape[:2]
    for c in contours:
        area = cv2.contourArea(c)
        if area < (w*h)*0.002:
            continue
        x,y,ww,hh = cv2.boundingRect(c)
        M = cv2.moments(c)
        if M['m00'] == 0: continue
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        pieces.append({'bbox': (x,y,ww,hh), 'area': area, 'centroid': (cx,cy)})
    pieces = sorted(pieces, key=lambda p: p['area'], reverse=True)
    return pieces


def pieces_to_grid(pieces, grid_w, grid_h, board_w, board_h):
    cell_w = board_w / grid_w
    cell_h = board_h / grid_h
    out = []
    seen = set()
    for p in pieces:
        x,y,ww,hh = p['bbox']
        gx0 = x / cell_w
        gy0 = y / cell_h
        gx1 = (x + ww) / cell_w
        gy1 = (y + hh) / cell_h
        ix0 = int(round(gx0 - 1e-9))
        iy0 = int(round(gy0 - 1e-9))
        ix1 = int(round(gx1 + 1e-9))
        iy1 = int(round(gy1 + 1e-9))
        ix0 = max(0, min(grid_w-1, ix0))
        iy0 = max(0, min(grid_h-1, iy0))
        ix1 = max(ix0+1, min(grid_w, ix1))
        iy1 = max(iy0+1, min(grid_h, iy1))
        w = ix1 - ix0
        h = iy1 - iy0
        key = (ix0, iy0, w, h)
        if key in seen:
            continue
        seen.add(key)
        out.append({'x': ix0, 'y': iy0, 'w': w, 'h': h, 'area': p['area'], 'centroid': p['centroid']})
    return out


def detect_pieces_from_image(img, grid_w=4, grid_h=5, debug_mode=False):
    h, w = img.shape[:2]
    board_pts = detect_board_polygon(img)
    warped, M = four_point_transform(img, board_pts, width=400, height=500)
    pieces = find_piece_contours(warped)
    mapped = pieces_to_grid(pieces, grid_w, grid_h, board_w=400, board_h=500)
    debug = {'board_pts': board_pts.tolist() if hasattr(board_pts, 'tolist') else None,
             'raw_pieces': pieces}
    return mapped, debug


def normalize_pieces(pieces, grid_w=4, grid_h=5):
    out = []
    for p in pieces:
        out.append({'x': int(p['x']), 'y': int(p['y']), 'w': int(p['w']), 'h': int(p['h'])})
    out = sorted(out, key=lambda q: (q['y'], q['x']))
    return out
