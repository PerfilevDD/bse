#include <sqlpp11/sqlpp11.h>
#include <sqlpp11/sqlite3/sqlite3.h>

namespace BSE {
    namespace OrderTable_ {

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


        struct Trader_id {
            struct _alias_t {
                static constexpr const char _literal[] = "trader_id";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T trader_id;

                    T &operator()() { return trader_id; }

                    const T &operator()() const { return trader_id; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };


        struct PairId {
            struct _alias_t {
                static constexpr const char _literal[] = "pair_id";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T pair_id;

                    T &operator()() { return pair_id; }

                    const T &operator()() const { return pair_id; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };

        struct Price {
            struct _alias_t {
                static constexpr const char _literal[] = "price";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T price;

                    T &operator()() { return price; }

                    const T &operator()() const { return price; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };


        struct Amount {
            struct _alias_t {
                static constexpr const char _literal[] = "amount";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T amount;

                    T &operator()() { return amount; }

                    const T &operator()() const { return amount; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };

        struct FullfilledAmount {
            struct _alias_t {
                static constexpr const char _literal[] = "fullfilled_amount";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T fullfilled_amount;

                    T &operator()() { return fullfilled_amount; }

                    const T &operator()() const { return fullfilled_amount; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };


        struct Completed {
            struct _alias_t {
                static constexpr const char _literal[] = "completed";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T completed;

                    T &operator()() { return completed; }

                    const T &operator()() const { return completed; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::boolean>;
        };

        struct CompletedTimestamp {
            struct _alias_t {
                static constexpr const char _literal[] = "completed_timestamp";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T completed_timestamp;

                    T &operator()() { return completed_timestamp; }

                    const T &operator()() const { return completed_timestamp; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };


        struct Buy {
            struct _alias_t {
                static constexpr const char _literal[] = "buy";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T buy;

                    T &operator()() { return buy; }

                    const T &operator()() const { return buy; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::boolean>;
        };
    }

    struct OrderTable
            : sqlpp::table_t<OrderTable, OrderTable_::Id, OrderTable_::Trader_id, OrderTable_::PairId, OrderTable_::Price, OrderTable_::Amount, OrderTable_::Buy, OrderTable_::Completed, OrderTable_::CompletedTimestamp, OrderTable_::FullfilledAmount> {
        struct _alias_t {
            static constexpr const char _literal[] = "Trade";
            using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

            template<typename T>
            struct _member_t {
                T OrderTable;

                T &operator()() { return OrderTable; }

                const T &operator()() const { return OrderTable; }
            };
        };
    };
}
