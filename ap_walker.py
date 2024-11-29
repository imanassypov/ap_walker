import dnac_inventory
import os
import time
import paramiko
from multiprocessing import Process
import json


def execute_command_on_host(host_ip, 
                            username, 
                            password, 
                            enable, 
                            command, 
                            timeout: float,
                            log_file):
    '''
            :Run a command on a network device using SSH
    '''
        
    output = ""
    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the host
        ssh.connect(host_ip, username=username, password=password)
        print (f"Connected to {host_ip}\n executing command: {command}\n")
        
        # Open a shell
        shell = ssh.invoke_shell()
        time.sleep(1)
        
        # Enter enable mode
        shell.send('enable\n')
        time.sleep(1)
        
        shell.send(enable + '\n')
        time.sleep(1)
        
        # Execute the command
        shell.send(command + '\n')
        time.sleep(1)
        
        # Wait for the command to complete and read the output
        start_time = time.time()
        while True:
            if shell.recv_ready():
                output += shell.recv(1024).decode('utf-8')
            elif time.time() - start_time > float(timeout):  # Break if timeout is reached
                print("Timeout waiting for command to complete")
                break
            else:
                time.sleep(1)  # Sleep briefly to avoid high CPU usage
            if output.strip().endswith("#"):
                break
            else:
                print(output)

        # Close the connection
        ssh.close()
        
    except Exception as e:
        print(f"Failed to execute command on {host_ip}: {str(e)}")
        
    # Append the output to a log file
    with open(log_file, 'w') as file:
        file.write(output)
    
    return output

def main():
    dnac_ip = os.getenv('DNAC_IP')
    dnac_username = os.getenv('DNAC_USERNAME')
    dnac_password = os.getenv('DNAC_PASSWORD')
    dnac_version = os.getenv('DNAC_VERSION')
    dnac_validate_certs = os.getenv('DNAC_VALIDATE_CERTS')
    dnac_site_name_file = os.getenv('DNAC_SITE_NAMES_FILE')
    dnac_device_family = os.getenv('DNAC_DEVICE_FAMILY')
    ap_username = os.getenv('AP_USERNAME')
    ap_password = os.getenv('AP_PASSWORD')
    ap_enable = os.getenv('AP_ENABLE')
    ap_cli = os.getenv('AP_CLI')
    ap_cli_timeout = os.getenv('AP_CLI_TIMEOUT')
    log_folder = os.getenv('LOG_FOLDER')

    if dnac_site_name_file is None:
        raise Exception("Environment variable DNAC_SITE_NAMES_FILE is not set")
    
    with open(dnac_site_name_file, 'r') as file:
        dnac_site_names = json.load(file)
        print (f"Read DNAC Site names: {json.dumps(dnac_site_names, indent=4)}")

    required_vars = {
        'DNAC_IP': dnac_ip,
        'DNAC_USERNAME': dnac_username,
        'DNAC_PASSWORD': dnac_password,
        'DNAC_VERSION': dnac_version,
        'DNAC_VALIDATE_CERTS': dnac_validate_certs,
        'DNAC_SITE_NAMES': dnac_site_names,
        'DNAC_DEVICE_FAMILY': dnac_device_family,
        'AP_USERNAME': ap_username,
        'AP_PASSWORD': ap_password,
        'AP_ENABLE': ap_enable,
        'AP_CLI': ap_cli,
        'AP_CLI_TIMEOUT': ap_cli_timeout,
        'LOG_FOLDER': log_folder,
    }

    for var_name, var_value in required_vars.items():
        if var_value is None:
            raise Exception(f"Environment variable {var_name} is not set")
 
    inventory_module = dnac_inventory.InventoryModule()
    inventory_module.validate_certs = False
    inventory_module.host = dnac_ip
    inventory_module.dnac_version = dnac_version
    inventory_module.username = dnac_username
    inventory_module.password = dnac_password
    
    # initialize the DNAC API
    _dnac_api = inventory_module._login()
    
    # iterate over site list specified in site list file
    for site_name in dnac_site_names['sites']:
        # pull devices associated to the site
        _dnac_hosts = inventory_module._get_hosts_per_site(site_name=site_name,
                                                           family=dnac_device_family)
        site_index = dnac_site_names['sites'].index(site_name) + 1
        total_sites = len(dnac_site_names['sites'])
        print (f"Site [{site_index}/{total_sites}]:\t{site_name},\tHosts: {len(_dnac_hosts)}")
        
        processes = []
        print (f"\tSpawning [{len(_dnac_hosts)}] processes to connect to APs...")
        for host in _dnac_hosts:
            management_ip = host["managementIpAddress"]
            log_file = os.path.join(log_folder, f"{management_ip}.log")
            p = Process(target=execute_command_on_host, 
                        args=(management_ip, 
                            ap_username, 
                            ap_password, 
                            ap_enable, 
                            ap_cli,
                            ap_cli_timeout,
                            log_file))
            p.start()
            processes.append(p)
        print (f"Spawned {len(processes)} processes. Awaiting completion")
        for p in processes:
            p.join()
            if p.exitcode != 0:
                print(f"Process {p.pid} failed with exit code {p.exitcode}")
            else:
                print(f"Process {p.pid} completed successfully")


if __name__ == "__main__":
    main()