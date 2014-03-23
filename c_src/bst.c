/*
 * Sample program 6: BST
 * by Kim Merrill
 * updated: 2/2/14
 */

#include <stdio.h>
#include <stdlib.h>

struct node
{
	int data;
	struct node *left;
	struct node *right;
};

struct node *insert(struct node *, int);
void in_order(struct node *);
void post_order(struct node *);
void pre_order(struct node *);
void delete_all(struct node *root);

int main(void)
{
	struct node *root = NULL;

	int i;
	for (i = 0; i < 5; i++)
	{
		root = insert(root, rand() % 25);
	}

	printf("preorder traversal: ");
	pre_order(root);
	printf("\ninorder traversal: ");
	in_order(root);
	printf("\npostorder traversal: ");
	post_order(root);
	printf("\n");

	delete_all(root);

	return 0;
}

struct node *insert(struct node *root, int val)
{
	if (!root)
	{
		root = (struct node*)malloc(sizeof(struct node));
		root->data = val;
		root->left = NULL;
		root->right = NULL;
	}
	else if (root->data > val)
	{
		root->left = insert(root->left, val);
	}
	else if (root->data < val)
	{
		root->right = insert(root->right, val);
	}

	return root;
}

void in_order(struct node *root)
{
	if (root)
	{
		in_order(root->left);
		printf("%d ", root->data);
		in_order(root->right);
	}
}

void post_order(struct node *root)
{
	if (root)
	{
		post_order(root->left);
		post_order(root->right);
		printf("%d ", root->data);
	}
}

void pre_order(struct node* root)
{
	if (root)
	{
		printf("%d ", root->data);
		pre_order(root->left);
		pre_order(root->right);
	}
}

void delete_all(struct node *root)
{
	if (root)
	{
		delete_all(root->left);
		delete_all(root->right);
		free(root);
	}
}
