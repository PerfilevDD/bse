#pragma once

#include <string>

#include "db/sqlite.hpp"
#include "sqlite3.h"

namespace BSE {
    class Order {
    public:


        // Constructor for new orders -> Performs an insert
        Order(Database &Database,
              int trader_id,
              int pair_id,
              int price,
              int amount,
              bool buy);

        // Constructor to create existing orders without insert
        Order(Database &Database,
              int trader_id,
              int pair_id,
              int price,
              int amount,
              int fullfilled_amount,
              bool completed,
              bool buy);


        Order(Database &Database,
              int order_id);

        inline static std::string create_table =
                "CREATE TABLE IF NOT EXISTS ORDER("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "trader_id INT NOT NULL,"
                "pair_id INT NOT NULL,"
                "price INT NOT NULL,"
                "amount INT NOT NULL,"
                "fullfilled_amount INT NOT NULL,"
                "completed BOOL NOT NULL DEFAULT FALSE,"
                "buy BOOL NOT NULL);";

        int get_price() const {
            return price;
        }

        int get_amount() const {
            return amount;
        }

        int get_fullfilled_amount() const {
            return fullfilled_amount;
        }

        int get_trader_id() const {
            return trader_id;
        }

        bool is_completed() {
            return completed;
        }

        bool is_buy() {
            return buy;
        }

        void set_completed(bool c);

        void set_fullfilled_amount(int new_fullfilled_amount);


    private:
        int order_id;
        Database &db;
        int trader_id;
        int pair_id;
        int price;
        int amount;
        int fullfilled_amount;
        bool buy;
        bool completed;
    };
}  // namespace BSE