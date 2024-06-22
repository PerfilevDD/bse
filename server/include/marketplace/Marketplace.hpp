#pragma once
#include <string>

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

    inline static std::string create_table =
        "CREATE TABLE IF NOT EXISTS MARKETPLACE("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "trader_id INTEGER NOT NULL,"
        "item TEXT NOT NULL,"
        "pair_item TEXT NOT NULL,"
        "price INTEGER NOT NULL,"
        "item_amount INTEGER NOT NULL);";

   private:
    int supply_good_1 = 0;
    int supply_good_2 = 0;
};
}  // namespace BSE