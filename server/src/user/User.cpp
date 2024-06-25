#include <sqlpp11/sqlite3/sqlite3.h>
#include <sqlpp11/sqlpp11.h>

#include <db/sqlite.hpp>
#include <iostream>
#include <sstream>
#include <user/User.hpp>
#include <user/user_table.hpp>

namespace BSE {

std::string User::hash(std::string& password) {
    size_t phash = std::hash<std::string>{}(password);
    std::ostringstream oss;
    oss << phash;
    return oss.str();
}

User::User(BSE::Database &database, int &user_id): user_id(user_id), db(database) {
    auto& sqlppDb = *db.get_sqlpp11_db();

    UserTable userTable;

    auto results = sqlppDb(
            sqlpp::select(all_of(userTable)).
            from(userTable).
            where(userTable.id == user_id));

    if (results.empty())
        throw std::invalid_argument("User not found");

    const auto& result = results.front();
    email = result.email;
    password_hash = result.password;
}

User::User(Database& database, std::string& email) : db(database), email(email) {
    auto& sqlppDb = *db.get_sqlpp11_db();

    UserTable userTable;

    for (const auto& row : sqlppDb(sqlpp::select(userTable.password).from(userTable).where(userTable.email == email))) {
        password_hash = row.password;
    }
    std::cout << "hash " << password_hash << std::endl;
}

User::User(Database& database, std::string& email, std::string& password)
    : db(database), email(email), password_hash(hash(password)) {
    auto& sqlppDb = *db.get_sqlpp11_db();

    UserTable userTable;

    try {
        sqlppDb(sqlpp::insert_into(userTable).set(
            userTable.email = email,
            userTable.password = password_hash,
            userTable.balanceFRC = 10,
            userTable.balancePOEUR = 101));
    } catch (const sqlpp::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}

bool User::check_password(std::string& password) {
    std::cout << "pass " << password << std::endl;
    std::cout << "hash " << password_hash << std::endl;
    return password_hash == hash(password);
}

int User::get_balance() {
    return 0;
}

void User::update_balance(int change, int asset_id) {
}
}  // namespace BSE
