import sqlite3
from typing import List, Tuple, Optional


class InteractiveLibrary:
    def __init__(self, db_name: str = "library.db"):
        """Инициализация интерактивной библиотеки"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.insert_initial_data()

    def create_tables(self):
        """Создание таблиц базы данных"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            UNIQUE(first_name, last_name)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            author_id INTEGER,
            publication_year INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE SET NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            sale_date DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        )
        ''')

        self.conn.commit()

    def insert_initial_data(self):
        """Начальные данные для демонстрации"""
        authors = [
            ('Лев', 'Толстой'),
            ('Фёдор', 'Достоевский'),
            ('Антон', 'Чехов')
        ]

        books = [
            ('Война и мир', 1, 1869),
            ('Преступление и наказание', 2, 1866),
            ('Вишнёвый сад', 3, 1904)
        ]

        sales = [
            (1, 150),
            (2, 200),
            (3, 70)
        ]

        try:
            self.cursor.executemany(
                'INSERT OR IGNORE INTO authors (first_name, last_name) VALUES (?, ?)',
                authors
            )
            self.cursor.executemany(
                'INSERT OR IGNORE INTO books (title, author_id, publication_year) VALUES (?, ?, ?)',
                books
            )
            self.cursor.executemany(
                'INSERT OR IGNORE INTO sales (book_id, quantity) VALUES (?, ?)',
                sales
            )
            self.conn.commit()
        except sqlite3.Error:
            pass

    def print_results(self, title: str, query: str, params: Tuple = None):
        """Вывод результатов запроса"""
        print(f"\n{'=' * 60}")
        print(f"📊 {title}")
        print(f"{'=' * 60}")

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            columns = [description[0] for description in self.cursor.description]
            print(" | ".join(f"{col:<20}" for col in columns))
            print("-" * 80)

            results = self.cursor.fetchall()
            if not results:
                print("Нет данных")
            else:
                for row in results:
                    formatted_row = [str(item) if item is not None else "NULL" for item in row]
                    print(" | ".join(f"{item:<20}" for item in formatted_row))

        except sqlite3.Error as e:
            print(f"❌ Ошибка: {e}")

    def show_authors(self):
        """Показать всех авторов"""
        self.print_results(
            "СПИСОК АВТОРОВ",
            "SELECT id, first_name, last_name FROM authors ORDER BY last_name"
        )

    def show_books(self):
        """Показать все книги"""
        self.print_results(
            "СПИСОК КНИГ",
            '''
            SELECT b.id, b.title, a.first_name || ' ' || a.last_name as author, 
                   b.publication_year
            FROM books b
            LEFT JOIN authors a ON b.author_id = a.id
            ORDER BY b.title
            '''
        )

    def show_sales(self):
        """Показать все продажи"""
        self.print_results(
            "СПИСОК ПРОДАЖ",
            '''
            SELECT s.id, b.title, s.quantity, s.sale_date
            FROM sales s
            JOIN books b ON s.book_id = b.id
            ORDER BY s.sale_date DESC
            '''
        )

    def add_author(self):
        """Добавить нового автора"""
        print("\n➕ ДОБАВЛЕНИЕ НОВОГО АВТОРА")
        first_name = input("Имя автора: ").strip()
        last_name = input("Фамилия автора: ").strip()

        if not first_name or not last_name:
            print("❌ Имя и фамилия не могут быть пустыми")
            return

        try:
            self.cursor.execute(
                "INSERT INTO authors (first_name, last_name) VALUES (?, ?)",
                (first_name, last_name)
            )
            self.conn.commit()
            print(f"✅ Автор {first_name} {last_name} успешно добавлен!")
        except sqlite3.IntegrityError:
            print("❌ Автор с таким именем уже существует")

    def add_book(self):
        """Добавить новую книгу"""
        print("\n➕ ДОБАВЛЕНИЕ НОВОЙ КНИГИ")

        # Показать существующих авторов
        self.show_authors()

        title = input("\nНазвание книги: ").strip()
        if not title:
            print("❌ Название не может быть пустым")
            return

        try:
            publication_year = int(input("Год публикации: "))
        except ValueError:
            print("❌ Год должен быть числом")
            return

        author_id = input("ID автора (Enter если без автора): ").strip()
        if not author_id:
            author_id = None
        else:
            try:
                author_id = int(author_id)
            except ValueError:
                print("❌ ID автора должен быть числом")
                return

        try:
            self.cursor.execute(
                "INSERT INTO books (title, author_id, publication_year) VALUES (?, ?, ?)",
                (title, author_id, publication_year)
            )
            self.conn.commit()
            print(f"✅ Книга '{title}' успешно добавлена!")
        except sqlite3.IntegrityError:
            print("❌ Книга с таким названием уже существует")

    def add_sale(self):
        """Добавить новую продажу"""
        print("\n➕ ДОБАВЛЕНИЕ НОВОЙ ПРОДАЖИ")

        # Показать существующие книги
        self.show_books()

        try:
            book_id = int(input("\nID книги: "))
            quantity = int(input("Количество проданных экземпляров: "))
        except ValueError:
            print("❌ ID и количество должны быть числами")
            return

        try:
            self.cursor.execute(
                "INSERT INTO sales (book_id, quantity) VALUES (?, ?)",
                (book_id, quantity)
            )
            self.conn.commit()
            print(f"✅ Продажа успешно добавлена!")
        except sqlite3.Error as e:
            print(f"❌ Ошибка: {e}")

    def task_2_joins(self):
        """Задача 2: Использование JOIN"""
        print("\n🎯 ВЫБЕРИТЕ ТИП JOIN:")
        print("1. INNER JOIN - книги и их авторы")
        print("2. LEFT JOIN - все авторы и их книги")
        print("3. Все книги (включая без авторов)")

        choice = input("\nВаш выбор (1-3): ").strip()

        if choice == "1":
            self.print_results(
                "INNER JOIN: Книги и их авторы",
                '''
                SELECT b.title, b.publication_year, 
                       a.first_name || ' ' || a.last_name as author
                FROM books b
                INNER JOIN authors a ON b.author_id = a.id
                ORDER BY b.title
                '''
            )
        elif choice == "2":
            self.print_results(
                "LEFT JOIN: Все авторы и их книги",
                '''
                SELECT a.first_name, a.last_name, 
                       COALESCE(b.title, 'Нет книг') as book_title
                FROM authors a
                LEFT JOIN books b ON a.id = b.author_id
                ORDER BY a.last_name
                '''
            )
        elif choice == "3":
            self.print_results(
                "Все книги (с авторами если есть)",
                '''
                SELECT b.title, b.publication_year,
                       COALESCE(a.first_name || ' ' || a.last_name, 'Автор не указан') as author
                FROM books b
                LEFT JOIN authors a ON b.author_id = a.id
                ORDER BY b.title
                '''
            )
        else:
            print("❌ Неверный выбор")

    def task_3_multiple_joins(self):
        """Задача 3: Множественные JOIN"""
        print("\n🎯 ВЫБЕРИТЕ ТИП МНОЖЕСТВЕННОГО JOIN:")
        print("1. INNER JOIN - книги, авторы и продажи")
        print("2. LEFT JOIN - все авторы, книги и продажи")

        choice = input("\nВаш выбор (1-2): ").strip()

        if choice == "1":
            self.print_results(
                "INNER JOIN: Книги, авторы и продажи",
                '''
                SELECT a.first_name, a.last_name, b.title, 
                       s.quantity as продажи, s.sale_date
                FROM sales s
                INNER JOIN books b ON s.book_id = b.id
                INNER JOIN authors a ON b.author_id = a.id
                ORDER BY a.last_name, b.title
                '''
            )
        elif choice == "2":
            self.print_results(
                "LEFT JOIN: Все авторы, книги и продажи",
                '''
                SELECT a.first_name, a.last_name, 
                       b.title as книга,
                       COALESCE(s.quantity, 0) as продажи
                FROM authors a
                LEFT JOIN books b ON a.id = b.author_id
                LEFT JOIN sales s ON b.id = s.book_id
                ORDER BY a.last_name, b.title
                '''
            )
        else:
            print("❌ Неверный выбор")

    def task_4_aggregation(self):
        """Задача 4: Агрегация данных"""
        print("\n🎯 ВЫБЕРИТЕ ТИП АГРЕГАЦИИ:")
        print("1. Продажи по авторам (INNER JOIN)")
        print("2. Все авторы с продажами (LEFT JOIN)")
        print("3. Статистика по книгам")

        choice = input("\nВаш выбор (1-3): ").strip()

        if choice == "1":
            self.print_results(
                "Продажи по авторам",
                '''
                SELECT a.first_name, a.last_name,
                       COUNT(b.id) as книг_в_продаже,
                       SUM(s.quantity) as всего_продано
                FROM authors a
                INNER JOIN books b ON a.id = b.author_id
                INNER JOIN sales s ON b.id = s.book_id
                GROUP BY a.id
                ORDER BY всего_продано DESC
                '''
            )
        elif choice == "2":
            self.print_results(
                "Все авторы с продажами",
                '''
                SELECT a.first_name, a.last_name,
                       COUNT(b.id) as количество_книг,
                       COALESCE(SUM(s.quantity), 0) as всего_продано
                FROM authors a
                LEFT JOIN books b ON a.id = b.author_id
                LEFT JOIN sales s ON b.id = s.book_id
                GROUP BY a.id
                ORDER BY всего_продано DESC
                '''
            )
        elif choice == "3":
            self.print_results(
                "Статистика по книгам",
                '''
                SELECT b.title, 
                       COALESCE(a.first_name || ' ' || a.last_name, 'Нет автора') as author,
                       COALESCE(SUM(s.quantity), 0) as продано,
                       COUNT(s.id) as количество_продаж
                FROM books b
                LEFT JOIN authors a ON b.author_id = a.id
                LEFT JOIN sales s ON b.id = s.book_id
                GROUP BY b.id
                ORDER BY продано DESC
                '''
            )
        else:
            print("❌ Неверный выбор")

    def task_5_subqueries(self):
        """Задача 5: Подзапросы"""
        print("\n🎯 ВЫБЕРИТЕ ТИП ПОДЗАПРОСА:")
        print("1. Автор с наибольшими продажами")
        print("2. Книги с продажами выше среднего")
        print("3. Топ-3 книги по продажам")

        choice = input("\nВаш выбор (1-3): ").strip()

        if choice == "1":
            self.print_results(
                "Автор с наибольшими продажами",
                '''
                SELECT a.first_name, a.last_name, total_sales
                FROM authors a
                INNER JOIN (
                    SELECT b.author_id, SUM(s.quantity) as total_sales
                    FROM sales s
                    INNER JOIN books b ON s.book_id = b.id
                    WHERE b.author_id IS NOT NULL
                    GROUP BY b.author_id
                    ORDER BY total_sales DESC
                    LIMIT 1
                ) best_author ON a.id = best_author.author_id
                '''
            )
        elif choice == "2":
            self.print_results(
                "Книги с продажами выше среднего",
                '''
                SELECT b.title, 
                       a.first_name || ' ' || a.last_name as author,
                       book_sales.total_sold as продано
                FROM books b
                INNER JOIN authors a ON b.author_id = a.id
                INNER JOIN (
                    SELECT book_id, SUM(quantity) as total_sold
                    FROM sales
                    GROUP BY book_id
                ) book_sales ON b.id = book_sales.book_id
                WHERE book_sales.total_sold > (
                    SELECT AVG(total_sold) 
                    FROM (SELECT SUM(quantity) as total_sold 
                          FROM sales GROUP BY book_id)
                )
                ORDER BY book_sales.total_sold DESC
                '''
            )
        elif choice == "3":
            self.print_results(
                "Топ-3 книги по продажам",
                '''
                SELECT b.title, 
                       a.first_name || ' ' || a.last_name as author,
                       SUM(s.quantity) as продано
                FROM books b
                LEFT JOIN authors a ON b.author_id = a.id
                LEFT JOIN sales s ON b.id = s.book_id
                GROUP BY b.id
                ORDER BY продано DESC
                LIMIT 3
                '''
            )
        else:
            print("❌ Неверный выбор")

    def show_statistics(self):
        """Показать статистику базы данных"""
        self.print_results(
            "СТАТИСТИКА БАЗЫ ДАННЫХ",
            '''
            SELECT 'Авторы' as категория, COUNT(*) as количество FROM authors
            UNION ALL
            SELECT 'Книги', COUNT(*) FROM books
            UNION ALL
            SELECT 'Продажи', COUNT(*) FROM sales
            UNION ALL
            SELECT 'Книги без автора', COUNT(*) FROM books WHERE author_id IS NULL
            UNION ALL
            SELECT 'Книги без продаж', COUNT(*) FROM books 
            WHERE id NOT IN (SELECT DISTINCT book_id FROM sales)
            '''
        )

    def run(self):
        """Запуск интерактивного меню"""
        while True:
            print("\n" + "=" * 60)
            print("🏛️  ИНТЕРАКТИВНАЯ БИБЛИОТЕЧНАЯ СИСТЕМА")
            print("=" * 60)
            print("1. 📋 Просмотр данных")
            print("2. ➕ Добавление данных")
            print("3. 🎯 Задача 2: JOIN")
            print("4. 🎯 Задача 3: Множественные JOIN")
            print("5. 🎯 Задача 4: Агрегация")
            print("6. 🎯 Задача 5: Подзапросы")
            print("7. 📊 Статистика")
            print("0. ❌ Выход")

            choice = input("\nВаш выбор (0-7): ").strip()

            if choice == "0":
                print("👋 До свидания!")
                break
            elif choice == "1":
                self.show_data_menu()
            elif choice == "2":
                self.add_data_menu()
            elif choice == "3":
                self.task_2_joins()
            elif choice == "4":
                self.task_3_multiple_joins()
            elif choice == "5":
                self.task_4_aggregation()
            elif choice == "6":
                self.task_5_subqueries()
            elif choice == "7":
                self.show_statistics()
            else:
                print("❌ Неверный выбор, попробуйте снова")

            input("\nНажмите Enter чтобы продолжить...")

    def show_data_menu(self):
        """Меню просмотра данных"""
        print("\n📋 ВЫБЕРИТЕ ДАННЫЕ ДЛЯ ПРОСМОТРА:")
        print("1. Авторы")
        print("2. Книги")
        print("3. Продажи")

        choice = input("\nВаш выбор (1-3): ").strip()

        if choice == "1":
            self.show_authors()
        elif choice == "2":
            self.show_books()
        elif choice == "3":
            self.show_sales()
        else:
            print("❌ Неверный выбор")

    def add_data_menu(self):
        """Меню добавления данных"""
        print("\n➕ ВЫБЕРИТЕ ЧТО ДОБАВИТЬ:")
        print("1. Нового автора")
        print("2. Новую книгу")
        print("3. Новую продажу")

        choice = input("\nВаш выбор (1-3): ").strip()

        if choice == "1":
            self.add_author()
        elif choice == "2":
            self.add_book()
        elif choice == "3":
            self.add_sale()
        else:
            print("❌ Неверный выбор")


def main():
    """Основная функция"""
    print("🚀 ЗАПУСК ИНТЕРАКТИВНОЙ БИБЛИОТЕЧНОЙ СИСТЕМЫ")
    library = InteractiveLibrary()
    library.run()


if __name__ == "__main__":
    main()