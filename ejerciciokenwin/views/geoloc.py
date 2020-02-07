import geoip2.database

class Localization:
    def __init__(self, ip):
        self.ip = ip
        self.read = geoip2.database.Reader('ejerciciokenwin/views/GeoLite2-City.mmdb')
        self.resp = self.read.city(ip)
        self.city_name = self.resp.city.name
        self.province_name = self.resp.subdivisions.most_specific.name
        self.pc = self.resp.postal.code
        self.tz = self.resp.location.time_zone
        self.lat = self.resp.location.latitude
        self.lon = self.resp.location.longitude
        self.country_name = self.resp.country.name
        self.country_code = self.resp.country.iso_code
        self.hem = 'North Hemisphere' if self.lat > 0 else 'South Hemisphere'


    def close(self):
            self.read.close()

