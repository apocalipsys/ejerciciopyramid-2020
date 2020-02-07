import geoip2.database

class Localizacion:
    def __init__(self, ip):
        self.ip = ip
        self.read = geoip2.database.Reader('ejerciciokenwin/views/GeoLite2-City.mmdb')
        self.resp = self.read.city(ip)
        self.nombre_ciudad = self.resp.city.name
        self.nombre_provincia = self.resp.subdivisions.most_specific.name
        self.cp = self.resp.postal.code
        self.tz = self.resp.location.time_zone
        self.lat = self.resp.location.latitude
        self.lon = self.resp.location.longitude
        self.pais = self.resp.country.name
        self.cod_pais = self.resp.country.iso_code
        self.hem = 'hemisferio norte' if self.lat > 0 else 'hemisferio sur'


    def close(self):
            self.read.close()

