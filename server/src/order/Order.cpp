#include <sqlpp11/sqlite3/sqlite3.h>
#include <sqlpp11/sqlpp11.h>

#include <db/sqlite.hpp>
#include <iostream>
#include <sstream>
#include <order/Order.hpp>
#include <marketplace/marketplace_table.hpp>

namespace BSE {

Order::Order(Database& Database,
             int trader_id,
             std::string& item,
             std::string& pair_item,
             int price,
             int pair_price,
             int item_amount,
             int pair_amount) : db(Database),
                                trader_id(trader_id),
                                item(item),
                                pair_item(pair_item),
                                price(price),
                                pair_price(pair_price),
                                item_amount(item_amount),
                                pair_amount(pair_amount) {
    auto& sqlppDb = *db.get_sqlpp11_db();

    MarketplaceTable marketplaceTable;
    std::cout << item << std::endl;
    try {
        sqlppDb(sqlpp::insert_into(marketplaceTable).set(
            marketplaceTable.trader_id = trader_id,
            marketplaceTable.item = item,
            marketplaceTable.pair_item = pair_item,
            marketplaceTable.price = price,
            marketplaceTable.pair_price = pair_price,
            marketplaceTable.item_amount = item_amount,
            marketplaceTable.pair_amount = pair_amount));
    } catch (const sqlpp::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}

}  // namespace BSE
