### **UNION in SQL**

`UNION` is used to **combine results** from multiple `SELECT` queries into a **single result set**, removing duplicates.

🔹 **Syntax:**

```sql
SELECT column1, column2 FROM Table1
UNION
SELECT column1, column2 FROM Table2;
```

🔹 **Key Rules:**

-   Both `SELECT` queries **must have the same number of columns**.
-   The column **data types must match**.
-   Removes **duplicates** by default.

---

### **Example:**

#### 🏠 `Users` Table

| id  | name |
| --- | ---- |
| 1   | Ali  |
| 2   | Omar |

#### 🎓 `Students` Table

| id  | name  |
| --- | ----- |
| 2   | Omar  |
| 3   | Sarah |

#### **Query using `UNION`**

```sql
SELECT name FROM Users
UNION
SELECT name FROM Students;
```

#### **Result:**

| name  |
| ----- |
| Ali   |
| Omar  |
| Sarah |

🚀 **Omar appears only once because `UNION` removes duplicates!**

---

### **`UNION ALL` (Keeps Duplicates)**

If you want **all records (including duplicates)**, use `UNION ALL`:

```sql
SELECT name FROM Users
UNION ALL
SELECT name FROM Students;
```

**Result:**  
| name |  
|------|  
| Ali |  
| Omar |  
| Omar |  
| Sarah |

---

### **UNION in Sequelize (Raw Query)**

Sequelize doesn’t have a built-in `UNION` method, but you can use raw queries:

```js
sequelize
    .query(
        `
  SELECT name FROM Users  
  UNION  
  SELECT name FROM Students
`,
        { type: sequelize.QueryTypes.SELECT }
    )
    .then((data) => console.log(data));
```

📌 **Use Case:** When you need to merge results from different tables but don’t want duplicates.

Let me know if you need more details, bro! 🚀
