#pragma once

#include "db/sqlite.hpp"
#include "sqlite3.h"
#include "string"

namespace BSE {
class User {
   public:
    User(Database& database, std::string& email);
    User(Database& database, std::string& email, std::string& password);

    bool check_password(std::string& password);

    int get_balance();
    int get_user_id() {
        return user_id;
    };

    void update_balance(int change);

    std::string hash(std::string& password);

    inline static const std::string create_table =
        "CREATE TABLE IF NOT EXISTS USER("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "email TEXT NOT NULL,"
        "password TEXT NOT NULL,"
        "balance INTEGER DEFAULT 100);";

   private:
    int user_id;
    Database& db;
    std::string email;
    std::string password_hash;
};
}  // namespace BSE
