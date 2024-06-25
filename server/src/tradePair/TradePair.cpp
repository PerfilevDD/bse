#include <tradePair/TradePair.hpp>
#include <pybind11/cast.h>
#include "sqlpp11/select.h"
#include "order/order_table.hpp"
#include "list"
#include "user/User.hpp"

#include <algorithm>

namespace BSE {


    void TradePair::create_order(int pair_id, int trader_id, int amount, int price, bool buy) {
        auto &sqlpp11 = *db.get_sqlpp11_db();
        auto tx = start_transaction(sqlpp11);
        try {
            std::vector<Order> orders = get_open_orders(pair_id);
            User user = User(db, trader_id);
            if (buy) {
                user.update_balance(-(amount * price), price_asset);
            } else {
                user.update_balance(-(amount), base_asset);
            }

            std::list<Order> matched_orders;
            for (auto &order: orders) {
                // Check if the order is buy -> Match all orders with the same or lower price
                // If sell order then take all orders with a higher price
                if ((order.is_buy() && order.get_price() <= price) || (!order.is_buy() && order.get_price() >= price)) {
                    // If user wants to buy then we need to process the matching orders in ascending order (small to big)
                    // If he wants to sell then we need to match the smalles order first
                    // The orders are sorted ascending by default so the later the order the bigger the amount
                    if (buy)
                        matched_orders.push_back(order);
                    else
                        matched_orders.push_front(order);
                }
            }

            Order new_order = Order(db, trader_id, pair_id, price, amount, buy);

            for (auto &order: matched_orders) {
                if (new_order.get_fullfilled_amount() >= new_order.get_amount()) {
                    new_order.set_completed(true);
                }


                int amount_to_update;
                int matched_order_unfullfilled_amount = order.get_amount() - order.get_fullfilled_amount();
                int new_order_unfullfilled_amount = new_order.get_amount() - new_order.get_fullfilled_amount();
                if (matched_order_unfullfilled_amount > new_order_unfullfilled_amount) {
                    amount_to_update = new_order_unfullfilled_amount;
                } else {
                    amount_to_update = matched_order_unfullfilled_amount;
                }

                new_order.set_fullfilled_amount(new_order.get_fullfilled_amount() + amount_to_update);
                order.set_fullfilled_amount(order.get_fullfilled_amount() + amount_to_update);

                int partner_user_id = order.get_trader_id();
                User partner_user = User(db, partner_user_id);
                if (buy) {
                    // Es wurde eine Kaufen Order gematch -> Trader bekommt amount an base_asset
                    // Partner bekommt amount * price in price_asset
                    user.update_balance(amount_to_update, base_asset);
                    partner_user.update_balance(amount_to_update * order.get_price(), price_asset);

                } else {
                    // Es wurde eine Verkaufen Order gematch
                    partner_user.update_balance(amount_to_update, base_asset);
                    user.update_balance(amount_to_update * order.get_price(), price_asset);
                }
            }

            tx.commit();
        } catch (...) {
            tx.rollback();
            throw std::exception();

        }


    }

    std::vector<Order> TradePair::get_orders(int trade_pair_id, bool completed) {
        auto &sqlppDb = *db.get_sqlpp11_db();

        std::vector<Order> orders;
        OrderTable orderTable;
        try {
            for (const auto &row: sqlppDb(sqlpp::select(all_of(orderTable)).from(orderTable)
                                                  .order_by(orderTable.price.asc())
                                                  .where((orderTable.pair_id == trade_pair_id &&
                                                          orderTable.completed == completed)))) {
                Order order(
                        db,
                        row.trader_id,
                        row.pair_id,
                        row.price,
                        row.amount,
                        row.fullfilled_amount,
                        row.completed,
                        row.buy
                );
                orders.push_back(order);
            }
        } catch (const sqlpp::exception &e) {
            std::cerr << e.what() << std::endl;
        }

        return orders;
    }

    TradePair::TradePair(Database &db, int trade_pair_id) : trade_pair_id(trade_pair_id), db(db) {
        TradePairTable tradePairTable;

        auto &sqlpp11 = *db.get_sqlpp11_db();

        auto results = sqlpp11(sqlpp::select(sqlpp::all_of(tradePairTable)).from(tradePairTable).where(
                tradePairTable.id == trade_pair_id));
        for (auto &trade_pair: results) {
            price_asset = trade_pair.price_asset;
            base_asset = trade_pair.base_asset;
            return;
        }

        throw std::exception();
    }

    TradePair::TradePair(Database &db, int trade_pair_id, int base_asset_id, int price_asset_id) : trade_pair_id(
            trade_pair_id),
                                                                                                   price_asset(
                                                                                                           price_asset_id),
                                                                                                   base_asset(
                                                                                                           base_asset_id),
                                                                                                   db(db) {
    }


    pybind11::list TradePair::get_orders_as_python_list(int trade_pair_id) {
        pybind11::list orders_list = pybind11::cast(get_open_orders(trade_pair_id));
        return orders_list;
    }

    static std::vector<TradePair> get_all_trade_pairs(Database &db) {
        auto &sqlpp11 = *db.get_sqlpp11_db();

        std::vector<TradePair> trade_pair_vec;

        TradePairTable tradePairTable;

        auto results = sqlpp11(sqlpp::select(sqlpp::all_of(tradePairTable)).from(tradePairTable).unconditionally());

        for (auto &trade_pair: results) {
            trade_pair_vec.push_back(TradePair(db, trade_pair.id, trade_pair.base_asset, trade_pair.price_asset));
        }
        return trade_pair_vec;


    }
}