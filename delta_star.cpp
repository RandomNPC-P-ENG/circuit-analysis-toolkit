#include<iostream>
#include<cmath>
using namespace std;

// Delta-Star transform
// used this for Tutorial 7 assignment
// R1=A-B, R2=B-C, R3=C-A

int main()
{
	for(;;)
	{
		double r1,r2,r3;
		cout<<"Enter R1 (A-B): ";
		cin>>r1;
		cout<<"Enter R2 (B-C): ";
		cin>>r2;
		cout<<"Enter R3 (C-A): ";
		cin>>r3;
		
		if(r1<=0||r2<=0||r3<=0)
		{
			cout<<"invalid input try again"<<endl;
			cout<<endl;
			system("pause");
			cout<<endl;
			continue;
		}
		
		double s = r1+r2+r3;
		double ra = r2*r3/s;
		double rb = r1*r3/s;
		double rc = r1*r2/s;
		
		cout<<endl;
		cout<<"Star equivalent:"<<endl;
		cout<<"  Ra (at A) = "<<ra<<" ohm"<<endl;
		cout<<"  Rb (at B) = "<<rb<<" ohm"<<endl;
		cout<<"  Rc (at C) = "<<rc<<" ohm"<<endl;
		
		// verify
		cout<<endl;
		cout<<"Verification:"<<endl;
		double d_ab = r1*(r2+r3)/s;
		double s_ab = ra+rb;
		cout<<"  A-B: Delta="<<d_ab<<" Star="<<s_ab;
		if(abs(d_ab-s_ab)<0.01) cout<<" OK";
		else cout<<" FAIL";
		cout<<endl;
		
		// reverse: star to delta
		double p = ra*rb+rb*rc+ra*rc;
		double r1b = p/rc;
		double r2b = p/rb;
		double r3b = p/ra;
		cout<<endl;
		cout<<"Reverse (Star->Delta):"<<endl;
		cout<<"  R1 = "<<r1b<<" ohm"<<endl;
		cout<<"  R2 = "<<r2b<<" ohm"<<endl;
		cout<<"  R3 = "<<r3b<<" ohm"<<endl;
		
		cout<<endl;
		system("pause");
		cout<<endl;
	}
	return 0;
}
