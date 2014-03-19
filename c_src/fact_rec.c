/*
 * Sample program 1: Factorial (recursive)
 * by Kim Merrill
 * updated: 2/2/14
 */

 #include <stdio.h>

 int factorial(int);

 int main()
 {
 	int n = 5;
 	int result = factorial(n);
	printf("factorial(%d) = %d\n", n, result);

 	return 0;
 }

 int factorial(int n)
 {
 	if (n == 0 || n == 1)
 	{
 		return 1;
 	}
 	else
 	{
 		return n * factorial(n-1);
 	}
 }
 