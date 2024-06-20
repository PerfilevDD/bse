#include <random>
#include <randomizer.hpp>

namespace Fairoulette {

Randomizer::Randomizer() {}

size_t Randomizer::get_random_number() const {
    std::random_device dev;
    std::mt19937 rng(dev());
    std::uniform_int_distribution<std::mt19937::result_type> dist(0, 36);  // distribution in range [1, 6]

    return dist(rng);
}
}  // namespace Fairoulette
// bool Randomizer::is_balck(size_t number) const {}