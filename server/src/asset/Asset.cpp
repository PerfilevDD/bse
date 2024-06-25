#include <asset/Asset.hpp>

#include "asset/asset_table.hpp"

namespace BSE {

    Asset::Asset(int asset_id) {
    }

    Asset::Asset(int asset_id, std::string name, std::string ticker) : asset_id(asset_id), name(name), ticker(ticker) {

    }

    std::vector<Asset> Asset::get_all_assets(Database &db) {
        std::vector<Asset> asset_vec;

        AssetTable assetTable;
        auto &sqlpp11 = *db.get_sqlpp11_db();

        auto results = sqlpp11(sqlpp::select(sqlpp::all_of(assetTable)).from(assetTable).unconditionally());

        for (auto &asset: results) {
            asset_vec.push_back(Asset(asset.id, asset.name, asset.ticker));
        }
        return asset_vec;
    }


}  // namespace BSE