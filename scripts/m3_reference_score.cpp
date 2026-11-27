// Independent exact rejection draws within one ordered day/query stratum.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <iomanip>
#include <random>
#include <string_view>
#include <vector>

using Word = std::uint64_t;
struct Slot {
    Word account;
    Word group;
};

int main(int argc, char** argv) {
    if (argc != 4 && argc != 5) return 2;
    const bool assignments = argc == 5 && std::string_view(argv[4]) == "--assignments";
    const bool secondary = argc == 5 && !assignments;
    const Word draws = std::stoull(argv[1]);
    const Word seed = std::stoull(argv[2]);
    const Word proposal_limit = std::stoull(argv[3]);
    std::mt19937_64 random(seed);
    Word size;
    if (!std::cin.read(reinterpret_cast<char*>(&size), sizeof(size)) || !size) return 2;
    std::vector<Word> sharers(size), actions(size), authors(size), originals(size),
                      sharer_groups(size), author_groups(size);
    for (auto* column : {&sharers, &actions, &authors, &originals,
                          &sharer_groups, &author_groups}) {
        if (!std::cin.read(reinterpret_cast<char*>(column->data()), size * sizeof(Word))) return 2;
    }
    std::vector<double> weights;
    std::vector<Word> group_index;
    std::vector<Word> group_counts;
    if (secondary) {
        group_counts.resize(std::stoull(argv[4]) + 1);
        weights.resize(size);
        group_index.resize(size);
        if (!std::cin.read(reinterpret_cast<char*>(weights.data()), size * sizeof(double)) ||
            !std::cin.read(reinterpret_cast<char*>(group_index.data()), size * sizeof(Word)) ||
            *std::max_element(group_index.begin(), group_index.end()) >= group_counts.size()) return 2;
        std::cout << std::setprecision(17);
    }
    if (!std::is_sorted(actions.begin(), actions.end()) ||
        !std::is_sorted(originals.begin(), originals.end())) return 2;

    // Codes 0 are unassigned. Every entry remains a separate original-post slot.
    std::vector<Slot> pool;
    pool.reserve(size);
    std::vector<Word> assigned(assignments ? size : 0);
    Word accepted = 0;
    Word proposals = 0;
    while (accepted < draws && proposals < proposal_limit) {
        ++proposals;
        Word next = 0;
        Word score = 0;
        long double weighted = 0;
        std::fill(group_counts.begin(), group_counts.end(), 0);
        bool legal = true;
        pool.clear();
        for (Word row = 0; row < size; ++row) {
            while (next < size && originals[next] <= actions[row]) {
                pool.push_back({authors[next], author_groups[next]});
                ++next;
            }
            if (pool.empty()) return 3;
            const auto choice = pool.size() == 1 ? 0 :
                std::uniform_int_distribution<std::size_t>(0, pool.size() - 1)(random);
            const Slot slot = pool[choice];
            if (slot.account == sharers[row]) {
                legal = false;
                break;
            }
            if (assignments) assigned[row] = slot.account;
            if (slot.group != 0 && slot.group == sharer_groups[row]) {
                ++score;
                if (secondary) {
                    weighted += weights[row];
                    ++group_counts[group_index[row]];
                }
            }
            pool[choice] = pool.back();
            pool.pop_back();
        }
        if (legal) {
            ++accepted;
            if (assignments) {
                std::cout.write(reinterpret_cast<const char*>(assigned.data()),
                                assigned.size() * sizeof(Word));
                continue;
            }
            std::cout << score;
            if (secondary) {
                std::cout << ' ' << weighted;
                for (auto entry = group_counts.begin() + 1; entry != group_counts.end(); ++entry)
                    std::cout << ' ' << *entry;
            }
            std::cout << '\n';
        }
    }
    std::cerr << proposals << '\n';
    return accepted == draws ? 0 : 4;
}
