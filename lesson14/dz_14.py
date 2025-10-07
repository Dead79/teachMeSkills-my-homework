import sqlite3


class EmployeeDB:
    def __init__(self, db_name="company.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """Подключение к базе данных"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        """Закрытие соединения с базой данных"""
        if self.conn:
            self.conn.close()

    def create_table(self):
        """Создание таблицы Employees"""
        self.connect()
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT NOT NULL,
                    Position TEXT NOT NULL,
                    Department TEXT NOT NULL,
                    Salary REAL NOT NULL
                )
            ''')
            self.conn.commit()
            print("✅ Таблица 'Employees' создана успешно")
        except sqlite3.Error as e:
            print(f"❌ Ошибка при создании таблицы: {e}")
        finally:
            self.close()

    def insert_employees(self):
        """Вставка начальных данных о сотрудниках"""
        employees = [
            ("Дарт Вэйдер", "Manager", "Sales", 6000.0),
            ("Атрэй Кратосович", "Developer", "IT", 5500.0),
            ("Канеки Кен", "Manager", "HR", 5200.0),
            ("Волан Деморт", "Analyst", "Finance", 4800.0),
            ("Гарри Поттер", "Developer", "IT", 5800.0),
            ("Сома Поваров", "Manager", "Sales", 6200.0),
            ("Курт Кобейн", "Designer", "Marketing", 4500.0)
        ]

        self.connect()
        try:
            self.cursor.executemany('''
                INSERT INTO Employees (Name, Position, Department, Salary)
                VALUES (?, ?, ?, ?)
            ''', employees)
            self.conn.commit()
            print("✅ Данные о сотрудниках добавлены успешно")
        except sqlite3.Error as e:
            print(f"❌ Ошибка при добавлении данных: {e}")
        finally:
            self.close()

    def update_employee_position(self, employee_name, new_position):
        """Изменение должности сотрудника"""
        self.connect()
        try:
            self.cursor.execute('''
                UPDATE Employees 
                SET Position = ? 
                WHERE Name = ?
            ''', (new_position, employee_name))
            self.conn.commit()
            print(f"✅ Должность сотрудника {employee_name} изменена на {new_position}")
        except sqlite3.Error as e:
            print(f"❌ Ошибка при обновлении данных: {e}")
        finally:
            self.close()

    def add_hire_date_column(self):
        """Добавление нового поля HireDate"""
        self.connect()
        try:
            self.cursor.execute('''
                ALTER TABLE Employees 
                ADD COLUMN HireDate DATE
            ''')
            self.conn.commit()
            print("✅ Поле 'HireDate' добавлено в таблицу")
        except sqlite3.Error as e:
            print(f"❌ Ошибка при добавлении поля: {e}")
        finally:
            self.close()

    def update_hire_dates(self):
        """Добавление дат приема на работу"""
        hire_dates = [
            ("2020-03-15", "Дарт Вэйдер"),
            ("2019-07-20", "Атрэй Кратосович"),
            ("2021-01-10", "Канеки Кен"),
            ("2022-05-30", "Волан Деморт"),
            ("2018-11-12", "Гарри Поттер"),
            ("2020-09-05", "Сома Поваров"),
            ("2023-02-28", "Курт Кобейн")
        ]

        self.connect()
        try:
            self.cursor.executemany('''
                UPDATE Employees 
                SET HireDate = ? 
                WHERE Name = ?
            ''', hire_dates)
            self.conn.commit()
            print("✅ Даты приема на работу добавлены")
        except sqlite3.Error as e:
            print(f"❌ Ошибка при обновлении дат: {e}")
        finally:
            self.close()

    def find_managers(self):
        """Поиск всех менеджеров"""
        self.connect()
        try:
            self.cursor.execute('''
                SELECT Name, Department, Salary, HireDate
                FROM Employees 
                WHERE Position = 'Manager'
            ''')
            managers = self.cursor.fetchall()
            print("\n📊 Менеджеры:")
            for manager in managers:
                print(f"  {manager[0]} - {manager[1]} - ${manager[2]} - {manager[3]}")
            return managers
        except sqlite3.Error as e:
            print(f"❌ Ошибка при поиске менеджеров: {e}")
            return []
        finally:
            self.close()

    def find_high_salary_employees(self, min_salary=5000):
        """Поиск сотрудников с зарплатой больше указанной"""
        self.connect()
        try:
            self.cursor.execute('''
                SELECT Name, Position, Department, Salary, HireDate
                FROM Employees 
                WHERE Salary > ?
                ORDER BY Salary DESC
            ''', (min_salary,))
            employees = self.cursor.fetchall()
            print(f"\n💰 Сотрудники с зарплатой > ${min_salary}:")
            for emp in employees:
                print(f"  {emp[0]} - {emp[1]} - {emp[2]} - ${emp[3]} - {emp[4]}")
            return employees
        except sqlite3.Error as e:
            print(f"❌ Ошибка при поиске сотрудников: {e}")
            return []
        finally:
            self.close()

    def find_sales_department(self):
        """Поиск сотрудников отдела Sales"""
        self.connect()
        try:
            self.cursor.execute('''
                SELECT Name, Position, Salary, HireDate 
                FROM Employees 
                WHERE Department = 'Sales'
                ORDER BY Salary DESC
            ''')
            employees = self.cursor.fetchall()
            print("\n🛍️ Сотрудники отдела Sales:")
            for emp in employees:
                print(f"  {emp[0]} - {emp[1]} - ${emp[2]} - {emp[3]}")
            return employees
        except sqlite3.Error as e:
            print(f"❌ Ошибка при поиске сотрудников Sales: {e}")
            return []
        finally:
            self.close()

    def calculate_avg_salary(self):
        """Расчет средней зарплаты"""
        self.connect()
        try:
            self.cursor.execute('SELECT AVG(Salary) FROM Employees')
            avg_salary = self.cursor.fetchone()[0]
            print(f"\n📈 Средняя зарплата по компании: ${avg_salary:.2f}")
            return avg_salary
        except sqlite3.Error as e:
            print(f"❌ Ошибка при расчете средней зарплаты: {e}")
            return 0
        finally:
            self.close()

    # Методы для сложных запросов (аналог хранимых функций)
    def get_employees_by_position(self, position_filter):
        """Аналог хранимой функции - поиск по должности"""
        self.connect()
        try:
            self.cursor.execute('''
                SELECT Name, Department, Salary, HireDate 
                FROM Employees 
                WHERE Position = ?
                ORDER BY Salary DESC
            ''', (position_filter,))
            employees = self.cursor.fetchall()
            return employees
        except sqlite3.Error as e:
            print(f"❌ Ошибка при поиске по должности: {e}")
            return []
        finally:
            self.close()

    def get_high_salary_employees(self, min_salary):
        """Аналог хранимой функции - сотрудники с высокой зарплатой"""
        self.connect()
        try:
            self.cursor.execute('''
                SELECT Name, Position, Department, Salary, HireDate
                FROM Employees 
                WHERE Salary > ?
                ORDER BY Salary DESC
            ''', (min_salary,))
            employees = self.cursor.fetchall()
            return employees
        except sqlite3.Error as e:
            print(f"❌ Ошибка при поиске высокооплачиваемых: {e}")
            return []
        finally:
            self.close()

    def get_department_employees(self, dept_name):
        """Аналог хранимой функции - сотрудники отдела"""
        self.connect()
        try:
            self.cursor.execute('''
                SELECT Name, Position, Salary, HireDate 
                FROM Employees 
                WHERE Department = ?
                ORDER BY Salary DESC
            ''', (dept_name,))
            employees = self.cursor.fetchall()
            return employees
        except sqlite3.Error as e:
            print(f"❌ Ошибка при поиске по отделу: {e}")
            return []
        finally:
            self.close()

    def get_department_avg_salary(self, dept_name):
        """Аналог хранимой функции - средняя зарплата по отделу"""
        self.connect()
        try:
            self.cursor.execute('''
                SELECT AVG(Salary) FROM Employees WHERE Department = ?
            ''', (dept_name,))
            result = self.cursor.fetchone()
            return result[0] if result[0] else 0
        except sqlite3.Error as e:
            print(f"❌ Ошибка при расчете средней зарплаты отдела: {e}")
            return 0
        finally:
            self.close()

    def use_advanced_queries(self):
        """Использование сложных запросов (аналог хранимых функций)"""
        try:
            print("\n=== СЛОЖНЫЕ ЗАПРОСЫ (АНАЛОГ ХРАНИМЫХ ФУНКЦИЙ) ===")

            # Менеджеры
            print("\n📊 Менеджеры ):")
            managers = self.get_employees_by_position('Manager')
            for manager in managers:
                print(f"  {manager[0]} - {manager[1]} - ${manager[2]} - {manager[3]}")

            # Высокие зарплаты
            print(f"\n💰 Сотрудники с зарплатой > $5500 :")
            high_salary = self.get_high_salary_employees(5500)
            for emp in high_salary:
                print(f"  {emp[0]} - {emp[1]} - {emp[2]} - ${emp[3]} - {emp[4]}")

            # Отдел IT
            print(f"\n💻 Сотрудники отдела IT :")
            it_employees = self.get_department_employees('IT')
            for emp in it_employees:
                print(f"  {emp[0]} - {emp[1]} - ${emp[2]} - {emp[3]}")

            # Средняя зарплата по отделам
            print(f"\n📈 Средние зарплаты по отделам :")
            departments = ['Sales', 'IT', 'HR', 'Finance', 'Marketing']
            for dept in departments:
                avg_salary = self.get_department_avg_salary(dept)
                if avg_salary:
                    print(f"  {dept}: ${avg_salary:.2f}")

        except Exception as e:
            print(f"❌ Ошибка при выполнении сложных запросов: {e}")

    def drop_table(self):
        """Удаление таблицы"""
        self.connect()
        try:
            self.cursor.execute('DROP TABLE IF EXISTS Employees')
            self.conn.commit()
            print("✅ Таблица 'Employees' удалена")
        except sqlite3.Error as e:
            print(f"❌ Ошибка при удалении таблицы: {e}")
        finally:
            self.close()


def main():
    """Основная функция программы"""
    db = EmployeeDB()

    print("=== УПРАВЛЕНИЕ БАЗОЙ ДАННЫХ СОТРУДНИКОВ ===")

    while True:
        print("\n" + "=" * 50)
        print("1. Создать таблицу")
        print("2. Добавить сотрудников")
        print("3. Изменить должность сотрудника")
        print("4. Добавить поле HireDate")
        print("5. Добавить даты приема на работу")
        print("6. Найти менеджеров")
        print("7. Найти сотрудников с зарплатой > $5000")
        print("8. Найти сотрудников отдела Sales")
        print("9. Найти среднюю зарплату")
        print("10. Сложные запросы (аналог хранимых функций)")
        print("11. Удалить таблицу")
        print("12. Выйти")
        print("=" * 50)

        choice = input("Выберите действие (1-12): ")

        if choice == '1':
            db.create_table()
        elif choice == '2':
            db.insert_employees()
        elif choice == '3':
            name = input("Введите имя сотрудника: ")
            position = input("Введите новую должность: ")
            db.update_employee_position(name, position)
        elif choice == '4':
            db.add_hire_date_column()
        elif choice == '5':
            db.update_hire_dates()
        elif choice == '6':
            db.find_managers()
        elif choice == '7':
            db.find_high_salary_employees()
        elif choice == '8':
            db.find_sales_department()
        elif choice == '9':
            db.calculate_avg_salary()
        elif choice == '10':
            db.use_advanced_queries()
        elif choice == '11':
            db.drop_table()
        elif choice == '12':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()