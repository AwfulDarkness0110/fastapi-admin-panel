import inspect
from typing import Mapping, Optional, Union, no_type_check

from sqlalchemy import util
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

from db.model import Model


@no_type_check
async def async_call(
    self,
    session: AsyncSession,
    method_name: str = "",
    parameters: Optional[Mapping] = None,
    execution_options: Mapping = util.EMPTY_DICT,
) -> Union[Model, Row, list[Row]]:
    result = await session.execute(self, parameters, execution_options)
    result = result.unique()

    method_name = method_name if method_name else inspect.stack()[1][3]
    if row_method := getattr(result, method_name, None):
        return row_method()

    raise Exception("Invalid method name.")