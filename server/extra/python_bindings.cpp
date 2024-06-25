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
    pybind11::class_<Order>(m, "Order")
            .def(pybind11::init<Database &, int, int, int, int, bool>());

    pybind11::class_<OrderDB>(m, "OrderDB")
            .def(pybind11::init<>())
            .def_readwrite("id", &OrderDB::id)
            .def_readwrite("trader_id", &OrderDB::trader_id)
            .def_readwrite("item", &OrderDB::item)
            .def_readwrite("pair_item", &OrderDB::pair_item)
            .def_readwrite("price", &OrderDB::price)
            .def_readwrite("item_amount", &OrderDB::item_amount);

    pybind11::class_<Database, std::shared_ptr<Database>>(m, "Database")
            .def(pybind11::init<>())
            .def("get_sqlpp11_db", &Database::get_sqlpp11_db);

    pybind11::class_<Asset>(m, "Asset")
            .def(pybind11::init<int>());

    pybind11::class_<TradePair>(m, "TradePair")
            .def(pybind11::init<int>())
            .def("get_orders", &TradePair::get_orders)
            .def("get_open_orders", &TradePair::get_open_orders)
            .def("get_orders_as_python_list", &TradePair::get_orders_as_python_list)
            .def("create_order", &TradePair::create_order);

    pybind11::class_<User>(m, "User")
            .def(pybind11::init<Database &, std::string &>())
            .def(pybind11::init<Database &, int &>())
            .def(pybind11::init<Database &, std::string &, std::string &>())
            .def("check_password", &User::check_password)
            .def("get_balances", &User::get_balances)
            .def("get_user_id", &User::get_user_id)
            .def("update_balance", &User::update_balance);


    pybind11::class_<Balance>(m, "Balance")
            .def(pybind11::init<Database &, int, int>())
            .def("update_balance", &Balance::update_balance);
}
