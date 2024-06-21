#pragma once

namespace BSE {
    class Marketplace {
    public:
        Marketplace(int marketplace_id);
        Marketplace(int asset_1_id, int asset_2_id);

        int price_asset_1();
        int price_asset_2();

        int estimate_sell_asset_1(int amount);
        int sell_asset_1(int amount);

        int estimate_sell_asset_2(int amount);
        int sell_asset_2(int amount);


        inline static std::string create_table = "CREATE TABLE IF NOT EXISTS MARKETPLACE("  \
          "id INT PRIMARY KEY     NOT NULL," \
          "trade_pair          CHAR(50)    NOT NULL," \
          "price       INT     NOT NULL," \
          "in_asset_amount        INT DEFAULT 0," \
          "out_asset_amount        INT DEFAULT 0);";

    private:
        int supply_good_1 = 0;
        int supply_good_2 = 0;
    };
}