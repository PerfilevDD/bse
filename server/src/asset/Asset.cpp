#include <asset/Asset.hpp>

#include "asset/asset_table.hpp"

namespace BSE {

    Asset::Asset(int asset_id) : asset_id(asset_id), db(*(new Database()))   {
    }

    Asset::Asset(int asset_id, const std::string& name, const std::string& ticker) : asset_id(asset_id), name(name), ticker(ticker), db(*(new Database()))  {

    }

    Asset::Asset(BSE::Database &database, const std::string& name, const std::string& ticker) : asset_id(asset_id), name(name), ticker(ticker), db(database)  {

        auto &sqlppDb = *db.get_sqlpp11_db();

        AssetTable assetTable;

        try {
            sqlppDb(sqlpp::insert_into(assetTable).set(
                    assetTable.name = name,
                    assetTable.ticker = ticker));
        } catch (const sqlpp::exception &e) {
            std::cerr << e.what() << std::endl;
        }
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