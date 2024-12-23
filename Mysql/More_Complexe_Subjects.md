
### 1. **Window Functions**
Window functions allow you to perform calculations across a set of rows related to the current row, without collapsing the result like with `GROUP BY`.

Examples include:
- **ROW_NUMBER()**: Assigns a unique number to each row within a partition of a result set.
- **RANK()**: Assigns a rank to each row within a partition, but handles ties differently.
- **LEAD/LAG()**: Returns values from subsequent or previous rows, which is great for comparisons between rows.

**Example**:
```sql
SELECT name, salary, department_id,
       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rank
FROM Employees;
```

This ranks employees by salary within their department.

---

### 2. **Common Table Expressions (CTEs)**
A **CTE** provides a way to organize complex queries by allowing you to define a temporary result set, which can be referenced later in the query. It's often used to improve readability and manageability of queries.

**Example**:
```sql
WITH DepartmentSalaries AS (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM Employees
    GROUP BY department_id
)
SELECT e.name, e.salary, ds.avg_salary
FROM Employees e
JOIN DepartmentSalaries ds ON e.department_id = ds.department_id
WHERE e.salary > ds.avg_salary;
```

This query first calculates the average salary by department (in the CTE), and then uses it to find employees who earn more than their department’s average.

---

### 3. **Recursive CTEs**
Useful for handling **hierarchical data**, such as employees with managers.

**Example** (assume `Managers` table tracks who manages who):
```sql
WITH RECURSIVE EmployeeHierarchy AS (
    SELECT employee_id, name, manager_id
    FROM Employees
    WHERE manager_id IS NULL
    UNION
    SELECT e.employee_id, e.name, e.manager_id
    FROM Employees e
    JOIN EmployeeHierarchy eh ON e.manager_id = eh.employee_id
)
SELECT * FROM EmployeeHierarchy;
```

This recursively traverses an employee hierarchy, showing which employees report to whom.

---

### 4. **Stored Procedures**
Stored procedures allow you to create reusable SQL code. They can take input parameters and return data, making them very useful for complex operations or tasks that need to be performed repeatedly.

**Example**:
```sql
CREATE PROCEDURE GetEmployeesByDepartment(IN dept_id INT)
BEGIN
    SELECT * FROM Employees WHERE department_id = dept_id;
END;
```

You can then call the procedure:
```sql
CALL GetEmployeesByDepartment(2);
```

---

### 5. **User-Defined Functions (UDFs)**
While MySQL provides many built-in functions, you can define your own functions to perform custom calculations.

**Example**:
```sql
CREATE FUNCTION CalculateBonus(salary DECIMAL(10, 2))
RETURNS DECIMAL(10, 2)
BEGIN
    RETURN salary * 0.10;
END;
```

You can now use `CalculateBonus()` in queries:
```sql
SELECT name, salary, CalculateBonus(salary) AS bonus
FROM Employees;
```

---

### 6. **Advanced Indexing**
In addition to basic indexing, MySQL offers more specialized indexes:
- **Full-text Indexes**: Useful for searching large text fields (like articles).
    ```sql
    CREATE FULLTEXT INDEX idx_fulltext ON Articles(content);
    ```
- **Spatial Indexes**: For handling geographic data (e.g., latitude, longitude) using MySQL’s spatial extensions.

---

### 7. **Partitioning**
Partitioning allows you to split a large table into smaller, more manageable pieces. This can greatly improve query performance for very large datasets.

**Example**:
```sql
CREATE TABLE Employees (
    employee_id INT,
    name VARCHAR(100),
    department_id INT,
    salary DECIMAL(10, 2),
    hire_date DATE
)
PARTITION BY RANGE (YEAR(hire_date)) (
    PARTITION p0 VALUES LESS THAN (2010),
    PARTITION p1 VALUES LESS THAN (2020),
    PARTITION p2 VALUES LESS THAN MAXVALUE
);
```

This partitions the `Employees` table by hire year.

---

### 8. **Replication**
Replication allows you to create copies of your database on multiple servers to improve redundancy and read performance.
- **Master-Slave Replication**: One master server handles writes, and one or more slave servers handle reads.
- **Master-Master Replication**: Both servers can handle writes.

MySQL replication is configured at the server level, using commands like `CHANGE MASTER TO` and `START SLAVE`.

---

### 9. **Sharding**
Sharding involves splitting your data across multiple servers (horizontal partitioning). It's different from replication and is typically used for very large-scale applications where a single database can't handle the load.

While MySQL doesn’t natively support sharding, it can be implemented manually at the application level or with tools like **Vitess**.

---

### 10. **JSON Functions and Data Types**
MySQL supports JSON data types, making it easier to store and query semi-structured data.

**Example**:
```sql
CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    attributes JSON
);
```

You can then query the JSON fields using MySQL’s built-in functions:
```sql
SELECT product_id, JSON_EXTRACT(attributes, '$.color') AS color
FROM Products;
```

This extracts the `color` field from the `attributes` JSON column.

---

### 11. **Advanced Locking**
- **Table Locks**: Lock the entire table during a transaction.
- **Row-Level Locks**: Only lock specific rows.

You can also explicitly lock rows to prevent dirty reads or lost updates.

**Example**:
```sql
LOCK TABLES Employees WRITE;
-- Run queries here
UNLOCK TABLES;
```

---

### 12. **Concurrency Control with Isolation Levels**
You can control how transactions interact with each other using different isolation levels:
- **READ UNCOMMITTED**: Allows dirty reads (reading data from uncommitted transactions).
- **READ COMMITTED**: Prevents dirty reads.
- **REPEATABLE READ**: Ensures that repeated reads return the same data.
- **SERIALIZABLE**: The strictest isolation, ensuring transactions occur in a strictly sequential manner.

**Example** (setting isolation level):
```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
```

---

### 13. **Event Scheduler**
The event scheduler allows you to run SQL tasks at scheduled times, similar to **cron jobs** in Unix.

**Example**:
```sql
CREATE EVENT daily_salary_increase
ON SCHEDULE EVERY 1 DAY
DO
   UPDATE Employees SET salary = salary * 1.01;
```

This event increases all salaries by 1% every day.

---

### 14. **Horizontal Scaling (Federation)**
Federation allows MySQL servers to distribute data across multiple physical servers while maintaining the same schema. MySQL doesn’t natively support this, but tools like **ProxySQL** and **Vitess** help manage large-scale databases across many servers.

---

### 15. **Security and Permissions**
MySQL offers fine-grained control over user permissions with the `GRANT` and `REVOKE` commands. You can specify exactly which users can perform which operations on specific tables, databases, or even columns.

**Example**:
```sql
GRANT SELECT, INSERT ON Employees TO 'user1'@'localhost';
```

This gives `user1` permission to `SELECT` and `INSERT` on the `Employees` table.

---

### 16. **Materialized Views**
Unlike standard views, materialized views store the query result physically and can be refreshed periodically. MySQL doesn’t natively support materialized views, but you can emulate them by creating a table that stores the results of a query and updating it regularly.

---

### Advanced Query Optimization:
1. **Explain Plans**: You can use `EXPLAIN` to understand how MySQL executes a query and identify potential optimizations.
    ```sql
    EXPLAIN SELECT * FROM Employees WHERE department_id = 2;
    ```

2. **Optimizer Hints**: You can guide MySQL’s query optimizer with hints like `USE INDEX`, `IGNORE INDEX`, and `FORCE INDEX` to speed up certain queries.

---

### Summary
While the concepts you’ve learned (joins, aggregates, subqueries, transactions, etc.) form the core of SQL, MySQL has **many more advanced features**. These include window functions, CTEs, recursive queries, stored procedures, triggers, JSON support, indexing strategies, and scalability options like replication, sharding, and partitioning.

As your needs grow, so does the complexity of your SQL usage. You can achieve powerful results by **combining these basic and advanced techniques** depending on the problem you're solving.
