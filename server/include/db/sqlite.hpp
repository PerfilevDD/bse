#pragma once

#include <sqlite3.h>
#include <sqlpp11/sqlite3/connection.h>

#include "vector"

namespace BSE {
namespace sql = sqlpp::sqlite3;

struct OrderDB {
    int id;
    int trader_id;
    std::string item;
    std::string pair_item;
    int price;
    int item_amount;
};

class Database {
   public:
    Database();
    ~Database();

    std::shared_ptr<sql::connection> get_sqlpp11_db() {
        return sqlpp_db;
    }

    bool find_user_by_email(std::string& email);

    struct OrderDB give_order_by_id(int id);

    std::vector<OrderDB> get_all_orders();

   private:
    std::shared_ptr<sql::connection_config> config;
    std::shared_ptr<sql::connection> sqlpp_db;
};
}  // namespace BSE