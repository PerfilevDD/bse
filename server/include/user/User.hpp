#pragma once

#include "string"
#include "sqlite3.h"
#include "db/sqlite.hpp"

namespace BSM {
    class User {
    public:
        User(int user_id);
        User(std::string& email, std::string& password);

        bool check_password(std::string& password);

        int get_balance();
        int get_user_id() {
            return user_id;
        };

        void update_balance(int change);
    private:
        int user_id;
        Database db;
    };
}