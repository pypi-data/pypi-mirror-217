"""Data pipeline configuration.

Metadata configuration for running a data pipeline using Pushcart. Is instantiated
off of a Python dictionary, or a JSON, TOML or YAML file, optionally in conjuction
with a CSV file for transformation definitions.

Example:
-------
    config_dict = json.load(file)
    pipeline_config = Configuration.parse_obj(config_dict)

Notes:
-----
Configuration must have at least one stage (Source, Transformation, Destination) of the
data pipeline defined.

"""

import json
import logging
import os
from collections import defaultdict
from collections.abc import AsyncIterator
from io import StringIO
from itertools import groupby
from pathlib import Path

import aiofiles
import pandas as pd
import tomli
import yaml
from pydantic import (
    Field,
    conint,
    constr,
    dataclasses,
    field_validator,
    model_validator,
    validate_call,
)
from pydantic_core._pydantic_core import ArgsKwargs


async def get_transformations_from_csv(csv_path: Path | str) -> AsyncIterator[dict]:
    """Return transformations from the metadata .csv line-by-line.

    Parameters
    ----------
    csv_path : Path | str
        Path to an existing .csv file

    Returns
    -------
    AsyncIterator[dict]
        Iterates over transformation specifications in the input file

    Yields
    ------
    Iterator[AsyncIterator[dict]]
        One row containing details for one transformation step
    """
    if isinstance(csv_path, str):
        csv_path = Path(csv_path)

    types_dict = {
        "column_order": int,
        "source_column_name": str,
        "source_column_type": str,
        "dest_column_name": str,
        "dest_column_type": str,
        "transform_function": str,
        "default_value": str,
        "validation_rule": str,
        "validation_action": str,
    }

    async with aiofiles.open(csv_path, "r") as aio_file:
        contents = await aio_file.read()
        csv_file = StringIO(contents)

        csv_df = pd.read_csv(csv_file, dtype=types_dict).fillna("")
        csv_dict = csv_df.to_dict(orient="records")

        for row in csv_dict:
            yield row


async def get_transformations_from_sql(sql_path: Path | str) -> str:
    """Return transformations from SQL file.

    Parameters
    ----------
    sql_path : Path | str
        Path to an existing .sql file

    Returns
    -------
    str
        SQL string from input file
    """
    async with aiofiles.open(sql_path, "r") as sql_file:
        return await sql_file.read()


def expect_at_most_one_file(settings_path: Path | str) -> Path | None:
    """Check whether there is at most one configuration file for the given path.

    Parameters
    ----------
    settings_path : Path | str
        Path to a configuration file, may omit extension

    Returns
    -------
    Path | None
        Path containing the absolute path to the existing file

    Raises
    ------
    FileExistsError
        Can only have at most one configuration file for the given name. Extension
        can be any one of .json, .toml, .yml or .yaml
    """
    if isinstance(settings_path, str):
        settings_path = Path(settings_path)

    existing_paths = []

    for ext in [".json", ".toml", ".yml", ".yaml"]:
        file_path = settings_path.with_suffix(ext).resolve()

        if file_path.is_file():
            existing_paths.append(file_path)

    if not existing_paths:
        return None

    if len(existing_paths) > 1:
        msg = f"Expecting only one {settings_path}.[json|toml|yml|yaml] file. Found:\n{os.linesep.join(existing_paths)}"
        raise FileExistsError(msg)

    return existing_paths[0]


@validate_call
async def get_config_from_file(settings_path: Path | str) -> dict | None:
    """Load a configuration file into a dictionary. Supported formats are JSON, YAML, and TOML.

    Parameters
    ----------
    settings_path : Path | str
        Path to the configuration file.

    Returns
    -------
    dict | None
        The configuration data as a dictionary, or None if an error occurred.
    """
    loaders = defaultdict(
        lambda: None,
        {
            ".json": json.loads,
            ".toml": tomli.loads,
            ".yaml": yaml.safe_load,
            ".yml": yaml.safe_load,
        },
    )

    log = logging.getLogger(__name__)

    try:
        if isinstance(settings_path, str):
            settings_path = Path(settings_path)

        if settings_path.exists():
            ext = settings_path.suffix
            async with aiofiles.open(settings_path, "r") as settings_file:
                contents = await settings_file.read()

                return loaders[ext](contents)
    except FileNotFoundError:
        log.warning(f"File not found: {settings_path.as_posix()}")
    except OSError:
        log.warning(f"Could not open file: {settings_path.as_posix()}")
    except (json.JSONDecodeError, yaml.error.YAMLError, tomli.TOMLDecodeError):
        log.warning(f"File is not valid: {settings_path.as_posix()}")
    except TypeError:
        log.warning(f"Unsupported file type: {settings_path.as_posix()}")
    except RuntimeError as e:
        log.warning(f"Skipping: {settings_path.as_posix()} Encountered: {e}")


def _get_multiple_validations_with_same_rule(validations: dict) -> dict:
    """Group a list of validations by their rule and return only the groups that have more than one validation with the same rule."""
    validation_groups = {
        k: [v["validation_action"] for v in v]
        for k, v in groupby(
            sorted(validations, key=lambda v: str(v["validation_rule"]).strip()),
            lambda r: str(r["validation_rule"]).strip(),
        )
    }

    return {k: v for k, v in validation_groups.items() if len(v) > 1}


@dataclasses.dataclass
class Validation:
    """Provides a way to define validation rules and actions for data.

    Has two main fields: validation_rule and validation_action. The validation_rule
    field is a Spark SQL string that defines the rule that the input data must follow,
    while the validation_action field is a string that defines the action to take if
    the input data fails to meet the validation rule.
    """

    validation_rule: constr(min_length=1, strict=True)
    validation_action: constr(
        to_upper=True,
        strict=True,
        pattern=r"^(LOG|DROP|FAIL)$",
    )

    def __getitem__(self, item: str) -> any:
        """Avoid Pydantic throwing ValidationError: object not subscriptable.

        Parameters
        ----------
        item : str
            Name of parent object attribute

        Returns
        -------
        any
            Type of returned object
        """
        return self.__getattribute__(item)


@dataclasses.dataclass
class Source:
    """Represents a data source and its associated metadata.

    Handles different types of data sources, including local files, remote URLs, and
    non-empty strings. The class also allows for optional parameters and validations
    to be associated with the data source.

    Returns
    -------
    Source
        Object defining a Pipeline data source.

    Raises
    ------
    ValueError
        Only one action (WARN | DROP | FAIL) can be defined as consequence to a data
        validation rule
    """

    target_catalog_name: constr(strip_whitespace=True, min_length=1, strict=True)
    target_schema_name: constr(strip_whitespace=True, min_length=1, strict=True)
    pipeline_name: constr(strip_whitespace=True, min_length=1, strict=True)

    origin: constr(min_length=1, strict=True)
    datatype: constr(min_length=1, strict=True)
    target: constr(min_length=1, strict=True)
    params: str | None = None
    validations: list[Validation] | None = Field(default_factory=list)

    @field_validator("validations")
    @classmethod
    def check_multiple_validations_with_same_rule(cls, value: dict) -> dict:
        """Check that there are no multiple validation actions for the same rule."""
        if value and (fails := _get_multiple_validations_with_same_rule(value)):
            msg = f"Different actions for the same validation:\n{fails}"
            raise ValueError(msg)
        return value


@dataclasses.dataclass
class Transformation:
    """Represents a data transformation with optional validation rules.

    It ensures that only one of the config or sql_query fields is defined and that at
    least one of them is defined. It also allows for a list of Validation objects to
    be included to ensure that the transformed data meets desired criteria.

    Returns
    -------
    Transformation
        Object defining a transformation step within a data Pipeline.

    Raises
    ------
    ValueError
        Transformation needs to be based on a SQL query or a metadata .csv file
    ValueError
        Transformation must only have one of either a SQL query or a metadata .csv file
    ValueError
        Only one action (WARN | DROP | FAIL) can be defined as consequence to a data
        validation rule
    """

    target_catalog_name: constr(strip_whitespace=True, min_length=1, strict=True)
    target_schema_name: constr(strip_whitespace=True, min_length=1, strict=True)
    pipeline_name: constr(strip_whitespace=True, min_length=1, strict=True)

    origin: constr(min_length=1, strict=True)
    target: constr(min_length=1, strict=True)
    column_order: conint(ge=1) | None = 1
    source_column_name: constr(strict=True) | None = None
    source_column_type: constr(
        strict=True,
        pattern="^(string|int|double|date|timestamp|boolean|struct|array|map)$",
    ) | None = None
    dest_column_name: constr(strict=True) | None = None
    dest_column_type: constr(
        strict=True,
        pattern="^(string|int|double|date|timestamp|boolean|struct|array|map)$",
    ) | None = None
    transform_function: constr(strict=True) | None = None
    sql_query: constr(min_length=1, strict=True) | None = None
    default_value: constr(strict=True) | None = None
    validations: list[Validation] | None = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def check_only_one_of_config_or_sql_query_defined(cls, values: dict) -> dict:
        """Check that one and only one of the config or sql_query fields is defined."""
        data = values.kwargs if isinstance(values, ArgsKwargs) else values
        if not any(
            data.get(v) is not None
            for v in ["source_column_name", "dest_column_name", "sql_query"]
        ):
            msg = f"No transformation defined. Please provide either a config or a sql_query.\nGot: {data}"
            raise ValueError(msg)
        if all(
            data.get(t) for t in ["source_column_name", "dest_column_name", "sql_query"]
        ):
            msg = f"Only one of config or sql_query allowed.\nGot: {data}"
            raise ValueError(msg)
        return values

    @field_validator("validations")
    @classmethod
    def check_multiple_validations_with_same_rule(cls, value: dict) -> dict:
        """Validate that there are no multiple validations with the same rule."""
        if value and (fails := _get_multiple_validations_with_same_rule(value)):
            msg = f"Different actions for the same validation:\n{fails}"
            raise ValueError(msg)
        return value


@dataclasses.dataclass
class Destination:
    """Represents a Delta table destination for a batch of data.

    Defines fields for the source data view, the destination table, the path to the
    destination, the mode of writing (append or upsert), keys and sequence_by for
    upsert mode, and optional validations. Provides validation for the fields and
    checks that the keys and sequence_by fields are defined for upsert mode. Checks
    that there are no multiple validations with the same rule.

    Returns
    -------
    Destination
        Object defining a destination for the data Pipeline to write to.

    Raises
    ------
    ValueError
        When upserting to a destination, the primary key and sequence columns must be
        defined.
    ValueError
        Only one action (WARN | DROP | FAIL) can be defined as consequence to a data
        validation rule
    """

    target_catalog_name: constr(strip_whitespace=True, min_length=1, strict=True)
    target_schema_name: constr(strip_whitespace=True, min_length=1, strict=True)
    pipeline_name: constr(strip_whitespace=True, min_length=1, strict=True)

    origin: constr(min_length=1, strict=True)
    target: constr(min_length=1, strict=True)
    mode: constr(min_length=1, strict=True, pattern=r"^(append|upsert)$")
    path: Path | None = None
    keys: list[constr(min_length=1, strict=True)] | None = Field(
        default_factory=list,
    )
    sequence_by: constr(min_length=1, strict=True) | None = None
    validations: list[Validation] | None = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def check_keys_and_sequence_for_upsert(cls, values: dict) -> dict:
        """Check that the keys and sequence_by fields are defined for upsert mode."""
        data = values.kwargs if isinstance(values, ArgsKwargs) else values

        if data.get("mode") == "upsert" and not all(
            data[v] for v in ["keys", "sequence_by"]
        ):
            msg = "Mode upsert requires that keys and sequence_by are defined"
            raise ValueError(
                msg,
            )
        return values

    @field_validator("validations")
    @classmethod
    def check_multiple_validations_with_same_rule(cls, value: dict) -> dict:
        """Check that there are no multiple validations with the same rule."""
        if value and (fails := _get_multiple_validations_with_same_rule(value)):
            msg = f"Different actions for the same validation:\n{fails}"
            raise ValueError(msg)
        return value

    @field_validator("path", mode="after")
    @classmethod
    def convert_to_absolute_string(cls, value: Path | None) -> str | None:
        """Convert the Path object to its absolute POSIX representation."""
        if value:
            return value.absolute().as_posix()

        return None


@dataclasses.dataclass
class Configuration:
    """Represents a configuration file for a data pipeline.

    Returns
    -------
    Configuration
        Contains optional lists of Source, Transformation, and Destination objects,
        which define the stages of the pipeline. Provides validation to ensure that
        at least one stage is defined in the configuration file.

    Raises
    ------
    ValueError
        At least one stage definition (Source, Transformation, Destination) must exist.
    ValueError
        All values in the "target" fields of all pipeline stages taken together must be
        unique.
    """

    sources: list[Source] | None = Field(default_factory=list)
    transformations: list[Transformation] | None = Field(default_factory=list)
    destinations: list[Destination] | None = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def check_at_least_one_stage_defined(cls, values: dict[str, list[any]]) -> dict:
        """Check that at least one of the sources, transformations, or destinations fields is defined in the configuration file."""
        msg = "No stage definition found. Please define at least one of: sources, transformations, destinations"

        data = values.kwargs if isinstance(values, ArgsKwargs) else values

        if not data:
            raise ValueError(msg)

        if not any(v in ["sources", "transformations", "destinations"] for v in data):
            raise ValueError(msg)

        return values

    @model_validator(mode="before")
    @classmethod
    def check_all_dlt_target_objects_are_unique(
        cls,
        values: dict[str, list[any]],
    ) -> dict:
        """Check that no values of the "target" fields of "sources", "transformations" and "destinations", taken together, overlap."""
        data = values.kwargs if isinstance(values, ArgsKwargs) else values

        sources = (data or {}).get("sources", [])
        transformations = (data or {}).get("transformations", [])
        destinations = (data or {}).get("destinations", [])

        target_values = (
            [source.get("target") for source in sources if source]
            + [
                transformation.get("target")
                for transformation in transformations
                if transformation and transformation.get("sql_query")
            ]
            + [destination.get("target") for destination in destinations if destination]
        )

        duplicates = [
            value for value in set(target_values) if target_values.count(value) > 1
        ]

        if duplicates:
            msg = f"Duplicate 'target' values found: {', '.join(duplicates)}"
            raise ValueError(msg)

        return values
