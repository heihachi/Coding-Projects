#include<iostream>
#include<conio.h>
#include<string>
#include<stdio.h>
#include<stdlib.h>

void main()
{
    clrscr();
    char string[30],string1[30],opt;
    int ascii,n,i;
    cout<<"\n\tCODED BY AYESEYEF";
    cout<<"\n\tSelect the operation you would like to perform";
    cout<<"\n\n\t\tOperation Listn";
    cout<<"\n\tE - ENCRYPTION AND D - DECRYPTION\n\n\t\t";
    cin>>opt;
    if(opt=='e')
    {
        opt='E';
    }
    else if(opt=='d')
    {
        opt='D';
    }
    switch(opt)
    {
        case'E':
            cout<<"\tEnter the string to be encrypted by rot13 algorithm\n\t";
            gets(string1);
            n=strlen(string1);
            for(i=0;i<n;i++)
            {
                ascii=string1[i];
                if((ascii>=48)&&(ascii<=57))
                {
                    cout<<"\n\tThe string cannot be encrypted\n";
                    cout<<"\tPress any key to exit";
                    getch();
                    exit(0);
                }
            }
            for(i=0;i<n;i++)
            {
                ascii=string1[i];
                if((ascii>=65)&&(ascii<=77))
                {
                    string[i]=ascii+13;
                }
                else if((ascii>77)&&(ascii<=90))
                {
                    string[i]=ascii-13;
                }
                else if((ascii>=97)&&(ascii<=109))
                {
                    string[i]=ascii+13;
                }
                else if((ascii>109)&&(ascii<=122))
                {
                    string[i]=ascii-13;
                }
                else if(ascii==32)
                {
                    string[i]=ascii;
                }
                else
                {
                    cout<<"\n\tSpecial characters are not encryptable";
                    cout<<"\nPress any key to exit";
                    getch();
                    exit(0);
                }
            }
            cout<<"\n\tThe encrypted string for the text:";
            puts(string1);
            cout<<"tist";
        break;

        case'D':
            cout<<"\n\tEnter the Rot13 encrypted string\n\t";
            gets(string1);
            n=strlen(string1);
            for(i=0;i<n;i++)
            {
                ascii=string1[i];
                if((ascii>=48)&&(ascii<=57))
                {
                    cout<<"\n\tThe string cannot be decrypted\n";
                    cout<<"\tPress any key to exit";
                    getch();
                    exit(0);
                }
            }
            for(i=0;i<n;i++)
            {
                ascii=string1[i];
                if((ascii>=65)&&(ascii<=77))
                {
                    string[i]=ascii+13;
                }
                else if((ascii>77)&&(ascii<=90))
                {
                    string[i]=ascii-13;
                }
                else if((ascii>=97)&&(ascii<=109))
                {
                    string[i]=ascii+13;
                }
                else if((ascii>109)&&(ascii<=122))
                {
                    string[i]=ascii-13;
                }
                else if(ascii==32)
                {
                    string[i]=ascii;
                }
                else
                {
                    cout<<"\n\tSpecial characters are not decryptablen";
                    cout<<"\n\tPress any key to exit";
                    getch();
                    exit(0);
                }
            }
            cout<<"\n\tThe decrypted plain text for the string:";
            puts(string);
            cout<<"\tis\t";
        break;

        default:
            cout<<"\n\tWrong option";
            cout<<"\n\tPress any key to exit";
            getch();
            exit(0);
    }
    puts(string);
    getch();
}
