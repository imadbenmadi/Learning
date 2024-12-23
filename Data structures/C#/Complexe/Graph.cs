using System;
using System.Collections.Generic;

public class Graph
{
    private int V;
    private List<int>[] adjList;

    public Graph(int vertices)
    {
        V = vertices;
        adjList = new List<int>[V];
        for (int i = 0; i < V; i++)
            adjList[i] = new List<int>();
    }

    public void AddEdge(int v, int w)
    {
        adjList[v].Add(w);
        adjList[w].Add(v);
    }

    public bool BFS(int start, int target)
    {
        bool[] visited = new bool[V];
        Queue<int> queue = new Queue<int>();
        visited[start] = true;
        queue.Enqueue(start);

        while (queue.Count != 0)
        {
            int v = queue.Dequeue();

            foreach (int neighbor in adjList[v])
            {
                if (!visited[neighbor])
                {
                    if (neighbor == target) return true;
                    visited[neighbor] = true;
                    queue.Enqueue(neighbor);
                }
            }
        }

        return false;
    }

    public static void Main()
    {
        Graph g = new Graph(6);
        g.AddEdge(0, 1);
        g.AddEdge(0, 2);
        g.AddEdge(1, 3);
        g.AddEdge(2, 4);
        g.AddEdge(4, 5);

        Console.WriteLine(g.BFS(0, 5) ? "Path exists" : "No path");
    }
}
