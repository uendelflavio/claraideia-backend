from typing import Optional

from pydantic import AnyUrl

from ..models.rwmodel import RWModel


class Station(RWModel):
    description: str
    data_leitura: Optional[str] = ""
    leitura: Optional[AnyUrl] = None


class StationInDB(RWModel):
    pass


class StationInResponse(RWModel):
    station: Station


class StationInCreate(RWModel):
    pass


class StationInUpdate(RWModel):
    pass