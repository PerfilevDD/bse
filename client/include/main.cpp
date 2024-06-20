#include <chrono>
#include <matplot/matplot.h>
#include "datatypes/list/list.hpp"
#include <list>
#include <cmath>
#include <random>

using namespace matplot;

void compare_list(){
    // Test list
    List<int> ourList;
    std::list<int> stdList;
    auto stdIt = stdList.begin();

    std::vector<std::vector<int>>  ourListResult;
    std::vector<std::vector<int>> stdListResult;

    ourListResult.emplace_back();
    stdListResult.emplace_back();
    for (int i = 0; i < 10000; i++){
        std::random_device dev;
        std::mt19937 rng(dev());
        std::uniform_int_distribution<std::mt19937::result_type> dist6(1,10000);

        const auto t1 = std::chrono::high_resolution_clock::now();
        ourList.insert_front(dist6(rng));
        const auto t2 = std::chrono::high_resolution_clock::now();
        ourListResult[0].push_back((t2 - t1).count());
        const auto t3 = std::chrono::high_resolution_clock::now();
        stdList.insert(stdIt, dist6(rng));
        const auto t4 = std::chrono::high_resolution_clock::now();
        stdListResult[0].push_back((t4 - t3).count());

    }
    ourListResult.emplace_back();
    stdListResult.emplace_back();
    for (int i = 0; i < 10000; i++){
        std::random_device dev;
        std::mt19937 rng(dev());
        std::uniform_int_distribution<std::mt19937::result_type> dist6(1,10000);

        const auto t1 = std::chrono::high_resolution_clock::now();
        ourList.remove_front();
        const auto t2 = std::chrono::high_resolution_clock::now();
        ourListResult[1].push_back((t2 - t1).count());
        int firstElementStdList = *stdIt;
        const auto t3 = std::chrono::high_resolution_clock::now();
        stdList.remove(firstElementStdList);
        const auto t4 = std::chrono::high_resolution_clock::now();
        stdListResult[1].push_back((t4 - t3).count());

    }

    for (int i = 0; i < 1; i++){
        const auto t1 = std::chrono::high_resolution_clock::now();
        const auto t2 = std::chrono::high_resolution_clock::now();
        const auto t3 = std::chrono::high_resolution_clock::now();
    }


    std::vector<double> x = linspace(0, 10000);



    subplot(2, 1, 1);
    plot(x, ourListResult[0], "-:bs");
    hold(on);
    plot(x, stdListResult[0], "-:gs");
    title("Insert Front");

    subplot(2, 1, 2);
    plot(x, ourListResult[1], "-:bs");
    hold(on);
    plot(x, stdListResult[1], "-:gs");
    title("Remove Front");

    show();

}
int main() {
    compare_list();

    return 0;
}