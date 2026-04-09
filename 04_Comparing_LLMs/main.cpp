#include <cstdio>
#include <chrono>
#include <cstdint>

int main() {
    using namespace std::chrono;

    auto start_time = high_resolution_clock::now();

    constexpr int64_t iterations = 200000000;
    constexpr double inc = 4.0;
    constexpr double p2  = 1.0;

    double result = 1.0;
    double j1 = inc - p2; // 3.0
    double j2 = inc + p2; // 5.0

    int64_t n8 = iterations / 8;
    for (int64_t k = 0; k < n8; ++k) {
        result -= 1.0 / j1; result += 1.0 / j2; j1 += inc; j2 += inc;
        result -= 1.0 / j1; result += 1.0 / j2; j1 += inc; j2 += inc;
        result -= 1.0 / j1; result += 1.0 / j2; j1 += inc; j2 += inc;
        result -= 1.0 / j1; result += 1.0 / j2; j1 += inc; j2 += inc;
        result -= 1.0 / j1; result += 1.0 / j2; j1 += inc; j2 += inc;
        result -= 1.0 / j1; result += 1.0 / j2; j1 += inc; j2 += inc;
        result -= 1.0 / j1; result += 1.0 / j2; j1 += inc; j2 += inc;
        result -= 1.0 / j1; result += 1.0 / j2; j1 += inc; j2 += inc;
    }
    for (int64_t k = n8 * 8; k < iterations; ++k) {
        result -= 1.0 / j1;
        result += 1.0 / j2;
        j1 += inc;
        j2 += inc;
    }

    double final_result = result * 4.0;

    auto end_time = high_resolution_clock::now();
    double elapsed = duration<double>(end_time - start_time).count();

    std::printf("Result: %.12f\n", final_result);
    std::printf("Execution time: %.8f Seconds\n", elapsed);
    return 0;
}