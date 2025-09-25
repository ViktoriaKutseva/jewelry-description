"""
SQLite repository implementation for materials.
"""
import sqlite3
from typing import List, Dict, Optional, Any
from loguru import logger

from jewelry_description.config.settings import settings


class MaterialSQLiteRepository:
    """SQLite implementation of MaterialRepository."""
    
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or settings.database.path
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    async def get_all(self) -> List[Dict[str, Any]]:
        """Get all materials from the database."""
        logger.info("Fetching all materials from database", db_path=self.db_path)
        
        try:
            conn = self._get_connection()
            cursor = conn.execute("SELECT name, price, unit, category FROM materials ORDER BY name")
            materials = []
            for row in cursor:
                materials.append({
                    "name": row[0],
                    "price": row[1],
                    "unit": row[2],
                    "category": row[3]
                })
            conn.close()
            
            logger.info("Successfully fetched materials", count=len(materials))
            return materials
            
        except Exception as e:
            logger.error("Failed to fetch materials", error=str(e))
            raise
    
    async def add(self, name: str, price: float, unit: str = "г", category: str = "material") -> bool:
        """Add a new material to the database."""
        logger.info("Adding new material", name=name, price=price, unit=unit, category=category)
        
        try:
            conn = self._get_connection()
            conn.execute("INSERT OR REPLACE INTO materials VALUES (?, ?, ?, ?)",
                        (name, price, unit, category))
            conn.commit()
            conn.close()
            
            logger.info("Successfully added material", name=name)
            return True
            
        except Exception as e:
            logger.error("Failed to add material", name=name, error=str(e))
            return False
    
    async def find_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a material by name (case-insensitive)."""
        logger.debug("Searching for material by name", name=name)
        
        try:
            conn = self._get_connection()
            cursor = conn.execute("SELECT name, price, unit, category FROM materials WHERE name LIKE ?",
                                 (f"%{name}%",))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                result = {
                    "name": row[0],
                    "price": row[1],
                    "unit": row[2],
                    "category": row[3]
                }
                logger.debug("Found material", material=result)
                return result
            else:
                logger.debug("Material not found", name=name)
                return None
                
        except Exception as e:
            logger.error("Failed to search for material", name=name, error=str(e))
            return None