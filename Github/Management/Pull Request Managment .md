Good question! A **Pull Request (PR)** is **not the same as merging**—it’s basically a **request** to merge code, usually needing review before the actual merge happens.

---

### **What is a Pull Request (PR)?**  
A **Pull Request** is a **way to propose changes** before merging them into another branch (like `master`). It's mostly used in **team projects** to:  
✅ **Get code reviewed** by teammates.  
✅ **Run automated tests (CI/CD checks).**  
✅ **Prevent bad code from getting merged.**  

💡 In big companies, **developers create PRs, and team leads, senior devs, or admins review and approve before merging.**  

---

### **How a PR Works in GitHub/GitLab/Bitbucket**  
1️⃣ **A dev finishes a feature** in `sub2` and pushes it to GitHub:  
   ```sh
   git push origin sub2
   ```

2️⃣ **They open a Pull Request** in GitHub (or GitLab, Bitbucket, etc.):  
   - Select **`sub2` → `master`** as the merge target.  
   - Write a description of the changes.  
   - Request reviewers (team members or admins).  

3️⃣ **Team Reviews the Code**  
   - Other devs or admins check for **bugs, bad code, missing tests, etc.**  
   - If needed, the author **fixes issues and pushes updates** to the PR.  

4️⃣ **If Approved → The PR is Merged**  
   - Either the **admin merges it**, or GitHub allows the dev to merge it themselves.  
   - Some teams use **auto-merge** after all checks pass.  

5️⃣ **PR is Closed & `sub2` is Deleted (Optional)**  
   - After merging, the branch `sub2` is usually deleted to keep the repo clean.  

---

### **Who Actually Merges the PR?**
🔹 **Small Teams:** The developer merges after approval.  
🔹 **Medium Teams:** A team lead reviews & merges.  
🔹 **Big Companies:**  
   - Merging might be restricted to **admins, senior devs, or DevOps.**  
   - **CI/CD must pass** before merging is allowed.  

---

### **So, PR = Request, Merge = Action**
🔹 **PR = "Hey team, can you check my code before we add it to `master`?"**  
🔹 **Merge = The actual process of combining the code.**  

Let me know if you need help setting up a real PR workflow! 🚀