// ftdemo - Discrete Fourier transform demonstration program
#include <fstream>
#include <iostream>
#include "math.h"
#include "Matrix.h"

using namespace std;

void fft( Matrix& RealA, Matrix& ImagA);
         
int main() {

  //* Initialize the sine wave time series to be transformed.
  cout << "Enter the number of points: ";
  int N; cin >> N;
  cout << "Enter frequency of the sine wave: ";
  double freq; cin >> freq;
  cout << "Enter phase of the sine wave: ";
  double phase; cin >> phase;
  double tau = 1.0/N;  // Time increment
  const double pi = 3.141592654;
  Matrix t(N), y(N), f(N);
  int i,j,k;
  for( i=1; i<=N; i++ ) {
    t(i) = (i-1)*tau;                     // t = [0, tau, 2*tau, ... ]            
    y(i) = sin(2*pi*t(i)*freq + phase);   // Sine wave time series
    f(i) = (i-1)/(N*tau);                 // f = [0, 1/(N*tau), ... ] 
  }
  
  //* Compute the transform using desired method: direct summation
  //  or fast Fourier transform (FFT) algorithm.
  Matrix ytReal(N), ytImag(N);
  cout << "Compute transform by, 1) Direct summation; 2) FFT: ";
  int method; cin >> method;
  if( method == 1 ) {            // Direct summation
    double twoPiN = -2*pi/N;
    for( k=0; k<N; k++ ) {
      ytReal(k+1) = 0.0;
      ytImag(k+1) = 0.0;
      for( j=0; j<N; j++ ) {
        ytReal(k+1) += y(j+1)*cos(twoPiN*j*k);
        ytImag(k+1) += y(j+1)*sin(twoPiN*j*k);
      }
    }
  }  
  else  {                        // Fast Fourier transform
	ytReal = y;
	ytImag.set(0.0);     // Copy data for input to fft
    fft(ytReal, ytImag);
  }
  // Compute the power spectrum
  Matrix powSpec(N);
  for( k=1; k<=N; k++ )
    powSpec(k) = ytReal(k)*ytReal(k) + ytImag(k)*ytImag(k);
    
  //* Print out the plotting variables: 
  //    t, y, f, ytReal, ytImag, powspec
  ofstream tOut("t.txt"), yOut("y.txt"), fOut("f.txt"), 
	  ytRealOut("ytReal.txt"), ytImagOut("ytImag.txt"), 
	  powSpecOut("powSpec.txt");
  for( i=1; i<=N; i++ ) {
    yOut << t(i) << " " << y(i) << endl;
    ytRealOut << f(i) << " " << ytReal(i) << endl;
    ytImagOut << f(i) << " " << ytImag(i) << endl;
    powSpecOut << f(i) << " " << powSpec(i) << endl;
  }
}
