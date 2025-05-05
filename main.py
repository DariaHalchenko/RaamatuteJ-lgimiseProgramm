import json
import os
from datetime import datetime
from collections import defaultdict

books = []
DATA_FILE = "raamatud.json"
STATUSES = ["Tahan lugeda", "Loen", "Lõpetatud"]

def load_data():
    global books
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                books = json.load(file)
        except json.JSONDecodeError:
            books = []
    else:
        books = []

def save_data():
    with open(DATA_FILE, 'w') as file:
        json.dump(books, file, indent=4)

def add_book():
    title = input("Sisesta raamatu pealkiri: ").strip()
    author = input("Sisesta raamatu autor: ").strip()
    if title and author:
        book = {
            "title": title,
            "author": author,
            "status": "Tahan lugeda",
            "start_date": "",
            "end_date": "",
            "total_pages": 0,
            "pages_read": 0
        }
        books.append(book)
        save_data()
        print("Raamat lisatud edukalt!")
    else:
        print("Pealkiri ja autor ei tohi olla tühjad.")

def show_books(book_list=None):
    if book_list is None:
        book_list = books
    if not book_list:
        print("Nimekirjas pole raamatuid.")
        return
    for i, book in enumerate(book_list, 1):
        print(f"{i}. Pealkiri: {book['title']}, Autor: {book['author']}, Staatus: {book['status']}")
        print(f"   Alguskuupäev: {book['start_date'] or 'Pole määratud'}, Lõppkuupäev: {book['end_date'] or 'Pole määratud'}")
        print(f"   Lehekülgi: {book['pages_read']}/{book['total_pages']}")

def change_status():
    show_books()
    if not books:
        return
    try:
        index = int(input("Sisesta raamatu number staatuse muutmiseks: ")) - 1
        if 0 <= index < len(books):
            print("Võimalikud staatused:", ", ".join(STATUSES))
            new_status = input("Sisesta uus staatus: ").strip()
            if new_status in STATUSES:
                books[index]["status"] = new_status
                save_data()
                print("Staatus uuendatud!")
            else:
                print("Vigane staatus.")
        else:
            print("Vale raamatu number.")
    except ValueError:
        print("Palun sisesta korrektne number.")

def delete_book():
    show_books()
    if not books:
        return
    try:
        index = int(input("Sisesta raamatu number kustutamiseks: ")) - 1
        if 0 <= index < len(books):
            confirm = input("Kas oled kindel, et soovid selle raamatu kustutada? (j/e): ").lower()
            if confirm == 'j':
                deleted_book = books.pop(index)
                save_data()
                print(f"Raamat '{deleted_book['title']}' kustutatud.")
            else:
                print("Kustutamine tühistatud.")
        else:
            print("Vale raamatu number.")
    except ValueError:
        print("Palun sisesta korrektne number.")

def filter_by_status():
    print("Võimalikud staatused:", ", ".join(STATUSES))
    status = input("Sisesta staatus, mille järgi filtreerida: ").strip()
    if status not in STATUSES:
        print("Vigane staatus.")
        return
    filtered_books = [book for book in books if book["status"] == status]
    if filtered_books:
        show_books(filtered_books)
    else:
        print(f"Staatusega '{status}' raamatuid ei leitud.")

def add_reading_dates():
    show_books()
    if not books:
        return
    try:
        index = int(input("Sisesta raamatu number kuupäevade lisamiseks: ")) - 1
        if 0 <= index < len(books):
            start_date = input("Sisesta alguskuupäev (PP.KK.AAAA, jäta tühjaks vahelejätmiseks): ").strip()
            if start_date:
                try:
                    datetime.strptime(start_date, "%d.%m.%Y")
                    books[index]["start_date"] = start_date
                except ValueError:
                    print("Vale kuupäeva formaat. Kuupäeva ei lisatud.")
                    return
            end_date = input("Sisesta lõppkuupäev (PP.KK.AAAA, jäta tühjaks vahelejätmiseks): ").strip()
            if end_date:
                try:
                    datetime.strptime(end_date, "%d.%m.%Y")
                    books[index]["end_date"] = end_date
                except ValueError:
                    print("Vale kuupäeva formaat. Kuupäeva ei lisatud.")
                    return
            save_data()
            print("Kuupäevad uuendatud!")
        else:
            print("Vale raamatu number.")
    except ValueError:
        print("Palun sisesta korrektne number.")

def books_read_per_month():
    monthly_counts = defaultdict(int)
    for book in books:
        if book["end_date"]:
            try:
                date = datetime.strptime(book["end_date"], "%d.%m.%Y")
                month_year = date.strftime("%B %Y")
                monthly_counts[month_year] += 1
            except ValueError:
                continue
    if monthly_counts:
        print("Loetud raamatud kuude kaupa:")
        for month, count in sorted(monthly_counts.items()):
            print(f"{month}: {count} raamat(ut)")
    else:
        print("Lõppkuupäevadega raamatuid ei leitud.")

def update_pages():
    show_books()
    if not books:
        return
    try:
        index = int(input("Sisesta raamatu number lehekülgede uuendamiseks: ")) - 1
        if 0 <= index < len(books):
            total_pages = input("Sisesta lehekülgede koguarv (jäta tühjaks vahelejätmiseks): ").strip()
            if total_pages:
                try:
                    books[index]["total_pages"] = int(total_pages)
                except ValueError:
                    print("Vigane lehekülgede arv.")
                    return
            pages_read = input("Sisesta loetud lehekülgede arv (jäta tühjaks vahelejätmiseks): ").strip()
            if pages_read:
                try:
                    read = int(pages_read)
                    if read <= books[index]["total_pages"]:
                        books[index]["pages_read"] = read
                    else:
                        print("Loetud leheküljed ei saa ületada koguarvu.")
                        return
                except ValueError:
                    print("Vigane loetud lehekülgede arv.")
                    return
            save_data()
            print("Leheküljed uuendatud!")
        else:
            print("Vale raamatu number.")
    except ValueError:
        print("Palun sisesta korrektne number.")

def search_books():
    query = input("Sisesta otsingusõna (pealkiri või autor): ").strip().lower()
    if not query:
        print("Otsingusõna ei tohi olla tühi.")
        return
    results = [
        book for book in books
        if query in book["title"].lower() or query in book["author"].lower()
    ]
    if results:
        show_books(results)
    else:
        print("Raamatuid ei leitud.")

def main_menu():
    load_data()
    while True:
        print("\n=== Raamatute Jälgija ===")
        print("1. Lisa raamat")
        print("2. Kuva kõik raamatud")
        print("3. Muuda raamatu staatust")
        print("4. Kustuta raamat")
        print("5. Filtreeri raamatud staatuse järgi")
        print("6. Lisa lugemiskuupäevad")
        print("7. Näita kuude kaupa loetud raamatuid")
        print("8. Uuenda lehekülgi")
        print("9. Otsi raamatuid")
        print("0. Välju")
        choice = input("Sisesta oma valik (0-9): ").strip()
        if choice == "1":
            add_book()
        elif choice == "2":
            show_books()
        elif choice == "3":
            change_status()
        elif choice == "4":
            delete_book()
        elif choice == "5":
            filter_by_status()
        elif choice == "6":
            add_reading_dates()
        elif choice == "7":
            books_read_per_month()
        elif choice == "8":
            update_pages()
        elif choice == "9":
            search_books()
        elif choice == "0":
            print("Head aega!")
            break
        else:
            print("Vigane valik. Proovi uuesti.")

if __name__ == "__main__":
    main_menu()