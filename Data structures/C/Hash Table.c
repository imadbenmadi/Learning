#include <stdio.h>
#include <stdlib.h>

#define SIZE 10

struct HashItem {
    int key;
    int value;
};

struct HashItem* hashTable[SIZE];

int hashFunction(int key) {
    return key % SIZE;
}

void insert(int key, int value) {
    struct HashItem* item = (struct HashItem*)malloc(sizeof(struct HashItem));
    item->key = key;
    item->value = value;

    int index = hashFunction(key);
    while (hashTable[index] != NULL && hashTable[index]->key != -1)
        index = (index + 1) % SIZE;

    hashTable[index] = item;
}

int search(int key) {
    int index = hashFunction(key);

    while (hashTable[index] != NULL) {
        if (hashTable[index]->key == key)
            return hashTable[index]->value;
        index = (index + 1) % SIZE;
    }
    return -1;
}

void display() {
    for (int i = 0; i < SIZE; i++) {
        if (hashTable[i] != NULL)
            printf("Key: %d, Value: %d\n", hashTable[i]->key, hashTable[i]->value);
        else
            printf("Key: -1, Value: -1\n");
    }
}

int main() {
    insert(1, 20);
    insert(2, 70);
    insert(42, 80);
    insert(4, 25);

    printf("Hash table:\n");
    display();

    printf("Search for key 42: %d\n", search(42));

    return 0;
}
