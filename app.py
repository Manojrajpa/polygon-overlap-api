from flask import Flask, request, jsonify
from shapely.geometry import Polygon

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    all_polygons = data.get("polygons", [])

    results = []

    for i, coords in enumerate(all_polygons):
        try:
            this_poly = Polygon(coords)
        except:
            results.append({
                "self_overlap": True,
                "overlap_count": 0,
                "overlap_percent": 0
            })
            continue

        self_overlap = not this_poly.is_valid
        overlap_count = 0

        for j, other_coords in enumerate(all_polygons):
            if i == j:
                continue
            try:
                other_poly = Polygon(other_coords)
                if this_poly.intersects(other_poly):
                    overlap_count += 1
            except:
                continue

        overlap_percent = (overlap_count / (len(all_polygons) - 1)) * 100 if len(all_polygons) > 1 else 0

        results.append({
            "self_overlap": self_overlap,
            "overlap_count": overlap_count,
            "overlap_percent": round(overlap_percent, 2)
        })

    return jsonify(results)
