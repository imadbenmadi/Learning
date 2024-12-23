using System;
using System.Collections.Generic;

public class QueueUsingStacks
{
    Stack<int> stack1 = new Stack<int>();
    Stack<int> stack2 = new Stack<int>();

    public void Enqueue(int x)
    {
        stack1.Push(x);
    }

    public int Dequeue()
    {
        if (stack2.Count == 0)
        {
            while (stack1.Count > 0)
            {
                stack2.Push(stack1.Pop());
            }
        }
        return stack2.Pop();
    }

    public static void Main()
    {
        QueueUsingStacks q = new QueueUsingStacks();
        q.Enqueue(1);
        q.Enqueue(2);
        q.Enqueue(3);
        
        Console.WriteLine(q.Dequeue());  // Output: 1
        Console.WriteLine(q.Dequeue());  // Output: 2
    }
}
