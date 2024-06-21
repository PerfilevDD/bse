#pragma once

#include "string"
#include "sqlite3.h"
#include "db/sqlite.hpp"

namespace BSM {
    class User {
    public:
        User(Database database, int user_id);
        User(Database database, std::string& email, std::string& password);

        bool check_password(std::string& password);

        int get_balance();
        int get_user_id() {
            return user_id;
        };

        void update_balance(int change);

        inline static const std::string create_table = "CREATE TABLE IF NOT EXISTS USER("  \
          "ID INT PRIMARY KEY     NOT NULL," \
          "email          CHAR(50)    NOT NULL," \
          "password       CHAR(50)     NOT NULL," \
          "balance        INT DEFAULT 0);";
    private:
        int user_id;
        Database db;
    };
}