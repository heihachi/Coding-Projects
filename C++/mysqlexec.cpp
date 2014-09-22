#include <iostream>
#include <cstdio>
#include <string>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>

struct passwd *pws;

const std::string USER = "";
const std::string PASS = "";
const std::string USERNAME_LOCK = "";

int main(int argc, char* argv[])
{
    pws = getpwuid(geteuid());
    std::string username = std::string(pws->pw_name);
    if(username == USERNAME_LOCK)
    {
        if(argc < 4)
        {
            std::cerr << "Usage: " << argv[0] << " database '-e/-f' 'query/file'" << std::endl
                      << "Options:\n"
                      << "  database\tDatabase to execute on.\n"
                      << "  -e\t\tExecute query\n"
                      << "  -f\t\tExecute file\n"
                      << "  query\t\tQuery to execute (using -e)\n"
                      << "  file\t\tFile to execute (using -f)\n";
            return 1;
        }
        if(std::string(argv[2]) == "-e" || std::string(argv[2]) == "-f")
        {
            std::string database = std::string(argv[1]);
            std::string command = std::string(argv[2]);
            std::string fileOrQuery = std::string(argv[3]);
            FILE *shellCommand = NULL;
            if(command == "-e")
            {
                if(fileOrQuery[fileOrQuery.length()-1] != ';')
                    fileOrQuery += ";";
                std::string query = "mysql -u "+USER+" --password='"+PASS+"' "+database+" -e '"+fileOrQuery+"'";
                shellCommand = popen(query.c_str(), "r");
                if(shellCommand == 0)
                {
                    fprintf(stderr, "Could not execute!\n");
                    return 1;
                }
                else
                {
                    const int BUFSIZE = 1024;
                    char buf[BUFSIZE];
                    while(fgets(buf, BUFSIZE, shellCommand))
                    {
                        fprintf(stdout, "%s", buf);
                    }
                }
                pclose(shellCommand);
            }
            else if(command == "-f")
            {
                std::string query = "mysql -u "+USER+" --password='"+PASS+"' "+database+" < "+fileOrQuery+"";
                shellCommand = popen(query.c_str(), "r");
                if(shellCommand == 0)
                {
                    fprintf(stderr, "Could not execute!\n");
                    return 1;
                }
                else
                {
                    const int BUFSIZE = 1024;
                    char buf[BUFSIZE];
                    while(fgets(buf, BUFSIZE, shellCommand))
                    {
                        fprintf(stdout, "%s", buf);
                    }
                }
                pclose(shellCommand);
            }
        }
        else
        {
            std::cerr << "Please use -e or -f to execute a query or file. Not " << argv[2] << "\n"
                      << "Usage: " << argv[0] << " database '-e/-f' 'query/file'" << std::endl
                      << "Options:\n"
                      << "  database\tDatabase to execute on.\n"
                      << "  -e\t\tExecute query\n"
                      << "  -f\t\tExecute file\n"
                      << "  query\t\tQuery to execute (using -e)\n"
                      << "  file\t\tFile to execute (using -f)\n";
            return 1;
        }
    }
    else
    {
        std::cerr << "You are not " << USERNAME_LOCK << "! Please run " << argv[0] << " as " << USERNAME_LOCK << "\n";
        return 1;
    }
    return 0;
}
