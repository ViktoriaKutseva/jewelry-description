from dataclasses import dataclass, field
from typing import List, Dict, Optional
import pandas as pd
import os

@dataclass
class Material:
    name: str
    unit_price: float  # цена за единицу (грамм, штуку и т.д.)
    quantity: float    # количество (граммы, штуки и т.д.)
    unit: str = "г"    # единица измерения

    def cost(self) -> float:
        return self.unit_price * self.quantity

@dataclass
class Consumable:
    name: str
    approx_cost: float

@dataclass
class WorkTime:
    hours: float
    hourly_rate: float

    def cost(self) -> float:
        return self.hours * self.hourly_rate

@dataclass
class JewelryCostInput:
    materials: List[Material]
    consumables: List[Consumable]
    work_time: WorkTime
    electricity_cost: float = 0.0
    tool_depreciation: float = 0.0
    packaging_cost: float = 0.0
    extra_costs: List[Consumable] = field(default_factory=list)
    defect_percent: float = 0.0  # процент на брак (например, 5)

@dataclass
class JewelryCostResult:
    cost_breakdown: Dict[str, float]
    total_cost: float
    recommended_prices: Dict[str, float]
    price_comment: str

def calculate_jewelry_cost(data: JewelryCostInput) -> JewelryCostResult:
    breakdown = {}
    total = 0.0
    # Материалы
    for m in data.materials:
        c = m.cost()
        breakdown[f"{m.name} ({m.quantity} {m.unit})"] = c
        total += c
    # Время
    work_c = data.work_time.cost()
    breakdown[f"Время ({data.work_time.hours} ч)"] = work_c
    total += work_c
    # Расходники
    for c in data.consumables:
        breakdown[c.name] = c.approx_cost
        total += c.approx_cost
    # Электричество
    if data.electricity_cost:
        breakdown["Электричество"] = data.electricity_cost
        total += data.electricity_cost
    # Амортизация инструмента
    if data.tool_depreciation:
        breakdown["Амортизация инструмента"] = data.tool_depreciation
        total += data.tool_depreciation
    # Упаковка
    if data.packaging_cost:
        breakdown["Упаковка"] = data.packaging_cost
        total += data.packaging_cost
    # Прочие
    for c in data.extra_costs:
        breakdown[c.name] = c.approx_cost
        total += c.approx_cost
    # Брак
    if data.defect_percent:
        defect_cost = total * data.defect_percent / 100
        breakdown[f"Брак ({data.defect_percent}%)"] = defect_cost
        total += defect_cost
    # Рекомендации по цене
    min_price = total * 2
    comfort_price = total * 2.5
    premium_price = total * 3
    recommended = {
        "Минимальная (×2)": min_price,
        "Комфортная (×2.5)": comfort_price,
        "Премиум (×3)": premium_price
    }
    comment = f"👉 Отличная розничная цена: от {int(min_price*1.1)} до {int(comfort_price*1.1)} тг, в зависимости от упаковки и позиционирования."
    return JewelryCostResult(
        cost_breakdown=breakdown,
        total_cost=total,
        recommended_prices=recommended,
        price_comment=comment
    )

def load_materials_from_csv(csv_path: str = "info.csv") -> List[Material]:
    """
    Загружает материалы из CSV-файла и возвращает список объектов Material.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Файл {csv_path} не найден.")
    df = pd.read_csv(csv_path)
    materials = []
    for _, row in df.iterrows():
        name = str(row.get("Name", "")).strip()
        tag = str(row.get("tags ", "")).strip().lower()
        # Определяем цену и единицу измерения
        if pd.notnull(row.get("1 gram")) and float(row["1 gram"]) > 0:
            unit_price = float(row["1 gram"])
            unit = "г"
        elif pd.notnull(row.get("1 piece")) and float(row["1 piece"]) > 0:
            unit_price = float(row["1 piece"])
            unit = "шт"
        else:
            continue  # Пропускаем, если нет цены
        # По умолчанию количество = 0, пользователь укажет при расчёте
        materials.append(Material(name=name, unit_price=unit_price, quantity=0, unit=unit))
    return materials

def find_material_price(materials: List[Material], name: str) -> Optional[Material]:
    """
    Находит материал по имени (без учёта регистра, частичное совпадение).
    Возвращает объект Material с ценой и единицей измерения.
    """
    name = name.lower().strip()
    for m in materials:
        if name in m.name.lower():
            return m
    return None

def get_filtered_materials(csv_path: str = "info.csv") -> list:
    """
    Возвращает сокращённый список материалов:
    - Медь (средняя цена за грамм)
    - Квадратная медь (средняя цена за грамм)
    - Латунь (средняя цена за грамм)
    - Нейзильбер (средняя цена за грамм)
    - Все камни на русском (имя и цена за штуку/грамм)
    Инструменты исключаются.
    """
    import pandas as pd
    df = pd.read_csv(csv_path)
    result = []
    # Медь (все варианты, кроме квадратной)
    copper = df[df["Name"].str.lower().str.contains("медь") & ~df["Name"].str.lower().str.contains("square")]
    if not copper.empty:
        avg_price = copper["1 gram"].dropna().astype(float).mean()
        if not pd.isna(avg_price):
            result.append(Material(name="Медь (средняя)", unit_price=round(avg_price,2), quantity=0, unit="г"))
    # Квадратная медь
    sq_copper = df[df["Name"].str.lower().str.contains("square") & df["Name"].str.lower().str.contains("copper")]
    if not sq_copper.empty:
        avg_price = sq_copper["1 gram"].dropna().astype(float).mean()
        if not pd.isna(avg_price):
            result.append(Material(name="Квадратная медь (средняя)", unit_price=round(avg_price,2), quantity=0, unit="г"))
    # Латунь
    brass = df[df["Name"].str.lower().str.contains("латун")]
    if not brass.empty:
        avg_price = brass["1 gram"].dropna().astype(float).mean()
        if not pd.isna(avg_price):
            result.append(Material(name="Латунь (средняя)", unit_price=round(avg_price,2), quantity=0, unit="г"))
    # Нейзильбер
    neiz = df[df["Name"].str.lower().str.contains("нейз")]
    if not neiz.empty:
        avg_price = neiz["1 gram"].dropna().astype(float).mean()
        if not pd.isna(avg_price):
            result.append(Material(name="Нейзильбер (средняя)", unit_price=round(avg_price,2), quantity=0, unit="г"))
    # Все камни на русском (stone, но имя на кириллице)
    stones = df[(df["tags "]=="stone") & df["Name"].str.contains(r'[А-Яа-яЁё]', na=False)]
    for _, row in stones.iterrows():
        name = str(row["Name"]).strip()
        price = None
        unit = "шт"
        if pd.notnull(row.get("1 piece")) and float(row["1 piece"]) > 0:
            price = float(row["1 piece"])
            unit = "шт"
        elif pd.notnull(row.get("1 gram")) and float(row["1 gram"]) > 0:
            price = float(row["1 gram"])
            unit = "г"
        if price:
            result.append(Material(name=name, unit_price=round(price,2), quantity=0, unit=unit))
    return result 