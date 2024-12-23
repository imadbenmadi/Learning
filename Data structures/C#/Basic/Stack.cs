public class Stack
{
    private List<int> stack = new List<int>();

    public void Push(int value)
    {
        stack.Add(value);
    }

    public int Pop()
    {
        if (stack.Count == 0) throw new InvalidOperationException("Stack is empty");
        int value = stack[stack.Count - 1];
        stack.RemoveAt(stack.Count - 1);
        return value;
    }

    public int Peek()
    {
        if (stack.Count == 0) throw new InvalidOperationException("Stack is empty");
        return stack[stack.Count - 1];
    }
}
