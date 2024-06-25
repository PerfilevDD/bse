#include "balance/Balance.hpp"
#include "balance/balance_table.hpp"

#include <sqlpp11/sqlpp11.h>

namespace BSE {
    Balance::Balance(Database &database, int user_id, int asset_id) : database(database), user_id(user_id),
                                                                      asset_id(asset_id) {
        auto &sqlppDb = *database.get_sqlpp11_db();
        BalanceTable balanceTable;

        auto results = sqlppDb(sqlpp::select(balanceTable.balance, balanceTable.asset_id, balanceTable.user_id).from(balanceTable).where(
                balanceTable.asset_id == asset_id && balanceTable.user_id == user_id));
        for (auto &db_balance: results) {
            balance = db_balance.balance;
            return;
        }

        // If we arrived here then no balance is existing for the user
        balance = 0;
        try {
            sqlppDb(sqlpp::insert_into(balanceTable).set(
                    balanceTable.asset_id = asset_id,
                    balanceTable.user_id = user_id,
                    balanceTable.balance = 0));
        } catch (const sqlpp::exception &e) {
            throw std::exception();
        }
    }

    void Balance::update_balance(int change) {
        balance += change;

        // Update database
        auto &sqlppDb = *database.get_sqlpp11_db();
        BalanceTable balanceTable;

        sqlppDb(sqlpp::update(balanceTable).set(balanceTable.balance = balance).where(
                balanceTable.asset_id == asset_id && balanceTable.user_id == user_id));


    }
}