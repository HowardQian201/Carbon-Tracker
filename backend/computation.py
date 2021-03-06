#Base Python
import os
import requests
import sys
#Extended Python
from pprint import pprint
from session import get_rest

#Database Python
from sqlite3 import connect, Row

class Computation():
    def __init__(self, location_list, modes):
        super().__init__()
        self.rest = get_rest()
        self.url = "https://maps.googleapis.com/maps/api/directions/json"
        self.headers = {"Content-Type": "application/json"}
        self.locations = location_list
        self.modes = modes
        self.key = os.environ.get('GOOGLE_API_KEY')
        self.dist_list = []
        self.building_geo_mappings = {'Martel' : '29.72177,-95.39768', 'Brown': '29.72167,-95.39629', 'Hanszen': '29.71593,-95.40020',
            'Lovett':'29.71644,-95.39805', 'Wiess':'29.71523,-95.40079','Jones':'29.72166, -95.39680',
            'Duncan':'29.72199,-95.39849', 'McMurtry':'29.72062,-95.39773', 'Sid Richardson':'29.71514,-95.39905',
            'Baker': '29.71705,-95.39911', 'Will Rice': '29.71652,-95.39869', 'Herzstein Hall':'29.71933,-95.39851','Sewall Hall':'29.71821,-95.39773', 'Keck Hall': '29.71977, -95.39990',
            'RMC':'29.71797,-95.40179', 'Fondren':'29.71829,-95.40008', 'Cambridge Office Building':'29.71760, -95.39806',
            'Brockman Hall': '29.71976,-95.40160', 'Dell Butcher Hall':'29.71980,-95.40337', 'Rec center':'29.71824,-95.40326',
            'Shepherd School of Music':'29.71621,-95.40527', 'Duncan Hall':'29.72043,-95.39860', 'Ryon Laboratory':'29.72072,-95.40057', 'Mudd Building':'29.72047,-95.40103', 'Hamman Hall':'29.72017,-95.40180',
            'MD Anderson Labs':'29.71869,-95.40230', 'McNair Hall':'29.71759,-95.40343', 'Herring Hall':'29.71693,-95.40119', 'Brochstein Pavilion':'29.71789,-95.40066', 'Humanities Building':'29.71754,-95.39946', 'Rice Bikes':'29.71682,-95.40041', 'Kraft Hall':'29.71576,-95.40242',
            'Tudor Fieldhouse':'29.71539,-95.40352', 'Skyspace':'29.71662,-95.40400', 'Baker Institute':'29.71655,-95.40251', 'Jones School of Business':'29.71764,-95.40270', 'Valhalla':'29.71933,-95.40024', 'OEDK': '29.72112,-95.40126', 'Abercrombie':'29.72088, -95.39906', 'Lovett Hall':'29.71905,-95.39774',
            'Reckling Park':'29.71339,-95.40410', 'Moody Center for the Arts':'29.71425,-95.40549', 'Glasscock School':'29.71482,-95.40640', 'Rice Media Center':'29.71410, -95.40602', 'Tennis Courts':'29.71831,-95.40779', 'Rice Stadium':'29.71641,-95.40908', 'Patterson Center':'29.71733,-95.40831', 'Rice Bike Track':'29.71616,-95.41093',
            'Rayzor Hall':'29.71801,-95.39903', 'Anderson Hall': '29.71896,-95.39974', 'Liu Idea Lab':'29.71714,-95.39717', 'West Servery':'29.72111,-95.39847', 'North Servery':'29.72193,-95.39655', 'Baker Servery':'29.71706,-95.39948', 'South Servery':'29.71524,-95.40121', 'Seibel Servery':'29.71609,-95.39820', 'Sid Richardson Servery':'29.71522,-95.39883', 'Holloway Field':'29.71294,-95.40207', 'Founders Court':'29.71939,-95.39719',
            'Greenbriar Lot':'29.71645,-95.41198', 'West Lot':'29.71654,-95.40678', 'North Lot':'29.72052,-95.40273', 'South Lot':'29.71542,-95.39813', 'Founders Court Lot':'29.71863, -95.39675', 'Lovett Hall Lot':'29.72000,-95.39729', 'North Colleges Lot':'29.72108,-95.39494', 'Hess Lot':'29.71344,-95.40521'}

    def total_distances(self):
        print(self.key)
        ttl_walking_distance = 0.0
        ttl_driving_distance = 0.0
        ttl_cycling_distance = 0.0
        for i in range(len(self.locations)-1):
            start_point = self.locations[i]
            end_point = self.locations[i+1]
            if start_point in self.building_geo_mappings.keys() and end_point in self.building_geo_mappings.keys():
                api_url = self.url + "?origin=" + self.building_geo_mappings[start_point] + "&destination=" + self.building_geo_mappings[end_point] + "&mode="+self.modes[i]+"&key="+self.key
                response = self.rest.get(api_url)
                if response.status_code not in range(200,300):
                    print("Failed to get data on " + str(api_url))
                    return
                json_response = response.json()
                curr_dist = json_response['routes'][0]['legs'][0]['distance']['text']
                distances = curr_dist.split(" ")
                if "mi" in curr_dist:
                    distance = float(distances[0]) * 5280
                else:
                    distance = float(distances[0])

                if self.modes[i] == 'walking':
                    ttl_walking_distance+=distance
                if self.modes[i] == 'driving':
                    ttl_driving_distance+=distance
                if self.modes[i] == 'cycling':
                    ttl_cycling_distance+=distance
        self.dist_list.append(ttl_walking_distance/5280)
        self.dist_list.append(ttl_cycling_distance/5280)
        self.dist_list.append(ttl_driving_distance/5280)

    def walking_distance(self):
        return round(self.dist_list[0], 1)

    def cycling_distance(self):
        return round(self.dist_list[1], 1)

    def driving_distance(self):
        return round(self.dist_list[2], 1)

    def carbon_dioxide_saved(self):
        non_driving_distance = self.dist_list[0] + self.dist_list[1]
        pounds_saved = .9061 * non_driving_distance
        return round(pounds_saved, 1)

    def total_calories(self):
        cals = 75 * self.dist_list[0] + 55 * self.dist_list[1]
        return int(cals)



    def database_write(self, user,walked,biked,driven,co2,calories):
        DB_FILE = "app.db"
        db = connect(DB_FILE)
        c = db.cursor()
        c.execute("UPDATE users SET milesWalked=?, milesBiked=?, milesDriven=?, co2Saved=?, calories=? WHERE username=?", (str(walked),str(biked),str(driven),str(co2),str(calories),str(user)))
        db.commit()
        db.close()




if __name__ == "__main__":
    user_id = sys.argv[1]
    locations_string = sys.argv[2][1:-1]
    transport_modes_string = sys.argv[3][1:-1]

    locations = locations_string.split(",")
    transport_modes = transport_modes_string.split(",")

    comp = Computation(locations, transport_modes)
    comp.total_distances()
    walked_dist = comp.walking_distance()
    cycled_dist = comp.cycling_distance()
    driven_dist = comp.driving_distance()
    carbon_dioxide_saved = comp.carbon_dioxide_saved()
    calories_burned = comp.total_calories()

    comp.database_write(user_id, walked_dist, cycled_dist, driven_dist, carbon_dioxide_saved, calories_burned)
