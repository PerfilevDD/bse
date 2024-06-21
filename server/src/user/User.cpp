<<<<<<< HEAD
#include "user/User.hpp"

namespace BSM {
    User::User(std::string email, std::string password) {
        db = Database();

    }

    int User::get_user_id() {
        return 1;
    }



}
=======
#include <user/User.hpp>

namespace BSM {

User::User(int user_id) {
}
User::User(std::string& email, std::string& password) {
}

bool User::check_password(std::string& password) {
    return 0;
}

int User::get_balance() {
    return 0;
}

void User::update_balance(int change) {
    return;
}
}  // namespace BSM
>>>>>>> 2a0f282f8bdff06f5d1528acf17c441f01bd2aeb
