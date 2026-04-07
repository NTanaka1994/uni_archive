#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

void show_line() {
    printf("ADDRESS  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15  0123456789ABCDEF\n");
    printf("======== == == == == == == == == == == == == == == == ==  ================\n");
}
int main() {
	FILE *fp = fopen("tasks.json", "rb");
	unsigned char buf[16];
    size_t n;
    show_line();
    int j = 0;
    while ((n = fread(buf, 1, sizeof(buf), fp)) > 0) {
        printf("%08X ", j);
        size_t i;
        for (i = 0; i < n; i++) {
            printf("%02X ", buf[i]);
            
        }
        for (;i < 16;i++) {
            printf("   ");
        }
        printf(" ");
        for (size_t i = 0; i < n; i++) {
            if (buf[i] == '\r') {
                printf("\\r");
            }
            else if (buf[i] == '\n') {
                printf("\\n");
            }
            else if (buf[i] == '\t') {
                printf("\\t");
            }
            else {
                printf("%c", buf[i]);
            }
        }
        printf("\n");
        j = j + 16;
    }
}