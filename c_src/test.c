/*
 * Sample program 2: Factorial (iterative)
 * by Kim Merrill
 * updated: 2/2/14
 */

 #include <stdio.h>

 void factorial(int);

 int main()
 {
 	int n = 5;
 	factorial(n);
 	printf("factorial(%d)\n", n);

	// return comment
 	return 1;
 }

 void factorial(int n)
 {
 	int last_fact = 1;
 	int curr_fact = n;

 	while(n > 1)
 	{
 		curr_fact = last_fact * n;
 		last_fact = curr_fact;
 		n--;
 	}
 }
 