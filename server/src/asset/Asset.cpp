#include <asset/Asset.hpp>

namespace BSE {

    Asset::Asset(int asset_id) {
    }

    Asset::Asset(int asset_id, std::string name, std::string ticker) : asset_id(asset_id), name(name), ticker(ticker) {

    }

}  // namespace BSE