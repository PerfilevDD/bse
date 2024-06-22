#pragma once

#include <sqlite3.h>
#include <sqlpp11/sqlite3/connection.h>

namespace BSE {
    namespace sql = sqlpp::sqlite3;

    class Database {
    public:
        Database();
        ~Database();

        std::shared_ptr<sql::connection> get_sqlpp11_db(){
            return sqlpp_db;
        }

        bool find_user_by_email(std::string& email);


    private:
        std::shared_ptr<sql::connection_config> config;
        std::shared_ptr<sql::connection> sqlpp_db;
    };
}