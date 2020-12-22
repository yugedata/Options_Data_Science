//
//  main.c
//  Options_db
//
//  Created by Sato on 12/21/20.
//

#include <stdio.h>
#include <sqlite3.h>


static int createDB(const char* s);
static int createTable(const char* s);
static int insertData(const char* s);
static int selectData(const char* s);

static int callback(void* NotUsed, int argc, char** argv, char** azColName);


int main(int argc, char** argv)
{
    
    sqlite3* db;
    const char* dir = "/Users/Sato/Documents/PycharmProjects/Tsuru/Options_temp.db";
    
    createDB(dir);
    createTable(dir);
    
    return (0);
}

static int createDB(const char* s)
{
    sqlite3* db;
    int exit = 0;
    
    exit = sqlite3_open(s, &db);
    
    sqlite3_close(db);
    
    return 0;
}

int createTable(const char* s)
{
    sqlite3* db;
    
    string
    
    return 0;
    
}




