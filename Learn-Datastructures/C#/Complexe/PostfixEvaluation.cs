using System;
using System.Collections.Generic;

public class PostfixEvaluation
{
    public static int EvaluatePostfix(string expression)
    {
        Stack<int> stack = new Stack<int>();
        
        foreach (char token in expression)
        {
            if (char.IsDigit(token))
            {
                stack.Push(token - '0');
            }
            else
            {
                int val1 = stack.Pop();
                int val2 = stack.Pop();
                
                switch (token)
                {
                    case '+':
                        stack.Push(val2 + val1);
                        break;
                    case '-':
                        stack.Push(val2 - val1);
                        break;
                    case '*':
                        stack.Push(val2 * val1);
                        break;
                    case '/':
                        stack.Push(val2 / val1);
                        break;
                }
            }
        }
        return stack.Peek();
    }

    public static void Main()
    {
        string expression = "231*+9-";
        Console.WriteLine("Postfix Evaluation: " + EvaluatePostfix(expression));
    }
}
