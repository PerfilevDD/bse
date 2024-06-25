#pragma once
#include <string>

#include "db/sqlite.hpp"
#include "sqlite3.h"

namespace BSE {
class Order {
   public:
    Order(int id);

    Order(Database& Database,
          int trader_id,
          std::string& item,
          std::string& pair_item,
          int price,
          int item_amount);

    Order(Database& Database,
          int order_id);

   private:
    int order_id;
    Database& db;
    int trader_id;
    std::string item;
    std::string pair_item;
    int price;
    int item_amount;
};
}  // namespace BSE