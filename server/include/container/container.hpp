#pragma once

#include "exceptions/datatypes.hpp"

class Container {
public:
    // Get Size
    /**
     * @brief Get the size of the container
     *
     *
     * @return An amount of the elements
     */
    size_t size() const{
        return container_size;
    }
protected:
    size_t container_size = 0;
};