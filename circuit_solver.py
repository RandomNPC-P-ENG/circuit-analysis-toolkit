#include<iostream>
#include<cmath>
#include<vector>
#include<string>
using namespace std;

// circuit solver using MNA
// supports: resistor, voltage source, current source
// TODO: thevenin equivalent

struct Resistor
{
	string name;
	string node1;
	string node2;
	double resistance;
	double current;
	double voltage;
};

struct VoltageSource
{
	string name;
	string node1;
	string node2;
	double voltage;
	double current;
};

struct CurrentSource
{
	string name;
	string node1;
	string node2;
	double current;
};

int main()
{
	// example: voltage divider
	// VS=10V, R1=1k, R2=2k
	// A--VS--GND, A--R1--B, B--R2--GND
	
	double vs=10, r1=1000, r2=2000;
	
	// node voltage: VA = VS * R2/(R1+R2)
	double va = vs * r2 / (r1+r2);
	
	cout<<"Node Voltages:"<<endl;
	cout<<"  V_A = "<<vs<<" V"<<endl;
	cout<<"  V_B = "<<va<<" V"<<endl;
	cout<<"  V_GND = 0 V"<<endl;
	cout<<endl;
	
	// currents
	double i1 = (vs-va)/r1;
	double i2 = va/r2;
	
	cout<<"Currents:"<<endl;
	cout<<"  R1: "<<i1*1000<<" mA"<<endl;
	cout<<"  R2: "<<i2*1000<<" mA"<<endl;
	
	cout<<endl;
	system("pause");
	return 0;
}
