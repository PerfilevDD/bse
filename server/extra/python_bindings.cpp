#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <asset/Asset.hpp>
#include <marketplace/Marketplace.hpp>
#include <order/Order.hpp>
#include <user/User.hpp>

#include "db/sqlite.hpp"
#include "string"

using namespace BSE;

PYBIND11_MODULE(BSE, m) {
    m.doc() = "BSE";
    pybind11::class_<Order>(m, "Order")
        .def(pybind11::init<Database&, int, std::string&, std::string&, int, int, int, int>());

    pybind11::class_<Database, std::shared_ptr<Database>>(m, "Database")
        .def(pybind11::init<>())
        .def("get_sqlpp11_db", &Database::get_sqlpp11_db)
        .def("find_user_by_email", &Database::find_user_by_email);

    pybind11::class_<Asset>(m, "Asset")
        .def(pybind11::init<int>());

    pybind11::class_<Marketplace>(m, "Marketplace")
        .def(pybind11::init<int>())
        .def(pybind11::init<int, int>())
        .def("price_asset_1", &Marketplace::price_asset_1)
        .def("price_asset_2", &Marketplace::price_asset_2)
        .def("estimate_sell_asset_1", &Marketplace::estimate_sell_asset_1)
        .def("sell_asset_1", &Marketplace::sell_asset_1)
        .def("estimate_sell_asset_2", &Marketplace::estimate_sell_asset_2)
        .def("sell_asset_2", &Marketplace::sell_asset_2);

    pybind11::class_<User>(m, "User")
        .def(pybind11::init<Database&, std::string&>())
        .def(pybind11::init<Database&, std::string&, std::string&>())
        .def("check_password", &User::check_password)
        .def("get_balance", &User::get_balance)
        .def("get_user_id", &User::get_user_id)
        .def("update_balance", &User::update_balance);
}
