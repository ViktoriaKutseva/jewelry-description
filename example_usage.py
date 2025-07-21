import pandas as pd
import os
from datetime import datetime
from jewelry_cost_calculator import (
    Material, Consumable, WorkTime, JewelryCostInput, calculate_jewelry_cost
)

def generate_instagram_description(jewelry_type, materials, stones, style, features, photo_path):
    # Собираем строку материалов
    mat_str = ', '.join([m.name for m in materials if 'медь' in m.name.lower() or 'латунь' in m.name.lower() or 'нейзильбер' in m.name.lower()])
    stone_str = ', '.join([m.name for m in stones])
    desc = f"{jewelry_type.capitalize()} ручной работы"
    if mat_str:
        desc += f" из {mat_str}"
    if stone_str:
        desc += f" с натуральными камнями: {stone_str}"
    if style:
        desc += f". Стиль: {style}"
    if features:
        desc += f". Особенности: {features}"
    desc += ".\n\nКаждое изделие уникально, как и вы ✨\n"
    desc += "#украшения #ручнаяработа #handmade #подарок #уникально #jewelry"
    if photo_path:
        desc += f"\nФото: {photo_path}"
    return desc

# Загружаем сокращённый список материалов
short_df = pd.read_csv('short_materials.csv')
short_df = short_df.dropna(subset=['Цена'])  # Только с ценой
short_df = short_df.drop_duplicates(subset=['Название', 'Ед.изм.'])

print("\nДоступные материалы:")
for idx, row in short_df.iterrows():
    print(f"{idx+1}. {row['Название']} — {row['Цена']} тг/{row['Ед.изм.']}")

selected = []
stones = []
while True:
    choice = input("\nВведите номер материала (или Enter для завершения): ").strip()
    if not choice:
        break
    if not choice.isdigit() or not (1 <= int(choice) <= len(short_df)):
        print("Некорректный номер. Попробуйте снова.")
        continue
    idx = int(choice) - 1
    row = short_df.iloc[idx]
    qty = input(f"  Введите количество для '{row['Название']}' (в {row['Ед.изм.']}): ").replace(",", ".").strip()
    try:
        qty = float(qty)
        if qty <= 0:
            print("  Количество должно быть положительным!")
            continue
    except ValueError:
        print("  Некорректное количество!")
        continue
    mat = Material(
        name=row['Название'],
        unit_price=float(row['Цена']),
        quantity=qty,
        unit=row['Ед.изм.']
    )
    selected.append(mat)
    # Если это камень (не металл), добавляем в stones
    if not any(x in mat.name.lower() for x in ['медь', 'латунь', 'нейзильбер']):
        stones.append(mat)
    print(f"  Добавлено: {row['Название']} — {qty} {row['Ед.изм.']}")

if not selected:
    print("\nНе выбрано ни одного материала! Завершение.")
    exit(0)

# Запрашиваем ставку и время работы
while True:
    try:
        hourly_rate = float(input("\nВведите ставку за час работы (тг): ").replace(",", "."))
        if hourly_rate <= 0:
            print("Ставка должна быть положительной!")
            continue
        break
    except ValueError:
        print("Некорректная ставка!")

while True:
    try:
        hours = float(input("Введите затраченное время (часы): ").replace(",", "."))
        if hours <= 0:
            print("Время должно быть положительным!")
            continue
        break
    except ValueError:
        print("Некорректное время!")

# Вводим параметры для описания
jewelry_type = input("\nТип изделия (например, браслет, кольцо, серьги): ").strip()
style = input("Стиль/настроение (например, минимализм, бохо, винтаж): ").strip()
features = input("Особенности/для кого (например, подарок, женский, мужской): ").strip()
photo_path = input("Путь к фото (или оставьте пустым): ").strip()

consumables = [
    Consumable(name="Расходники (шлифовка, воск, упаковка)", approx_cost=350),
    Consumable(name="Электричество", approx_cost=20),
    Consumable(name="Амортизация инструмента", approx_cost=125),
    Consumable(name="Цаполак (лак для металла)", approx_cost=50),
]

work_time = WorkTime(hours=hours, hourly_rate=hourly_rate)

data = JewelryCostInput(
    materials=selected,
    consumables=consumables,
    work_time=work_time,
    electricity_cost=0,  # уже учтено в consumables
    tool_depreciation=0, # уже учтено в consumables
    packaging_cost=0,    # уже учтено в consumables
    defect_percent=0,    # не учитываем брак для чистоты примера
)

result = calculate_jewelry_cost(data)

# Красивый вывод
print("\nСебестоимость изделия (пересчитанная)")
for name, cost in result.cost_breakdown.items():
    print(f"- {name}: {int(cost)} тг")
print(f"\nИтого себестоимость: {int(result.total_cost)} тг\n")
print("Рекомендуемая цена продажи:")
for label, price in result.recommended_prices.items():
    print(f"- {label}: {int(price)} тг")
print(f"\n{result.price_comment}")

# Генерация описания для Instagram
print("\n---\nОписание для Instagram:\n")
desc = generate_instagram_description(jewelry_type, selected, stones, style, features, photo_path)
print(desc)

# Сохраняем всё в .md-файл
os.makedirs('jewelry', exist_ok=True)
today = datetime.now().strftime('%Y-%m-%d_%H-%M')
filename = f"jewelry/{jewelry_type.replace(' ', '_')}_{today}.md"
with open(filename, 'w', encoding='utf-8') as f:
    f.write(f"# {jewelry_type}\n\n")
    f.write(f"**Дата создания:** {today}\n\n")
    f.write("## Себестоимость и затраты\n\n")
    for name, cost in result.cost_breakdown.items():
        f.write(f"- {name}: {int(cost)} тг\n")
    f.write(f"\n**Итого себестоимость:** {int(result.total_cost)} тг\n\n")
    f.write("## Рекомендуемая цена продажи\n\n")
    for label, price in result.recommended_prices.items():
        f.write(f"- {label}: {int(price)} тг\n")
    f.write(f"\n{result.price_comment}\n\n")
    f.write("---\n\n")
    f.write("## Описание для Instagram\n\n")
    f.write(desc + '\n')
    if photo_path:
        f.write(f"\n![]({photo_path})\n")
print(f"\nВся информация сохранена в {filename}") 