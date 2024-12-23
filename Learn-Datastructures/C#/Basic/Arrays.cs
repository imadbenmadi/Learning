class Arrays
{
    public void InsertAt(int[] arr, int index, int value)
    {
        arr[index] = value;
    }

    public int Search(int[] arr, int value)
    {
        for (int i = 0; i < arr.Length; i++)
        {
            if (arr[i] == value) return i;
        }
        return -1; // Not found
    }

    public void DeleteAt(int[] arr, int index)
    {
        for (int i = index; i < arr.Length - 1; i++)
        {
            arr[i] = arr[i + 1];
        }
    }
    // static  void main(string[] args)
    // {
    //     int[] arr = new int[5];
    //     InsertAt(arr, 0, 10);
    //     InsertAt(arr, 1, 20);
    //     InsertAt(arr, 2, 30);
    //     InsertAt(arr, 3, 40);
    //     InsertAt(arr, 4, 50);

    //     DeleteAt(arr, 2);
    //     Search(arr, 30);
    // }
}
