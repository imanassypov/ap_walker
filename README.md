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

```bash
python ap_walker.py
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact Igor Manassypov, [imanassy@cisco.com].
