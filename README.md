# AWS EC2 On-demand & Spot Pricing

AWS EC2 On-demand & Spot Pricing is a Python script for preparing a comparative csv with basic details of EC2 instances
such as instance family, vCPU, memory, storage and price both on-demand as well as spot pricing, for easily identify the
 pricing difference and get help to calculate revenue.

## Installation

To execute the script you must have the following packages, such as requests, time, json, csv, sys, operator and itertools.
Use pip to install the following packages, see example

```bash
pip install requests
```

## Usage

To execute the script you must pass two parameters, such as region and environment respectively and the must be a valid AWS
EC2 region and environment parameter.

```python
python3 aws-on-demand-pricing.py us-east-1 linux
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)