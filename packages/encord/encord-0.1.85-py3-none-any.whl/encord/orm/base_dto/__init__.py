from encord.orm.base_dto.base_dto_interface import BaseDTOInterface

try:
    # For Python 3.8 and later
    import importlib.metadata as importlib_metadata
except ImportError:
    # For everyone else
    import importlib_metadata  # type: ignore[no-redef]

pydantic_version_str = importlib_metadata.version("pydantic")

pydantic_version = int(pydantic_version_str.split(".")[0])
if pydantic_version < 2:
    from encord.orm.base_dto.base_dto_pydantic_v1 import BaseDTO, GenericBaseDTO
else:
    from encord.orm.base_dto.base_dto_pydantic_v2 import (  # type: ignore[assignment]
        BaseDTO,
        GenericBaseDTO,
    )
