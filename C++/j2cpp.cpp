#include<stdio.h>
#include<string.h>
class Animal{
protected:
    char Name[200];
    int Age;
public:
    Animal(const char *name, int age){
        strncpy(this->Name, name, sizeof(this->Name)-1);
        this->Name[sizeof(this->Name)-1] = '\0';
        this->Age = age;
    }
    virtual void ShowProfile(){
        printf("name is %s. Age is %d\n", Name, Age);
    }
    virtual void speak(){
        printf("..........\n");
    }
    ~Animal(){
        printf("Deleted\n");
    }
};
class Cat: public Animal{
public:
    Cat(const char *name, int age): Animal(name, age){}
    void naki(){
        printf("Su-Su-\n");
    }
    void ShowProfile() override{
        printf("Cat name is %s. Age is %d\n", Name, Age);
    }
    void speak() override{
        printf("Miao!\n");
    }
};
class Dog: public Animal{
public:
    Dog(const char *name, int age):Animal(name, age){}
    void run(){
        printf("tokotoko\n");
    }
    void ShowProfile() override{
        printf("Dog name is %s. Age is %d\n", Name, Age);
    }
    void speak() override{
        printf("Wang!\n");
    }
};
int main(){
    Cat c("Tom", 14);
    c.ShowProfile();
    c.naki();
    Dog d("spike", 10);
    d.ShowProfile();
    d.run();
    c.speak();
    d.speak();
    return 0;
}