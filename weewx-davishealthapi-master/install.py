# installer for davishealthapi

import sys
import weewx

from weecfg.extension import ExtensionInstaller

def loader():

    return DavisHealthAPIInstaller()

class DavisHealthAPIInstaller(ExtensionInstaller):
    def __init__(self):
        super(DavisHealthAPIInstaller, self).__init__(
            version='0.20',
            name='davishealthapi',
            description='Collect and display station health information from the Davis WeatherLink API.',
            author='uajqq, KW',
            author_email='',
            data_services='user.davishealthapi.DavisHealthAPI',
            config = {
                'davishealthapi': {
                    'data_binding': 'davishealthapi_binding',
                    'station_id': '',
                    'api_key': '',
                    'api_secret': '',
                    '#max_age': 'None - default = 2592000',
                    'packet_log': '0',
                    '#packet_log': '0= first check and log available sensortypes once at start,  5= log all (packets ...)',
                    '#max_count': '13',
                    'sensor_tx1': '0',
                    'sensor_tx2': '0',
                    'sensor_tx3': '0',
                    'sensor_tx4': '0',
                    'sensor_tx5': '0',
                    'sensor_tx6': '0',
                    'sensor_tx7': '0',
                    'sensor_tx8': '0',
                },
                'DataBindings': {
                    'davishealthapi_binding': {
                        'database': 'davishealthapi_sqlite',
                        'table_name': 'archive',
                        'manager': 'weewx.manager.DaySummaryManager',
                        'schema': 'user.davishealthapi.schema'
                    }
                },
                'Databases': {
                    'davishealthapi_sqlite': {
                        'database_type': 'SQLite',
                        'database_name': 'davishealthapi.sdb'}
                },
                'StdReport': {
                    'DavisHealth': {
                        'skin': 'health',
                        'enable': 'True',
                        'HTML_ROOT': '/var/www/html/weewx/health'
                    },
                }
            },
            files=[('bin/user', ['bin/user/davishealthapi.py']),
                   ('skins/nws', ['skins/health/index.html.tmpl',
                    'skins/health/skin.conf',
                    'skins/health/health.css',
                    'skins/health/health.js',
                    'skins/health/favicon.ico',
                    'skins/health/sensors.inc',
                    'skins/health/sensorsair.inc',
                    'skins/health/titlebar.inc',
                    'skins/health/identifier.inc',
                ]),
            ]
        )
