#include "db/sqlite.hpp"

#include <user/user_table.hpp>

#include "asset/Asset.hpp"
#include "exception"
#include "tradePair/TradePair.hpp"
#include "order/order_table.hpp"
#include "string"
#include "user/User.hpp"

namespace BSE {
Database::Database() {
    config = std::make_shared<sql::connection_config>();
    config->path_to_database = "bonn_stock_exchange.sqlite3";
    config->flags = SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE;

    sqlpp_db = std::make_shared<sql::connection>(sql::connection(config));
    sqlpp_db->execute(User::create_table);
    sqlpp_db->execute(TradePair::create_table);
    sqlpp_db->execute(Asset::create_table);
}

std::vector<OrderDB> Database::get_all_orders(){
    std::vector<OrderDB> tmp_vec; // pybind requests return value
    return tmp_vec;
}



struct OrderDB Database::give_order_by_id(int id){
    OrderDB tmp_str; // pybind requests return value
    return tmp_str;
}

// USER

int Database::find_user_by_email(std::string& email) {
    auto& sqlppDb = *sqlpp_db;

    UserTable userTable;

    try {
        for (const auto& row : sqlppDb(sqlpp::select(all_of(userTable)).from(userTable).where(userTable.email == email))) {
            return row.id;
        }
        return 0;
    } catch (const sqlpp::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}

// BALANCE USER
int Database::get_user_balance_frc(std::string& email) {
    auto& sqlppDb = *sqlpp_db;

    UserTable userTable;

    try {
        for (const auto& row : sqlppDb(sqlpp::select(all_of(userTable)).from(userTable).where(userTable.email == email))) {
            return row.balanceFRC;
        }
    } catch (const sqlpp::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}

int Database::get_user_balance_poeur(std::string& email) {
    auto& sqlppDb = *sqlpp_db;

    UserTable userTable;

    try {
        for (const auto& row : sqlppDb(sqlpp::select(all_of(userTable)).from(userTable).where(userTable.email == email))) {
            return row.balancePOEUR;
        }
    } catch (const sqlpp::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}

void Database::update_user_balance_poeur(std::string& email, int amount) {
    auto& sqlppDb = *sqlpp_db;

    UserTable userTable;

    try {
        sqlppDb(sqlpp::update(userTable).set(userTable.balancePOEUR += amount).where(userTable.email == email));
    } catch (const sqlpp::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}

void Database::update_user_balance_frc(std::string& email, int amount) {
    auto& sqlppDb = *sqlpp_db;

    UserTable userTable;

    try {
        sqlppDb(sqlpp::update(userTable).set(userTable.balanceFRC += amount).where(userTable.email == email));
    } catch (const sqlpp::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}

Database::~Database() {
}

}  // namespace BSE