"""
Description generation service.
"""
import random
from typing import List, Dict
from loguru import logger


class JewelryDescriptionService:
    """Service for generating mystical jewelry descriptions."""
    
    def generate(self, jewelry_type: str, materials: List[Dict[str, any]]) -> str:
        """
        Generate mystical jewelry description for Instagram.
        Based on the existing example_usage.py logic.
        """
        logger.info("Generating description", jewelry_type=jewelry_type, material_count=len(materials))
        
        # Extract material names for description
        metal_materials = []
        stone_materials = []
        
        for mat in materials:
            name = mat["name"]
            if any(x in name.lower() for x in ['медь', 'латунь', 'нейзильбер']):
                metal_materials.append(name)
            else:
                stone_materials.append(name)
        
        mat_str = ', '.join(metal_materials)
        stone_str = ', '.join(stone_materials)
        
        # Generate mystical descriptions
        mystical_adjectives = [
            "словно артефакт древней цивилизации", 
            "пропитанный энергией земли", 
            "несущий в себе магию природы", 
            "созданный для души, стремящейся к гармонии",
            "излучающий силу и уверенность", 
            "хранящий в себе тайны мироздания"
        ]
        
        mystical_desc = random.choice(mystical_adjectives)
        
        # Russian description
        ru_desc = f"🌿 {jewelry_type.capitalize()}\n\n"
        ru_desc += f"{jewelry_type.capitalize()} — смелый акцент и магия линий, {mystical_desc}. "
        
        if mat_str:
            ru_desc += f"Материалы: {mat_str}. "
        if stone_str:
            ru_desc += f"Камни: {stone_str}. "
        
        ru_desc += "\nКаждая деталь выполнена вручную, с вниманием к текстуре и свету.\n"
        ru_desc += "\n💌 В наличии — пишите в директ, если тронуло ваше сердечко\n"
        
        # English description  
        en_desc = f"🌲 {jewelry_type.capitalize()}\n\n"
        en_desc += "Inspired by the power of nature and a touch of mystery. "
        
        if mat_str:
            en_desc += f"Materials: {mat_str}. "
        if stone_str:
            en_desc += f"Stones: {stone_str}. "
        
        en_desc += "\nEach detail is handcrafted with care for texture and light.\n"
        en_desc += "\n💌 This one-of-a-kind piece is available — message me if it speaks to you\n"
        
        # Hashtags
        hashtags = "#украшенияручнойработы #авторскиеукрашения #ручнаяработа #медь #кафф #кольцо #брошь #жемчуг #стиль #магия #handmadejewelry #earcuff #copperjewelry #baroquepearl #uniquejewelry #slowmade #natureinspired #giftideas #madeinkazakhstan #authorjewelry #jewelry #artisanjewelry #oneofakind #naturejewelry #craftwithlove #exclusivejewelry"
        
        # Complete description
        description = f"{ru_desc}\n---\n\n{en_desc}\n🧷 Хэштеги / Hashtags:\n{hashtags}"
        
        logger.info("Generated description", length=len(description))
        return description