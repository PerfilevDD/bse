#pragma once

#include <sqlite3.h>

namespace BSM {
    class Database {
    public:
        Database();
        ~Database();
    private:
        sqlite3 *db{};
    };
}