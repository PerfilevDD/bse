#include <user/User.hpp>

namespace BSM {

User::User(Database database, int user_id) {
}
User::User(Database database, std::string& email, std::string& password) {
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
