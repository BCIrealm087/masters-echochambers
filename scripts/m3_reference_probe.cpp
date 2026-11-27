// Benchmark rejection from the exact uniform reference constrained by time alone.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <limits>
#include <random>
#include <string_view>
#include <vector>

int main(int argc, char** argv) {
    if (argc != 3 && argc != 4) return 2;
    const bool early_reject = argc == 4 && std::string_view(argv[3]) == "--early-reject";
    const auto draws = std::stoull(argv[1]);
    std::mt19937_64 random(std::stoull(argv[2]));
    std::uint64_t n;
    if (!std::cin.read(reinterpret_cast<char*>(&n), sizeof(n)) || !n || !draws) return 2;
    std::vector<std::uint64_t> sharers(n), actions(n), authors(n), originals(n);
    for (auto* values : {&sharers, &actions, &authors, &originals}) {
        if (!std::cin.read(reinterpret_cast<char*>(values->data()), n * sizeof(n))) return 2;
    }
    std::vector<std::uint64_t> pool;
    pool.reserve(n);
    std::uint64_t accepted = 0, total_self = 0;
    std::uint64_t minimum = std::numeric_limits<std::uint64_t>::max(), maximum = 0;
    for (std::uint64_t draw = 0; draw < draws; ++draw) {
        std::uint64_t next = 0, self = 0;
        pool.clear();
        for (std::uint64_t row = 0; row < n; ++row) {
            while (next < n && originals[next] <= actions[row]) pool.push_back(authors[next++]);
            if (pool.empty()) return 3;
            const auto choice = pool.size() == 1 ? 0 :
                std::uniform_int_distribution<std::size_t>(0, pool.size() - 1)(random);
            self += pool[choice] == sharers[row];
            pool[choice] = pool.back();
            pool.pop_back();
            if (early_reject && self) break;
        }
        accepted += self == 0;
        total_self += self;
        minimum = std::min(minimum, self);
        maximum = std::max(maximum, self);
    }
    std::cout << accepted << ' ' << total_self << ' ' << minimum << ' ' << maximum << '\n';
}
