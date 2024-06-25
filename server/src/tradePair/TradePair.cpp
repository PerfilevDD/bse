#include <tradePair/TradePair.hpp>
#include <pybind11/cast.h>
#include "sqlpp11/select.h"
#include "order/order_table.hpp"


namespace BSE {


    void TradePair::create_order(int trader_id, int amount, int price, bool buy) {

    }

    std::vector<Order> TradePair::get_orders() {
        auto& sqlppDb = *db.get_sqlpp11_db();

        std::vector<Order> orders;
        OrderTable orderTable;
        try {
            for (const auto& row : sqlppDb(sqlpp::select(all_of(orderTable)).from(orderTable).unconditionally())) {
                Order order(
                        db,
                        row.trader_id,
                        row.pair_id,
                        row.price,
                        row.amount,
                        row.buy,
                        false
                        );
                orders.push_back(order);
            }
        } catch (const sqlpp::exception& e) {
            std::cerr << e.what() << std::endl;
        }

        return orders;
    }

    TradePair::TradePair(int trade_pair_id) {

    }

    /*pybind11::list TradePair::get_orders_as_python_list() {
        pybind11::list orders_list = pybind11::cast(get_orders());
        return orders_list;
    }*/
}  // namespace BSE