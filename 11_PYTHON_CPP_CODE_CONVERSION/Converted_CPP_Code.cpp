#include <iostream>
#include <iomanip>
#include <chrono>

using namespace std;
using namespace std::chrono;

double calculate(long long iterations, double param1, double param2) {
    double result = 1.0;
    double j;
    for (long long i = 1; i <= iterations; ++i) {
        j = i * param1 - param2;
        result -= 1.0 / j;
        j = i * param1 + param2;
        result += 1.0 / j;
    }
    return result;
}

int main() {
    long long iterations = 10;
    double param1 = 4.0;
    double param2 = 1.0;

    cout << iterations << "\n" << param1 << "\n" << param2 << "\n";

    auto start = high_resolution_clock::now();
    double result = calculate(iterations, param1, param2) * 4.0;
    auto end = high_resolution_clock::now();

    duration<double> elapsed = end - start;

    cout << fixed << setprecision(12);
    cout << "Result: " << result << "\n";
    cout << "Execution Time: " << elapsed.count() << " seconds\n";

    return 0;
}