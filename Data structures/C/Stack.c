#include <stdio.h>
#define MAX 5

int stack[MAX];
int top = -1;

void push(int value) {
    if (top == MAX - 1)
        printf("Stack overflow\n");
    else
        stack[++top] = value;
}

int pop() {
    if (top == -1)
        printf("Stack underflow\n");
    else
        return stack[top--];
}

void display() {
    if (top == -1)
        printf("Stack is empty\n");
    else {
        for (int i = top; i >= 0; i--)
            printf("%d ", stack[i]);
        printf("\n");
    }
}

int main() {
    push(10);
    push(20);
    push(30);
    display();
    pop();
    display();
    return 0;
}
