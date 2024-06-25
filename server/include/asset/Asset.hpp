#pragma once

#include <string>

#include "db/sqlite.hpp"

namespace BSE {
    class Asset {
    public:
        // Constructors
        Asset(int asset_id);

        Asset(int asset_id, std::string name, std::string ticker);

        inline static std::string create_table = 
              "CREATE TABLE IF NOT EXISTS ASSET("  \
              "id INTEGER PRIMARY KEY        AUTOINCREMENT," \
              "name          CHAR(50)       NOT NULL," \
              "ticker       CHAR(50)        NOT NULL," \
              "supply        INT            DEFAULT 0);";

        // Getters & Setters
        static std::vector<Asset> get_all_assets(Database &db);

        int get_asset_id() {
            return asset_id;
        }

        std::string get_asset_name() {
            return name;
        }

        std::string get_asset_ticker() {
            return ticker;
        }


    private:
        std::string name;
        std::string ticker;
        int asset_id;

    };

}