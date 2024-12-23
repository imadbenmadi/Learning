using System;

public class LinkedListCycle
{
    public class ListNode
    {
        public int Value;
        public ListNode Next;
        public ListNode(int value)
        {
            Value = value;
            Next = null;
        }
    }

    public static bool HasCycle(ListNode head)
    {
        if (head == null) return false;
        
        ListNode slow = head;
        ListNode fast = head;
        
        while (fast != null && fast.Next != null)
        {
            slow = slow.Next;
            fast = fast.Next.Next;
            
            if (slow == fast)
                return true;
        }
        
        return false;
    }

    public static void Main()
    {
        ListNode head = new ListNode(3);
        head.Next = new ListNode(2);
        head.Next.Next = new ListNode(0);
        head.Next.Next.Next = new ListNode(-4);
        head.Next.Next.Next.Next = head.Next; // Create cycle
        
        Console.WriteLine(HasCycle(head) ? "Cycle Detected" : "No Cycle");
    }
}
