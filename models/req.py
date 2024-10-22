from typing import List, Optional, Union

from pydantic import BaseModel


class Status(BaseModel):
    id: int
    description: str


class Output(BaseModel):
    stdout: Optional[str] = None
    time: Optional[str] = None
    memory: Optional[int] = None
    stderr: Optional[str] = None
    token: Optional[str] = None
    compile_output: Optional[str] = None
    message: Optional[str] = None
    status: Optional[Status] = None


class Resource(BaseModel):
    path: str
    filename: str


class Test(BaseModel):
    id: int
    input: Optional[Union[str, Resource]] = None
    expected: Optional[Union[str, Resource]] = None
    visibility: str
    actual: Optional[Union[str, Resource]] = None
    output: Optional[Union[str, Output]] = None
    success: Optional[bool] = None
    points: Optional[int] = None


class File(BaseModel):
    filename: str
    type: str
    size: int
    languageId: int
    content: str
    tests: List[Test]

class EventData(BaseModel):
    event: str
    title: str
    difficulty: str 
    points: int
    validator: Optional[str] = None
    runner: Optional[str] = None
    maxFiles: Optional[int] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    files: List[File]
