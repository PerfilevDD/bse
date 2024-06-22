#include <sqlpp11/sqlpp11.h>
#include <sqlpp11/sqlite3/sqlite3.h>

namespace BSE {
    namespace MarketplaceTable_ {

// https://github.com/rbock/sqlpp11/blob/main/tests/sqlite3/usage/Sample.cpp 
// Dont delete, sonst ich lösch alles

        struct Id {
            struct _alias_t {
                static constexpr const char _literal[] = "id";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;
                template<typename T>
                struct _member_t {
                    T id;
                    T& operator()() { return id; }
                    const T& operator()() const { return id; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer, sqlpp::tag::must_not_insert>;
        };



        struct Trader_id {
            struct _alias_t {
                static constexpr const char _literal[] = "trader_id";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;
                template<typename T>
                struct _member_t {
                    T trader_id;
                    T& operator()() { return trader_id; }
                    const T& operator()() const { return trader_id; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };



        struct Item {
            struct _alias_t {
                static constexpr const char _literal[] = "item";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;
                template<typename T>
                struct _member_t {
                    T item;
                    T& operator()() { return item; }
                    const T& operator()() const { return item; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::varchar>;
        };

        struct Pair_item {
            struct _alias_t {
                static constexpr const char _literal[] = "pair_item";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;
                template<typename T>
                struct _member_t {
                    T pair_item;
                    T& operator()() { return pair_item; }
                    const T& operator()() const { return pair_item; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::varchar>;
        };
        


        struct Price {
            struct _alias_t {
                static constexpr const char _literal[] = "price";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;
                template<typename T>
                struct _member_t {
                    T price;
                    T& operator()() { return price; }
                    const T& operator()() const { return price; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };



        struct Item_amount {
            struct _alias_t {
                static constexpr const char _literal[] = "item_amount";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;
                template<typename T>
                struct _member_t {
                    T item_amount;
                    T& operator()() { return item_amount; }
                    const T& operator()() const { return item_amount; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };
    }
    
    struct MarketplaceTable : sqlpp::table_t<MarketplaceTable, MarketplaceTable_::Id, MarketplaceTable_::Trader_id, MarketplaceTable_::Item, MarketplaceTable_::Pair_item, MarketplaceTable_::Price, MarketplaceTable_::Item_amount> {
        struct _alias_t {
            static constexpr const char _literal[] = "MARKETPLACE";
            using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;
            template<typename T>
            struct _member_t {
                T marketplaceTable;
                T& operator()() { return marketplaceTable; }
                const T& operator()() const { return marketplaceTable; }
            };
        };
    };
}
