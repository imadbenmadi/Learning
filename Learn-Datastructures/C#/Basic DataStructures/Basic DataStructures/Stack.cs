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
        stack.RemoveAt(stack.Count - 1);
    }

    public int Peek()
    {
        if (stack.Count == 0) throw new InvalidOperationException("Stack is empty");
        return stack[stack.Count - 1];
    }
}
