#include <sqlpp11/sqlpp11.h>

#include <db/sqlite.hpp>
#include <iostream>
#include <sstream>
#include <user/User.hpp>
#include <user/user_table.hpp>
#include "asset/asset_table.hpp"
#include "balance/balance_table.hpp"

namespace BSE {

    std::string User::hash(std::string &password) {
        size_t phash = std::hash<std::string>{}(password);
        std::ostringstream oss;
        oss << phash;
        return oss.str();
    }

    User::User(BSE::Database &database, int &user_id) : user_id(user_id), db(database) {
        auto &sqlppDb = *db.get_sqlpp11_db();

        UserTable userTable;

        auto results = sqlppDb(
                sqlpp::select(all_of(userTable)).
                        from(userTable).
                        where(userTable.id == user_id));

        if (results.empty())
            throw std::invalid_argument("User not found");

        const auto &result = results.front();
        email = result.email;
        password_hash = result.password;
    }

    User::User(Database &database, std::string &email) : db(database), email(email) {
        auto &sqlppDb = *db.get_sqlpp11_db();

        UserTable userTable;

        auto results = sqlppDb(
                sqlpp::select(all_of(userTable))
                        .from(userTable)
                        .where(userTable.email == email));

        if (results.empty()) {
            throw std::invalid_argument("User not found");
        }

        auto &result = results.front();
        user_id = result.id;
        password_hash = result.password;
    }

    User::User(Database &database, std::string &email, std::string &password)
            : db(database), email(email), password_hash(hash(password)) {
        auto &sqlppDb = *db.get_sqlpp11_db();

        UserTable userTable;

        try {
            sqlppDb(sqlpp::insert_into(userTable).set(
                    userTable.email = email,
                    userTable.password = password_hash));
        } catch (const sqlpp::exception &e) {
            std::cerr << e.what() << std::endl;
        }
    }

    bool User::check_password(std::string &password) {
        return password_hash == hash(password);
    }

    std::vector<BalanceAndAsset> User::get_balances() {
        auto &sqlppDb = *db.get_sqlpp11_db();
        std::vector<BalanceAndAsset> balances;
        AssetTable assetTable;
        BalanceTable balanceTable;
        auto assets = sqlppDb(sqlpp::select(sqlpp::all_of(assetTable)).from(assetTable).unconditionally());
        for (const auto &asset: assets) {
            bool asset_found = false;
            for (const auto &row: sqlppDb(
                    sqlpp::select(balanceTable.balance).from(balanceTable).where(balanceTable.asset_id == asset.id))) {
                balances.push_back({
                                           static_cast<int>(row.balance),
                                           asset.name.text,
                                           asset.ticker.text
                                   });
                asset_found = true;
                break;
            }
            if (!asset_found) {
                balances.push_back({
                                           0,
                                           asset.name.text,
                                           asset.ticker.text
                                   });
            }

        }

        return balances;

    }

    void User::update_balance(int change, int asset_id) {
        Balance balance(db, user_id, asset_id);
        balance.update_balance(change);
    }
}
