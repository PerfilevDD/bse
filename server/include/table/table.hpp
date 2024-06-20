#pragma once

#include "bet/bet.hpp"
#include "ctime"
#include "list"
#include "vector"
#include <pybind11/stl.h>

namespace Fairoulette {
class Table {
   public:
    Table(int table_id);

    void add_participant(int pid);      // Teilnehmer mit ID wird hinzugefügt
    void add_or_update_bet_by_bet_id(int pid, Bet bet); // Eine Wette wird für einen Teilnehmer hinzugefügt
    int calculate_result();     // Berechnen und Zurückgeben des Ergebnisses der Runde

    Bet get_bet_by_bet_id(int bet_id);  // Wette mit der angegebenen ID zurückgeben

    pybind11::list get_and_clear_bets();    // Gibt eine Liste aller Wetten zurück und löscht diese anschließend.

    int get_table_id(){
        return table_id;
    }

   private:
    std::time_t next_round = 0;
    std::list<int> participants;
    std::list<Bet> bets;
    int table_id;
};
}  // namespace Fairoulette