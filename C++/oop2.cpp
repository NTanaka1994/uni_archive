#include<stdio.h>
#include<string.h>
class Character{
protected:
    char name[200];
    int hp;
    int attack;
public:
    Character(const char* name, int hp, int attack){
        strncpy(this->name, name, sizeof(this->name) - 1);
        this->name[sizeof(this->name) - 1] = '\0';
        this->hp = hp;
        this->attack = attack;
    }
    void showStatus(){
        printf("Name: %s\nHP: %d\nAttack: %d\n", name, hp, attack);
    }
    void damage(int point){
        hp = hp - point;
        if(hp < 0){
            hp = 0;
        }
    }
    bool isDead(){
        return hp == 0;
    }
    const char* getName(){
        return name;
    }
    virtual void attackTo(Character* enemy){
        enemy->damage(attack);
        printf("%s takes %d damage\n", enemy->name, attack);
    }
    virtual ~Character(){
        printf("%s was deleted\n", name);
    }
};
class Fighter : public Character{
public:
    Fighter(const char* name, int hp, int attack) : Character(name, hp, attack){
        strncpy(this->name, name, sizeof(this->name) - 1);
        this->name[sizeof(this->name) - 1] = '\0';
        this->hp = hp;
        this->attack = attack;
    }
    void attackTo(Character* enemy) override{
        enemy->damage(attack);
        printf("%s's Fighter attack!\n", name);
        printf("%s takes %d damage\n", enemy->getName(), attack);
    }
    ~Fighter(){
        printf("Fighter %s was deleted\n", name);
    }
};
class Mage : public Character{
public:
    Mage(const char* name, int hp, int attack) : Character(name, hp, attack){
        strncpy(this->name, name, sizeof(this->name) - 1);
        this->name[sizeof(this->name) - 1] = '\0';
        this->hp = hp;
        this->attack = attack;
    }
    void attackTo(Character* enemy) override {
        enemy->damage(attack*2);
        printf("%s's Magic attack!\n", name);
        printf("%s takes %d damage\n", enemy->getName(), attack*2);
    }
    ~Mage(){
        printf("Magician %s was deleted\n", name);
    }
};
int main(){
    Fighter f1("Tanaka", 100, 25);
    Mage m1("Yamada", 70, 20);
    Fighter f2("Suzuki", 80, 15);
    Character* party[3];
    party[0] = &f1;
    party[1] = &m1;
    party[2] = &f2;
    for(int i=0; i<3; i=i+1){
        party[i]->showStatus();
    }
    party[0]->attackTo(party[2]);
    party[1]->attackTo(party[2]);
    party[2]->attackTo(party[0]);
    Character* c;
    c = &f1;
    c->attackTo(&f2);
    c = &m1;
    c->attackTo(&f1);
    return 1;
}