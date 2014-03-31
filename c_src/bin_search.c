/*
 * Sample program 5: Binary search
 * by Kim Merrill
 * updated: 2/2/14
 */

 #include <stdio.h>

int bin_search(int list[], int lo, int hi, int key);

 int main()
 {
 	int n = 4;
 	int list[10] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
 	int result = bin_search(list, 0, sizeof(list) / sizeof(list[0]) - 1, n);
 	printf("element %d %s\n", n, result > -1 ? "found" : "not found");

 	return 0;
 }


int bin_search(int list[], int lo, int hi, int key)
{
	int mid;

	if (lo > hi)
	{
		return -1;
	}

	mid = (lo + hi) / 2;
	if (list[mid] == key)
	{
		return mid;
	}
	else if (list[mid] > key)
	{
		return bin_search(list, lo, mid-1, key);
	}
	else
	{
		// list[mid] < key
		return bin_search(list, mid+1, hi, key);
	}
}
 