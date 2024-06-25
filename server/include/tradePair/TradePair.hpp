#pragma once

#include <string>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


#include "order/Order.hpp"

namespace BSE {
    class TradePair {
    public:
        // Constructors
        TradePair(int trade_pair_id);

        //TradePair(int asset_1_id, int sset_2_id);
        inline static std::string create_table =
                "CREATE TABLE IF NOT EXISTS TRADEPAIR("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "base_asset INT NOT NULL,"
                "price_asset TEXT NOT NULL);";

        // Functions
        void create_order(int pair_id, int trader_id, int amount, int price, bool buy);

        // Getters and Setters
        std::vector<Order> get_orders(int trade_pair_id, bool completed);

        std::vector<Order> get_open_orders(int trade_pair_id) {
            return get_orders(trade_pair_id, false);
        };

        pybind11::list get_orders_as_python_list(int trade_pair_id);

    private:
        int id{};
        Database db;
        int price_asset{};
        int base_asset{};
    };
}  // namespace BSE