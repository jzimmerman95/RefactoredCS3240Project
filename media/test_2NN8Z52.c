#include <stdio.h>
#include <stdlib.h>

/* A struct is like a class, but without methods */
struct foo {
  int x;
  struct foo *next;
}; int* p;


int main() {
  /*int *p;*/
  //struct foo *list, *tmp;

  /* dynamically allocate an array of ints */
  /*p = (int *) malloc(sizeof (int) * 5);
  p[1] = 10;
  printf ("%d\n", p[1]);*/

  /* free up that array */
  //free(p);

  /* calling free(p) again is an error, and will crash the program */


	int reverse_x;
	int alt_return;
	int check_for_zero;
	int a, b, c;
	int ans;
	//int x = 0x80000000;
	int x = 0x7fffffff;
	//if x is the minimum, x = reverse_x
	reverse_x = ~x + 1;

	//if a = 0, then x is the minimum
	a = x ^ reverse_x;

	a = !a;
	b = 1; //return 1 if a = 1
	c = 0; //return 0 if a = 0

	alt_return = ((~(!!a)+1) & b) | ((~(!a)+1) &c);

	//check if x is zero - if x = 0 then check_for_zero = 0 —> return 0
	check_for_zero = x ^ 0; 
	check_for_zero = !check_for_zero;

	ans = ((~(!!check_for_zero)+1) & 0) | ((~(!check_for_zero)+1) & alt_return);
	printf("%d\n", ans);
	

}
