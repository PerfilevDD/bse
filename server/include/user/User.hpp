#pragma once

#include "db/sqlite.hpp"
#include "user/User.hpp"
#include "balance/Balance.hpp"

#include "sqlite3.h"
#include <pybind11/stl.h>

namespace BSE {
    class User {
    public:
        // Constructors
        User(Database &database, std::string &email);

        User(Database &database, int &user_id);

        User(Database &database, std::string &email, std::string &password);

        inline static const std::string create_table =
                "CREATE TABLE IF NOT EXISTS USER("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "email TEXT NOT NULL,"
                "password TEXT NOT NULL);";

        // Functions
        bool check_password(std::string &password);

        std::string hash(std::string &password);
        void update_balance(int change, int asset_id);


        // Getters and Setters
        std::vector<BalanceAndAsset> get_balances();

        int get_balance(int asset_id);

        int get_user_id() {
            return user_id;
        };

        std::string get_email() {
            return email;
        };



    private:
        int user_id;
        Database &db;
        std::string email;
        std::string password_hash;
    };
}  // namespace BSE
