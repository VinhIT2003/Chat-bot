```cpp
#include <iostream>
#include <vector>
#include <numeric>
#include <chrono>
#include <iomanip>

// Use uint64_t to prevent overflow
uint64_t lcg(uint64_t seed, uint64_t a = 1664525, uint64_t c = 1013904223, uint64_t m = 4294967296) { // m = 2**32
    static uint64_t value = seed; // Use static for generator
    value = (a * value + c) % m;
    return value;
}

int64_t max_subarray_sum(int n, uint64_t seed, int min_val, int max_val) {
    std::vector<int> random_numbers(n);
    for (int i = 0; i < n; ++i) {
        random_numbers[i] = lcg(seed) % (max_val - min_val + 1) + min_val;
    }

    int64_t max_sum = -2147483647 - 1LL;  // Initialize to minimum int64_t value
    for (int i = 0; i < n; ++i) {
        int64_t current_sum = 0;
        for (int j = i; j < n; ++j) {
            current_sum += random_numbers[j];
            max_sum = std::max(max_sum, current_sum);
        }
    }
    return max_sum;
}

int64_t total_max_subarray_sum(int n, uint64_t initial_seed, int min_val, int max_val) {
    int64_t total_sum = 0;
    uint64_t seed = initial_seed;
    for (int i = 0; i < 20; ++i) {
        seed = lcg(seed);
        total_sum += max_subarray_sum(n, seed, min_val, max_val);
    }
    return total_sum;
}

int main() {
    // Parameters
    int n = 10000;            // Number of random numbers
    uint64_t initial_seed = 42;  // Initial seed for the LCG
    int min_val = -10;        // Minimum value of random numbers
    int max_val = 10;         // Maximum value of random numbers

    // Timing the function
    auto start_time = std::chrono::high_resolution_clock::now();
    int64_t result = total_max_subarray_sum(n, initial_seed, min_val, max_val);
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);

    std::cout << "Total Maximum Subarray Sum (20 runs): " << result << std::endl;
    std::cout << "Execution Time: " << std::fixed << std::setprecision(6) << static_cast<double>(duration.count()) / 1000000.0 << " seconds" << std::endl;

    return 0;
}

```