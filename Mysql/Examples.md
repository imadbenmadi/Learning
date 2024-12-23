Let's assume we have this data:

### **Employees** Table
| employee_id | name          | department_id | salary  |
|-------------|---------------|---------------|---------|
| 101         | John Doe      | 1             | 60000   |
| 102         | Jane Smith    | 2             | 80000   |
| 103         | Mike Johnson  | 2             | 75000   |
| 104         | NULL          | 3             | NULL    |

### **Departments** Table
| department_id | department_name |
|---------------|-----------------|
| 1             | HR              |
| 2             | Engineering     |
| 3             | Marketing       |
| 4             | Sales           |

### **What happens with different JOIN queries?**

#### 1. **INNER JOIN**
- Returns only rows that have matching values in both tables.
  
```sql
SELECT e.name, d.department_name
FROM Employees e
INNER JOIN Departments d ON e.department_id = d.department_id;
```

**Result:**
| name          | department_name |
|---------------|-----------------|
| John Doe      | HR              |
| Jane Smith    | Engineering     |
| Mike Johnson  | Engineering     |

- Explanation: It only returns employees who have a matching `department_id` in the `Departments` table. The `NULL` in the `name` field or non-matching department (like `Sales`) is excluded.

#### 2. **LEFT JOIN**
- Returns all rows from the left table (`Employees`) and matched rows from the right (`Departments`). Unmatched departments will be `NULL`.

```sql
SELECT e.name, d.department_name
FROM Employees e
LEFT JOIN Departments d ON e.department_id = d.department_id;
```

**Result:**
| name          | department_name |
|---------------|-----------------|
| John Doe      | HR              |
| Jane Smith    | Engineering     |
| Mike Johnson  | Engineering     |
| NULL          | Marketing       |

- Explanation: All employees are included, even if their department doesn't exist (e.g., no department for "NULL" employee). The `Marketing` employee has no corresponding name in `Employees`, but the department is shown.

#### 3. **RIGHT JOIN**
- Returns all rows from the right table (`Departments`) and matched rows from the left (`Employees`). Unmatched employees will have `NULL` in their place.

```sql
SELECT e.name, d.department_name
FROM Employees e
RIGHT JOIN Departments d ON e.department_id = d.department_id;
```

**Result:**
| name          | department_name |
|---------------|-----------------|
| John Doe      | HR              |
| Jane Smith    | Engineering     |
| Mike Johnson  | Engineering     |
| NULL          | Marketing       |
| NULL          | Sales           |

- Explanation: All departments are shown, even if there are no employees in that department. For example, `Sales` appears with no employee, and `Marketing` shows `NULL` for the employee name.

#### 4. **FULL JOIN (emulated using LEFT JOIN + UNION RIGHT JOIN)**
- Returns all rows where there is a match in either `Employees` or `Departments`.

```sql
SELECT e.name, d.department_name
FROM Employees e
LEFT JOIN Departments d ON e.department_id = d.department_id
UNION
SELECT e.name, d.department_name
FROM Employees e
RIGHT JOIN Departments d ON e.department_id = d.department_id;
```

**Result:**
| name          | department_name |
|---------------|-----------------|
| John Doe      | HR              |
| Jane Smith    | Engineering     |
| Mike Johnson  | Engineering     |
| NULL          | Marketing       |
| NULL          | Sales           |

- Explanation: This combines the results of the `LEFT JOIN` and `RIGHT JOIN`, showing all employees and all departments. Unmatched rows from either table are included.

### Summary:
- **INNER JOIN**: Only shows rows with matching `department_id` in both tables (excludes unmatched rows).
- **LEFT JOIN**: Shows all employees, even if there's no matching department (`NULL` in `department_name`).
- **RIGHT JOIN**: Shows all departments, even if there's no matching employee (`NULL` in `name`).
- **FULL JOIN** (emulated): Shows everything from both tables, filling in `NULL` for missing matches.

# **Let's expand the data to make things clearer and explain more concepts using a larger set of data.**

### **Employees** Table
| employee_id | name          | department_id | salary  |
|-------------|---------------|---------------|---------|
| 101         | John Doe      | 1             | 60000   |
| 102         | Jane Smith    | 2             | 80000   |
| 103         | Mike Johnson  | 2             | 75000   |
| 104         | Sarah Davis   | 3             | 50000   |
| 105         | Adam Brown    | 4             | 90000   |
| 106         | Linda Green   | NULL          | 65000   |
| 107         | NULL          | NULL          | NULL    |

### **Departments** Table
| department_id | department_name |
|---------------|-----------------|
| 1             | HR              |
| 2             | Engineering     |
| 3             | Marketing       |
| 4             | Sales           |
| 5             | Finance         |

---

### 1. **GROUP BY**
- Used to group rows that have the same values in specified columns and often combined with aggregate functions like `COUNT`, `SUM`, `AVG`, etc.
  
```sql
SELECT department_id, COUNT(*) AS num_employees
FROM Employees
GROUP BY department_id;
```

**Result:**
| department_id | num_employees |
|---------------|---------------|
| 1             | 1             |
| 2             | 2             |
| 3             | 1             |
| 4             | 1             |
| NULL          | 2             |

- Explanation: This query groups employees by `department_id` and counts how many employees are in each department. Notice that two employees (`Linda Green` and `NULL`) have no department (`NULL`).

---

### 2. **HAVING**
- The `HAVING` clause is like `WHERE`, but it works with aggregate functions (after `GROUP BY`).

```sql
SELECT department_id, COUNT(*) AS num_employees
FROM Employees
GROUP BY department_id
HAVING num_employees > 1;
```

**Result:**
| department_id | num_employees |
|---------------|---------------|
| 2             | 2             |
| NULL          | 2             |

- Explanation: This query groups employees by department and only shows departments that have more than 1 employee. `Engineering` and the `NULL` department meet this condition.

---

### 3. **Aggregate Functions**
- **COUNT**: Counts the number of rows.
    ```sql
    SELECT COUNT(*) FROM Employees;
    ```

    **Result:**
    | COUNT(*) |
    |----------|
    | 7        |

    - Explanation: There are 7 rows in the `Employees` table.

- **SUM**: Adds up the values in a column.
    ```sql
    SELECT SUM(salary) FROM Employees WHERE department_id = 2;
    ```

    **Result:**
    | SUM(salary) |
    |-------------|
    | 155000      |

    - Explanation: This sums the salaries of all employees in the `Engineering` department.

- **AVG**: Finds the average value.
    ```sql
    SELECT AVG(salary) FROM Employees WHERE department_id = 2;
    ```

    **Result:**
    | AVG(salary) |
    |-------------|
    | 77500       |

    - Explanation: This calculates the average salary in the `Engineering` department.

- **MIN/MAX**: Finds the minimum and maximum values in a column.
    ```sql
    SELECT MIN(salary), MAX(salary) FROM Employees;
    ```

    **Result:**
    | MIN(salary) | MAX(salary) |
    |-------------|-------------|
    | 50000       | 90000       |

    - Explanation: This shows the minimum and maximum salaries across all employees.

---

### 4. **Subqueries**
- A subquery is a query inside another query. Here's an example where we find employees who earn more than the average salary.

```sql
SELECT name, salary
FROM Employees
WHERE salary > (SELECT AVG(salary) FROM Employees);
```

**Result:**
| name         | salary |
|--------------|--------|
| Jane Smith   | 80000  |
| Adam Brown   | 90000  |

- Explanation: This subquery first calculates the average salary of all employees. Then, it returns only those employees who have a salary greater than that average.

---

### 5. **Indexes**
- Indexes speed up queries by creating a quick lookup for specific columns. For example, if you're often searching for employees by department, you can create an index on `department_id`.

```sql
CREATE INDEX idx_department ON Employees(department_id);
```

- **Explanation**: This index allows the database to find employees by `department_id` faster, especially useful when the table grows larger.

---

### 6. **Foreign Keys**
- A foreign key ensures that the `department_id` in `Employees` must exist in the `Departments` table. This maintains referential integrity.

```sql
ALTER TABLE Employees
ADD CONSTRAINT fk_department
FOREIGN KEY (department_id) REFERENCES Departments(department_id);
```

- **Explanation**: After adding this foreign key, you cannot insert an employee with a `department_id` that doesn't exist in the `Departments` table.

---

### 7. **Transactions**
- Transactions ensure that multiple queries are executed as a single unit. If something fails, you can roll back the changes.

```sql
START TRANSACTION;

UPDATE Employees SET salary = salary * 1.1 WHERE department_id = 2;
DELETE FROM Employees WHERE employee_id = 107;

COMMIT;
```

- **Explanation**: This transaction updates all salaries in the `Engineering` department and deletes an employee with `employee_id = 107`. If both actions succeed, the changes are committed. If something goes wrong, you can issue a `ROLLBACK` to undo the changes.

---

### 8. **UNION**
- `UNION` combines results from multiple `SELECT` queries. Both queries must have the same number of columns and data types.

```sql
SELECT name FROM Employees WHERE department_id = 1
UNION
SELECT name FROM Employees WHERE salary > 70000;
```

**Result:**
| name         |
|--------------|
| John Doe     |
| Jane Smith   |
| Mike Johnson |
| Adam Brown   |

- **Explanation**: This query first selects employees from the `HR` department, then adds employees with a salary greater than 70,000, without duplicates.

---

### 9. **Triggers**
- Triggers automatically perform actions when a specified event occurs, such as before or after inserting, updating, or deleting a row.

```sql
CREATE TRIGGER salary_before_update
BEFORE UPDATE ON Employees
FOR EACH ROW
SET NEW.salary = NEW.salary + 5000;
```

- **Explanation**: This trigger automatically increases an employee’s salary by 5,000 before any update to their salary.

---

### 10. **Views**
- A view is a virtual table based on the result of a `SELECT` query. It's useful for creating simplified or specific data views.

```sql
CREATE VIEW high_earning_employees AS
SELECT name, salary
FROM Employees
WHERE salary > 70000;
```

- **Explanation**: This view allows you to quickly access a list of high-earning employees without writing the full query every time.

---

### Complex Query Example:
```sql
SELECT d.department_name, COUNT(e.employee_id) AS total_employees, AVG(e.salary) AS average_salary
FROM Employees e
INNER JOIN Departments d ON e.department_id = d.department_id
GROUP BY d.department_name
HAVING AVG(e.salary) > 60000
ORDER BY total_employees DESC;
```

**Result:**
| department_name | total_employees | average_salary |
|-----------------|-----------------|----------------|
| Engineering     | 2               | 77500          |
| Sales           | 1               | 90000          |

- **Explanation**: This complex query:
  - Joins `Employees` and `Departments`.
  - Groups by `department_name`.
  - Filters only departments where the average salary is greater than 60,000.
  - Sorts the result by the number of employees in descending order.

---

This larger dataset and these more complex examples should give you a clearer idea of how these MySQL concepts work in practice. Let me know if you need more clarification on any of them!
