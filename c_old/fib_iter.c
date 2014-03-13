/*
 * Sample program 4: Fibonacci (iterative)
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

 	int fib_1 = 1;
 	int fib_2 = 0;

 	while (n > 1)
 	{
 		int temp = fib_1;
 		fib_1 += fib_2;
 		fib_2 = temp;
 		n--;
 	}

 	return fib_1;
 }
 