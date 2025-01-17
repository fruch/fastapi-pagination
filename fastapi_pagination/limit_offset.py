from __future__ import annotations

from dataclasses import asdict
from typing import Any, Generic, Optional, Sequence, TypeVar

from fastapi import Query
from pydantic import BaseModel
from pydantic.types import conint

from .bases import AbstractParams, BasePage, RawParams

T = TypeVar("T")


class LimitOffsetParams(BaseModel, AbstractParams):
    limit: int = Query(50, ge=1, le=100, description="Page size limit")
    offset: int = Query(0, ge=0, description="Page offset")

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.limit,
            offset=self.offset,
        )


class LimitOffsetPage(BasePage[T], Generic[T]):
    limit: conint(ge=1)  # type: ignore
    offset: conint(ge=0)  # type: ignore

    __params_type__ = LimitOffsetParams

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        params: AbstractParams,
        *,
        total: Optional[int] = None,
        **kwargs: Any,
    ) -> LimitOffsetPage[T]:
        raw_params = params.to_raw_params().as_limit_offset()

        return cls(
            total=total,
            items=items,
            limit=raw_params.limit,
            offset=raw_params.offset,
            **kwargs,
        )


__all__ = [
    "LimitOffsetPage",
    "LimitOffsetParams",
]
