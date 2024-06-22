#include "db/sqlite.hpp"

#include <user/user_table.hpp>

#include "asset/Asset.hpp"
#include "exception"
#include "marketplace/Marketplace.hpp"
#include "string"
#include "user/User.hpp"

namespace BSE {
Database::Database() {
    config = std::make_shared<sql::connection_config>();
    config->path_to_database = "bonn_stock_exchange.sqlite3";
    config->flags = SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE;

    sqlpp_db = std::make_shared<sql::connection>(sql::connection(config));
    sqlpp_db->execute(User::create_table);
    sqlpp_db->execute(Marketplace::create_table);
    sqlpp_db->execute(Asset::create_table);
}
/*
bool Database::find_user_by_email(std::string& email) {
    auto& sqlppDb = *sqlpp_db;

    UserTable userTable;

    try {
        sqlppDb(sqlpp::select(all_of(userTable)).from(userTable).where(userTable.email == email));
    } catch (const sqlpp::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}*/

bool Database::find_user_by_email(std::string& email) {
    auto& sqlppDb = *sqlpp_db;

    UserTable userTable;

    try {
        for (const auto& row : sqlppDb(sqlpp::select(userTable.email).from(userTable).where(userTable.email == email))) {
            if (row.email == email) {
                return 1;
            }
        }
        return 0;
    } catch (const sqlpp::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}

Database::~Database() {
}

}  // namespace BSE