using System;

public class InvertBinaryTree
{
    public class TreeNode
    {
        public int Value;
        public TreeNode Left, Right;
        public TreeNode(int value)
        {
            Value = value;
            Left = Right = null;
        }
    }

    public static TreeNode InvertTree(TreeNode root)
    {
        if (root == null) return null;

        TreeNode left = InvertTree(root.Left);
        TreeNode right = InvertTree(root.Right);

        root.Left = right;
        root.Right = left;

        return root;
    }

    public static void PreorderTraversal(TreeNode root)
    {
        if (root == null) return;
        Console.Write(root.Value + " ");
        PreorderTraversal(root.Left);
        PreorderTraversal(root.Right);
    }

    public static void Main()
    {
        TreeNode root = new TreeNode(4);
        root.Left = new TreeNode(2);
        root.Right = new TreeNode(7);
        root.Left.Left = new TreeNode(1);
        root.Left.Right = new TreeNode(3);
        root.Right.Left = new TreeNode(6);
        root.Right.Right = new TreeNode(9);

        Console.WriteLine("Original Tree:");
        PreorderTraversal(root);
        Console.WriteLine();

        InvertTree(root);

        Console.WriteLine("Inverted Tree:");
        PreorderTraversal(root);
    }
}
