from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional
  

class TradeDirection(Enum):
  IMPORT = "import"
  EXPORT = "export"


class ProductCategory(Enum):
  ANIMALS = "Live Animals & Animal Products"
  ART = "Art & Antiques"
  CHEMICALS = "Chemicals"
  ELECTRONICS = "Electronics"
  ENERGY = "Energy & Petroleum"
  HEALTH = "Health & Pharmaceuticals"
  INSTRUMENTS = "Instruments (Measuring, Musical, etc.)"
  MACHINERY = "Machinery & Equipment"
  MANUFACTURED = "Manufactured Articles"
  METALS = "Metals & Minerals"
  MINERALS = "Mineral Products"
  OTHER = "Other"
  PLANTS = "Plants & Agriculture"
  PLASTICS_RUBBER = "Plastics & Rubber"
  SPECIAL = "Special Classifications"
  STONE_CERAMIC_GLASS = "Stone, Ceramic, Glass, etc."
  TEXTILES = "Textiles & Apparel"
  VEHICLES = "Vehicles & Transport"
  WEAPONS = "Weapons & Defense"
  WOOD_PAPER = "Wood & Paper"


class ProductType:
  """A collection of different categorization methods for an import or export shimpent."""
  category: ProductCategory
  potential_to_weaponize: bool

  def __init__(self, category, potential_to_weaponize):
    self.category = category
    self.potential_to_weaponize = potential_to_weaponize


@dataclass
class TradeRecord:
  """A single trade record representing an import or export shipment."""
  direction: TradeDirection
  country_code: str
  country_name: str
  hs_code: str
  commodity_description: str
  type: ProductType
  value_usd: float
  weight_kg: Optional[float] = None
  quantity: Optional[float] = None
  qunatity_unit: Optional[str] = None
  year: int = 0
  month: int = 0
  port_code: str = "2101"
  port_name: str = "New Orleans, LA"
  source: str = ""

  @property
  def period(self) -> str:
    return f"{self.year}-{self.month:02d}"
  
  @property
  def date_approx(self) -> date:
    return date(self.year, self.month, 1)


@dataclass
class TradeQuery:
  """Parameters for filtering trade data."""
  direction: Optional[TradeDirection] = None
  country_code: Optional[str] = None
  country_name: Optional[str] = None
  categories: list[ProductCategory] = field(default_factory=list)
  weaponizable: Optional[bool] = None
  hs_code_prefix: Optional[str] = None
  year_start: Optional[int] = None
  year_end: Optional[int] = None
  month: Optional[int] = None
  min_value_usd: Optional[float] = None


@dataclass
class TradeSummary:
  """Aggregated trade statistics."""
  total_value_usd: float
  record_count: int
  by_category: dict[str, float] = field(default_factory=dict)
  by_weaponizable: dict[str, float] = field(default_factory=dict)
  by_country: dict[str, float] = field(default_factory=dict)
  by_period: dict[str, float] = field(default_factory=dict)
  by_direction: dict[str, float] = field(default_factory=dict)
