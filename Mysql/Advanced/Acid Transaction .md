### **Using Transactions in Sequelize**

#### **1️⃣ Auto-Managed Transaction (Simple Way)**

Sequelize automatically commits or rolls back the transaction based on success or failure.

```javascript
const { Sequelize } = require("sequelize");
const sequelize = new Sequelize("database", "user", "password", {
    dialect: "mysql",
});

async function transferFunds(fromUserId, toUserId, amount) {
    await sequelize.transaction(async (t) => {
        const fromUser = await User.findByPk(fromUserId, { transaction: t });
        const toUser = await User.findByPk(toUserId, { transaction: t });

        if (!fromUser || !toUser || fromUser.balance < amount) {
            throw new Error("Transaction failed");
        }

        await fromUser.update(
            { balance: fromUser.balance - amount },
            { transaction: t }
        );
        await toUser.update(
            { balance: toUser.balance + amount },
            { transaction: t }
        );
    });
}
```

✅ **Why use this?**

-   No need to manually commit or rollback.
-   If an error occurs, Sequelize automatically rolls back the transaction.

---

#### **2️⃣ Manually Managed Transaction (More Control)**

If you need more control over commits and rollbacks:

```javascript
async function transferFunds(fromUserId, toUserId, amount) {
    const t = await sequelize.transaction(); // Start transaction
    try {
        const fromUser = await User.findByPk(fromUserId, { transaction: t });
        const toUser = await User.findByPk(toUserId, { transaction: t });

        if (!fromUser || !toUser || fromUser.balance < amount) {
            throw new Error("Transaction failed");
        }

        await fromUser.update(
            { balance: fromUser.balance - amount },
            { transaction: t }
        );
        await toUser.update(
            { balance: toUser.balance + amount },
            { transaction: t }
        );

        await t.commit(); // Commit if everything is okay
    } catch (error) {
        await t.rollback(); // Rollback if something goes wrong
        throw error;
    }
}
```

✅ **Why use this?**

-   Gives **more flexibility** to handle complex scenarios.
-   You can **decide when to commit or rollback** manually.

---

### **Does Sequelize Handle ACID Transactions Well?**

✅ **Yes!** Sequelize transactions fully support ACID:

-   **Atomicity:** If one query fails, everything is rolled back.
-   **Consistency:** The database remains in a valid state after a transaction.
-   **Isolation:** Each transaction runs separately (you can even set isolation levels).
-   **Durability:** Once committed, data changes are permanent.

### **Should You Use Sequelize Transactions Instead of Raw SQL?**

-   **Yes**, because it keeps your code clean and ORM-driven.
-   But **raw SQL is sometimes faster** for bulk operations.

---

### **Final Thoughts**

Sequelize **handles ACID transactions well**, and you **don’t need raw SQL** for most cases. Use **auto-managed transactions** for simple cases and **manually managed transactions** for complex scenarios. 🚀
