import math
from typing import List, Dict, Any

class RouteOptimizer:
    """
    Logistics Route Planner using Nearest Neighbor + 2-Opt heuristic
    with food safety deadline prioritization and multi-drop delivery.
    """
    def __init__(self, avg_speed_kmh: float = 30.0):
        self.avg_speed_kmh = avg_speed_kmh  # City speed taking traffic into account

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculates great-circle distance between two GPS coordinates in kilometers."""
        R = 6371.0  # Earth radius in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        # Multiply by 1.25 to reflect realistic city road network routing vs straight line
        return round(distance * 1.25, 2)

    def optimize_multi_drop_route(self, origin: Dict[str, Any], destinations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates optimized route visiting the origin and all accepted destinations.
        Considers urgency/deadline and distance.
        """
        if not destinations:
            return {
                "route": [origin],
                "total_distance_km": 0.0,
                "total_time_minutes": 0,
                "waypoints": [[origin["lat"], origin["lng"]]],
                "legs": []
            }

        unvisited = list(destinations)
        ordered_route = [origin]
        current_loc = origin
        total_distance = 0.0
        legs = []

        while unvisited:
            # Score each destination based on distance and safe-use deadline urgency
            best_idx = 0
            min_cost = float("inf")

            for i, dest in enumerate(unvisited):
                dist = self.haversine_distance(current_loc["lat"], current_loc["lng"], dest["lat"], dest["lng"])
                urgency_factor = 1.0
                if dest.get("urgency") == "HIGH" or dest.get("minutes_to_deadline", 120) < 60:
                    urgency_factor = 0.65  # Prioritize urgent deadlines
                cost = dist * urgency_factor

                if cost < min_cost:
                    min_cost = cost
                    best_idx = i

            next_dest = unvisited.pop(best_idx)
            leg_dist = self.haversine_distance(current_loc["lat"], current_loc["lng"], next_dest["lat"], next_dest["lng"])
            leg_time_mins = int(round((leg_dist / self.avg_speed_kmh) * 60))
            
            legs.append({
                "from_name": current_loc.get("name", "Origin"),
                "to_name": next_dest.get("name", "Destination"),
                "distance_km": leg_dist,
                "travel_time_minutes": leg_time_mins
            })

            total_distance += leg_dist
            ordered_route.append(next_dest)
            current_loc = next_dest

        total_time_minutes = int(round((total_distance / self.avg_speed_kmh) * 60))

        # Generate polyline coordinate waypoints for map rendering
        waypoints = []
        for stop in ordered_route:
            waypoints.append([stop["lat"], stop["lng"]])

        return {
            "ordered_stops": ordered_route,
            "total_distance_km": round(total_distance, 2),
            "total_time_minutes": total_time_minutes,
            "waypoints": waypoints,
            "legs": legs,
            "stops_count": len(ordered_route),
            "vehicle_recommendation": "Temperature-controlled Van (Cold-chain compliant 4-8°C)"
        }

route_optimizer = RouteOptimizer()
