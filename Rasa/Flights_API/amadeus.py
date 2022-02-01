import requests
import json
from dotenv import load_dotenv
import argparse
import random
import os
import sys

sys.path.append('..')
load_dotenv('../../.env')

def get_oauth_headers():
    oauth_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    return oauth_headers

def get_oauth_keys(grant_type, client_id, client_secret):
    oauth_keys = {
        'grant_type': grant_type,
        'client_id': client_id,
        'client_secret': client_secret
    }
    return oauth_keys

def get_oauth_response(oauth_url, oauth_headers, oauth_keys):
    oauth_response = requests.post(oauth_url, headers=oauth_headers, data=oauth_keys).json()
    return oauth_response

def get_oauth_token(oauth_response, access_token_key):
    access_token = oauth_response[access_token_key]
    return access_token

def get_headers(token):
    headers = {
        'Authorization': 'Bearer ' + token,
    }
    return headers

def get_iata_code(dict_cityname, cityname):
    if len(cityname) == 3:
        return cityname.upper()
    return dict_cityname["data"][cityname.lower()]['code']
def get_city_name(dict_citycode, citycode):
    return dict_citycode["data"][citycode]['city']

def get_api_and_params(opt):
    originLocationCode, destinationLocationCode, departureDate, returnDate, adults, nonStop, maxPrice = \
        opt.originLocationCode, opt.destinationLocationCode, opt.departureDate, opt.returnDate, opt.adults, opt.nonStop, opt.maxPrice
    # api = 'https://test.api.amadeus.com/v1/shopping/flight-destinations'
    # params = (
        # ('origin', 'PAR'),
        # ('maxPrice', '200'),
    # )

    api = 'https://test.api.amadeus.com/v2/shopping/flight-offers'

    params = (
        ('originLocationCode', originLocationCode),
        ('destinationLocationCode', destinationLocationCode),
        ('departureDate', departureDate), #YEAR-MONTH-DATE
        ('returnDate', returnDate), #YEAR-MONTH-DATE
        ('adults', adults),
        ('nonStop', nonStop),
        ('maxPrice', maxPrice)
        # ('currencies', 'EUR'),
    )

    return api, params

def get_response(api, headers, params):
    response = requests.get(api, headers=headers, params=params).json()
    # response = requests.get(api+'?origin=PAR&maxPrice=200', headers=headers).json()
    # response = requests.get(api+'?originLocationCode=PAR&destinationLocationCode=MAD&departureDate=2021-11-03&returnDate=2021-11-10&adults=1&nonStop=false&maxPrice=200', headers=headers).json()
    return response

def get_response_data(response, data_key):
    return response[data_key]
def get_flight_code(carrierCode, number):
    return carrierCode + str(number)
def add_more_response_manually(gate_number, segment_response):
    segment_response['gate_number'] = gate_number
    seatlist = ['A', 'B', 'C', 'D', 'E', 'F']
    segment_response['seat_number'] = str(random.randint(1,100)) + random.choice(seatlist)
    return segment_response


def to_inr(conv_rate, amount):
    return amount * conv_rate
def to_euro(conv_rate, amount):
    return amount / conv_rate


def get_required_response(opt, dict_citycode, ticket_id, direction, response_data):
    # response_data[i]['itineraries'][j]['segments'][k]
    # i = ticket_id; j = 0 if oneway, 1 if twoway; k = number of stops in a single way
    segment_resp = {"segment" : []}
    num_of_segments = len(response_data[ticket_id]['itineraries'][direction]['segments'])
    for segment in range(0, num_of_segments):
        segment_response = {}

        segment_response['origin_iata_code'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['departure']['iataCode']
        segment_response['destination_iata_code'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['arrival']['iataCode']
    
        segment_response['origin'] = dict_citycode["data"][segment_response['origin_iata_code']]['city']
        segment_response['destination'] = dict_citycode["data"][segment_response['destination_iata_code']]['city']

        segment_response['departure_at'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['departure']['at']
        segment_response['departure_date'] = segment_response['departure_at'][:10]
        segment_response['departure_time'] = segment_response['departure_at'][10:]
        segment_response['arrival_at'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['arrival']['at']
        segment_response['arrival_date'] = segment_response['arrival_at'][:10]
        segment_response['arrival_time'] = segment_response['arrival_at'][10:]
        del segment_response['departure_at']
        del segment_response['arrival_at']

        segment_response['price'] = to_inr(opt.conv_rate, float(response_data[ticket_id]['price']['total']))
        segment_response['flight_code'] = get_flight_code(response_data[ticket_id]['itineraries'][direction]['segments'][segment]['carrierCode'], \
                                            response_data[ticket_id]['itineraries'][direction]['segments'][segment]['number'])
        segment_response['aircraft_code'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['aircraft']['code']
        segment_response['duration'] = response_data[ticket_id]['itineraries'][direction]['segments'][segment]['duration'][2:]
        segment_response['num_of_stops'] = num_of_segments - 1
        segment_response['cabin'] = response_data[ticket_id]['travelerPricings'][0]['fareDetailsBySegment'][segment]['cabin']
        

        segment_response['origin_airportname'] = dict_citycode["data"][segment_response['origin_iata_code']]['airportname']
        segment_response['destination_airportname'] = dict_citycode["data"][segment_response['destination_iata_code']]['airportname']
        segment_response['origin_GMT'] = dict_citycode["data"][segment_response['origin_iata_code']]['gmt']
        segment_response['destination_GMT'] = dict_citycode["data"][segment_response['destination_iata_code']]['gmt']

        segment_response['numberOfBookableSeats'] = response_data[ticket_id]['numberOfBookableSeats']


        gate_number = random.randint(0,50)
        segment_response = add_more_response_manually(gate_number, segment_response)

        segment_resp["segment"].append(segment_response)

    return segment_resp


def parse_opt(known = False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--conv-rate', type=float, default=86.17, help=' EUR to INR currency conversion rate i.e. EUR = conv_rate * INR')
    parser.add_argument('--originLocationName', type=str, default='mumbai', help='origin airport IATA code')
    parser.add_argument('--destinationLocationName', type=str, default='NAGpur', help='destination airport IATA code')
    parser.add_argument('--departureDate', type=str, default='2021-11-10', help='date of onboarding')
    parser.add_argument('--returnDate', type=str, default='2021-11-11', help='date of onboarding')
    parser.add_argument('--adults', type=str, default='1', help='number of tickets')
    parser.add_argument('--nonStop', type=str, default='false', help='requirement of nonStop flight')
    parser.add_argument('--maxPrice', type=str, default='10000', help='maxPrice in INR for the total journey')
    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt

def run(**kwargs):
    opt = parse_opt(True)
    for k, v in kwargs.items():
        setattr(opt, k, v)
    return main(opt)

def main(opt):
    oauth_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
    oauth_headers = get_oauth_headers()
    grant_type = 'client_credentials'
    client_id = os.getenv('API_KEY', 'api key from amadeus')
    client_secret = os.getenv('API_SECRET', 'api secret from amadeus')
    oauth_keys = get_oauth_keys(grant_type, client_id, client_secret)
    oauth_response = get_oauth_response(oauth_url, oauth_headers, oauth_keys)
    # print("oauth_response", oauth_response)
    access_token_key = 'access_token'
    token = get_oauth_token(oauth_response, access_token_key)
    # print("token", token)

    # should start from here
    # load the stored token
    # try to get the response data
    # if success, then continue below onwards
    # if catch block then generate the token from above
    # TWO stuffs : LOAD THE TOKEN | GENERATE THE TOKEN AND STORE IT(encoded; JWT??)
    headers = get_headers(token)

    # with open('dict_cityname.json') as json_file:
    with open('../Flights_API/dict_cityname.json') as json_file:
        dict_cityname = json.load(json_file)
    opt.originLocationCode = get_iata_code(dict_cityname, opt.originLocationName)
    opt.destinationLocationCode = get_iata_code(dict_cityname, opt.destinationLocationName)

    api, params = get_api_and_params(opt)
    response = get_response(api, headers, params)
    # print(response)
    data_key = 'data'
    response_data = get_response_data(response, data_key)

    # with open('dict_citycode.json') as json_file:
    with open('../Flights_API/dict_citycode.json') as json_file:
        dict_citycode = json.load(json_file)

    opt.originLocationName = get_city_name(dict_citycode, opt.originLocationCode)
    opt.destinationLocationName = get_city_name(dict_citycode, opt.destinationLocationCode)

    opt.maxPrice = to_euro(opt.conv_rate, float(opt.maxPrice))

    final_response = {"data" : []}
    num_of_directions = 2 # 1 or 2
    for ticket_id in range(0, int(opt.adults)):
        direction_response = {"direction" : []}
        for direction in range(0, num_of_directions):
            segment_response = get_required_response(opt, dict_citycode, ticket_id, direction, response_data)
            direction_response["direction"].append(segment_response)
        final_response["data"].append(direction_response)

    return final_response


if "__main__" == __name__:
    opt = parse_opt(True)
    main(opt)

