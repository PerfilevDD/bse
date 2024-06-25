#pragma once

#include <string>
#include <vector>

#include "sqlite3.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "tradePair/trade_pair_table.hpp"
#include "order/Order.hpp"

namespace BSE {
    class TradePair {
    public:
        // Constructorsget_all_trade_pairs
        TradePair(Database &db, int trade_pair_id);

        TradePair(Database &db, int trade_pair_id, int base_asset_id, int price_asset_id);

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

        static std::vector<TradePair> get_all_trade_pairs(Database& db);

    private:
        Database db;
        int trade_pair_id;
        int price_asset;
        int base_asset;
    };
}  // namespace BSE