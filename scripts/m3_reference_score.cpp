// Independent exact rejection draws within one ordered day/query stratum.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

using Word = std::uint64_t;
struct Slot {
    Word account;
    Word group;
};

int main(int argc, char** argv) {
    if (argc != 4) return 2;
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
    if (!std::is_sorted(actions.begin(), actions.end()) ||
        !std::is_sorted(originals.begin(), originals.end())) return 2;

    // Codes 0 are unassigned. Every entry remains a separate original-post slot.
    std::vector<Slot> pool;
    pool.reserve(size);
    Word accepted = 0;
    Word proposals = 0;
    while (accepted < draws && proposals < proposal_limit) {
        ++proposals;
        Word next = 0;
        Word score = 0;
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
            score += slot.group != 0 && slot.group == sharer_groups[row];
            pool[choice] = pool.back();
            pool.pop_back();
        }
        if (legal) {
            ++accepted;
            std::cout << score << '\n';
        }
    }
    std::cerr << proposals << '\n';
    return accepted == draws ? 0 : 4;
}
