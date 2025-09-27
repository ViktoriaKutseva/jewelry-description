from typing import List, Optional
import pandas as pd
import os
from ...models.entities import Material
from ...models.exceptions import InvalidMaterialDataError
from ...business.interfaces import MaterialRepository


class CsvMaterialRepository(MaterialRepository):
    """Implementation of MaterialRepository using CSV files."""

    def load_materials_from_csv(self, csv_path: str = "info.csv") -> List[Material]:
        """Load materials from CSV file."""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"File {csv_path} not found.")

        try:
            df = pd.read_csv(csv_path)
            materials = []
            for _, row in df.iterrows():
                name = str(row.get("Name", "")).strip()

                # Determine price and unit
                if pd.notnull(row.get("1 gram")) and float(row["1 gram"]) > 0:
                    unit_price = float(row["1 gram"])
                    unit = "г"
                elif pd.notnull(row.get("1 piece")) and float(row["1 piece"]) > 0:
                    unit_price = float(row["1 piece"])
                    unit = "шт"
                else:
                    continue  # Skip if no price

                materials.append(
                    Material(name=name, unit_price=unit_price, quantity=0, unit=unit)
                )
            return materials
        except Exception as e:
            raise InvalidMaterialDataError(
                f"Error loading materials from CSV: {e}"
            ) from e

    def find_material_by_name(self, name: str) -> Optional[Material]:
        """Find material by name (case-insensitive partial match)."""
        materials = self.load_materials_from_csv()
        name = name.lower().strip()
        for material in materials:
            if name in material.name.lower():
                return material
        return None

    def get_filtered_materials(self, csv_path: str = "info.csv") -> List[Material]:
        """Return filtered list of materials for common use."""
        try:
            df = pd.read_csv(csv_path)
            result = []

            # Copper (all variants except square)
            copper = df[
                df["Name"].str.lower().str.contains("медь")
                & ~df["Name"].str.lower().str.contains("square")
            ]
            if not copper.empty:
                avg_price = copper["1 gram"].dropna().astype(float).mean()
                if not pd.isna(avg_price):
                    result.append(
                        Material(
                            name="Медь (средняя)",
                            unit_price=round(avg_price, 2),
                            quantity=0,
                            unit="г",
                        )
                    )

            # Square copper
            sq_copper = df[
                df["Name"].str.lower().str.contains("square")
                & df["Name"].str.lower().str.contains("copper")
            ]
            if not sq_copper.empty:
                avg_price = sq_copper["1 gram"].dropna().astype(float).mean()
                if not pd.isna(avg_price):
                    result.append(
                        Material(
                            name="Квадратная медь (средняя)",
                            unit_price=round(avg_price, 2),
                            quantity=0,
                            unit="г",
                        )
                    )

            # Brass
            brass = df[df["Name"].str.lower().str.contains("латун")]
            if not brass.empty:
                avg_price = brass["1 gram"].dropna().astype(float).mean()
                if not pd.isna(avg_price):
                    result.append(
                        Material(
                            name="Латунь (средняя)",
                            unit_price=round(avg_price, 2),
                            quantity=0,
                            unit="г",
                        )
                    )

            # Nickel silver
            neiz = df[df["Name"].str.lower().str.contains("нейз")]
            if not neiz.empty:
                avg_price = neiz["1 gram"].dropna().astype(float).mean()
                if not pd.isna(avg_price):
                    result.append(
                        Material(
                            name="Нейзильбер (средняя)",
                            unit_price=round(avg_price, 2),
                            quantity=0,
                            unit="г",
                        )
                    )

            # All stones in Russian
            stones = df[
                (df["tags "] == "stone")
                & df["Name"].str.contains(r"[А-Яа-яЁё]", na=False)
            ]
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
                    result.append(
                        Material(
                            name=name, unit_price=round(price, 2), quantity=0, unit=unit
                        )
                    )

            return result
        except Exception as e:
            raise InvalidMaterialDataError(f"Error filtering materials: {e}") from e
