#include <sqlpp11/sqlpp11.h>
#include <sqlpp11/sqlite3/sqlite3.h>

namespace BSE {
    namespace BalanceTable_ {

// https://github.com/rbock/sqlpp11/blob/main/tests/sqlite3/usage/Sample.cpp
// Dont delete, sonst ich lösch alles

        struct Id {
            struct _alias_t {
                static constexpr const char _literal[] = "id";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T id;

                    T &operator()() { return id; }

                    const T &operator()() const { return id; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer, sqlpp::tag::must_not_insert>;
        };


        struct UserId {
            struct _alias_t {
                static constexpr const char _literal[] = "user_id";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T user_id;

                    T &operator()() { return user_id; }

                    const T &operator()() const { return user_id; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };


        struct AssetId {
            struct _alias_t {
                static constexpr const char _literal[] = "asset_id";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T asset_id;

                    T &operator()() { return asset_id; }

                    const T &operator()() const { return asset_id; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };

        struct Balance {
            struct _alias_t {
                static constexpr const char _literal[] = "balance";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T balance;

                    T &operator()() { return balance; }

                    const T &operator()() const { return balance; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };
    }


    struct BalanceTable
            : sqlpp::table_t<BalanceTable, BalanceTable_::Id, BalanceTable_::AssetId, BalanceTable_::UserId, BalanceTable_::Balance> {
        struct _alias_t {
            static constexpr const char _literal[] = "Balance";
            using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

            template<typename T>
            struct _member_t {
                T BalanceTable;

                T &operator()() { return BalanceTable; }

                const T &operator()() const { return BalanceTable; }
            };
        };
    };

}