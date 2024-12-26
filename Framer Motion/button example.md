```jsx
<motion.div
    className="fixed right-12"
    animate={{
        bottom: showInput ? "20rem" : "3rem", // Moves button upward when input is visible
    }}
    initial={{ bottom: "3rem" }}
    transition={{
        type: "spring",
        stiffness: 300,
        damping: 30,
    }}
>
    <button
        onClick={() => setShowInput(!showInput)}
        className="bg-blue-500 text-white p-4 rounded-full shadow-xl hover:bg-blue-600 transition font-semibold"
    >
        {showInput ? "Close" : "Add Note"}
    </button>
</motion.div>
```
