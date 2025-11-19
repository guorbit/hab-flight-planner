import warnings
import numpy as np

# Some code is loosely based off of https://github.com/seangrogan/great_circle_calculator


class LatLon:
    def __init__(self, lat: float, lon: float):
        if (-90 <= lat <= 90) and (-180 <= lon <= 180):
            self.lat = lat
            self.lon = lon
        elif (-90 <= lon <= 90) and (-180 <= lat <= 180):
            _msg = '\n'.join(("\nThe provided latitude and longtitude appears to be flipped",
                              "Acceptable range is -90 ≤ lat ≤ 90 and -180 ≤ lon ≤ 180",
                              "However, opposite holds for the given values. Re-interpreting as (lon, lat)"))
            warnings.warn(_msg)
            self.lat = lon
            self.lon = lat
        else:
            raise ValueError(
                "Acceptable range is -90 ≤ lat ≤ 90 and -180 ≤ lon ≤ 180")

    @classmethod
    def from_base60_deg(cls, lat: tuple[int, int, float], east: bool, lon: tuple[int, int, float], north: bool):
        lat_abs = np.abs(lat)
        lon_abs = np.abs(lon)
        lat_deg = (lat_abs[0] + lat_abs[1] / 60 +
                   lat_abs[2] / 3600) * [-1, 1][east]
        lon_deg = (lon_abs[0] + lon_abs[1] / 60 +
                   lon_abs[2] / 3600) * [-1, 1][north]
        return cls(lat_deg, lon_deg)

    def to_radians(self) -> tuple[float, float]:
        return (np.radians(self.lat), np.radians(self.lon))

    def __str__(self):
        lat_sign = ('N', 'N', 'S')[int(np.sign(self.lat))]
        lat_min, lat_sec = np.divmod(np.abs(self.lat)*3600, 60)
        lat_deg, lat_min = np.divmod(lat_min, 60)
        lon_sign = ('E', 'E', 'W')[int(np.sign(self.lon))]
        lon_min, lon_sec = np.divmod(np.abs(self.lon)*3600, 60)
        lon_deg, lon_min = np.divmod(lon_min, 60)
        return f"{lat_deg:.0f}°{lat_min:02.0f}'{lat_sec:04.1f}\"{lat_sign} "\
            f"{lon_deg:.0f}°{lon_min:02.0f}'{lon_sec:04.1f}\"{lon_sign}"


def great_circle_distance(p1: LatLon, p2: LatLon):
    R_EARTH = 6371000
    lat1, lon1 = p1.to_radians()
    lat2, lon2 = p2.to_radians()
    distance = np.acos(np.sin(lat1) * np.sin(lat2) + np.cos(lat1)
                       * np.cos(lat2) * np.cos(lon2 - lon1)) * R_EARTH
    return distance
