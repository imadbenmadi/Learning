public class Queue
{
    private Queue<int> queue = new Queue<int>();

    public void Enqueue(int value)
    {
        queue.Enqueue(value);
    }

    public int Dequeue()
    {
        if (queue.Count == 0) throw new InvalidOperationException("Queue is empty");
        return queue.Dequeue();
    }

    public int Peek()
    {
        if (queue.Count == 0) throw new InvalidOperationException("Queue is empty");
        return queue.Peek();
    }
}
