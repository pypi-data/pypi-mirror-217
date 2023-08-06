import click

from oa3_responses_validator.validator import StatusCodesValidator


@click.command()
@click.option(
    "-i",
    "--input-file",
    required=True,
    type=click.Path(exists=True),
    help="OpenAPI file path",
)
@click.option(
    "-c", "--codes", multiple=True, default=["2XX", "400", "500"], type=click.STRING
)
def main(input_file: str, codes: list[str]):
    validator = StatusCodesValidator(input_file, codes)
    validator.validate_codes()


if __name__ == "__main__":
    main()
