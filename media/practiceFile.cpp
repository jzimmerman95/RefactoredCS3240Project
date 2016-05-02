#include <iostream>
#include <string>
#define PI 3.14159
#include <climits>
#include <cfloat>
#include <cstdlib>
using namespace std;

int main() {

  string x ("abc");
  int y = x.at(0) + x.at(1) + x.at(2);
  cout << y << endl;
  
  // string s("-5");
  // if (isdigit(s[0]) == true || isdigit(s[1]) == true) {
  //   cout << s << endl;
  // }
  
  // union {
  //   float f;
  //   int i;
  //   double *p;
  // } bar;

  // bar.f = -35.5;
  // cout << bar.p << endl;
  // bar.i = -234;
  // cout << bar.p << endl;
  
  // int* intPt = new int();
  // cout << *intPt << endl;
  
  // int x = INT_MAX;
  // cout << x << endl;
  // unsigned int y = UINT_MAX;
  // cout << y << endl;
  // double z = DBL_MAX;
  // cout << z << endl;
  // float w = FLT_MAX;
  // cout << w << endl;

  // string newS = "Hello World";
  // cout << newS.at(0) << endl;
  // char newC = newS.at(0);
  // cout << newC << endl;

  // string str ("5");
  // x = atoi(str.c_str());
  // cout << x << endl;

  // if (isdigit(str.at(0))) {

  // }
  
  // if (PI == 3.14159) {
  //   cout << "Pi" << endl;
  // }

  return 0;
  
}
