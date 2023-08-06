from typing import List, Optional

from pydantic import validator
from tortoise.contrib.pydantic import pydantic_model_creator

from fastgenerateapi.pydantic_utils.base_model import BaseModel
from fastgenerateapi.schemas_factory import get_all_schema_factory
from fastgenerateapi.schemas_factory.common_schema_factory import common_schema_factory
from modules.example.models import CompanyInfo, StaffInfo


class CompanyInfoRead(BaseModel, pydantic_model_creator(
    CompanyInfo,
    name='CompanyInfoRead',
)):
    ...


class CompanyInfoCreate(BaseModel, pydantic_model_creator(
    CompanyInfo,
    name='CompanyInfoCreate',
    exclude_readonly=True,
)):
    ...


class TestSchema(BaseModel):
    name: str


class ListTestSchema(BaseModel):
    data_list: List[TestSchema]


class StaffReadSchema(common_schema_factory(
    StaffInfo,
    name="StaffReadSchema",
    extra_include=["test"],
)):
    test_name: Optional[str]

    @validator("test")
    def check_test(cls, value):
        if value == "test":
            return "test11"
        return value



