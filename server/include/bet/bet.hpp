#pragma once

#include "array"

namespace Fairoulette {
struct OutsideBets {
    int odd = 0;
    int even = 0;
    int red = 0;
    int black = 0;
    int col1 = 0;
    int col2 = 0;
    int col3 = 0;
    int dozen1 = 0;
    int dozen2 = 0;
    int dozen3 = 0;
};

class Bet {
   public:
    Bet(int user_id, int bet_id);       // Eine Instanz mit Benutzer und Wetten-ID wird erstellt
    int calculate_result(int number);   // Berechnet und gibt das Ergebnis der Wetten basierend auf der Gewinnzahl number zurück.
    void add_number_bet(int number, int worth);
    void add_red_bet(int worth);
    void add_black_bet(int worth);
    void add_even_bet(int worth);
    void add_odd_bet(int worth);
    void add_col_bet(int col, int worth);
    void add_dozen_bet(int dozen, int worth);

    std::array<int, 37> get_number_bets() {
        return number_bets;
    }

    int get_user_id() {
        return user_id;
    }

    int get_bet_id () {
        return bet_id;
    }

    int get_bet_worth() {
        return bet_worth;
    }

   private:
    std::array<int, 37> number_bets = {};
    struct OutsideBets outside_bets = {};
    int user_id;
    int bet_id;
    int bet_worth = 0;
};
}  // namespace Fairoulette