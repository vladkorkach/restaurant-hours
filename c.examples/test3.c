#include <stdio.h>
#include <string.h>

#define TYPE_INT	1
#define TYPE_DOUBLE	2
#define TYPE_CHAR	3
#define TYPE_STRING	4

char *f(void * p, unsigned int uiOffset, unsigned int uiType)
{
    char str[255];
    char s[3];

    switch (uiType) 
    {
	case 1: strcpy(s, "%d");
               break; 
	case 2: strcpy(s, "%fL");
                break; 
	case 3: strcpy(s, "%c");
               break; 
	case 4: strcpy(s, "%s");
               break; 
	default: printf("Choice other than 1, 2, 3 and 4"); 
                break;   
    } 

    sprintf(str, s, p);
    printf("%s\n", str);
    return str;
}

int main()
{
    int i=20;
    int *p = &i;

//    char *p = "c";

    unsigned int uiOffset = sizeof(*p);

    const char *t = f(p,uiOffset,TYPE_INT);
    printf("%s", t);

    return 0;
}