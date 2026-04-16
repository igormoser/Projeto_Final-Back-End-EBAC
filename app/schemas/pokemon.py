from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


VALID_TYPES = {
    "Bug", "Dark", "Dragon", "Electric", "Fairy", "Fighting", "Fire", "Flying",
    "Ghost", "Grass", "Ground", "Ice", "Normal", "Poison", "Psychic", "Rock",
    "Steel", "Water",
}


class PokemonBase(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    numero_pokedex: int = Field(ge=1)
    tipo_primario: str = Field(min_length=1, max_length=50)
    tipo_secundario: str | None = Field(default=None, min_length=1, max_length=50)
    altura: float = Field(gt=0)
    peso: float = Field(gt=0)
    descricao: str | None = Field(default=None, max_length=500)

    @field_validator("nome")
    @classmethod
    def normalize_nome(cls, value: str) -> str:
        return value.strip().title()

    @field_validator("tipo_primario", "tipo_secundario")
    @classmethod
    def normalize_tipo(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().title()
        if normalized not in VALID_TYPES:
            raise ValueError("Tipo de Pokémon inválido.")
        return normalized

    @field_validator("descricao")
    @classmethod
    def normalize_descricao(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    @model_validator(mode="after")
    def validate_secondary_type(self) -> "PokemonBase":
        if self.tipo_secundario and self.tipo_secundario == self.tipo_primario:
            raise ValueError("O tipo secundário deve ser diferente do tipo primário.")
        return self


class PokemonCreate(PokemonBase):
    pass


class PokemonUpdate(PokemonBase):
    pass


class PokemonResponse(PokemonBase):
    id: int
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)


class PokemonListResponse(BaseModel):
    items: list[PokemonResponse]
    total: int
    skip: int
    limit: int


class PokemonDeleteResponse(BaseModel):
    mensagem: str
    pokemon: PokemonResponse
