#pragma once

#include "db/sqlite.hpp"
#include "string"

namespace BSE {
    class Balance {
    public:
        Balance(Database &database, int user_id, int asset_id);

        inline static std::string create_table = "CREATE TABLE IF NOT EXISTS BALANCE("  \
              "user_id INT           NOT NULL," \
              "asset_id          INT       NOT NULL," \
              "balance        INT            DEFAULT 0," \
             "PRIMARY KEY (user_id, asset_id));";


        void update_balance(int change);

    private:
        int balance;
        int asset_id;
        int user_id;

        Database &database;
    };

    struct BalanceAndAsset {
        int balance;
        std::string name;
        std::string ticker;
    };
}
