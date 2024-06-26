#include <sqlpp11/sqlpp11.h>

#include <db/sqlite.hpp>
#include <iostream>
#include <sstream>
#include <user/User.hpp>
#include <user/user_table.hpp>
#include "asset/asset_table.hpp"
#include "balance/balance_table.hpp"

namespace BSE {

    std::string User::hash(std::string &password) {         // Die Funktion erzeugt einen Hash-Wert für ein Passwort, damit die Daten in der Datenbank gesichert gespeichert werden
        size_t phash = std::hash<std::string>{}(password);
        std::ostringstream oss;
        oss << phash;
        return oss.str();
    }

    User::User(BSE::Database &database, int &user_id) : user_id(user_id), db(database) {    // Initialisiert ein "User"-Objekt anhander der User-id
        auto &sqlppDb = *db.get_sqlpp11_db();                                               // Führt eine SQL-Abfrage aus

        UserTable userTable;

        auto results = sqlppDb(                                     
                sqlpp::select(all_of(userTable)).
                        from(userTable).
                        where(userTable.id == user_id));

        if (results.empty())                                    // Falls der Benutzer nach der Abfrage in der Datenbank zu finden ist, dann wird das gehashte Passwort und die "user-id" geladen, sonst wird der Benutzer rausgeschmissen. 
            throw std::invalid_argument("User not found");

        const auto &result = results.front();
        email = result.email;
        password_hash = result.password;
    }

    User::User(Database &database, std::string &email) : db(database), email(email) {   // Ein "user"-Objekt anhand der E-Mail Adresse initialisert
        auto &sqlppDb = *db.get_sqlpp11_db();

        UserTable userTable;

        auto results = sqlppDb(                                 // Führt eine SQL-Abfrage 
                sqlpp::select(all_of(userTable))
                        .from(userTable)
                        .where(userTable.email == email));

        if (results.empty()) {                                  // Falls der Benutzer in der Datenbank existiert, wird dann die User-id und das gehashte Passwort geladen, sonst ist "Bella Tschau" 
            throw std::invalid_argument("User not found");
        }

        auto &result = results.front();
        user_id = result.id;
        password_hash = result.password;
    }

    User::User(Database &database, std::string &email, std::string &password)   //Erstellt einen neuen Benutzer in der Datenbank 
            : db(database), email(email), password_hash(hash(password)) {       // Erzeugt Hashwert des Passworts
        auto &sqlppDb = *db.get_sqlpp11_db();

        UserTable userTable;

        try {
            sqlppDb(sqlpp::insert_into(userTable).set(
                    userTable.email = email,                // Setzt das Email-Feld des neuen Benutzer 
                    userTable.password = password_hash));   // Setzt das Passwort mit dem gehashten Passwort 
        } catch (const sqlpp::exception &e) {               // Fehlerbehandlung, falls die Einfügeoperation fehlschlägt. 
            std::cerr << e.what() << std::endl;             // Gibt die Fehlermeldung auf der Konsole aus
        }
    }

    bool User::check_password(std::string &password) {      // Überprüft, ob das gegebene Passwort dem gespeicherten gehashten Passwort entspricht 
        return password_hash == hash(password);
    }

    std::vector<BalanceAndAsset> User::get_balances() {    // Abrufen der Salden des Benutzers
        auto &sqlppDb = *db.get_sqlpp11_db();
        std::vector<BalanceAndAsset> balances;             // Hier wird die Liste "BalanceAndAsset" zurückgegeben
        AssetTable assetTable;
        BalanceTable balanceTable;
        auto assets = sqlppDb(sqlpp::select(sqlpp::all_of(assetTable)).from(assetTable).unconditionally());     // Abrufen aller Assets aus der Asset-Table
        for (const auto &asset: assets) {
            bool asset_found = false;           // Überprüft ob der Benutzer einen Saldo für das Asset hat, oder nicht.
            for (const auto &row: sqlppDb(      // Abrufen des Saldos des Benutzers für das aktuelle Asset
                    sqlpp::select(balanceTable.balance).from(balanceTable).where(balanceTable.asset_id == asset.id))) {
                balances.push_back({
                                           static_cast<int>(row.balance),
                                           asset.name.text,
                                           asset.ticker.text,
                                           static_cast<int>(asset.id)
                                   });
                asset_found = true;
                break;
            }
            if (!asset_found) {     // Wenn kein Saldo für das Asset gefunden wurde, füge einen Saldo von 0 hinzu
                balances.push_back({
                                           0,                   // Saldo von 0, da der Benutzer keinen Saldo für das Asset hat
                                           asset.name.text,
                                           asset.ticker.text,
                                           static_cast<int>(asset.id)
                                   });
            }

        }

        return balances;

    }

    int User::get_balance(int asset_id) {
        BalanceTable balanceTable;
        auto &sqlppDb = *db.get_sqlpp11_db();

        auto assets = sqlppDb(sqlpp::select(sqlpp::all_of(balanceTable)).from(
                balanceTable).where(balanceTable.user_id == user_id && balanceTable.asset_id == asset_id));     // Abrufen aller Assets aus der Asset-Table
        for (const auto &asset: assets) {
            return static_cast<int>(asset.balance);
        }
        return 0;
    }

    void User::update_balance(int change, int asset_id) {       // Hier wird Saldo eines bestimmten Assets für den Benutzer aktualisert 
        Balance balance(db, user_id, asset_id);     
        balance.update_balance(change);
    }
}
