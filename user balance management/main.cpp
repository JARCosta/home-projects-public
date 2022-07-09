// C++ program to insert a node in AVL tree
#include<bits/stdc++.h>
using namespace std;

// An AVL tree node
class Node
{
	public:
	char* username;
	Node *left;
	Node *right;
	int height;

	int credit_card;
	int expire_date;
};

// A utility function to get maximum
// of two integers
int max(int a, int b);

// A utility function to get the
// height of the tree
int height(Node *N)
{
	if (N == NULL)
		return 0;
	return N->height;
}

// A utility function to get maximum
// of two integers
int max(int a, int b)
{
	return (a > b)? a : b;
}

/* Helper function that allocates a
new node with the given username and
NULL left and right pointers. */
Node* newNode(char* username, int credit_card, int expire_date)
{
	Node* node = new Node();
	node -> username = username;
	node -> left = NULL;
	node -> right = NULL;
	node -> height = 1; // new node is initially
					// added at leaf

	node -> credit_card = credit_card;
	node -> expire_date = expire_date;
	return(node);
}

// A utility function to right
// rotate subtree rooted with y
// See the diagram given above.
Node *rightRotate(Node *y)
{
	Node *x = y->left;
	Node *T2 = x->right;

	// Perform rotation
	x->right = y;
	y->left = T2;

	// Update heights
	y->height = max(height(y->left),
					height(y->right)) + 1;
	x->height = max(height(x->left),
					height(x->right)) + 1;

	// Return new root
	return x;
}

// A utility function to left
// rotate subtree rooted with x
// See the diagram given above.
Node *leftRotate(Node *x)
{
	Node *y = x->right;
	Node *T2 = y->left;

	// Perform rotation
	y->left = x;
	x->right = T2;

	// Update heights
	x->height = max(height(x->left),
					height(x->right)) + 1;
	y->height = max(height(y->left),
					height(y->right)) + 1;

	// Return new root
	return y;
}

// Get Balance factor of node N
int getBalance(Node *N)
{
	if (N == NULL)
		return 0;
	return height(N->left) - height(N->right);
}

// Recursive function to insert a username
// in the subtree rooted with node and
// returns the new root of the subtree.
Node* insert(Node* node, char* username, int credit_card, int expire_date)
{
	/* 1. Perform the normal BST insertion */
	if (node == NULL)
		return(newNode(username, credit_card, expire_date));

	if (strcmp(username, node->username) < 0)
		node->left = insert(node->left, username, credit_card, expire_date);
	else if (strcmp(username, node->username) > 0)
		node->right = insert(node->right, username, credit_card, expire_date);
	else // Equal usernames are not allowed in BST
		return node;

	/* 2. Update height of this ancestor node */
	node->height = 1 + max(height(node->left),
						height(node->right));

	/* 3. Get the balance factor of this ancestor
		node to check whether this node became
		unbalanced */
	int balance = getBalance(node);

	// If this node becomes unbalanced, then
	// there are 4 cases

	// Left Left Case
	if (balance > 1 && strcmp(username, node->left->username) < 0 )
		return rightRotate(node);

	// Right Right Case
	if (balance < -1 && strcmp(username, node->right->username) > 0)
		return leftRotate(node);

	// Left Right Case
	if (balance > 1 && strcmp(username, node->left->username) > 0)
	{
		node->left = leftRotate(node->left);
		return rightRotate(node);
	}

	// Right Left Case
	if (balance < -1 && strcmp(username, node->right->username) < 0)
	{
		node->right = rightRotate(node->right);
		return leftRotate(node);
	}

	/* return the (unchanged) node pointer */
	return node;
}

// A utility function to print preorder
// traversal of the tree.
// The function also prints height
// of every node
void preOrder(Node *root)
{
	if(root != NULL)
	{
		cout << root->username << " ";
		preOrder(root->left);
		preOrder(root->right);
	}
}

Node* find(Node *root, char* username){
	if(root == NULL) return NULL;
	if(strcmp(root -> username, username) == 0)
		return root;
	else if(strcmp(root -> username, username) < 0)
			return find( root -> right, username);
	else if(strcmp(root -> username, username) > 0)
			return find( root -> left, username);
	return NULL;
}
void print_node(Node *root){
	if(root != NULL)
		printf("%d %d\n", root -> credit_card, root -> expire_date);
}

void print_node_alphabetically(Node *root){
	//printf("test v\n");
	//print_node(root);
	//printf("test ^\n");
	
	if(root -> left != NULL)
		print_node_alphabetically(root -> left);
	
	print_node(root);

	if( root -> right != NULL)
		print_node_alphabetically(root -> right);
}

Node* insert_update(Node *root, char* username, int credit_card, int expire_date){
	Node *temp = find(root, username);
	if(temp != NULL){
		if(temp -> credit_card == credit_card)
			//insert
		temp -> credit_card = credit_card;
		temp -> expire_date = expire_date;
		return root;
	} else
		return insert(root, username, credit_card, expire_date);
}

// Driver Code
int main()
{
	Node *root = NULL;
	
	printf("%d\n", strcmp("33", "22"));
	/* Constructing tree given in
	the above figure */
	root = insert_update(root, "11", 1111, 11);
	root = insert_update(root, "22", 2222, 22);
	root = insert_update(root, "33", 3333, 33);
	root = insert_update(root, "44", 4444, 44);
	root = insert_update(root, "55", 5555, 55);
	root = insert_update(root, "26", 2266, 26);
	
	root = insert_update(root, "55", 1000, 10);

	Node* temp;

	printf("\n find 11\n");
	temp = find(root, "11");
	print_node(temp);

	printf("\n find 22\n");
	temp = find(root, "22");
	print_node(temp);

	printf("\n find 44\n");
	temp = find(root, "44");
	print_node(temp);

	printf("\n find 55\n");
	temp = find(root, "55");
	print_node(temp);

	printf("\n find 26\n");
	temp = find(root, "26");
	print_node(temp);

	printf("\n find 12\n");
	temp = find(root, "12");
	print_node(temp);

	printf("\n printf alfabetico\n");
	print_node_alphabetically(root);
	
	/* The constructed AVL Tree would be
				30
			/ \
			20 40
			/ \ \
		10 25 50
	cout << "Preorder traversal of the constructed AVL tree is \n";
	preOrder(root);
	*/
	
	return 0;
}

// This code is contributed by
// rathbhupendra
