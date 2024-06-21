#include "user/User.hpp"

namespace BSM {
    User::User(std::string email, std::string password) {
        db = Database();

    }

    int User::get_user_id() {
        return 1;
    }



}