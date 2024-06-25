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


}  // namespace BSE