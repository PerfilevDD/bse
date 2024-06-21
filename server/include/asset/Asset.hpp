#pragma once

namespace BSE {
    class Asset {
    public:
        Asset(int asset_id);

        inline static std::string create_table = "CREATE TABLE IF NOT EXISTS ASSET("  \
              "id INT PRIMARY KEY     NOT NULL," \
              "name          CHAR(50)    NOT NULL," \
              "ticker       CHAR(50)     NOT NULL," \
              "supply        INT DEFAULT 0);";


    };
}