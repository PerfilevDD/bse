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

   private:
    Database& db;
    int trader_id;
    std::string item;
    std::string pair_item;
    int price;
    int item_amount;
};
}  // namespace BSE