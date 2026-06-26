#include<stdio.h>
#include<string.h>
class Book{
private:
    char title[100];
    int price;
    int stock;
public:
    Book(const char *title, int price, int stock){
        strncpy(this->title, title, sizeof(this->title)-1);
        this->title[sizeof(this->title) - 1] = '\0';
        this->price = price;
        this->stock = stock;
    }
    void showInfo(){
        printf("Title: %s\nPrice: %d\nStock: %d\n", title, price, stock);
    }
    void sell(int n){
        if(n > stock){
            printf("Not enough stock.\n");
        }
        else{
            stock = stock - n;
            printf("Sold %d books\n", n);
        }
    }
    void addStock(int n){
        stock = stock + n;
        printf("Added %d books.\n", n);
    }
    ~Book(){
        printf("\n");
    }
};
int main(){
    Book b1("C Programming", 2500, 5);
    b1.showInfo();
    b1.sell(2);
    b1.showInfo();
    b1.sell(10);
    b1.addStock(3);
    b1.showInfo();
    return 1;
}