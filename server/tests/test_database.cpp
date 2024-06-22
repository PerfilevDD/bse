#include <gtest/gtest.h>
#include "db/sqlite.hpp"
#include "user/User.hpp"

TEST(SimpleTest, Database) {
    BSE::Database db;
    auto testdb = db.get_sqlpp11_db();


}
