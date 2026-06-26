#include<stdio.h>
class dog{
    private:
    char name[200];
    public:
    void set_name();
    void print_name(){
        printf("%s", name);
    }
};
void dog::set_name(){   
    scanf("%s", &name);
}
int main(){
    dog d;
    d.set_name();
    d.print_name();
    return 1;
}