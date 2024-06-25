#pragma once
#include <string>

#include "db/sqlite.hpp"
#include "sqlite3.h"

namespace BSE {
class Order {
   public:

    Order(Database& Database,
          int trader_id,
          int pair_id,
          int price,
          int amount,
          bool buy);

    Order(Database& Database,
          int order_id);

    inline static std::string create_table =
            "CREATE TABLE IF NOT EXISTS ORDER("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "pair_id INT NOT NULL,"
            "price INT NOT NULL,"
            "amount INT NOT NULL,"
            "buy BOOL NOT NULL);";


private:
    int order_id;
    Database& db;
    int trader_id;
    int price;
    int item_amount;
};
}  // namespace BSE