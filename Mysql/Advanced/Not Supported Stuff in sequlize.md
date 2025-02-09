Sequelize is powerful, but it doesn't support everything in SQL. Here are some **limitations** where you might need **raw SQL** instead:

---

### **🚫 1. Complex SQL Queries (CTEs, Recursive Queries)**

-   Sequelize **doesn’t natively support** Common Table Expressions (CTEs) or recursive queries.
-   Example: **WITH RECURSIVE** for hierarchical data (e.g., categories, org charts).

✅ **Workaround:** Use **raw SQL**

```javascript
await sequelize.query(`
  WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id FROM categories WHERE id = 1
    UNION ALL
    SELECT c.id, c.name, c.parent_id FROM categories c
    JOIN category_tree ct ON ct.id = c.parent_id
  ) SELECT * FROM category_tree;
`);
```

---

### **🚫 2. Stored Procedures & Functions**

-   You **can call** stored procedures using raw SQL, but Sequelize **can’t define** them directly.

✅ **Workaround:** Define procedures in SQL, then call them in Sequelize.

```javascript
await sequelize.query("CALL my_stored_procedure(:param1, :param2)", {
    replacements: { param1: value1, param2: value2 },
});
```

---

### **🚫 3. Triggers**

-   Sequelize **doesn't support** database triggers (e.g., auto-update timestamps across related tables).

✅ **Workaround:** Manually create triggers in SQL.

---

### **🚫 4. Full-Text Search (LIMITED)**

-   **Basic searching (`LIKE` & `ILIKE`)** works, but **full-text search (`MATCH AGAINST`)** isn’t fully supported.

✅ **Workaround:** Use **raw SQL** for full-text search in MySQL/PostgreSQL.

```javascript
await sequelize.query(
    "SELECT * FROM articles WHERE MATCH(title, content) AGAINST(:query IN NATURAL LANGUAGE MODE)",
    { replacements: { query: "Sequelize" }, type: QueryTypes.SELECT }
);
```

---

### **🚫 5. Advanced Indexing (Partial Indexes, Function-Based Indexes)**

-   You **can’t define advanced indexes** like:
    -   Partial indexes (e.g., indexing only rows where `status = 'active'`).
    -   Function-based indexes (`INDEX ON LOWER(email)`).

✅ **Workaround:** Create them manually in SQL.

---

### **🚫 6. Lateral Joins (`LATERAL`)**

-   Sequelize supports **basic joins**, but **lateral joins** (needed for subqueries within joins) **aren’t natively supported**.

✅ **Workaround:** Use **raw SQL** for performance-heavy subquery joins.

---

### **🚫 7. Table Inheritance (PostgreSQL `INHERITS`)**

-   Sequelize **doesn’t support table inheritance**, which is useful for defining common structures across multiple tables in PostgreSQL.

✅ **Workaround:** Use raw SQL for creating inherited tables.

---

### **🚫 8. Fine-Tuned Performance Optimizations**

-   Complex **query hints**, **parallel queries**, and **optimizer tweaks** aren’t supported.

✅ **Workaround:** Run raw SQL where needed.

---

### **🔥 Final Verdict**

Sequelize is great **90% of the time**, but for:

-   **Complex queries (CTEs, recursive, lateral joins)**
-   **Stored procedures & triggers**
-   **Advanced indexing & full-text search**
-   **High-performance SQL optimizations**

👉 **Raw SQL is better**.

If you're working with high-performance apps, sometimes **mixing Sequelize & raw SQL** is the best approach. 🚀
