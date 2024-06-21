#include <user/User.hpp>

#include <sstream>
namespace BSE {

    std::string hash(std::string password) {
        size_t phash = std::hash<std::string>{}(password);
        std::ostringstream oss;
        oss << phash;
        std::string password_hash = oss.str();

    }

User::User(Database database, int user_id) {
}
User::User(Database database, std::string& email, std::string& password) {
    std::string password_hash = hash(password);

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
}  // namespace BSE
