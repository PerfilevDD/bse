#include <asset/Asset.hpp>

#include "asset/asset_table.hpp"

namespace BSE {

    Asset::Asset(int asset_id) : asset_id(asset_id), db(*(new Database()))   {      // Initialisiert ein Asset-Objekt mit einer gegebenen asset_id und erstellt eine neue Database-Instanz.
    }

    Asset::Asset(int asset_id, const std::string& name, const std::string& ticker) : asset_id(asset_id), name(name), ticker(ticker), db(*(new Database()))  { 
    // Initialisiert ein Asset-Objekt mit den gegebenen Werten für asset_id, name, und ticker, und erstellt eine neue Database-Instanz.

    }

    Asset::Asset(BSE::Database &database, const std::string& name, const std::string& ticker) : asset_id(asset_id), name(name), ticker(ticker), db(database)  {

        auto &sqlppDb = *db.get_sqlpp11_db();

        AssetTable assetTable;

        try {
            sqlppDb(sqlpp::insert_into(assetTable).set(
                    assetTable.name = name,
                    assetTable.ticker = ticker));
        // SQL-Abfrage ausführen, um ein neues Asset mit dem angegebenen Namen und Ticker in die Asset-Tabelle einzufügen.
        } catch (const sqlpp::exception &e) {
            std::cerr << e.what() << std::endl;
        // Ausnahmebehandlung: Falls ein SQL-Fehler auftritt, wird die Fehlermeldung auf der Standardfehlerausgabe (cerr) ausgegeben.
        }
    }

    std::vector<Asset> Asset::get_all_assets(Database &db) {        // Ruft alle Assets aus der Datenbank ab
        std::vector<Asset> asset_vec;                               // Dann wird das als Vektor von "Asset"-Objekten zurückgegeben

        AssetTable assetTable;
        auto &sqlpp11 = *db.get_sqlpp11_db();

        auto results = sqlpp11(sqlpp::select(sqlpp::all_of(assetTable)).from(assetTable).unconditionally());

        for (auto &asset: results) {
            asset_vec.push_back(Asset(asset.id, asset.name, asset.ticker));
        }
        return asset_vec;       // Dann wird der Vektor "asset_vec" zurück
    }


}  // namespace BSE