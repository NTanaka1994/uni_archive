#include<stdio.h>
#include<string.h>
class Fighter{
private:
    int hp;
    char name[200];
    int attack;
public:
    Fighter(const char* name, int hp, int attack){
        strncpy(this->name, name, sizeof(this->name) - 1);
        this->name[sizeof(this->name) - 1] = '\0';
        this->hp = hp;
        this->attack = attack;
    }
    void showstatus(){
        printf("Name: %s\nHP: %d\nAttack: %d\n", name, hp, attack);
    }
    void damage(int point){
        hp = hp - point;
        if(hp < 0){
            hp = 0;
        }
    }
    void attackTo(Fighter* enemy){
        enemy->damage(attack);
        printf("%s attacks %s!\n%s takes %d damage.\n", name, enemy->name, enemy->name, attack);
    }
    void isDead(){
        if(hp <= 0){
            printf("dead\n");
        }
    }
    ~Fighter(){
        printf("%s was deleted\n", name);
    }
};

int main(){
    Fighter f1("Tanaka", 100, 25);
    Fighter f2("Suzuki", 80, 15);
    f1.showstatus();
    f2.showstatus();
    f1.attackTo(&f2);
    f2.attackTo(&f1);
    f1.showstatus();
    f2.showstatus();
    f1.attackTo(&f2);
    f1.attackTo(&f2);
    f1.attackTo(&f2);
    f2.isDead();
}