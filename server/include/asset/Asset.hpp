#pragma once

#include <string>

namespace BSE {
    class Asset {
    public:
        // Constructors
        Asset(int asset_id);

        inline static std::string create_table = "CREATE TABLE IF NOT EXISTS ASSET("  \
              "id INT PRIMARY KEY           NOT NULL," \
              "name          CHAR(50)       NOT NULL," \
              "ticker       CHAR(50)        NOT NULL," \
              "supply        INT            DEFAULT 0);";

        // Getters & Setters
        int get_asset_id() {
            return asset_id;
        }

    private:
        std::string name;
        std::string ticker;
        int asset_id;

    };

}