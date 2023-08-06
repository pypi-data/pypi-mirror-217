import logging as logger
import re
import sys

import yaml
from openapi3 import OpenAPI
from openapi3.paths import Operation, Path

logger.basicConfig(level=logger.INFO, format="%(message)s")


class StatusCodesValidator:
    def __init__(self, openapi_path: str, response_codes: list[str]):
        self.response_codes = response_codes
        self.openapi_path = openapi_path
        self.openapi = self._read_openapi()
        self.errors = []

    http_methods = ["get", "post", "put", "delete", "options", "head", "patch", "trace"]

    def _read_openapi(self) -> OpenAPI:
        with open(self.openapi_path) as f:
            spec = yaml.safe_load(f.read())
        openapi = OpenAPI(spec)
        return openapi

    def _get_path_operations(self, path_info: Path) -> list[Operation]:
        operations = [
            getattr(path_info, method)
            for method in self.http_methods
            if isinstance(getattr(path_info, method), Operation)
        ]
        return operations

    def _validate_operations_responses(self, path: str, operations: list[Operation]):
        for operation in operations:
            method = operation.path[-1]
            response_codes = list(operation.responses.keys())
            for required_code in self.response_codes:
                if "X" in required_code:
                    pattern = required_code.replace("X", ".")
                    if not any(re.match(pattern, code) for code in response_codes):
                        self.errors.append(
                            {
                                "path": path,
                                "missing_code": required_code,
                                "method": method,
                            }
                        )
                else:
                    if required_code not in response_codes:
                        self.errors.append(
                            {
                                "path": path,
                                "missing_code": required_code,
                                "method": method,
                            }
                        )

    def validate_codes(self):
        for path, path_info in self.openapi.paths.items():
            operations = self._get_path_operations(path_info)
            self._validate_operations_responses(path, operations)
        for error in self.errors:
            missing_code = error.get("missing_code")
            path = error.get("path")
            method = error.get("method").upper()
            logger.error(
                f"Response with code {missing_code} for '{method}' method is missing in '{path}'"
            )
        if self.errors:
            logger.error("ERROR: OpenAPI file is invalid")
            sys.exit(1)
        logger.info("OpenAPI file is valid")
