#include <sqlpp11/sqlpp11.h>
#include <sqlpp11/sqlite3/sqlite3.h>

namespace BSE {
    namespace UserTable_ {

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

        struct Email {
            struct _alias_t {
                static constexpr const char _literal[] = "email";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;
                template<typename T>
                struct _member_t {
                    T email;
                    T& operator()() { return email; }
                    const T& operator()() const { return email; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::varchar>;
        };
        
        struct Password {
            struct _alias_t {
                static constexpr const char _literal[] = "password";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;
                template<typename T>
                struct _member_t {
                    T password;
                    T& operator()() { return password; }
                    const T& operator()() const { return password; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::varchar>;
        };

        struct Balance {
            struct _alias_t {
                static constexpr const char _literal[] = "balance";
                using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;
                template<typename T>
                struct _member_t {
                    T balance;
                    T& operator()() { return balance; }
                    const T& operator()() const { return balance; }
                };
            };
            using _traits = sqlpp::make_traits<sqlpp::integer>;
        };
    }
    
    struct UserTable : sqlpp::table_t<UserTable, UserTable_::Id, UserTable_::Email, UserTable_::Password, UserTable_::Balance> {
        struct _alias_t {
            static constexpr const char _literal[] = "USER";
            using _name_t = sqlpp::make_char_sequence<sizeof(_literal), _literal>;
            template<typename T>
            struct _member_t {
                T userTable;
                T& operator()() { return userTable; }
                const T& operator()() const { return userTable; }
            };
        };
    };
}
