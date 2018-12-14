# Prism Service Check - Check if Prism services are running. If not then reboot the system.
# By Zach Cutberth

import psutil
import os
import time

services_list = ['PrismMQService',
                'PrismCommonService',
                'PrismResiliencyService',
                'PrismBackOfficeService',
                'PrismV9Service',
                'PrismLicSvr',
                'rabbitmq',
                'Apache']

time_and_date = time.strftime("%Y\\%m\\%d %H:%M:%S")

log = open('PrismServiceCheckLog.txt', 'a')
log.write('[' + time_and_date + '] Checking the state Prism services...\n')

def getServiceStatus(serviceName):
    try:
        service = psutil.win_service_get(serviceName).as_dict()
    except:
        return 'Not Installed'
    
    return service
    
for service in services_list:
    service = getServiceStatus(service)

    if service == 'Not Installed':
        continue

    if service['status'] != 'running':
        log.write('[Service Name] ' + service['name'] + ' [Service State] ' + service['status'] + '\n')
        log.write(service['name'] + ' is not in a running state.\n')
        log.write('Not all Prism services are running, rebooting system...\n')
        os.system('shutdown -t 0 -r -f')

    if service['status'] == 'running':
        log.write('[Service Name] ' + service['name'] + ' [Service State] ' + service['status'] + '\n')

log.write('Logging stopped. \n\n')
log.close()