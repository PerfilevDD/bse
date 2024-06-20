#include <memory>

//!  The Queue Interface
/*!
 */

namespace Fairoulette {
class Randomizer {
   public:
    Randomizer();

    /**
     * @brief Insert an element at the end
     *
     *
     * @param insert_element The element to insert
     */
    size_t get_random_number() const;

   private:
    bool is_balck(size_t number) const;
};
}  // namespace Fairoulette
