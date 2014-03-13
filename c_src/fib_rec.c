/*
 * Sample program 3: Fibonacci (recursive)
 * by Kim Merrill
 * updated: 2/2/14
 */

 #include <stdio.h>

 int fib(int);

 int main()
 {
 	int n = 8;
 	int result = fib(n);
 	printf("fibonacci(%d) = %d\n", n, result);

 	return 0;
 }

 int fib(int n)
 {
 	if (n == 0)
 	{
 		return 0;
 	}
 	else if (n == 1)
 	{
 		return 1;
 	}
 	else
 	{
 		return fib(n-1) + fib(n-2);
 	}
 }
 