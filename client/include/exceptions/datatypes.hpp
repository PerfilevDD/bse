#pragma once

#include <exception>

class NoNextItem : std::exception {
    const char* what() {
        return "There's no next item.";
    }
};

class NoPrevItem : std::exception {
    const char* what() {
        return "There's no prev item.";
    }
};

class EmptyItemProvided : std::exception {
    const char* what() {
        return "The provided item is empty.";
    }
};

class EmptyContainer : std::exception {
    const char* what() {
        return "The provided item is empty.";
    }
};

class ItemNotFound : std::exception {
    const char* what() {
        return "The provided item hasn't been found.";
    }
};

class ItemAlreadyExisting : std::exception {
    const char* what() {
        return "The provided item is already existing.";
    }
};
