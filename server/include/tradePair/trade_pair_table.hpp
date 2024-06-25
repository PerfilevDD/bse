#include <sqlpp11/sqlpp11.h>
#include <sqlpp11/sqlite3/sqlite3.h>

namespace BSE {
    namespace TradePairTable_ {

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

        struct BaseAsset {
            struct _alias_t {
                static constexpr const char _literal[] = "base_asset";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T base_asset;

                    T &operator()() { return base_asset; }

                    const T &operator()() const { return base_asset; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };

        struct PriceAsset {
            struct _alias_t {
                static constexpr const char _literal[] = "price_asset";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

                template<typename T>
                struct _member_t {
                    T price_asset;

                    T &operator()() { return price_asset; }

                    const T &operator()() const { return price_asset; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };
    }
    struct TradePairTable
            : sqlpp::table_t<TradePairTable, TradePairTable_::Id, TradePairTable_::BaseAsset, TradePairTable_::PriceAsset> {
        struct _alias_t {
            static constexpr const char _literal[] = "TradePair";
            using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;

            template<typename T>
            struct _member_t {
                T tradePairTable;

                T &operator()() { return tradePairTable; }

                const T &operator()() const { return tradePairTable; }
            };
        };
    };
}

