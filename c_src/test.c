/*
 * Sample program 2: Factorial (iterative)
 * by Kim Merrill
 * updated: 2/2/14
 */

 #include <stdio.h>

 void hello(int);
 void factorial(int);

 int main()
 {
 	int n = 5;
	hello(n);
 	printf("factorial(%d)\n", n);

	// return comment
 	return 1;
 }

 void hello(int n)
 {
	int num = 3;
	int num2 = 4;
	
	factorial(n);
 }

 void factorial(int n)
 {
	 if (n == 0 || n == 1)
	 {
		 n--;
		 return;
	 }
	 else
	 {
		 factorial(n-1);
	 }
 }
 