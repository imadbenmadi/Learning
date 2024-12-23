

## SQLite Documentation Structure

### 1. **Introduction**
- Brief overview of SQLite
- Key differences between SQLite and other SQL databases (e.g., MySQL)
- Why use SQLite? (Lightweight, file-based, no server needed)

### 2. **Installation and Setup**
- Installation for different platforms (Windows, macOS, Linux)
- Using SQLite from the command line
- Integrating SQLite with Python (useful for your Flask projects)

### 3. **Basic SQLite Commands**
- **Creating a Database**:
    ```bash
    sqlite3 mydatabase.db
    ```
- **Creating a Table**:
    ```sql
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age INTEGER
    );
    ```

- **Inserting Data**:
    ```sql
    INSERT INTO users (name, email, age)
    VALUES ('John Doe', 'john@example.com', 30);
    ```

- **Querying Data**:
    ```sql
    SELECT * FROM users;
    ```

- **Updating Data**:
    ```sql
    UPDATE users
    SET age = 31
    WHERE name = 'John Doe';
    ```

- **Deleting Data**:
    ```sql
    DELETE FROM users
    WHERE id = 1;
    ```

### 4. **Advanced SQLite Features**
- **Transactions**:
    ```sql
    BEGIN TRANSACTION;
    INSERT INTO users (name, email, age) VALUES ('Alice', 'alice@example.com', 28);
    COMMIT;
    ```

- **Joins**:
    ```sql
    SELECT orders.id, users.name, orders.amount
    FROM orders
    INNER JOIN users ON orders.user_id = users.id;
    ```

- **Subqueries**:
    ```sql
    SELECT name FROM users
    WHERE age > (SELECT AVG(age) FROM users);
    ```

### 5. **Database Management**
- **Exporting Data**:
    ```bash
    .output backup.sql
    .dump
    ```
- **Importing Data**:
    ```bash
    .read backup.sql
    ```

- **Backing Up a Database**:
    ```bash
    sqlite3 mydatabase.db ".backup backup.db"
    ```

### 6. **SQLite Functions**
- **Date and Time**:
    ```sql
    SELECT date('now'), datetime('now'), strftime('%Y-%m-%d', 'now');
    ```

- **String Manipulation**:
    ```sql
    SELECT UPPER(name), LENGTH(email) FROM users;
    ```

- **Aggregate Functions**:
    ```sql
    SELECT COUNT(*), AVG(age) FROM users;
    ```

### 7. **Performance Tips**
- Using indexes:
    ```sql
    CREATE INDEX idx_users_email ON users(email);
    ```
- Analyzing queries:
    ```sql
    EXPLAIN QUERY PLAN
    SELECT * FROM users WHERE email = 'john@example.com';
    ```

### 8. **SQLite with Python (Flask Integration)**
A quick example of connecting SQLite with Flask:
```python
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/users')
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

if __name__ == '__main__':
    app.run(debug=True)
```

### 9. **SQLite Limitations**
- No built-in user management (handled at the application level)
- Limited concurrent write access
- Limited to certain SQL features (e.g., no RIGHT JOIN or FULL OUTER JOIN)

### 10. **Resources and Further Reading**
- [Official SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLite Cheat Sheet](https://www.sqlite.org/cli.html)
- [Flask with SQLite Tutorial](https://flask.palletsprojects.com/en/2.3.x/tutorial/database/)

---

**deep dive into advanced SQLite topics** and use **Flask integration**, let's focus on the following areas:

1. **Advanced SQLite Concepts**
2. **Performance Optimization Techniques**
3. **SQLite Integration with Flask (Deep Dive)**
4. **Concurrency and Multi-threading in SQLite**
5. **Using SQLite Extensions and Virtual Tables**
6. **Handling Complex Queries and Subqueries**
7. **Best Practices for Production Use with Flask**

Let's get started.

## 1. **Advanced SQLite Concepts**

### 1.1. **Foreign Key Constraints**
SQLite supports foreign key constraints, but they are disabled by default. You need to enable them manually.

**Enable Foreign Keys:**
```sql
PRAGMA foreign_keys = ON;
```

**Example Table with Foreign Keys:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 1.2. **Triggers**
Triggers are used to automatically execute a SQL statement when a specified event occurs.

**Example Trigger:**
```sql
CREATE TRIGGER update_timestamp
AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

### 1.3. **Common Table Expressions (CTEs)**
CTEs make complex queries more readable.

**Example Using CTE:**
```sql
WITH user_orders AS (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
)
SELECT users.name, user_orders.order_count
FROM users
JOIN user_orders ON users.id = user_orders.user_id;
```

### 1.4. **Window Functions**
Window functions allow you to perform calculations across a set of table rows.

**Example Using Window Function:**
```sql
SELECT name, age, AVG(age) OVER() as avg_age
FROM users;
```

---

## 2. **Performance Optimization Techniques**

### 2.1. **Using Indexes Effectively**
Indexes can speed up query performance but may slow down write operations.

**Creating an Index:**
```sql
CREATE INDEX idx_users_name ON users(name);
```

**Check Index Usage:**
```sql
EXPLAIN QUERY PLAN
SELECT * FROM users WHERE name = 'Alice';
```

### 2.2. **Using `PRAGMA` Statements for Optimization**
- **Analyze Indexes:**
    ```sql
    PRAGMA analysis_limit = 1000;
    PRAGMA optimize;
    ```

- **Page Size and Cache Size:**
    ```sql
    PRAGMA page_size = 4096;
    PRAGMA cache_size = 10000;
    ```

### 2.3. **Using `VACUUM` for Database Maintenance**
Running `VACUUM` reorganizes the database and reduces its size.
```sql
VACUUM;
```

---

## 3. **SQLite Integration with Flask (Deep Dive)**

Let’s build a more advanced Flask application that includes:

- Database initialization
- Data models using SQLite
- CRUD API routes with Flask
- Error handling and database connection management

### 3.1. **Flask Application Setup**

```python
from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)
DATABASE = 'mydatabase.db'

# Database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

# Initialize database
def init_db():
    with app.app_context():
        db = get_db()
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())
        print("Database initialized.")

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404
```

### 3.2. **Schema Definition (schema.sql)**
```sql
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 3.3. **CRUD Routes**
```python
# Create user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    db = get_db()
    db.execute('INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
               (data['name'], data['email'], data['age']))
    db.commit()
    return jsonify({"message": "User created"}), 201

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    return jsonify([dict(user) for user in users])

# Update user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    db = get_db()
    db.execute('UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?',
               (data['name'], data['email'], data['age'], id))
    db.commit()
    return jsonify({"message": "User updated"})

# Delete user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (id,))
    db.commit()
    return jsonify({"message": "User deleted"})
```

---

## 4. **Concurrency and Multi-threading in SQLite**

SQLite is thread-safe and can handle concurrent reads, but concurrent writes are limited. To enable multi-threading:

**Enable Multi-threading:**
```python
import sqlite3

conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
```

### 4.1. **Using Write-Ahead Logging (WAL) for Concurrency**
```sql
PRAGMA journal_mode = WAL;
```

This allows concurrent reads while a write operation is in progress.

---

## 5. **SQLite Extensions and Virtual Tables**

### 5.1. **Using FTS5 for Full-Text Search**
Full-Text Search (FTS5) is a built-in SQLite extension for efficient text searches.

**Create FTS5 Table:**
```sql
CREATE VIRTUAL TABLE documents USING fts5(title, content);
```

**Search Example:**
```sql
SELECT * FROM documents WHERE documents MATCH 'search query';
```

### 5.2. **JSON Support in SQLite**
SQLite has native support for JSON functions.

**Example:**
```sql
CREATE TABLE json_data (data JSON);
INSERT INTO json_data (data) VALUES ('{"name": "Alice", "age": 30}');
SELECT json_extract(data, '$.name') FROM json_data;
```

---

## 6. **Best Practices for Production Use with Flask**
- Use `g` for managing database connections in Flask.
- Enable `PRAGMA foreign_keys = ON` for data integrity.
- Regularly backup the database using `.backup` command.
- Use `WAL` mode for better concurrency handling.
- Monitor query performance with `EXPLAIN QUERY PLAN`.

---
