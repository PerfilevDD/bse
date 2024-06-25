#include "db/sqlite.hpp"

#include <user/user_table.hpp>

#include "asset/Asset.hpp"
#include "exception"
#include "tradePair/TradePair.hpp"
#include "order/order_table.hpp"
#include "string"
#include "user/User.hpp"
#include "asset/asset_table.hpp"

namespace BSE {
    Database::Database() {
        config = std::make_shared<sql::connection_config>();
        config->path_to_database = "bonn_stock_exchange.sqlite3";
        config->flags = SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE;

        sqlpp_db = std::make_shared<sql::connection>(sql::connection(config));
        sqlpp_db->execute(User::create_table);
        sqlpp_db->execute(TradePair::create_table);
        sqlpp_db->execute(Asset::create_table);
        sqlpp_db->execute(Balance::create_table);
        sqlpp_db->execute(Order::create_table);
    }


    Database::~Database() {
    }

    std::vector<Asset> Database::get_assets() {
        std::vector<Asset> asset_vec;

        AssetTable assetTable;
        auto &sqlpp11 = *get_sqlpp11_db();

        auto results = sqlpp11(sqlpp::select(sqlpp::all_of(assetTable)).from(assetTable).unconditionally());

        for (auto &asset: results) {
            asset_vec.push_back(Asset(asset.id, asset.name, asset.ticker));
        }
        return asset_vec;
    }

}  // namespace BSE