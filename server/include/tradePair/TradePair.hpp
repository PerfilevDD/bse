#pragma once
#include <string>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


#include "order/Order.hpp"

namespace BSE {
class TradePair {
   public:
    TradePair(int trade_pair_id);
    TradePair(int asset_1_id, int asset_2_id);

    std::vector<Order> get_orders();
    pybind11::list get_orders_as_python_list();

    void create_order(int trader_id, int amount, int price, bool buy);
    inline static std::string create_table =
        "CREATE TABLE IF NOT EXISTS TRADEPAIR("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "base_asset INT NOT NULL,"
        "price_asset TEXT NOT NULL);";

   private:
    int id;
    Database db;
    int supply_good_1 = 0;
    int supply_good_2 = 0;
};
}  // namespace BSE