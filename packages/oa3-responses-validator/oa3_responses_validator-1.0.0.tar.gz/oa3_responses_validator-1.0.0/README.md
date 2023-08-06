## OpenAPI3 Responses Validator


### Checking if certain HTTP codes are specified in each of the responses for each route

## Installation

```bash
pip install oa3-responses-validator
```

Usage:

```bash
oa3-responses-validator -i /path/to/openapi.yaml -c 400 -c 500 -c 2XX
```

You can use the 2XX code pattern to indicate that any 2XX code should be among the response codes