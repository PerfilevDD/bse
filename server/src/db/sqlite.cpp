#include "db/sqlite.hpp"

#include "exception"
#include "string"

#include "user/User.hpp"
#include "marketplace/Marketplace.hpp"
#include "asset/Asset.hpp"




namespace BSE {
        Database::Database(){


            config = std::make_shared<sql::connection_config>();
            config->path_to_database = "bonn_stock_exchange.sql";
            config->flags = SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE;

            sqlpp_db = std::make_shared<sql::connection>(sql::connection(config));
            sqlpp_db->execute(User::create_table);
            sqlpp_db->execute(Marketplace::create_table);
            sqlpp_db->execute(Asset::create_table);
        }

        Database::~Database(){
        }

}