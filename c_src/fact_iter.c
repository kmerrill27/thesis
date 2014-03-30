/*
 * Sample program 2: Factorial (iterative)
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
 	int curr_fact = 1;

 	while(n > 1)
 	{
 		curr_fact = curr_fact * n;
 		n--;
 	}

 	return curr_fact;
 }
 