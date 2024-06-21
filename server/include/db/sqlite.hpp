#pragma once

#include <sqlite3.h>

namespace BSM {
    class Database {
    public:
        Database();
        ~Database();

        sqlite3* get_db_handle(){
            return db;
        }

    private:
        sqlite3 *db{};
    };
}