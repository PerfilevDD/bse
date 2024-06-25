#include <sqlpp11/sqlite3/sqlite3.h>
#include <sqlpp11/sqlpp11.h>

#include <db/sqlite.hpp>
#include <iostream>
#include <sstream>
#include <order/Order.hpp>
#include <order/order_table.hpp>

namespace BSE {

Order::Order(Database& Database,
             int trader_id,
             int pair_id,
             int price,
             int item_amount,
             bool buy) : db(Database),
                                trader_id(trader_id),
                                price(price),
                                item_amount(item_amount) {
    auto& sqlppDb = *db.get_sqlpp11_db();

    OrderTable orderTable;

    try {
        sqlppDb(sqlpp::insert_into(orderTable).set(
            orderTable.trader_id = trader_id,
            orderTable.price = price,
            orderTable.item_amount = item_amount));
    } catch (const sqlpp::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}

Order::Order(BSE::Database &Database, int order_id): db(Database), order_id(order_id) {}

}  // namespace BSE
