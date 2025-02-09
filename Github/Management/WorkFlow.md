Yeah bro, let’s go step by step through the **entire Git workflow**, from creating branches to merging via pull requests.  

---

## **🚀 Step-by-Step Git Workflow in a Team**

Let’s say you're working on a **feature** (`sub-branch`) and need to merge it into `master`. Here’s the full process:

---

### **1️⃣ Clone the Repository (Only for First Time)**
If you don’t have the repo yet, clone it:  
```sh
git clone <repo-link>
cd <repo-name>
```

If you already have it, just make sure you’re on the latest `master`:
```sh
git checkout master
git pull origin master
```
☑️ This ensures you’re working on the latest version.

---

### **2️⃣ Create a New Branch for Your Feature**
```sh
git checkout -b feature-branch
```
☑️ This creates a new branch (`feature-branch`) and switches to it.

---

### **3️⃣ Work on Your Code & Save Changes**
After modifying files, check what you changed:
```sh
git status
```

To stage the changes:
```sh
git add .
```

Commit with a message:
```sh
git commit -m "Added new feature"
```

---

### **4️⃣ Push Your Branch to GitHub**
```sh
git push origin feature-branch
```
☑️ This uploads your branch to GitHub so others can see it.

---

### **5️⃣ Open a Pull Request (PR) on GitHub**
1. Go to **GitHub → Your Repo**  
2. Click **"Compare & Pull Request"**  
3. Select:
   - **Base branch:** `master`
   - **Compare branch:** `feature-branch`
4. Add a description of your changes.  
5. Request a **review from teammates** or admin.

---

### **6️⃣ Review Process (Admin or Team Checks Your Code)**
✅ If everything is good, they **approve the PR**.  
❌ If changes are needed, they **comment** and you fix the issues:  
   - Edit the files locally.  
   - Run:
     ```sh
     git add .
     git commit -m "Fixed requested changes"
     git push origin feature-branch
     ```
   - The PR **updates automatically**.

---

### **7️⃣ Merge the PR**
Once approved, you can **merge it into `master`**:
- Click **"Merge Pull Request"** on GitHub.  
- OR if merging manually:
  ```sh
  git checkout master
  git pull origin master  # Get latest master
  git merge feature-branch  # Merge changes
  git push origin master  # Push updated master
  ```

---

### **8️⃣ Delete the Feature Branch (Optional)**
After merging, delete the branch to keep things clean:
```sh
git branch -d feature-branch
git push origin --delete feature-branch
```
☑️ This removes the branch locally and remotely.

---

### **9️⃣ Keep Your Local Repo Updated**
Before starting a new feature, always get the latest code:
```sh
git checkout master
git pull origin master
```
Then create a new branch for your next task:
```sh
git checkout -b new-feature
```

---

## **🔥 Quick Summary**
1️⃣ **Create & switch to a new branch**: `git checkout -b feature-branch`  
2️⃣ **Make changes, commit them**: `git add . && git commit -m "message"`  
3️⃣ **Push to GitHub**: `git push origin feature-branch`  
4️⃣ **Open a Pull Request** on GitHub  
5️⃣ **Fix any requested changes** (if needed)  
6️⃣ **Merge the PR** (on GitHub or via `git merge`)  
7️⃣ **Delete the feature branch** (optional)  

---

### **🔹 Bonus: Handling `master` Updates While Working on `feature-branch`**
If `master` gets updated while you’re still working, **update your branch to avoid conflicts**:  
```sh
git checkout feature-branch
git pull origin master  # Merge latest master changes
```
Or for a cleaner history:
```sh
git rebase master
git rebase --continue  # If conflicts appear
```

---

That’s the **full Git workflow** from start to finish. Let me know if you need more details or a specific scenario! 🚀