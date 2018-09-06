from getpass import getpass
import netmiko
import csv
import json


#################################################################################################
#Script connects to cisco_ios device extracts bgp data, parses with textfsm, then               #
#outputs to .csv "show_bgp.csv"                                                                 #
#################################################################################################


def get_input(prompt=''):
    try:
        line = input(prompt)
    except NameError:
        line = input(prompt)
    return line

def get_credentials(): #Prompts for, and returns, a username and password.
    username = get_input('Enter Username: ')
    password = None
    while not password:
        password = getpass()
        password_verify = getpass('Retype to verify your password: ')
        if password != password_verify:
            print('Passwords do not match. Please try again')
            password = None
    return username, password


#Device ssh timeout and ssh authentication errors
netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,netmiko.ssh_exception.NetMikoAuthenticationException)



username, password = get_credentials()

#Opens json formatted device file for devices to be examined
with open('devices.json') as dev_file:
    devices = json.load(dev_file)



bgp_results = []

results = {'Successful':[], 'Failed':[]}


for device in devices:
    device['username'] = username
    device['password'] = password
    try:
        print('~' * 79) #Prints message for what device is being connected
        print('Connecting to device', device['ip'])
        connection = netmiko.ConnectHandler(**device)
        local_host = (connection.find_prompt())
        print(local_host)
        output = connection.send_command("show standby brief", use_textfsm=True)##textfsm integrated into Netmiko

        for item in output:
            item.update({"local_host":local_host})#Insert Local Hostname into dictionary
            bgp_results.append(item) #For Loop to append the OUTPUT results from connection.send_command


        connection.disconnect()
        results['Successful'].append(device['ip'])

    except netmiko_exceptions as e:
        print('Failed to', device, e)
        results['Failed'].append('.'.join((device['ip'], str(e))))

print(bgp_results)

print(json.dumps(results, indent=2))
with open('bgp_results.json', 'w') as results_file:
    json.dump(results, results_file, indent=2)


with open('sho_bgp.csv','w', newline='')as new_file:
   fieldnames = ['local_host','as_path','local_pref','metric', 'network', 'next_hop', 'origin','path_selection','route_source','status','weight']
   csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')

   csv_writer.writeheader()

   for line in (bgp_results):
     csv_writer.writerow(line)
     print(line)