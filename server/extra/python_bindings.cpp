#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <asset/Asset.hpp>
#include <tradePair/TradePair.hpp>
#include <order/Order.hpp>
#include <user/User.hpp>
#include <vector>

#include "db/sqlite.hpp"
#include "string"

using namespace BSE;

PYBIND11_MODULE(BSE, m) {
    m.doc() = "BSE";

    pybind11::register_exception<std::invalid_argument>(m, "invalid_argument");
    pybind11::register_exception<std::exception>(m, "exception");
    pybind11::register_exception<std::bad_alloc>(m, "bad_alloc");
    pybind11::register_exception<std::domain_error>(m, "domain_error");
    pybind11::register_exception<std::length_error>(m, "length_error");
    pybind11::register_exception<std::out_of_range>(m, "out_of_range");
    pybind11::register_exception<std::range_error>(m, "range_error");
    pybind11::register_exception<std::overflow_error>(m, "overflow_error");

    pybind11::class_<Order>(m, "Order")
            .def(pybind11::init<Database &, int, int, int, int, bool>())
            .def(pybind11::init<Database &, int, int, int, int, int, int, bool, bool>())
            .def(pybind11::init<Database &, int, int, int, int, int, int, std::string&, bool, bool>())
            .def(pybind11::init<Database &, int>())
            .def("get_trader_id", &Order::get_trader_id)
            .def("get_price", &Order::get_price)
            .def("get_amount", &Order::get_amount)
            .def("get_order_id", &Order::get_order_id)
            .def("get_pair_id", &Order::get_pair_id)
            .def("get_completed_timestamp", &Order::get_completed_timestamp)
            .def("get_fullfilled_amount", &Order::get_fullfilled_amount)
            .def_static("get_all_completed_orders", &Order::get_all_completed_orders)
            .def("is_buy", &Order::is_buy)
            .def("set_completed", &Order::set_completed)
            .def("is_completed", &Order::is_completed);

    pybind11::class_<OrderDB>(m, "OrderDB")
            .def(pybind11::init<>())
            .def_readwrite("id", &OrderDB::id)
            .def_readwrite("trader_id", &OrderDB::trader_id)
            .def_readwrite("item", &OrderDB::item)
            .def_readwrite("pair_item", &OrderDB::pair_item)
            .def_readwrite("price", &OrderDB::price)
            .def_readwrite("item_amount", &OrderDB::item_amount);


    pybind11::class_<BalanceAndAsset>(m, "BalanceAndAsset")
            .def(pybind11::init<>())
            .def_readwrite("balance", &BalanceAndAsset::balance)
            .def_readwrite("name", &BalanceAndAsset::name)
            .def_readwrite("ticker", &BalanceAndAsset::ticker);

    pybind11::class_<Database, std::shared_ptr<Database>>(m, "Database")
            .def(pybind11::init<>())
            .def("get_sqlpp11_db", &Database::get_sqlpp11_db);

    pybind11::class_<Asset>(m, "Asset")
            .def(pybind11::init<int>())
            .def(pybind11::init<int, std::string &, std::string &>())
            .def(pybind11::init<Database &, std::string &, std::string &>())
            .def_static("get_all_assets", &Asset::get_all_assets)
            .def("get_asset_id", &Asset::get_asset_id)
            .def("get_asset_ticker", &Asset::get_asset_ticker)
            .def("get_asset_name", &Asset::get_asset_name);


    pybind11::class_<TradePair>(m, "TradePair")
            .def(pybind11::init<Database &, int>())
            .def(pybind11::init<Database &, int, int>())
            .def(pybind11::init<Database &, int, int, int>())
            .def("get_orders", &TradePair::get_orders)
            .def("get_open_orders", &TradePair::get_open_orders)
            .def("get_orders_as_python_list", &TradePair::get_orders_as_python_list)
            .def_static("get_all_trade_pairs", &TradePair::get_all_trade_pairs)
            .def("get_base_asset", &TradePair::get_base_asset)
            .def("get_price_asset", &TradePair::get_price_asset)
            .def("get_trade_pair_id", &TradePair::get_trade_pair_id)
            .def("create_order", &TradePair::create_order);

    pybind11::class_<User>(m, "User")
            .def(pybind11::init<Database &, std::string &>())
            .def(pybind11::init<Database &, int &>())
            .def(pybind11::init<Database &, std::string &, std::string &>())
            .def("check_password", &User::check_password)
            .def("get_balances", &User::get_balances)
            .def("get_user_id", &User::get_user_id)
            .def("get_balance", &User::get_balance)
            .def("update_balance", &User::update_balance);


    pybind11::class_<Balance>(m, "Balance")
            .def(pybind11::init<Database &, int, int>())
            .def("update_balance", &Balance::update_balance);
}
