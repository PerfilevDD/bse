#include <sqlpp11/sqlpp11.h>
#include <sqlpp11/sqlite3/sqlite3.h>

namespace BSE {
    namespace AssetTable_ {

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


        struct Name {
            struct _alias_t {
                static constexpr const char _literal[] = "name";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T name;

                    T &operator()() { return name; }

                    const T &operator()() const { return name; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::varchar>;
        };


        struct Ticker {
            struct _alias_t {
                static constexpr const char _literal[] = "ticker";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T ticker;

                    T &operator()() { return ticker; }

                    const T &operator()() const { return ticker; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::varchar>;
        };

        struct Supply {
            struct _alias_t {
                static constexpr const char _literal[] = "supply";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T supply;

                    T &operator()() { return supply; }

                    const T &operator()() const { return supply; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };
    }


    struct AssetTable
            : sqlpp::table_t<AssetTable, AssetTable_::Id, AssetTable_::Name, AssetTable_::Ticker, AssetTable_::Supply> {
        struct _alias_t {
            static constexpr const char _literal[] = "Asset";
            using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

            template<typename T>
            struct _member_t {
                T AssetTable;

                T &operator()() { return AssetTable; }

                const T &operator()() const { return AssetTable; }
            };
        };
    };

}