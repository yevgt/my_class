# Console application for searching movies in Sakila database

## 📌 Project Description
The console application is designed to search for movies in the **Sakila** database.
The project allows users to find movies by keywords, genres and year of release.
In addition, the application saves search queries and provides the ability to see the most popular queries.

## 🎯 Project goal
- Implement a convenient tool for searching movies in the **Sakila** database.
- Allow users to find movies by keyword (10+ results).
- Filter movies by genre and year (10+ results).
- Display a list of the most popular queries.

## 🛠 Establishing a connection to the database

### 1️⃣ Сonnection MySQL Server
Connect to the **Sakila** database.
use sakila; 

### 2️⃣  Setting up connection configuration
Create a .env or config.py file with database connection parameters:

python
CONFIG = {
'host': 'localhost',
'user': 'root',
'password': 'your_password',
'database': 'sakila'
}

Final structure of the project:
movie_app/
├── main.py             # entry point, menu launch
├── db.py               # working with the database, connecting, initializing, saving queries
├── models.py           # data models
├── search.py           ​​# search logic, output, working with queries
├── utils.py            # beautiful output
├── menu.py             # main menu
├── menu_search.py      ​​# additional menu
└── valid_years.py      # year validity

### 🚀 Available commands
The application works interactively through the console..

Main commands:

-- Search by movie title

Enter keyword:

Output: List of found movies.

- Search by genre

Enter genre name:

Output: List of movies of this genre.

- Search by year

Enter year:

Output: Movies released in the specified year.

- Display popular queries

Enter command:

Output: most frequent queries.

Exit the program
Enter command: exit

### 📌 Example of use

$ python main.py

Select query number:
1. Search by part of title (10+ results)
2. Search by genre (10+ results)
3. Display popular queries
0. Exit

> Enter keyword: "Ava"
Output:

Movies matching keyword 'Ava':
╒═════╤═══════════════╤════════════════╤════════════╤══════════╤═══════════════╤══════════╤══════════════════════╤════════════════════════════════╕
│  #  │     Title     │  Release Year  │  Category  │  Length  │  Rental Rate  │  Rating  │  Rating Description  │          Description           │
╞═════╪═══════════════╪════════════════╪════════════╪══════════╪═══════════════╪══════════╪══════════════════════╪════════════════════════════════╡
│  1  │ SAVANNAH TOWN │      1998      │   Drama    │    84    │     0.99      │  PG-13   │   Parents Strongly   │   A Awe-Inspiring Tale of a    │
│     │               │                │            │          │               │          │      Cautioned       │    Astronaut And a Database    │
│     │               │                │            │          │               │          │                      │ Administrator who must Chase a │
│     │               │                │            │          │               │          │                      │  Secret Agent in The Gulf of   │
│     │               │                │            │          │               │          │                      │             Mexico             │
├─────┼───────────────┼────────────────┼────────────┼──────────┼───────────────┼──────────┼──────────────────────┼────────────────────────────────┤
│  2  │   ANYTHING    │      1999      │   Horror   │    82    │     2.99      │    R     │      Restricted      │ A Epic Story of a Pastry Chef  │
│     │   SAVANNAH    │                │            │          │               │          │                      │  And a Woman who must Chase a  │
│     │               │                │            │          │               │          │                      │  Feminist in An Abandoned Fun  │
│     │               │                │            │          │               │          │                      │             House              │
├─────┼───────────────┼────────────────┼────────────┼──────────┼───────────────┼──────────┼──────────────────────┼────────────────────────────────┤
│  3  │ KICK SAVANNAH │      1992      │   Travel   │   179    │     0.99      │  PG-13   │   Parents Strongly   │ A Emotional Drama of a Monkey  │
│     │               │                │            │          │               │          │      Cautioned       │ And a Robot who must Defeat a  │
│     │               │                │            │          │               │          │                      │     Monkey in New Orleans      │

🏆 Conclusion
This project provides a convenient tool for searching movies in the Sakila database.
Use the application for quick search, analysis of genres and years of release of movies.

🎬 Enjoy using it!
