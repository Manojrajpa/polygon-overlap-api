from flask import Flask, request, jsonify
from shapely.geometry import Polygon
import logging

app = Flask(__name__)

@app.route('/')
def health_check():
    return "API is running!"

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        all_polygons = data.get("polygons", [])
    except Exception as e:
        return jsonify({"error": "Invalid input JSON", "details": str(e)}), 400

    results = []

    for i, coords in enumerate(all_polygons):
        try:
            this_poly = Polygon(coords)
            self_overlap = not this_poly.is_valid
        except Exception:
            results.append({
                "self_overlap": True,
                "overlap_count": 0,
                "overlap_percent": 0,
                "error": "Invalid polygon"
            })
            continue

        overlap_count = 0
        for j, other_coords in enumerate(all_polygons):
            if i == j:
                continue
            try:
                other_poly = Polygon(other_coords)
                if this_poly.intersects(other_poly):
                    overlap_count += 1
            except Exception:
                continue

        overlap_percent = (overlap_count / (len(all_polygons) - 1)) * 100 if len(all_polygons) > 1 else 0

        results.append({
            "self_overlap": self_overlap,
            "overlap_count": overlap_count,
            "overlap_percent": round(overlap_percent, 2)
        })

    return jsonify(results)
