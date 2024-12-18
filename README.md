# AP Walker

AP Walker is a Python project designed to execute arbitrary set of CLI against Cisco Access Points registered to and managed by Cisco Catalyst Center.

## Features

- Runs arbitrary CLI command against Cisco Unified AP (ClickOS)
- Supports concurrent execution
- Logs CLI output to per-management-ip of each AP

## Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

To use AP Walker, ensure you have necessary environment variables (refer to sample .env file) defining your Catalyst Center credentials, etc.
The script will read the list of Sites where the target Access Points are associated to, and execute the CLI against each of the AP's per site. 
The list of Catalyst Center Sites where the target AP's are associated to is defined in dnac_site_list.json

Prepare a tftp server, and place the required AP image into tftpboot folder.
To figure out the version of AP sofware image matching to the target Wireless Lan Controller image, use the following reference:
https://www.cisco.com/c/en/us/td/docs/wireless/compatibility/matrix/compatibility-matrix.html

```bash
python ap_walker.py
```

## Test results
After the execution of the script the following is the snippet of show version from one of the APs
```bash
AP Running Image     : 17.6.4.56
Primary Boot Image   : 17.6.4.56
Backup Boot Image    : 17.9.4.27
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact Igor Manassypov, [imanassy@cisco.com].
