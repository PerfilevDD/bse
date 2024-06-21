#pragma once

#include <sqlite3.h>
#include <sqlpp11/sqlite3/connection.h>

namespace BSM {
    namespace sql = sqlpp::sqlite3;

    class Database {
    public:
        Database();
        ~Database();

        sqlite3* get_db_handle(){
            return db;
        }


    private:
        sqlite3 *db;
        std::shared_ptr<sql::connection_config> config;
    };
}