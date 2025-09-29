from typing import List, Optional
import pandas as pd
import os
from loguru import logger
from ...models.entities import Material
from ...models.exceptions import InvalidMaterialDataError
from ...business.interfaces import IMaterialRepository


class CsvMaterialRepository(IMaterialRepository):
    """Implementation of MaterialRepository using CSV files."""

    def load_materials_from_csv(self, csv_path: str = "old_data/info.csv") -> List[Material]:
        """Load materials from CSV file."""
        logger.debug("Loading materials from CSV", csv_path=csv_path)

        if not os.path.exists(csv_path):
            logger.error("CSV file not found", csv_path=csv_path)
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

            logger.info("Successfully loaded materials from CSV", count=len(materials), csv_path=csv_path)
            return materials
        except Exception as e:
            logger.error("Failed to load materials from CSV", error=str(e), csv_path=csv_path)
            raise InvalidMaterialDataError(
                f"Error loading materials from CSV: {e}"
            ) from e

    def find_material_by_name(self, name: str) -> Optional[Material]:
        """Find material by name (case-insensitive partial match)."""
        logger.debug("Searching for material by name", search_name=name)

        materials = self.load_materials_from_csv()
        name = name.lower().strip()
        for material in materials:
            if name in material.name.lower():
                logger.debug("Material found", material_name=material.name, search_name=name)
                return material

        logger.debug("Material not found", search_name=name)
        return None

    def get_filtered_materials(self, csv_path: str = "old_data/info.csv") -> List[Material]:
        """Return filtered list of materials for common use."""
        logger.debug("Filtering materials for common use", csv_path=csv_path)

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

            logger.info("Successfully filtered materials", count=len(result), csv_path=csv_path)
            return result
        except Exception as e:
            logger.error("Failed to filter materials", error=str(e), csv_path=csv_path)
            raise InvalidMaterialDataError(f"Error filtering materials: {e}") from e
