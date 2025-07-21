import pandas as pd

# Ручной перевод английских названий камней
STONE_TRANSLATE = {
    'Turmaline': 'Турмалин',
    'Electroplated quartz': 'Кварц',
    'Opal': 'Опал',
    'Green Apatite': 'Апатит зелёный',
    'Lapis Lazuli': 'Лазурит',
    'White Natural Freshwater Pearls': 'Белый натуральный жемчуг',
    'Black Baroque Freshwater Pearl Beads': 'Чёрный барочный жемчуг',
    'Garnet Stone Beads Gravel Chip': 'Гранат',
    'Natural Aquamarine': 'Аквамарин',
    'Onyx beads': 'Оникс',
    'Black onyx': 'Чёрный оникс',
    'Apatite': 'Апатит',
    'Golden sand': 'Золотой песок',
    'Pearl': 'Жемчуг',
    'Phoenix': 'Феникс',
    'Agat': 'Агат',
    'Drop Shaped Glass Beads': 'Каплевидные стеклянные бусины',
    'Natural Stone Chrysanthemum & Conch': 'Хризантема и ракушка',
    'Carnelian Crystal Chips': 'Сердолик',
    "Tiger's Eye Small Tumbled Chips": 'Тигровый глаз',
    'Natural Garnet Crystal Fragments': 'Гранат (осколки)',
    'High-Quality 3Pcs Natural Garnet Small Oval Naked Stone': 'Гранат (овал)',
    'Ceramic Snail Beads': 'Керамические бусины-улитки',
    'High-Flash Labradorite Slabs': 'Лабрадорит',
    'Black Natural Agate Crystal Slices,': 'Чёрный агат (срезы)',
    'Natural Stone Yellow Tiger Eye Loose Beads 4': 'Тигровый глаз (жёлтый)',
    'Natural Natural chrysoprase stone': 'Хризопраз',
    "Natural Dragon'S Blood Stone": 'Камень Кровь дракона',
    'Grade A Natural Peridot Round Cabochons,': 'Перидот (кабошон)',
}

src = 'info.csv'
df = pd.read_csv(src)

# 1. Медь (все варианты, кроме квадратной)
copper = df[df['Name'].str.lower().str.contains('медь') & ~df['Name'].str.lower().str.contains('square')]
copper_price = copper['1 gram'].dropna().astype(float).mean()

# 2. Квадратная медь
sq_copper = df[df['Name'].str.lower().str.contains('square') & df['Name'].str.lower().str.contains('copper')]
sq_copper_price = sq_copper['1 gram'].dropna().astype(float).mean()

# 3. Латунь
brass = df[df['Name'].str.lower().str.contains('латун')]
brass_price = brass['1 gram'].dropna().astype(float).mean()

# 4. Нейзильбер
german_silver = df[df['Name'].str.lower().str.contains('нейз')]
german_silver_price = german_silver['1 gram'].dropna().astype(float).mean()

# 5. Все камни (stone)
stones = df[(df['tags ']=='stone')]
stone_rows = []
for _, row in stones.iterrows():
    name = str(row['Name']).strip()
    # Если на русском — оставляем, если на английском — переводим вручную
    if any('а' <= c.lower() <= 'я' for c in name):
        name_ru = name
    else:
        name_ru = STONE_TRANSLATE.get(name.strip(), name.strip())
    price = None
    unit = 'шт'
    if pd.notnull(row.get('1 piece')) and float(row['1 piece']) > 0:
        price = float(row['1 piece'])
        unit = 'шт'
    elif pd.notnull(row.get('1 gram')) and float(row['1 gram']) > 0:
        price = float(row['1 gram'])
        unit = 'г'
    if price:
        stone_rows.append({'Название': name_ru, 'Цена': round(price,2), 'Ед.изм.': unit})

# Формируем итоговый DataFrame
rows = [
    {'Название': 'Медь (средняя)', 'Цена': round(copper_price,2), 'Ед.изм.': 'г'},
    {'Название': 'Квадратная медь (средняя)', 'Цена': round(sq_copper_price,2), 'Ед.изм.': 'г'},
    {'Название': 'Латунь (средняя)', 'Цена': round(brass_price,2), 'Ед.изм.': 'г'},
    {'Название': 'Нейзильбер (средняя)', 'Цена': round(german_silver_price,2), 'Ед.изм.': 'г'},
]
rows.extend(stone_rows)
short_df = pd.DataFrame(rows)
short_df.to_csv('short_materials.csv', index=False, encoding='utf-8-sig')
print('Сокращённый список сохранён в short_materials.csv') 