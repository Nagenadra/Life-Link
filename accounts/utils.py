"""
Utility functions for location and distance calculations
"""
import math


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r


def get_nearby_users(user, users_queryset, max_distance_km=50):
    """
    Filter users based on distance from current user
    Returns users within max_distance_km radius
    """
    if not user.latitude or not user.longitude:
        return users_queryset.none()
    
    nearby_users = []
    for other_user in users_queryset:
        if other_user.latitude and other_user.longitude:
            distance = haversine_distance(
                user.latitude, user.longitude,
                other_user.latitude, other_user.longitude
            )
            if distance <= max_distance_km:
                other_user.distance_km = round(distance, 2)
                nearby_users.append(other_user)
    
    return nearby_users

