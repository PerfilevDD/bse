#include "db/sqlite.hpp"

#include "exception"
#include "string"

#include "user/User.hpp"
#include "marketplace/Marketplace.hpp"
#include "asset/Asset.hpp"


static int callback(void *NotUsed, int argc, char **argv, char **azColName) {
    int i;
    for(i = 0; i<argc; i++) {
        printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
    }
    printf("\n");
    return 0;
}

namespace BSM {
        Database::Database(){
            char *zErrMsg = 0;
            int rc;

            rc = sqlite3_open("bonn_stock_exchange.sql", &db);

            if( rc ) {
                fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
            } else {
                fprintf(stderr, "Opened database successfully\n");
            }



            rc = sqlite3_exec(db, User::create_table.c_str(), callback, 0, &zErrMsg);
            rc = sqlite3_exec(db, Asset::create_table.c_str(), callback, 0, &zErrMsg);
            rc = sqlite3_exec(db, Marketplace::create_table.c_str(), callback, 0, &zErrMsg);
        }

        Database::~Database(){
            sqlite3_close(db);
        }

}