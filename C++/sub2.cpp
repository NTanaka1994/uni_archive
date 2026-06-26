#include<stdio.h>
class Dog{
    private:
    char name[200];
    public:
    void set_name(){
        scanf("%s", name);
    }
    void print_name(){
        printf("dog name is %s", name);
    }
};
int main(){
    Dog d;
    d.set_name();
    d.print_name();
    return 0;
}