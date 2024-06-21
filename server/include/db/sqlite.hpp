#pragma once

#include <sqlite3.h>
#include <sqlpp11/sqlite3/connection.h>

namespace BSM {
    namespace sql = sqlpp::sqlite3;

    class Database {
    public:
        Database();
        ~Database();

        std::shared_ptr<sql::connection> get_sqlpp11_db(){
            return sqlpp_db;
        }



    private:
        std::shared_ptr<sql::connection_config> config;
        std::shared_ptr<sql::connection> sqlpp_db;
    };
}