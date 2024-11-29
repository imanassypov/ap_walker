try: 
    import requests, urllib3, math
    from dnacentersdk import DNACenterAPI
    from dnacentersdk import ApiError

except ApiError as e:
    print ('Python requests module is required for this plugin. Error: %s' % e)

class InventoryModule():

    NAME = 'dna_center'

    def __init__(self):

        self.username = None
        self.password = None
        self.host = None
        self.dnac_version = None
        self.validate_certs = False
        self.use_dnac_mgmt_int = None
        self.toplevel = None
        self.api_record_limit = 500
        
        # global attributes 
        self._site_list = None
        self._inventory = []
        self._host_list = None
        self._dnac_api = None

    def _login(self):
        '''
            :return initialized DNACenterAPI object
        '''

        if not self.validate_certs:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        try:
            self._dnac_api = DNACenterAPI(
                username=self.username, 
                password=self.password, 
                base_url='https://' + self.host, 
                version=self.dnac_version,
                verify=self.validate_certs)
        except ApiError as e:
            print ('failed to login to DNA Center: %s' % e)
            
            return self._dnac_api
    
    def _get_hosts_per_site(self, site_name, family):
        '''
            :return devices associated to a given site
        '''
        # Get the site ID for the given site name
        site_id = self._dnac_api.sites.get_site(name=site_name)
        hosts = self._dnac_api.devices.get_device_list(site_id=site_id,family=family)
        return hosts.response
        
 