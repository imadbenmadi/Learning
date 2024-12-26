# Framer Motion in React

Framer Motion is a powerful animation library for React. It simplifies the creation of animations and gestures with a clean API. Here is everything you need to know to get started and master it.

---

## Installation

Install Framer Motion via npm or yarn:
```bash
npm install framer-motion
```

---

## Basics

### Animate a Component
To animate a component, use the `motion` object:
```jsx
import { motion } from 'framer-motion';

function Example() {
  return (
    <motion.div
      animate={{ opacity: 1 }}
      initial={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
    >
      Hello World
    </motion.div>
  );
}
```
- **`initial`**: Defines the starting animation state.
- **`animate`**: Defines the end animation state.
- **`transition`**: Controls the animation’s timing (e.g., `duration`, `ease`).

### Motion Components
Framer Motion provides motion-enhanced components like:
```jsx
<motion.div>
<motion.span>
<motion.img>
```
You can also create custom motion components:
```jsx
import { motion } from 'framer-motion';
const MotionButton = motion.button;
```

---

## Variants

Variants allow you to define reusable animation states.
```jsx
const boxVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, scale: 1.2 },
};

function Example() {
  return (
    <motion.div
      variants={boxVariants}
      initial="hidden"
      animate="visible"
    >
      Animated Box
    </motion.div>
  );
}
```
- **`variants`**: Defines multiple animation states (e.g., `hidden` and `visible`).
- **`initial`**: Specifies which variant to start with.
- **`animate`**: Specifies which variant to transition to.

Variants are reusable and keep your code clean, especially when multiple components share the same animation logic.

---

## Gestures

Framer Motion supports gestures like drag, hover, and tap.

### Drag
```jsx
<motion.div drag dragConstraints={{ left: 0, right: 300 }}>
  Drag me
</motion.div>
```
- **`drag`**: Enables dragging.
- **`dragConstraints`**: Limits the drag area (e.g., `{ left: 0, right: 300 }`).

### Hover
```jsx
<motion.div whileHover={{ scale: 1.1 }}>
  Hover over me
</motion.div>
```
- **`whileHover`**: Defines the animation state when the user hovers over the component.

### Tap
```jsx
<motion.div whileTap={{ scale: 0.9 }}>
  Tap me
</motion.div>
```
- **`whileTap`**: Defines the animation state when the user taps the component.

---

## AnimatePresence

The `AnimatePresence` component manages enter/exit animations for dynamically added/removed components.

### Example: Animated List
```jsx
import { motion, AnimatePresence } from 'framer-motion';

function List({ items }) {
  return (
    <AnimatePresence>
      {items.map((item) => (
        <motion.div
          key={item}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          {item}
        </motion.div>
      ))}
    </AnimatePresence>
  );
}
```
- **`AnimatePresence`**: Wraps around components to enable exit animations.
- **`exit`**: Defines the animation state when a component is removed.

This is especially useful for lists or modals where components are dynamically added or removed.

---

## Advanced Features

### Transition Options

#### Timing Functions
- `duration`: Duration of the animation.
- `delay`: Delay before the animation starts.
- `ease`: Easing function (e.g., `easeIn`, `easeOut`, `linear`).

#### Spring Physics
- `type: 'spring'`: Enables spring animations.
- `stiffness`: Controls the spring’s stiffness.
- `damping`: Controls the spring’s oscillations.
```jsx
<motion.div
  animate={{ x: 100 }}
  transition={{ type: 'spring', stiffness: 100 }}
/>
```

---

## Best Practices

1. **Reuse Variants:** Use variants for consistency and reusability.
2. **Use AnimatePresence:** For enter/exit animations, wrap your components with `AnimatePresence`.
3. **Optimize Performance:** Avoid animating large DOM trees or complex components.

---

## Resources

- [Official Documentation](https://www.framer.com/docs/)
- [Examples](https://www.framer.com/motion/examples/)
- [API Reference](https://www.framer.com/docs/transition/)

---

This guide covers the most essential features of Framer Motion. Experiment with the examples and dive deeper into the documentation for advanced use cases.

