#include "db/sqlite.hpp"

#include "exception"
#include "string"

std::string create_user_table = "CREATE TABLE IF NOT EXISTS USER("  \
      "ID INT PRIMARY KEY     NOT NULL," \
      "email          CHAR(50)    NOT NULL," \
      "password       CHAR(50)     NOT NULL," \
      "balance        INT DEFAULT 0);";

std::string create_assets_table = "CREATE TABLE IF NOT EXISTS ASSET("  \
      "ID INT PRIMARY KEY     NOT NULL," \
      "name          CHAR(50)    NOT NULL," \
      "ticker       CHAR(50)     NOT NULL," \
      "supply        INT DEFAULT 0);";


std::string create_trades_table = "CREATE TABLE IF NOT EXISTS TRADE("  \
      "ID INT PRIMARY KEY     NOT NULL," \
      "trade_pair          CHAR(50)    NOT NULL," \
      "price       INT     NOT NULL," \
      "in        INT DEFAULT 0," \
      "out        INT DEFAULT 0);";

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

            rc = sqlite3_exec(db, create_user_table.c_str(), callback, 0, &zErrMsg);
            rc = sqlite3_exec(db, create_assets_table.c_str(), callback, 0, &zErrMsg);
            rc = sqlite3_exec(db, create_trades_table.c_str(), callback, 0, &zErrMsg);
        }

        Database::~Database(){
            sqlite3_close(db);
        }

}