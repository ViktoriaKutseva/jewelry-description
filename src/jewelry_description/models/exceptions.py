class JewelryDomainError(Exception):
    """Base exception for jewelry domain errors."""

    pass


class MaterialNotFoundError(JewelryDomainError):
    """Raised when a material cannot be found."""

    pass


class InvalidMaterialDataError(JewelryDomainError):
    """Raised when material data is invalid."""

    pass


class CalculationError(JewelryDomainError):
    """Raised when cost calculation fails."""

    pass
