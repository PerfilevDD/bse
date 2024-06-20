#pragma once

namespace BSM {
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

    private:
        int supply_good_1 = 0;
        int supply_good_2 = 0;
    };
}