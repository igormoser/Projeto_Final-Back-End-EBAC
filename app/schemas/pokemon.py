from pydantic import BaseModel, ConfigDict, Field


class PokemonSprites(BaseModel):
    front_default: str | None = None
    back_default: str | None = None


class PokemonResponse(BaseModel):
    name: str = Field(min_length=1)
    id: int = Field(ge=1)
    height: int = Field(ge=0)
    weight: int = Field(ge=0)
    types: list[str]
    sprites: PokemonSprites

    model_config = ConfigDict(extra="ignore")


class PaginationResponse(BaseModel):
    total: int = Field(ge=0)
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)
    next: str | None = None
    previous: str | None = None


class PokemonListResponse(BaseModel):
    data: list[PokemonResponse]
    pagination: PaginationResponse
