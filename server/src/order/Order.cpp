#include <sqlpp11/sqlite3/sqlite3.h>
#include <sqlpp11/sqlpp11.h>

#include <db/sqlite.hpp>
#include <iostream>
#include <sstream>
#include <order/Order.hpp>
#include <order/order_table.hpp>
#include <date/date.h>
#include <date/tz.h>

namespace BSE {

    Order::Order(Database &Database,
                 int trader_id,
                 int pair_id,
                 int price,
                 int amount,
                 bool buy) : db(Database),
                             trader_id(trader_id),
                             pair_id(pair_id),
                             price(price),
                             amount(amount),
                             buy(buy),
                             fullfilled_amount(0),
                             completed(false) {
        auto &sqlppDb = *db.get_sqlpp11_db();

        OrderTable orderTable;

        try {
            sqlppDb(sqlpp::insert_into(orderTable).set(
                    orderTable.trader_id = trader_id,
                    orderTable.price = price,
                    orderTable.amount = amount,
                    orderTable.pair_id = pair_id,
                    orderTable.completed = false,
                    orderTable.fullfilled_amount = 0,
                    orderTable.buy = buy));
        } catch (const sqlpp::exception &e) {
            std::cerr << e.what() << std::endl;
        }
    }

    Order::Order(BSE::Database &Database, int order_id) : db(Database), order_id(order_id) {
        auto &sqlppDb = *db.get_sqlpp11_db();

        OrderTable orderTable;

        try {
            for (const auto &row: sqlppDb(
                    sqlpp::select(all_of(orderTable)).from(orderTable).where(orderTable.id == order_id))) {
                trader_id = row.trader_id;
                price = row.price;
                pair_id = row.pair_id;
                buy = row.buy;
                amount = row.amount;
                completed = row.completed;
                fullfilled_amount = row.fullfilled_amount;
                return;
            }
        } catch (const sqlpp::exception &e) {
            std::cerr << e.what() << std::endl;
        }

        throw std::exception();

    }

    Order::Order(Database &Database,
                 int trader_id,
                 int pair_id,
                 int price,
                 int amount,
                 int fullfilled_amount,
                 bool completed,
                 bool buy) : db(Database),
                             trader_id(trader_id),
                             pair_id(pair_id),
                             price(price),
                             amount(amount),
                             buy(buy),
                             completed(completed),
                             fullfilled_amount(fullfilled_amount) {}

    void Order::set_completed(bool c) {
        auto &sqlpp11 = *db.get_sqlpp11_db();
        OrderTable orderTable;

        auto timestamp_UTC = std::chrono::system_clock::now();

        sqlpp11(sqlpp::update(orderTable).set(orderTable.completed = c,
                                              orderTable.completed_timestamp = timestamp_UTC).where(
                orderTable.id == order_id));
        completed = c;
    }

    void Order::set_fullfilled_amount(int new_fullfilled_amount) {
        auto &sqlpp11 = *db.get_sqlpp11_db();
        OrderTable orderTable;

        sqlpp11(sqlpp::update(orderTable).set(orderTable.fullfilled_amount = new_fullfilled_amount).where(
                orderTable.id == order_id));
        fullfilled_amount = new_fullfilled_amount;

    }


}  // namespace BSE
