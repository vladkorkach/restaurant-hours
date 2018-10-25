#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char* stringToBinary(char* s) {
    if(s == NULL) return 0; 
    size_t len = strlen(s);
    char *binary = malloc(len*8 + 1); 
    binary[0] = '\0';
    for(size_t i = 0; i < len; ++i) {
        char ch = s[i];
        for(int j = 7; j >= 0; --j){
            if(ch & (1 << j)) {
                strcat(binary,"1");
            } else {
                strcat(binary,"0");
            }
        }
    }
    return binary;
}

char* substring(const char* str, size_t begin, size_t len) 
{ 
  if (str == 0 || strlen(str) == 0 || strlen(str) < begin || strlen(str) < (begin+len)) 
    return 0; 

  return strndup(str + begin, len); 
} 

int main() 
{ 
    char *p = "ABC";
    char *bs = stringToBinary(p);
    char finalstr[8];
    char c;

    printf("start string: %s\n", bs);

    printf("first half-octet: %s\n", &bs[strlen(bs) - 4]);
    printf("last half-octet: %s\n", substring(bs, 0, 4));

    strcpy(finalstr, &bs[strlen(bs) - 4]);
    strcat(finalstr, substring(bs, 0, 4));

    printf("FINAL bin string: %s\n", finalstr);

    c = strtol(finalstr, 0, 2);

    printf("FINAL char string: %i\n", c);

    return 0; 
} 

