using System;

class Arrays
{
    // Inserting a value at the specified index
    public static void InsertAt(int[] arr, int index, int value)
    {
        arr[index] = value;
    }

    // Searching for a value in the array
    public static int Search(int[] arr, int value)
    {
        for (int i = 0; i < arr.Length; i++)
        {
            if (arr[i] == value)
                return i;
        }
        return -1; // Not found
    }

    // Deleting an element at the specified index and shifting
    public static void DeleteAt(int[] arr, int index)
    {
        for (int i = index; i < arr.Length - 1; i++)
        {
            arr[i] = arr[i + 1];
        }
        arr[arr.Length - 1] = 0; // Set the last element to 0 after shifting
    }
    public static void Main(string[] args)
    {
        int[] arr = new int[5];
        InsertAt(arr, 0, 10);
        InsertAt(arr, 1, 20);
        InsertAt(arr, 2, 30);
        InsertAt(arr, 3, 40);
        InsertAt(arr, 4, 50);
        Console.Write(" Array before : \n");

        foreach (var item in arr)
        {
            Console.Write(item + " ");
        }
        Console.Write(" Array before : \n");
        DeleteAt(arr, 2);
        foreach (var item in arr)
        {
            Console.Write(item + " ");
        }
        Console.Write(" Array Searching : \n");

        Console.WriteLine(Search(arr, 30));
    }
}
