#include<stdio.h>
#include<string.h>
class Dog{
    private:
    char name[200];
    public:
    Dog(const char* n){
        strcpy(name, n);
    }
    ~Dog(){
        printf("destructor was occured");
    }
    void print_name(){
        printf("dog name is %s\n", name);
    }
};
int main(){
    char name[] = "Tom";
    Dog d(name);
    d.print_name();
    return 0;
}