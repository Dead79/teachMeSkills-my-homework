import sqlite3
from datetime import datetime, date
from typing import Tuple


def input_date(prompt: str) -> date:
    while True:
        try:
            date_str = input(prompt).strip()
            if not date_str:
                return date.today()
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("❌ Неверный формат даты. Используйте ГГГГ-ММ-ДД или Enter для сегодня")


class AlcoholTracker:
    def __init__(self, db_name: str = "alcohol_tracker.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        # Устанавливаем соединение с правильной адаптацией дат
        conn = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.execute("PRAGMA foreign_keys = ON")  # Включаем внешние ключи
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alcohol_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            typical_strength REAL NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS consumption_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alcohol_type_id INTEGER NOT NULL,
            volume_ml REAL NOT NULL,
            strength REAL NOT NULL,
            consumption_date DATE NOT NULL,
            notes TEXT,
            FOREIGN KEY (alcohol_type_id) REFERENCES alcohol_types(id)
        )
        ''')

        default_types = [
            ('Пиво', 5.0), ('Вино', 12.0), ('Водка', 40.0),
            ('Виски', 40.0), ('Ром', 40.0), ('Текила', 38.0),
            ('Коньяк', 40.0), ('Шампанское', 12.0), ('Ликёр', 20.0)
        ]

        cursor.executemany(
            'INSERT OR IGNORE INTO alcohol_types (name, typical_strength) VALUES (?, ?)',
            default_types
        )

        conn.commit()
        conn.close()
        print("✅ База данных инициализирована")

    def execute_query(self, query: str, params: Tuple = None, fetch: bool = False):
        # Используем правильную адаптацию типов для дат
        conn = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        try:
            if params:
                # Преобразуем даты в строки для SQLite
                processed_params = []
                for param in params:
                    if isinstance(param, date):
                        processed_params.append(param.isoformat())
                    else:
                        processed_params.append(param)
                cursor.execute(query, processed_params)
            else:
                cursor.execute(query)

            if fetch:
                result = cursor.fetchall()
                # Преобразуем строки дат обратно в объекты date
                processed_result = []
                for row in result:
                    processed_row = []
                    for item in row:
                        if isinstance(item, str) and len(item) == 10 and item[4] == '-' and item[7] == '-':
                            try:
                                processed_row.append(date.fromisoformat(item))
                            except ValueError:
                                processed_row.append(item)
                        else:
                            processed_row.append(item)
                    processed_result.append(tuple(processed_row))
                result = processed_result
            else:
                result = None

            conn.commit()
            return result
        except sqlite3.Error as e:
            print(f"❌ Ошибка БД: {e}")
            return None
        finally:
            conn.close()

    def get_alcohol_strength(self, alcohol_id: int) -> float:
        """Получить крепость алкоголя по умолчанию"""
        result = self.execute_query(
            "SELECT typical_strength FROM alcohol_types WHERE id = ?",
            (alcohol_id,),
            fetch=True
        )
        return result[0][0] if result else 40.0

    def get_alcohol_name(self, alcohol_id: int) -> str:
        """Получить название алкоголя по ID"""
        result = self.execute_query(
            "SELECT name FROM alcohol_types WHERE id = ?",
            (alcohol_id,),
            fetch=True
        )
        return result[0][0] if result else "Неизвестный напиток"

    def show_alcohol_types(self):
        """Показать список алкоголя"""
        print("\n🍷 СПИСОК АЛКОГОЛЯ:")
        print("-" * 45)

        types = self.execute_query(
            "SELECT id, name, typical_strength FROM alcohol_types ORDER BY id",
            fetch=True
        )

        if types:
            print(f"{'№':<3} {'Напиток':<15} {'Крепость':<10}")
            print("-" * 45)
            for type_id, name, strength in types:
                print(f"{type_id:<3} {name:<15} {strength:5.1f}%")
        else:
            print("Нет данных о видах алкоголя")

    def add_alcohol_type(self):
        print("\n➕ ДОБАВЛЕНИЕ НОВОГО ВИДА АЛКОГОЛЯ")
        name = input("Название: ").strip()

        if not name:
            print("❌ Название не может быть пустым")
            return

        try:
            strength_input = input("Крепость (%) [по умолчанию 40]: ").strip()
            if not strength_input:
                strength = 40.0
                print(f"✅ Использована крепость по умолчанию: {strength}%")
            else:
                strength = float(strength_input)

            if strength < 0 or strength > 100:
                print("❌ Крепость должна быть от 0 до 100%")
                return
        except ValueError:
            print("❌ Крепость должна быть числом")
            return

        if self.execute_query(
                "INSERT INTO alcohol_types (name, typical_strength) VALUES (?, ?)",
                (name, strength)
        ):
            print(f"✅ '{name}' добавлен!")
            self.show_alcohol_types()

    def add_consumption(self):
        print("\n🍺 ДОБАВЛЕНИЕ ЗАПИСИ О ПОТРЕБЛЕНИИ")

        self.show_alcohol_types()

        try:
            alcohol_id = int(input("\n№ напитка: "))

            check = self.execute_query(
                "SELECT id, name, typical_strength FROM alcohol_types WHERE id = ?",
                (alcohol_id,),
                fetch=True
            )

            if not check:
                print(f"❌ Напиток с №{alcohol_id} не найден")
                return

            drink_name, default_strength = check[0][1], check[0][2]
            print(f"✅ Выбран: {drink_name} (крепость по умолчанию: {default_strength}%)")

        except ValueError:
            print("❌ Номер должен быть числом")
            return

        try:
            volume = float(input("Объем (мл): "))
            if volume <= 0:
                print("❌ Объем должен быть положительным числом")
                return
        except ValueError:
            print("❌ Объем должен быть числом")
            return

        try:
            strength_input = input(f"Крепость (%) [по умолчанию {default_strength}%]: ").strip()
            if not strength_input:
                strength = default_strength
                print(f"✅ Использована крепость по умолчанию: {strength}%")
            else:
                strength = float(strength_input)

            if strength < 0 or strength > 100:
                print("❌ Крепость должна быть от 0 до 100%")
                return
        except ValueError:
            print("❌ Крепость должна быть числом")
            return

        consumption_date = input_date("Дата употребления (ГГГГ-ММ-ДД или Enter для сегодня): ")
        notes = input("Примечания: ").strip()

        if self.execute_query(
                '''INSERT INTO consumption_records 
                   (alcohol_type_id, volume_ml, strength, consumption_date, notes) 
                   VALUES (?, ?, ?, ?, ?)''',
                (alcohol_id, volume, strength, consumption_date, notes)
        ):
            print(f"✅ Потребление '{drink_name}' добавлено!")

    def show_consumption(self):
        print("\n📊 ИСТОРИЯ ПОТРЕБЛЕНИЯ:")
        print("1. За все время")
        print("2. За определенный период")
        print("3. За конкретную дату")

        choice = input("Выберите вариант (1-3): ").strip()

        query = '''
            SELECT cr.id, at.name, cr.volume_ml, cr.strength, cr.consumption_date, cr.notes
            FROM consumption_records cr
            JOIN alcohol_types at ON cr.alcohol_type_id = at.id
        '''
        params = ()

        if choice == "2":
            start_date = input_date("Начальная дата (ГГГГ-ММ-ДД): ")
            end_date = input_date("Конечная дата (ГГГГ-ММ-ДД): ")
            query += " WHERE consumption_date BETWEEN ? AND ?"
            params = (start_date, end_date)
        elif choice == "3":
            target_date = input_date("Дата (ГГГГ-ММ-ДД): ")
            query += " WHERE consumption_date = ?"
            params = (target_date,)

        query += " ORDER BY cr.consumption_date DESC, cr.id DESC LIMIT 20"

        records = self.execute_query(query, params, fetch=True)

        if records:
            print(f"\n{'ID':<3} {'Напиток':<12} {'Объем':<6} {'Крепость':<8} {'Дата':<12} Примечания")
            print("-" * 70)
            for record in records:
                date_str = record[4].strftime('%Y-%m-%d') if isinstance(record[4], date) else str(record[4])
                print(
                    f"{record[0]:<3} {record[1]:<12} {record[2]:<6.1f} {record[3]:<8.1f} {date_str:<12} {record[5] or ''}")
        else:
            print("Нет записей о потреблении")

    def show_stats(self):
        print("\n📈 СТАТИСТИКА ПОТРЕБЛЕНИЯ:")
        print("1. За все время")
        print("2. За определенный период")
        print("3. За конкретную дату")
        print("4. По видам алкоголя")

        choice = input("Выберите вариант (1-4): ").strip()

        if choice == "4":
            self.show_stats_by_alcohol_type()
            return

        query = '''
            SELECT 
                COUNT(*) as records,
                SUM(volume_ml) as total_ml,
                AVG(strength) as avg_strength
            FROM consumption_records
        '''
        params = ()

        if choice == "2":
            start_date = input_date("Начальная дата (ГГГГ-ММ-ДД): ")
            end_date = input_date("Конечная дата (ГГГГ-ММ-ДД): ")
            query += " WHERE consumption_date BETWEEN ? AND ?"
            params = (start_date, end_date)
        elif choice == "3":
            target_date = input_date("Дата (ГГГГ-ММ-ДД): ")
            query += " WHERE consumption_date = ?"
            params = (target_date,)

        stats = self.execute_query(query, params, fetch=True)

        if stats and stats[0][0]:
            records, total_ml, avg_strength = stats[0]
            print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
            print(f"Количество записей: {records}")
            print(f"Общий объем: {total_ml:.1f} мл")
            print(f"Средняя крепость: {avg_strength:.1f}%")

            if total_ml and avg_strength:
                pure_alcohol = total_ml * avg_strength / 100
                print(f"Чистого алкоголя: {pure_alcohol:.1f} мл")
        else:
            print("Нет данных для статистики")

    def show_stats_by_alcohol_type(self):
        """Статистика по видам алкоголя"""
        print("\n📊 СТАТИСТИКА ПО ВИДАМ АЛКОГОЛЯ:")

        query = '''
            SELECT 
                at.name as alcohol_name,
                COUNT(cr.id) as records_count,
                SUM(cr.volume_ml) as total_volume,
                AVG(cr.strength) as avg_strength,
                SUM(cr.volume_ml * cr.strength / 100) as pure_alcohol
            FROM alcohol_types at
            LEFT JOIN consumption_records cr ON at.id = cr.alcohol_type_id
            GROUP BY at.id
            HAVING records_count > 0
            ORDER BY total_volume DESC
        '''

        stats = self.execute_query(query, fetch=True)

        if stats:
            print(f"\n{'Напиток':<15} {'Записей':<8} {'Объем':<10} {'Крепость':<10} {'Чистый алк.':<12}")
            print("-" * 65)
            total_pure_alcohol = 0

            for alcohol_name, records, volume, strength, pure_alc in stats:
                if records > 0:
                    strength_str = f"{strength:.1f}%" if strength else "0%"
                    volume_str = f"{volume:.1f} мл" if volume else "0 мл"
                    pure_alc_str = f"{pure_alc:.1f} мл" if pure_alc else "0 мл"

                    print(f"{alcohol_name:<15} {records:<8} {volume_str:<10} {strength_str:<10} {pure_alc_str:<12}")

                    if pure_alc:
                        total_pure_alcohol += pure_alc

            if total_pure_alcohol > 0:
                print("-" * 65)
                print(f"{'ВСЕГО':<15} {'':<8} {'':<10} {'':<10} {total_pure_alcohol:<12.1f} мл")
        else:
            print("Нет данных для статистики по видам алкоголя")

    def clear_history(self):
        print("\n🗑️  УПРАВЛЕНИЕ ИСТОРИЕЙ:")
        print("1. Удалить все записи о потреблении")
        print("2. Удалить записи за конкретную дату")
        print("3. Показать список алкоголя")
        print("4. Удалить вид алкоголя")
        print("0. Назад")

        choice = input("Выберите вариант (0-4): ").strip()

        if choice == "0":
            return
        elif choice == "1":
            confirm = input("❌ ВЫ УВЕРЕНЫ? Это удалит ВСЮ историю потребления! (y/n): ").strip().lower()
            if confirm in ['y', 'yes', 'д', 'да']:
                if self.execute_query("DELETE FROM consumption_records"):
                    print("✅ Вся история потребления удалена!")
            else:
                print("❌ Отменено")
        elif choice == "2":
            target_date = input_date("Дата для удаления (ГГГГ-ММ-ДД): ")
            confirm = input(f"❌ Удалить все записи за {target_date}? (y/n): ").strip().lower()
            if confirm in ['y', 'yes', 'д', 'да']:
                if self.execute_query(
                        "DELETE FROM consumption_records WHERE consumption_date = ?",
                        (target_date,)
                ):
                    print(f"✅ Записи за {target_date} удалены!")
            else:
                print("❌ Отменено")
        elif choice == "3":
            self.show_alcohol_types()
        elif choice == "4":
            self.show_alcohol_types()
            try:
                alcohol_id = int(input("\n№ алкоголя для удаления: "))
                alcohol_name = self.get_alcohol_name(alcohol_id)
                confirm = input(f"❌ Удалить '{alcohol_name}'? (y/n): ").strip().lower()
                if confirm in ['y', 'yes', 'д', 'да']:
                    self.execute_query(
                        "DELETE FROM consumption_records WHERE alcohol_type_id = ?",
                        (alcohol_id,)
                    )
                    if self.execute_query(
                            "DELETE FROM alcohol_types WHERE id = ?",
                            (alcohol_id,)
                    ):
                        print(f"✅ '{alcohol_name}' удален!")
            except ValueError:
                print("❌ Номер должен быть числом")

    def run(self):
        while True:
            print("\n" + "=" * 50)
            print("🍻 ТРЕКЕР ПОТРЕБЛЕНИЯ АЛКОГОЛЯ")
            print("=" * 50)
            print("1. 📋 Список алкоголя")
            print("2. ➕ Добавить вид алкоголя")
            print("3. 🍺 Добавить потребление")
            print("4. 📊 История потребления")
            print("5. 📈 Статистика")
            print("6. 🗑️  Управление историей")
            print("0. ❌ Выход")

            choice = input("\nВаш выбор (0-6): ").strip()

            if choice == "0":
                print("👋 До свидания! Пейте ответственно!")
                break
            elif choice == "1":
                self.show_alcohol_types()
            elif choice == "2":
                self.add_alcohol_type()
            elif choice == "3":
                self.add_consumption()
            elif choice == "4":
                self.show_consumption()
            elif choice == "5":
                self.show_stats()
            elif choice == "6":
                self.clear_history()
            else:
                print("❌ Неверный выбор")

            input("\n↵ Нажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    tracker = AlcoholTracker()
    tracker.run()