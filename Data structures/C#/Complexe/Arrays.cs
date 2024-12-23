using System;

public class Arrays
{
    public static void Rotate(int[] arr, int k)
    {
        k = k % arr.Length;
        Reverse(arr, 0, arr.Length - 1);
        Reverse(arr, 0, k - 1);
        Reverse(arr, k, arr.Length - 1);
    }

    private static void Reverse(int[] arr, int start, int end)
    {
        while (start < end)
        {
            int temp = arr[start];
            arr[start] = arr[end];
            arr[end] = temp;
            start++;
            end--;
        }
    }

    public static void PrintArray(int[] arr)
    {
        Console.WriteLine(string.Join(", ", arr));
    }

    public static void Main(string[] args)
    {
        int[] arr = { 1, 2, 3, 4, 5, 6, 7 };
        int k = 3;
        Rotate(arr, k);
        PrintArray(arr);
    }
}
