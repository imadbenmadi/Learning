```jsx
<AnimatePresence>
    {showInput && (
        <motion.div
            className="fixed bottom-0 w-full shadow-lg"
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            transition={{ duration: 0.3 }}
        >
            <Input setNotes={setNotes} setShowInput={setShowInput} />
        </motion.div>
    )}
</AnimatePresence>
```
