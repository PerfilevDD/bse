#include "table/table.hpp"

#include "exception"
#include "randomizer.hpp"

namespace Fairoulette {

    Table::Table(int table_id): table_id(table_id) {}

    int Table::calculate_result() { // Hier wird berechnet, ob der Nutzer gewonnen hat, oder nicht
        Fairoulette::Randomizer rand;   // Eine zufällige Zahl wird geneiriert 
        int result = rand.get_random_number();
        return result;
    }

    void Table::add_or_update_bet_by_bet_id(int bid, Bet bet) {   // Die Wette wird aktualisiert "also hinzugefügt"
        for (auto it = bets.begin(); it != bets.end(); ++it) {
            if (it->get_bet_id() == bid) {
                bets.erase(it);
                break;
            }
        }
        bets.push_back(bet);
    }

    pybind11::list Table::get_and_clear_bets() {    // List aller Wetten werden zurückgegeben und dann gelöscht
        pybind11::list tmp_list = pybind11::cast(bets);
        bets.clear();
        return tmp_list;
    }

    Bet Table::get_bet_by_bet_id(int bet_id) {
        for (auto it = bets.begin(); it != bets.end(); ++it) {
            if (it->get_bet_id() == bet_id) {           // Überprüft die Bedingung, ob die aktuelle Wette die gesuchte Wetten-ID hat
                return (*it);
            }
        }
    }
}