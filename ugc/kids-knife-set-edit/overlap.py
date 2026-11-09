"""Gate oracle: python3 overlap.py -> NO_OVERLAP when no segment of the reframed V2 shares any moment (HD timeline) with V1's 12 segments."""
import json,sys
V1=[(0.0,1.4),(4.4,5.6),(10.0,11.4),(14.8,16.0),(18.0,19.2),(22.0,23.0),(26.0,27.2),(28.5,29.7),(32.0,33.2),(34.5,35.5),(36.4,37.6),(40.0,41.4)]
segs=json.load(open("out/knife_v3.json"))["segs"]
hits=[(a,b,c,d) for a,b in segs for c,d in V1 if a<d and c<b]
print("NO_OVERLAP" if not hits else f"OVERLAP {hits}"); sys.exit(1 if hits else 0)
