#include <pybind11/pybind11.h>

#include <asset/Asset.hpp>
#include <marketplace/Marketplace.hpp>
#include <user/User.hpp>
#include "string"

using namespace BSM;

PYBIND11_MODULE(BSM, m) {
    m.doc() = "BSM";
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
        .def(pybind11::init<int>())
        .def(pybind11::init<std::string&, std::string&>())
        .def("check_password", &User::check_password)
        .def("get_balance", &User::get_balance)
        .def("get_user_id", &User::get_user_id)
        .def("update_balance", &User::update_balance);
}
